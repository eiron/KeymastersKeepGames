
"""
Playnite Library integration for Keymasters Keep: provides attribute extraction, filtering, and challenge objective generation.
"""

from __future__ import annotations

import functools
import json
import requests  # type: ignore
from os import environ
from pathlib import Path
from typing import List, Dict, Set, Any

from dataclasses import dataclass

# Project-specific imports (provide stubs for standalone WIP testing)
from Options import NamedRange, FreeText, OptionSet  # type: ignore
from ..game import Game  # type: ignore
from ..game_objective_template import GameObjectiveTemplate  # type: ignore
from ..enums import KeymastersKeepGamePlatforms  # type: ignore

# Option Dataclass
@dataclass
class PlayniteLibraryArchipelagoOptions:
    playnite_library_min_time_played: "PlayniteLibraryMinTimePlayed"
    playnite_library_max_time_played: "PlayniteLibraryMaxTimePlayed"
    playnite_library_json_path: "PlayniteLibraryJsonPath"
    playnite_library_excluded_games: "PlayniteLibraryExcludedGames"
    playnite_library_excluded_completion_statuses: "PlayniteLibraryExcludedCompletionStatuses"
    playnite_library_min_release_year: "PlayniteLibraryMinReleaseYear"
    playnite_library_max_release_year: "PlayniteLibraryMaxReleaseYear"
    playnite_library_min_user_score: "PlayniteLibraryMinUserScore"
    playnite_library_min_critic_score: "PlayniteLibraryMinCriticScore"
    playnite_library_min_community_score: "PlayniteLibraryMinCommunityScore"


