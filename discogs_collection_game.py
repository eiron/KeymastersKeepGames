"""
Discogs Collection game for Keymaster's Keep.

Fetches a player's public Discogs collection via the Discogs API and generates
listening challenges based on the albums, artists, genres, styles, labels,
decades, and formats in their collection.

Configure with your Discogs username (and optionally a personal access token
for private collections or higher rate limits).
"""

from __future__ import annotations

import functools
import re
from typing import Dict, List, Set, Tuple, Any

import requests  # type: ignore

from dataclasses import dataclass

from Options import FreeText, OptionSet, Toggle  # type: ignore
from ..game import Game  # type: ignore
from ..game_objective_template import GameObjectiveTemplate  # type: ignore
from ..enums import KeymastersKeepGamePlatforms  # type: ignore


# === Options Dataclass ===
@dataclass
class DiscogsCollectionArchipelagoOptions:
    discogs_collection_username: "DiscogsCollectionUsername"
    discogs_collection_token: "DiscogsCollectionToken"
    discogs_collection_excluded_genres: "DiscogsCollectionExcludedGenres"
    discogs_collection_excluded_formats: "DiscogsCollectionExcludedFormats"
    discogs_collection_include_deep_dives: "DiscogsCollectionIncludeDeepDives"


# === Module-level data holder with caching ===
class _DiscogsCollectionHolder:
    """Caches raw Discogs collection data keyed by (username, token)."""

    def __init__(self):
        self._notice_printed = False

    @functools.lru_cache(maxsize=4)
    def fetch_collection(self, username: str, token: str) -> List[Dict[str, Any]]:
        """Fetch all releases from a Discogs user's collection folder 0 (All).

        Returns a list of release dicts with keys: title, artists, genres, styles,
        labels, year, formats.
        """
        if not username:
            return []

        releases: List[Dict[str, Any]] = []
        page = 1
        per_page = 100
        base_url = f"https://api.discogs.com/users/{username}/collection/folders/0/releases"

        headers = {"User-Agent": "KeymastersKeepGames/1.0"}
        params: Dict[str, Any] = {"per_page": per_page}
        if token:
            headers["Authorization"] = f"Discogs token={token}"

        try:
            while True:
                params["page"] = page
                resp = requests.get(base_url, headers=headers, params=params, timeout=30)

                if resp.status_code == 404:
                    if not self._notice_printed:
                        print(f"[Discogs] User '{username}' not found or collection is private.")
                        self._notice_printed = True
                    return []
                if resp.status_code == 401:
                    if not self._notice_printed:
                        print(f"[Discogs] Authentication failed for '{username}'. Check your token.")
                        self._notice_printed = True
                    return []
                if resp.status_code == 429:
                    if not self._notice_printed:
                        print("[Discogs] Rate limit exceeded. Try adding a personal access token.")
                        self._notice_printed = True
                    break
                if resp.status_code != 200:
                    if not self._notice_printed:
                        print(f"[Discogs] Unexpected status {resp.status_code} fetching collection.")
                        self._notice_printed = True
                    break

                data = resp.json()
                for item in data.get("releases", []):
                    basic_info = item.get("basic_information", {})
                    artists = [a.get("name", "") for a in basic_info.get("artists", [])]
                    # Clean artist names (remove Discogs disambiguation suffixes like " (2)")
                    artists = [re.sub(r"\s*\(\d+\)$", "", a) for a in artists if a]

                    formats_raw = basic_info.get("formats", [])
                    format_names: List[str] = []
                    for fmt in formats_raw:
                        name = fmt.get("name", "")
                        if name:
                            format_names.append(name)

                    # Collect format descriptions for disambiguation
                    format_descriptions: List[str] = []
                    for fmt in formats_raw:
                        name = fmt.get("name", "")
                        desc_parts = fmt.get("descriptions", [])
                        if name and desc_parts:
                            format_descriptions.append(f"{name} ({', '.join(desc_parts)})")
                        elif name:
                            format_descriptions.append(name)

                    # Collect catalog numbers for disambiguation
                    labels_with_catno = []
                    for l in basic_info.get("labels", []):
                        label_name = l.get("name", "")
                        catno = l.get("catno", "")
                        if label_name:
                            labels_with_catno.append({
                                "name": label_name,
                                "catno": catno,
                            })

                    releases.append({
                        "title": basic_info.get("title", "Unknown"),
                        "artists": artists,
                        "genres": basic_info.get("genres", []),
                        "styles": basic_info.get("styles", []),
                        "labels": [l["name"] for l in labels_with_catno],
                        "labels_with_catno": labels_with_catno,
                        "year": basic_info.get("year", 0),
                        "formats": format_names,
                        "format_descriptions": format_descriptions,
                    })

                pagination = data.get("pagination", {})
                if page >= pagination.get("pages", 1):
                    break
                page += 1

        except requests.RequestException as e:
            if not self._notice_printed:
                print(f"[Discogs] Network error fetching collection: {e}")
                self._notice_printed = True

        return releases