class PlayniteLibraryGame(Game):
    def print_distinct_elements(self):
        """Print a summary of distinct element counts from the Playnite library."""
        tags = self.tags()
        genres = self.genres()
        features = self.features()
        platforms = self.platforms()
        categories = self.categories()
        series = self.series()
        print("Distinct element counts from Playnite library:")
        print(f"- Tags: {len(tags)}")
        print(f"- Genres: {len(genres)}")
        print(f"- Features: {len(features)}")
        print(f"- Platforms: {len(platforms)}")
        print(f"- Categories: {len(categories)}")
        print(f"- Series: {len(series)}")
    # === Attribute extraction helpers ===
    def categories(self) -> List[str]:
        json_path = self._get_json_path()
        if not json_path:
            return []
        cats: Set[str] = set()
        for g in playnite_library.games(json_path):
            for cat in g.get("Categories") or []:
                if isinstance(cat, dict) and "Name" in cat:
                    cats.add(cat["Name"])
                elif isinstance(cat, str):
                    cats.add(cat)
        return sorted(cats)

    def series(self) -> List[str]:
        json_path = self._get_json_path()
        if not json_path:
            return []
        sers: Set[str] = set()
        for g in playnite_library.games(json_path):
            ser = g.get("Series")
            if isinstance(ser, list):
                for s in ser:
                    if isinstance(s, dict) and "Name" in s:
                        sers.add(s["Name"])
                    elif isinstance(s, str) and s:
                        sers.add(s)
            elif isinstance(ser, dict) and "Name" in ser:
                sers.add(ser["Name"])
            elif isinstance(ser, str) and ser:
                sers.add(ser)
        return sorted(sers)
    def tags(self) -> List[str]:
        json_path = self._get_json_path()
        if not json_path:
            return []
        tags: Set[str] = set()
        for g in playnite_library.games(json_path):
            for tag in g.get("Tags") or []:
                if isinstance(tag, dict) and "Name" in tag:
                    tags.add(tag["Name"])
                elif isinstance(tag, str):
                    tags.add(tag)
        return sorted(tags)

    def genres(self) -> List[str]:
        json_path = self._get_json_path()
        if not json_path:
            return []
        genres: Set[str] = set()
        for g in playnite_library.games(json_path):
            for genre in g.get("Genres") or []:
                if isinstance(genre, dict) and "Name" in genre:
                    genres.add(genre["Name"])
                elif isinstance(genre, str):
                    genres.add(genre)
        return sorted(genres)

    def sources(self) -> List[str]:
        json_path = self._get_json_path()
        if not json_path:
            return []
        sources: Set[str] = set()
        for g in playnite_library.games(json_path):
            src = g.get("source")
            if src:
                sources.add(src)
        return sorted(sources)

    def platforms(self) -> List[str]:
        json_path = self._get_json_path()
        if not json_path:
            return []
        platforms: Set[str] = set()
        for g in playnite_library.games(json_path):
            for plat in g.get("Platforms") or []:
                if isinstance(plat, dict) and "Name" in plat:
                    platforms.add(plat["Name"])
                elif isinstance(plat, str):
                    platforms.add(plat)
        return sorted(platforms)

    def features(self) -> List[str]:
        json_path = self._get_json_path()
        if not json_path:
            return []
        features: Set[str] = set()
        for g in playnite_library.games(json_path):
            for feat in g.get("Features") or []:
                if isinstance(feat, dict) and "Name" in feat:
                    features.add(feat["Name"])
                elif isinstance(feat, str):
                    features.add(feat)
        return sorted(features)

    def _get_json_path(self) -> str:
        arch_opts = getattr(self, "archipelago_options", None)
        json_path = ""
        if arch_opts is not None:
            try:
                json_path = str(getattr(arch_opts.playnite_library_json_path, "value", "") or "").strip()
            except Exception:
                json_path = ""
        if not json_path:
            json_path = (environ.get("PLAYNITE_LIBRARY_JSON") or "").strip()
        return json_path
    name = "Playnite Library"
    platform = KeymastersKeepGamePlatforms.META

    is_adult_only_or_unrated = False

    options_cls = PlayniteLibraryArchipelagoOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        """Generate all unique Playnite library challenge objectives.

        If the Playnite JSON is missing or unreadable, return an empty list so
        no Playnite objectives are generated.
        """
        # Early out if we have no games (e.g., JSON missing)
        json_path = self._get_json_path()
        if not json_path or not playnite_library.games(json_path):
            return []
        # Also skip if filters result in no playable games
        if not self.games():
            return []

        objectives = [
            GameObjectiveTemplate(
                label="Play GAME from your Playnite library",
                data={"GAME": (self.games, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
        ]
        # Only add series/year objectives if choices exist
        if self.series():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play a Playnite library game from the SERIES series",
                    data={"SERIES": (self.series, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )
        if self.release_year_choices():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play a Playnite library game released in YEAR",
                    data={"YEAR": (self.release_year_choices, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )

        attribute_types = [
            ("TAG", self.tags),
            ("GENRE", self.genres),
            ("FEATURE", self.features),
            ("PLATFORM", self.platforms),
            ("CATEGORY", self.categories),
            ("SOURCE", self.sources),
        ]
        ordering_options = [
            ("most recently added", "Most Recently Added"),
            ("oldest", "Oldest"),
            ("newest", "Newest"),
            ("highest-rated (UserScore)", "Highest-Rated (UserScore)"),
            ("highest-rated (CriticScore)", "Highest-Rated (CriticScore)"),
            ("highest-rated (CommunityScore)", "Highest-Rated (CommunityScore)"),
        ]

        for attr_label, attr_func in attribute_types:
            attr_values = attr_func()
            # Only add objectives if there are enough values to sample from
            if not attr_values or len(attr_values) < 1:
                continue
            objectives.append(
                GameObjectiveTemplate(
                    label=f"Play a Playnite library game with the {attr_label} {attr_label.lower()}",
                    data={attr_label: (attr_func, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                )
            )
            # Only add random objective if there are at least 2 values to sample from
            if len(attr_values) >= 2:
                objectives.append(
                    GameObjectiveTemplate(
                        label=f"Play a random Playnite library game with the {attr_label} {attr_label.lower()}",
                        data={attr_label: (attr_func, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=4,
                    )
                )
        for order_key, order_label in ordering_options:
            if self.nth_choices():
                objectives.append(
                    GameObjectiveTemplate(
                        label=f"Play your NTH {order_label} Playnite library game",
                        data={"NTH": (self.nth_choices, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=2,
                    )
                )
        seen_labels = set()
        unique_objectives = []
        for obj in objectives:
            if obj.label not in seen_labels:
                unique_objectives.append(obj)
                seen_labels.add(obj.label)
        return unique_objectives

    def games_with_tag(self, tag: str) -> List[str]:
        json_path = self._get_json_path()
        result: List[str] = []
        for game in playnite_library.games(json_path):
            tags = set()
            for t in game.get("Tags", []):
                if isinstance(t, dict) and "Name" in t:
                    tags.add(t["Name"])
                elif isinstance(t, str):
                    tags.add(t)
            if tag in tags:
                display_name = game["name"]
                source = game.get("source")
                if source:
                    display_name = f"{display_name} [Source: {source}]"
                result.append(display_name)
        return result

    def nth_choices(self) -> List[str]:
        """Offer NTH choices bounded by available games to avoid out-of-range indices.

        Returns ordinals from 1 up to min(10, total_available_games). If there are
        no available games, returns an empty list.
        """
        total = len(self.games())
        if total <= 0:
            return []
        max_n = min(10, total)
        return [self._ordinal(n) for n in range(1, max_n + 1)]

    def _ordinal(self, n: int) -> str:
        # Grammar-correct ordinal: 1st, 2nd, 3rd, 4th, ... including 11th/12th/13th exceptions
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

    def release_year_choices(self) -> List[int]:
        # Offer a range of years from the games
        json_path = self._get_json_path()
        if not json_path:
            return []
        years = set()
        for g in playnite_library.games(json_path):
            y = g.get("release_year", 0)
            if y:
                years.add(y)
        return sorted(years)

    def games(self) -> List[str]:
        # Be resilient when options aren't set yet (during options JSON generation)
        arch_opts = getattr(self, "archipelago_options", None)
        min_time_played = 0
        max_time_played = -1
        json_path = ""
        excluded_statuses: Set[str] = set()
        min_release_year = 0
        max_release_year = 9999
        min_user_score = 0
        min_critic_score = 0
        min_community_score = 0
        
        if arch_opts is not None:
            try:
                min_time_played = int(getattr(arch_opts.playnite_library_min_time_played, "value", 0))
            except Exception:
                min_time_played = 0
            try:
                max_time_played = int(getattr(arch_opts.playnite_library_max_time_played, "value", -1))
            except Exception:
                max_time_played = -1
            try:
                json_path = str(getattr(arch_opts.playnite_library_json_path, "value", "") or "").strip()
            except Exception:
                json_path = ""
            try:
                excluded_statuses = getattr(arch_opts.playnite_library_excluded_completion_statuses, "value", set())
            except Exception:
                excluded_statuses = set()
            try:
                min_release_year = int(getattr(arch_opts.playnite_library_min_release_year, "value", 0))
            except Exception:
                min_release_year = 0
            try:
                max_release_year = int(getattr(arch_opts.playnite_library_max_release_year, "value", 9999))
            except Exception:
                max_release_year = 9999
            try:
                min_user_score = int(getattr(arch_opts.playnite_library_min_user_score, "value", 0))
            except Exception:
                min_user_score = 0
            try:
                min_critic_score = int(getattr(arch_opts.playnite_library_min_critic_score, "value", 0))
            except Exception:
                min_critic_score = 0
            try:
                min_community_score = int(getattr(arch_opts.playnite_library_min_community_score, "value", 0))
            except Exception:
                min_community_score = 0

        if not json_path:
            json_path = (environ.get("PLAYNITE_LIBRARY_JSON") or "").strip()

        # Compute excluded games once for logging and reuse
        excluded_games_set = self.excluded_games()

        # Print filter summary only once per session to avoid flooding console
        if not hasattr(self, '_playnite_filter_log_printed'):
            print(
                "Filtering Playnite library with "
                f"min_time={min_time_played}, max_time={max_time_played}, "
                f"min_year={min_release_year}, max_year={max_release_year}, "
                f"min_user={min_user_score}, min_critic={min_critic_score}, min_community={min_community_score}, "
                f"excluded_statuses={len(excluded_statuses)}, excluded_games={len(excluded_games_set)}"
            )
            self._playnite_filter_log_printed = True

        # If we still don't have a JSON path, return empty list rather than erroring during option generation
        if not json_path:
            return []

        result: List[str] = []
        for game in playnite_library.games(json_path):
            # Playtime filter
            if game.get("playtime_minutes", 0) < min_time_played:
                continue
            if max_time_played != -1 and game.get("playtime_minutes", 0) > max_time_played:
                continue
            
            # Exclusion filter
            if game["name"] in excluded_games_set or str(game.get("id", "")) in excluded_games_set:
                continue
            
            # Completion status filter
            completion_status = game.get("completion_status")
            if completion_status and excluded_statuses and completion_status in excluded_statuses:
                continue
            
            # Release year filter
            release_year = game.get("release_year", 0)
            if release_year:
                if release_year < min_release_year or release_year > max_release_year:
                    continue
            
            # Score filters (User -> Critic -> Community)
            user_score = game.get("user_score", 0)
            if user_score < min_user_score:
                continue

            critic_score = game.get("critic_score", 0)
            if critic_score < min_critic_score:
                continue

            community_score = game.get("community_score", 0)
            if community_score < min_community_score:
                continue

            display_name = game["name"]
            source = game.get("source")
            if source:
                display_name = f"{display_name} [Source: {source}]"

            result.append(display_name)

        return result

    def excluded_games(self) -> Set[str]:
        arch_opts = getattr(self, "archipelago_options", None)
        if arch_opts is None:
            return set()
        try:
            excluded_games = arch_opts.playnite_library_excluded_games.value
        except Exception:
            return set()
        return excluded_games or set()


class PlayniteLibraryMinTimePlayed(NamedRange):
    """
    Only include games from your Playnite library that have been played at least this many minutes.

    Use 0 or "no_limit" for no minimum.
    """

    display_name = "Playnite Library Min-Time Played"
    default = 0
    range_start = 0
    range_end = 5256000
    special_range_names = {
        "no_limit": 0,
    }


class PlayniteLibraryMaxTimePlayed(NamedRange):
    """
    Only include games from your Playnite library that have been played at most this many minutes.

    Use -1 or "no_limit" for no maximum.
    """

    display_name = "Playnite Library Max-Time Played"
    default = -1
    range_start = -1
    range_end = 5256000
    special_range_names = {
        "no_limit": -1,
        "never_played": 0,
    }


class PlayniteLibraryJsonPath(FreeText):
    """
    Path to a JSON export of your Playnite library.

    Recommended: Use Playnite's Library Exporter extension or a custom export to produce a JSON file
    that includes fields like Name and Playtime (seconds or minutes). This file can be stored in your documents
    and referenced here. If Playnite is open and locking its database, exporting a snapshot avoids file locks.
    """

    display_name = "Playnite Library JSON Path"


class PlayniteLibraryExcludedGames(OptionSet):
    """
    List of game names (exact match) or Playnite Game IDs to exclude from the Playnite library.
    """

    display_name = "Playnite Library Excluded Games"


class PlayniteLibraryExcludedCompletionStatuses(OptionSet):
    """
    Completion statuses to exclude from the library (e.g., "Completed", "Beaten", "Playing").
    Use exact names from your Playnite completion statuses.
    """

    display_name = "Playnite Library Excluded Completion Statuses"


class PlayniteLibraryMinReleaseYear(NamedRange):
    """
    Only include games released in or after this year. Use 0 for no minimum.
    """

    display_name = "Playnite Library Min Release Year"
    default = 0
    range_start = 0
    range_end = 9999
    special_range_names = {
        "no_limit": 0,
    }


class PlayniteLibraryMaxReleaseYear(NamedRange):
    """
    Only include games released in or before this year. Use 9999 for no maximum.
    """

    display_name = "Playnite Library Max Release Year"
    default = 9999
    range_start = 1970
    range_end = 9999
    special_range_names = {
        "no_limit": 9999,
    }


class PlayniteLibraryMinUserScore(NamedRange):
    """
    Only include games with a user score of at least this value (0-100). Use 0 for no minimum.
    """

    display_name = "Playnite Library Min User Score"
    default = 0
    range_start = 0
    range_end = 100
    special_range_names = {
        "no_limit": 0,
    }


class PlayniteLibraryMinCriticScore(NamedRange):
    """
    Only include games with a critic score of at least this value (0-100). Use 0 for no minimum.
    """

    display_name = "Playnite Library Min Critic Score"
    default = 0
    range_start = 0
    range_end = 100
    special_range_names = {
        "no_limit": 0,
    }


class PlayniteLibraryMinCommunityScore(NamedRange):
    """
    Only include games with a community score of at least this value (0-100). Use 0 for no minimum.
    """

    display_name = "Playnite Library Min Community Score"
    default = 0
    range_start = 0
    range_end = 100
    special_range_names = {
        "no_limit": 0,
    }


class PlayniteLibraryHolder:
    def __init__(self):
        self._printed_elements = False
        # Print a one-time notice if JSON is missing/unreadable so we don't spam logs
        self._missing_ok_notice_printed = False
    
    @functools.lru_cache(maxsize=None)
    def games(self, json_path: str) -> List[Dict[str, Any]]:
        # If the JSON cannot be found or read, treat as empty gracefully
        try:
            normalized = self._read_and_normalize(json_path)
        except Exception as e:
            if not self._missing_ok_notice_printed:
                print(f"[Playnite] No library JSON found or unreadable at '{json_path}': {e}. Skipping Playnite objectives.")
                self._missing_ok_notice_printed = True
            return []
        # Print distinct elements only once per session
        if not self._printed_elements:
            self._printed_elements = True
            self._print_distinct_elements_from_data(normalized)
        return normalized
    
    def _print_distinct_elements_from_data(self, normalized: List[Dict[str, Any]]):
        """Extract and print distinct elements directly from normalized data to avoid recursion."""
        tags: Set[str] = set()
        genres: Set[str] = set()
        features: Set[str] = set()
        platforms: Set[str] = set()
        categories: Set[str] = set()
        series: Set[str] = set()
        sources: Set[str] = set()
        
        for g in normalized:
            # Tags
            for tag in g.get("Tags") or []:
                if isinstance(tag, dict) and "Name" in tag:
                    tags.add(tag["Name"])
                elif isinstance(tag, str):
                    tags.add(tag)
            
            # Genres
            for genre in g.get("Genres") or []:
                if isinstance(genre, dict) and "Name" in genre:
                    genres.add(genre["Name"])
                elif isinstance(genre, str):
                    genres.add(genre)
            
            # Features
            for feat in g.get("Features") or []:
                if isinstance(feat, dict) and "Name" in feat:
                    features.add(feat["Name"])
                elif isinstance(feat, str):
                    features.add(feat)
            
            # Platforms
            for plat in g.get("Platforms") or []:
                if isinstance(plat, dict) and "Name" in plat:
                    platforms.add(plat["Name"])
                elif isinstance(plat, str):
                    platforms.add(plat)
            
            # Categories
            for cat in g.get("Categories") or []:
                if isinstance(cat, dict) and "Name" in cat:
                    categories.add(cat["Name"])
                elif isinstance(cat, str):
                    categories.add(cat)
            
            # Sources
            src = g.get("source")
            if src:
                sources.add(src)
            
            # Series (can be a list of series objects, a single dict, a string, or None)
            ser = g.get("Series")
            if isinstance(ser, list):
                for s in ser:
                    if isinstance(s, dict) and "Name" in s:
                        series.add(s["Name"])
                    elif isinstance(s, str) and s:
                        series.add(s)
            elif isinstance(ser, dict) and "Name" in ser:
                series.add(ser["Name"])
            elif isinstance(ser, str) and ser:
                series.add(ser)
        
        print("\n=== Playnite Library Statistics ===")
        print(f"Tags: {len(tags)}")
        print(f"Genres: {len(genres)}")
        print(f"Features: {len(features)}")
        print(f"Platforms: {len(platforms)}")
        print(f"Categories: {len(categories)}")
        print(f"Sources: {len(sources)}")
        print(f"Series: {len(series)}")
        print(f"Total Games: {len(normalized)}")
        print("=" * 36 + "\n")

    def _read_and_normalize(self, json_path: str) -> List[Dict[str, Any]]:
        if not json_path:
            raise RuntimeError(
                "No Playnite Library JSON path provided. Set playnite_library_json_path or PLAYNITE_LIBRARY_JSON."
            )

        data: Any
        if json_path.lower().startswith("http://") or json_path.lower().startswith("https://"):
            print(f"Fetching Playnite library JSON from URL: {json_path}...")
            try:
                if requests is None:
                    raise RuntimeError("The 'requests' package is required to fetch HTTP URLs. Install it or use a local file path.")
                resp = requests.get(json_path, timeout=15)
                if resp.status_code != 200:
                    raise RuntimeError(f"HTTP {resp.status_code} fetching Playnite library JSON")
                data = resp.json()
            except Exception as e:
                raise RuntimeError(f"Failed to fetch Playnite library JSON from URL: {e}")
        else:
            path = Path(json_path).expanduser()
            # If a folder was provided, look for games.json inside it
            if path.is_dir():
                candidate = path / "games.json"
                if candidate.exists():
                    path = candidate
                else:
                    raise RuntimeError(
                        f"Provided folder '{path}' does not contain 'games.json'. Please place your export there or provide a file path."
                    )

            if not path.exists():
                raise RuntimeError(
                    f"Playnite Library JSON not found at '{path}'. Provide a folder containing 'games.json' or a direct file path."
                )

            print(f"Loading Playnite library from {path}...")
            # Read JSON content; allow either a list of games or a dict with a games collection
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                raise RuntimeError(f"Failed to read Playnite library JSON: {e}")

        games_raw: List[Dict[str, Any]]
        if isinstance(data, list):
            games_raw = data
        elif isinstance(data, dict):
            # Common keys used by exporters
            for key in ("Games", "games", "Items", "items", "Library", "library"):
                if key in data and isinstance(data[key], list):
                    games_raw = data[key]  # type: ignore[assignment]
                    break
            else:
                raise RuntimeError(
                    "Unsupported Playnite JSON format: expected a list or a dict containing a games list."
                )
        else:
            raise RuntimeError("Unsupported Playnite JSON structure.")

        # Normalize game entries
        normalized: List[Dict[str, Any]] = []
        for g in games_raw:
            # Name - exact field from Playnite JSON
            name = g.get("Name")
            if not name:
                # Skip entries without a name
                continue

            # IDs - Playnite uses GUID strings in Id field
            gid = g.get("Id", "")

            # Playtime - stored in seconds in Playnite JSON
            playtime_seconds = g.get("Playtime", 0)
            playtime_minutes = int(playtime_seconds) // 60

            # Source - object with Name field (e.g., Steam, GOG, itch.io)
            source_name = None
            source_obj = g.get("Source")
            if isinstance(source_obj, dict):
                source_name = source_obj.get("Name")

            # Completion status - object with Name field
            completion_status = None
            completion_obj = g.get("CompletionStatus")
            if isinstance(completion_obj, dict):
                completion_status = completion_obj.get("Name")

            # Release year (int)
            release_year = int(g.get("ReleaseYear", 0) or 0)

            # Scores
            user_score = int(g.get("UserScore", 0) or 0)
            critic_score = int(g.get("CriticScore", 0) or 0)
            community_score = int(g.get("CommunityScore", 0) or 0)

            # Additional attributes commonly present in Playnite exports
            tags_list = g.get("Tags", [])
            genres_list = g.get("Genres", [])
            features_list = g.get("Features", [])
            platforms_list = g.get("Platforms", [])
            categories_list = g.get("Categories", [])
            series_obj = g.get("Series")
            favorite_flag = bool(g.get("Favorite", False))
            added_date = g.get("Added")
            modified_date = g.get("Modified")

            normalized.append({
                "name": str(name),
                "id": str(gid),
                "playtime_minutes": playtime_minutes,
                "source": str(source_name) if source_name else None,
                "completion_status": str(completion_status) if completion_status else None,
                "release_year": release_year,
                "user_score": user_score,
                "critic_score": critic_score,
                "community_score": community_score,
                # Pass-through attributes for helper-based filtering
                "Tags": tags_list,
                "Genres": genres_list,
                "Features": features_list,
                "Platforms": platforms_list,
                "Categories": categories_list,
                "Series": series_obj,
                "Favorite": favorite_flag,
                "Added": added_date,
                "Modified": modified_date,
            })

        return normalized


playnite_library = PlayniteLibraryHolder()