_discogs_holder = _DiscogsCollectionHolder()


# === Main Game Class ===
class DiscogsCollectionGame(Game):
    name = "Discogs Collection"
    platform = KeymastersKeepGamePlatforms.META
    is_adult_only_or_unrated = False
    options_cls = DiscogsCollectionArchipelagoOptions

    def _get_username(self) -> str:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return ""
        return str(getattr(opts.discogs_collection_username, "value", "") or "").strip()

    def _get_token(self) -> str:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return ""
        return str(getattr(opts.discogs_collection_token, "value", "") or "").strip()

    def _get_raw_collection(self) -> List[Dict[str, Any]]:
        username = self._get_username()
        token = self._get_token()
        if not username:
            return []
        return _discogs_holder.fetch_collection(username, token)

    def _excluded_genres(self) -> Set[str]:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return set()
        try:
            return set(opts.discogs_collection_excluded_genres.value or [])
        except Exception:
            return set()

    def _excluded_formats(self) -> Set[str]:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return set()
        try:
            return set(opts.discogs_collection_excluded_formats.value or [])
        except Exception:
            return set()

    def _include_deep_dives(self) -> bool:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return True
        try:
            return bool(getattr(opts.discogs_collection_include_deep_dives, "value", True))
        except Exception:
            return True

    def _filtered_collection(self) -> List[Dict[str, Any]]:
        """Apply exclusions to the raw collection."""
        raw = self._get_raw_collection()
        excluded_genres = self._excluded_genres()
        excluded_formats = self._excluded_formats()

        if not excluded_genres and not excluded_formats:
            return raw

        filtered = []
        for release in raw:
            # Skip if all genres are excluded
            if excluded_genres and release["genres"]:
                if all(g in excluded_genres for g in release["genres"]):
                    continue
            # Skip if all formats are excluded
            if excluded_formats and release["formats"]:
                if all(f in excluded_formats for f in release["formats"]):
                    continue
            filtered.append(release)

        return filtered

    # === Attribute extraction ===
    def albums(self) -> List[str]:
        """Returns 'Artist - Title' strings for all releases.

        Disambiguation info (year, format, label/catno) is always appended
        so the player knows which specific physical edition to look for.
        """
        collection = self._filtered_collection()

        # Build base keys and detect duplicates
        base_key_counts: Dict[str, int] = {}
        entries: List[Tuple[str, Dict[str, Any]]] = []
        for r in collection:
            artist_str = ", ".join(r["artists"]) if r["artists"] else "Various Artists"
            base_key = f"{artist_str} - {r['title']}"
            base_key_counts[base_key] = base_key_counts.get(base_key, 0) + 1
            entries.append((base_key, r))

        albums = []
        for base_key, r in entries:
            # Always include disambiguation info (year, format, label/catno)
            parts = []
            year = r.get("year", 0)
            if year and year > 0:
                parts.append(str(year))
            if r.get("format_descriptions"):
                parts.append(r["format_descriptions"][0])
            elif r.get("formats"):
                parts.append(r["formats"][0])
            labels_catno = r.get("labels_with_catno", [])
            if labels_catno:
                lc = labels_catno[0]
                if lc.get("catno") and lc["catno"].lower() not in ("none", ""):
                    parts.append(f"{lc['name']} {lc['catno']}")
                elif lc.get("name"):
                    parts.append(lc["name"])
            if parts:
                albums.append(f"{base_key} [{', '.join(parts)}]")
            else:
                albums.append(base_key)

        return sorted(set(albums))

    def artists(self) -> List[str]:
        """Returns unique artist names."""
        collection = self._filtered_collection()
        artists: Set[str] = set()
        for r in collection:
            for a in r["artists"]:
                if a and a.lower() != "various":
                    artists.add(a)
        return sorted(artists)

    def genres(self) -> List[str]:
        """Returns unique genres (after exclusion filtering)."""
        collection = self._filtered_collection()
        excluded = self._excluded_genres()
        genres: Set[str] = set()
        for r in collection:
            for g in r["genres"]:
                if g and g not in excluded:
                    genres.add(g)
        return sorted(genres)

    def styles(self) -> List[str]:
        """Returns unique styles/subgenres."""
        collection = self._filtered_collection()
        styles: Set[str] = set()
        for r in collection:
            for s in r["styles"]:
                if s:
                    styles.add(s)
        return sorted(styles)

    def labels(self) -> List[str]:
        """Returns unique record labels."""
        collection = self._filtered_collection()
        labels: Set[str] = set()
        for r in collection:
            for l in r["labels"]:
                if l:
                    labels.add(l)
        return sorted(labels)

    def genre_decade_combos(self) -> List[str]:
        """Returns validated 'genre album from the decade' combo strings."""
        collection = self._filtered_collection()
        excluded = self._excluded_genres()
        combos: Set[str] = set()
        for r in collection:
            year = r.get("year", 0)
            if not year or year <= 0:
                continue
            decade = f"{(year // 10) * 10}s"
            for g in r["genres"]:
                if g and g not in excluded:
                    combos.add(f"{g} album from the {decade}")
        return sorted(combos)

    def decades(self) -> List[str]:
        """Returns decade strings like '1980s', '1990s'."""
        collection = self._filtered_collection()
        decade_set: Set[str] = set()
        for r in collection:
            year = r.get("year", 0)
            if year and year > 0:
                decade = (year // 10) * 10
                decade_set.add(f"{decade}s")
        return sorted(decade_set)

    def formats(self) -> List[str]:
        """Returns unique format names (Vinyl, CD, Cassette, etc.)."""
        collection = self._filtered_collection()
        excluded = self._excluded_formats()
        formats: Set[str] = set()
        for r in collection:
            for f in r["formats"]:
                if f and f not in excluded:
                    formats.add(f)
        return sorted(formats)

    # === Objective generation ===
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return []

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = []

        # If no username configured, provide a fallback
        if not self._get_username():
            objectives.append(
                GameObjectiveTemplate(
                    label="Listen to a random album from your collection",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )
            return objectives

        # If collection is empty (API error, private, etc.), fallback
        if not self._filtered_collection():
            objectives.append(
                GameObjectiveTemplate(
                    label="Listen to a random album from your Discogs collection",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )
            return objectives

        # Primary: Listen to a specific album
        if self.albums():
            objectives.append(
                GameObjectiveTemplate(
                    label="Listen to ALBUM",
                    data={"ALBUM": (self.albums, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                )
            )

        # Genre-based exploration
        if self.genres():
            objectives.append(
                GameObjectiveTemplate(
                    label="Listen to an album from the GENRE genre in your collection",
                    data={"GENRE": (self.genres, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Style/subgenre-based exploration
        if self.styles():
            objectives.append(
                GameObjectiveTemplate(
                    label="Listen to a STYLE release from your collection",
                    data={"STYLE": (self.styles, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Decade-based listening
        if self.decades():
            objectives.append(
                GameObjectiveTemplate(
                    label="Listen to something from the DECADE from your collection",
                    data={"DECADE": (self.decades, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Label exploration
        if self.labels():
            objectives.append(
                GameObjectiveTemplate(
                    label="Explore a release on the LABEL label from your collection",
                    data={"LABEL": (self.labels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )

        # Format-based listening
        if self.formats():
            objectives.append(
                GameObjectiveTemplate(
                    label="Listen to a FORMAT release from your collection",
                    data={"FORMAT": (self.formats, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )

        # Artist deep dive (time consuming)
        if self._include_deep_dives() and self.artists():
            objectives.append(
                GameObjectiveTemplate(
                    label="Deep dive into ARTIST's releases in your collection",
                    data={"ARTIST": (self.artists, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Combo: genre + decade (pre-validated)
        if self.genre_decade_combos():
            objectives.append(
                GameObjectiveTemplate(
                    label="Listen to a GENRE_DECADE in your collection",
                    data={"GENRE_DECADE": (self.genre_decade_combos, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )

        return objectives


# === Archipelago Option Classes ===
class DiscogsCollectionUsername(FreeText):
    """
    Your Discogs username. Your collection must be set to public (or provide a
    personal access token below for private collections).

    Find your username at: https://www.discogs.com/settings/account
    """

    display_name = "Discogs Collection Username"


class DiscogsCollectionToken(FreeText):
    """
    Optional: Your Discogs personal access token for private collections or
    higher API rate limits.

    Generate one at: https://www.discogs.com/settings/developers
    Leave blank if your collection is public.
    """

    display_name = "Discogs Collection Token"


class DiscogsCollectionExcludedGenres(OptionSet):
    """
    Genres to exclude from challenge generation. Releases where ALL genres
    are excluded will be filtered out.

    Common Discogs genres: Rock, Electronic, Pop, Jazz, Funk / Soul,
    Classical, Hip Hop, Latin, Reggae, Blues, Non-Music, Stage & Screen
    """

    display_name = "Discogs Collection Excluded Genres"
    default = []


class DiscogsCollectionExcludedFormats(OptionSet):
    """
    Formats to exclude from challenge generation. Releases where ALL formats
    are excluded will be filtered out.

    Common Discogs formats: Vinyl, CD, Cassette, File, Box Set
    """

    display_name = "Discogs Collection Excluded Formats"
    default = []


class DiscogsCollectionIncludeDeepDives(Toggle):
    """
    Include 'deep dive' objectives that ask you to explore an artist's full
    discography within your collection. These are more time-consuming.
    """

    display_name = "Discogs Collection Include Deep Dives"
