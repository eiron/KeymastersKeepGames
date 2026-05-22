"""
Film Collection game for Keymaster's Keep.

Parses Letterboxd and/or IMDb CSV exports and generates film-watching challenges
based on the movies, directors, genres, decades, runtimes, and ratings in the
player's collection.

CSV files should be placed in the film_collection/ subfolder alongside this file:
    film_collection/
        letterboxd/   <- Drop Letterboxd CSV exports here
        imdb/         <- Drop IMDb CSV exports here

Multiple CSVs per source are supported; all files in each subfolder are merged.
"""

from __future__ import annotations

import csv
import functools
from pathlib import Path
from typing import Dict, List, Set, Any

from dataclasses import dataclass

from Options import FreeText, OptionSet, TextChoice, Toggle  # type: ignore
from ..game import Game  # type: ignore
from ..game_objective_template import GameObjectiveTemplate  # type: ignore
from ..enums import KeymastersKeepGamePlatforms  # type: ignore


# === Options Dataclass ===
@dataclass
class FilmCollectionArchipelagoOptions:
    film_collection_folder: "FilmCollectionFolder"
    film_collection_source: "FilmCollectionSource"
    film_collection_excluded_genres: "FilmCollectionExcludedGenres"
    film_collection_excluded_directors: "FilmCollectionExcludedDirectors"
    film_collection_include_runtime_challenges: "FilmCollectionIncludeRuntimeChallenges"
    film_collection_include_rating_challenges: "FilmCollectionIncludeRatingChallenges"


# === Module-level CSV holder with caching ===
# Base folder lives alongside this file
_FILM_COLLECTION_DIR = Path(__file__).parent / "film_collection"


class _FilmCollectionHolder:
    """Caches parsed CSV data keyed by source name."""

    def __init__(self):
        self._notice_printed = False

    @functools.lru_cache(maxsize=4)
    def parse_source(self, source: str, base_dir: str = "") -> List[Dict[str, Any]]:
        """Parse all CSVs for the given source(s).

        source: "letterboxd", "imdb", or "both"
        base_dir: custom folder path (empty = use default)
        """
        films: List[Dict[str, Any]] = []
        collection_dir = Path(base_dir) if base_dir else _FILM_COLLECTION_DIR

        sources_to_load: List[str] = []
        if source == "both":
            sources_to_load = ["letterboxd", "imdb"]
        else:
            sources_to_load = [source]

        for src in sources_to_load:
            src_dir = collection_dir / src
            if not src_dir.is_dir():
                if not self._notice_printed:
                    print(f"[Film Collection] Source folder not found: {src_dir}")
                    self._notice_printed = True
                continue

            csv_files = sorted(src_dir.glob("*.csv"))
            if not csv_files:
                if not self._notice_printed:
                    print(f"[Film Collection] No CSV files found in: {src_dir}")
                    self._notice_printed = True
                continue

            for csv_file in csv_files:
                films.extend(self._parse_csv_file(csv_file, src))

        return films

    def _parse_csv_file(self, path: Path, csv_format: str) -> List[Dict[str, Any]]:
        """Parse a single CSV file in the given format."""
        try:
            with open(path, "r", encoding="utf-8-sig", newline="") as f:
                if csv_format == "imdb":
                    reader = csv.DictReader(f)
                    if reader.fieldnames is None:
                        return []
                    normalized_fields = {h.strip().lower(): h for h in reader.fieldnames}
                    return self._parse_imdb(reader, normalized_fields)

                # Letterboxd: detect list exports vs standard CSVs
                first_line = f.readline().strip()

                if first_line.startswith("Letterboxd list export"):
                    # List export — scan for the header row containing "Name" and "Year"
                    header_line = None
                    for line in f:
                        stripped = line.strip()
                        if not stripped:
                            continue
                        parts = [p.strip().lower() for p in stripped.split(",")]
                        if "name" in parts and "year" in parts:
                            header_line = stripped
                            break

                    if header_line is None:
                        return []

                    reader = csv.DictReader(f, fieldnames=[h.strip() for h in header_line.split(",")])
                else:
                    # Standard Letterboxd CSV — first line is the header
                    f.seek(0)
                    reader = csv.DictReader(f)

                if reader.fieldnames is None:
                    return []

                normalized_fields = {h.strip().lower(): h for h in reader.fieldnames}
                return self._parse_letterboxd(reader, normalized_fields)

        except Exception as e:
            if not self._notice_printed:
                print(f"[Film Collection] Error reading CSV '{path.name}': {e}")
                self._notice_printed = True
            return []

    def _parse_letterboxd(self, reader: csv.DictReader, field_map: Dict[str, str]) -> List[Dict[str, Any]]:
        """Parse Letterboxd CSV format.

        Handles all Letterboxd export types:
          - watchlist.csv / watched.csv / likes: Date, Name, Year, Letterboxd URI
          - ratings.csv: Date, Name, Year, Letterboxd URI, Rating
          - diary.csv: Date, Name, Year, Letterboxd URI, Rating, Rewatch, Tags, Watched Date
          - lists/*.csv: Position, Name, Year, URL, Description
        """
        films: List[Dict[str, Any]] = []

        name_key = field_map.get("name", "") or field_map.get("title", "")
        year_key = field_map.get("year", "")
        rating_key = field_map.get("rating", "") or field_map.get("your rating", "")
        tags_key = field_map.get("tags", "")

        for row in reader:
            title = (row.get(name_key, "") or "").strip()
            if not title:
                continue

            # Year
            year = 0
            year_raw = (row.get(year_key, "") or "").strip()
            try:
                year = int(year_raw) if year_raw else 0
            except ValueError:
                year = 0

            # Rating (Letterboxd uses 0.5-5.0 scale; not present in all export types)
            rating = 0.0
            if rating_key:
                rating_raw = (row.get(rating_key, "") or "").strip()
                try:
                    rating = float(rating_raw) if rating_raw else 0.0
                except ValueError:
                    rating = 0.0

            # Tags as pseudo-genres (only in diary exports)
            genres: List[str] = []
            if tags_key:
                tags_raw = (row.get(tags_key, "") or "").strip()
                if tags_raw:
                    genres = [t.strip() for t in tags_raw.split(",") if t.strip()]

            films.append({
                "title": title,
                "year": year,
                "directors": [],
                "genres": genres,
                "runtime": 0,
                "rating": rating,
                "title_type": "movie",
                "source": "letterboxd",
            })

        return films

    def _parse_imdb(self, reader: csv.DictReader, field_map: Dict[str, str]) -> List[Dict[str, Any]]:
        """Parse IMDb CSV format (ratings or watchlist export)."""
        films: List[Dict[str, Any]] = []

        title_key = field_map.get("title", "")
        year_key = field_map.get("year", "")
        directors_key = field_map.get("directors", "") or field_map.get("director", "")
        genres_key = field_map.get("genres", "")
        runtime_key = field_map.get("runtime (mins)", "") or field_map.get("runtime", "")
        rating_key = field_map.get("you rated", "") or field_map.get("your rating", "") or field_map.get("imdb rating", "")
        type_key = field_map.get("title type", "")

        for row in reader:
            title = (row.get(title_key, "") or "").strip()
            if not title:
                continue

            # Year
            year = 0
            year_raw = (row.get(year_key, "") or "").strip()
            try:
                year = int(year_raw) if year_raw else 0
            except ValueError:
                year = 0

            # Directors
            directors: List[str] = []
            directors_raw = (row.get(directors_key, "") or "").strip()
            if directors_raw:
                directors = [d.strip() for d in directors_raw.split(",") if d.strip()]

            # Genres
            genres: List[str] = []
            genres_raw = (row.get(genres_key, "") or "").strip()
            if genres_raw:
                genres = [g.strip() for g in genres_raw.split(",") if g.strip()]

            # Runtime
            runtime = 0
            runtime_raw = (row.get(runtime_key, "") or "").strip()
            try:
                runtime = int(runtime_raw) if runtime_raw else 0
            except ValueError:
                runtime = 0

            # Rating
            rating = 0.0
            rating_raw = (row.get(rating_key, "") or "").strip()
            try:
                rating = float(rating_raw) if rating_raw else 0.0
            except ValueError:
                rating = 0.0

            # Title type
            title_type = (row.get(type_key, "") or "movie").strip().lower()

            films.append({
                "title": title,
                "year": year,
                "directors": directors,
                "genres": genres,
                "runtime": runtime,
                "rating": rating,
                "title_type": title_type,
                "source": "imdb",
            })

        return films


_film_holder = _FilmCollectionHolder()


# === Main Game Class ===
class FilmCollectionGame(Game):
    name = "Film Collection"
    platform = KeymastersKeepGamePlatforms.META
    is_adult_only_or_unrated = False
    options_cls = FilmCollectionArchipelagoOptions

    def _get_collection_dir(self) -> str:
        """Get collection folder path, accounting for player subfolder.

        If a player folder is set (e.g., "eiron"), resolves to:
            <game_file_parent>/eiron/film_collection/
        If an absolute path is given, uses it directly.
        If empty, uses the default film_collection/ alongside this file.
        """
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return ""
        try:
            val = (opts.film_collection_folder.value or "").strip()
            if not val:
                return ""
            p = Path(val)
            if p.is_absolute():
                return val
            # Treat as a player subfolder name relative to game file parent
            return str(Path(__file__).parent / val / "film_collection")
        except Exception:
            return ""

    def _get_source(self) -> str:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return "both"
        try:
            val = opts.film_collection_source.value
            if val == 1:
                return "imdb"
            elif val == 2:
                return "both"
            return "letterboxd"
        except Exception:
            return "both"

    def _excluded_genres(self) -> Set[str]:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return set()
        try:
            return set(opts.film_collection_excluded_genres.value or [])
        except Exception:
            return set()

    def _excluded_directors(self) -> Set[str]:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return set()
        try:
            return set(opts.film_collection_excluded_directors.value or [])
        except Exception:
            return set()

    def _include_runtime_challenges(self) -> bool:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return True
        try:
            return bool(getattr(opts.film_collection_include_runtime_challenges, "value", True))
        except Exception:
            return True

    def _include_rating_challenges(self) -> bool:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return True
        try:
            return bool(getattr(opts.film_collection_include_rating_challenges, "value", True))
        except Exception:
            return True

    def _get_raw_films(self) -> List[Dict[str, Any]]:
        source = self._get_source()
        return _film_holder.parse_source(source, self._get_collection_dir())

    def _filtered_films(self) -> List[Dict[str, Any]]:
        """Apply genre and director exclusion filters."""
        raw = self._get_raw_films()
        excluded_genres = self._excluded_genres()
        excluded_directors = self._excluded_directors()

        if not excluded_genres and not excluded_directors:
            return raw

        filtered = []
        for film in raw:
            # Skip if all genres are excluded
            if excluded_genres and film["genres"]:
                if all(g in excluded_genres for g in film["genres"]):
                    continue

            # Skip if all directors are excluded
            if excluded_directors and film["directors"]:
                if all(d in excluded_directors for d in film["directors"]):
                    continue

            filtered.append(film)

        return filtered

    # === Attribute extraction ===
    def films(self) -> List[str]:
        """Returns 'Title (Year)' strings for all films."""
        collection = self._filtered_films()
        film_list = []
        for f in collection:
            if f["year"]:
                film_list.append(f"{f['title']} ({f['year']})")
            else:
                film_list.append(f["title"])
        return sorted(set(film_list))

    def directors(self) -> List[str]:
        """Returns unique director names."""
        collection = self._filtered_films()
        excluded = self._excluded_directors()
        director_set: Set[str] = set()
        for f in collection:
            for d in f["directors"]:
                if d and d not in excluded:
                    director_set.add(d)
        return sorted(director_set)

    def genres(self) -> List[str]:
        """Returns unique genres (after exclusion filtering)."""
        collection = self._filtered_films()
        excluded = self._excluded_genres()
        genre_set: Set[str] = set()
        for f in collection:
            for g in f["genres"]:
                if g and g not in excluded:
                    genre_set.add(g)
        return sorted(genre_set)

    def decades(self) -> List[str]:
        """Returns decade strings like '1980s', '2000s'."""
        collection = self._filtered_films()
        decade_set: Set[str] = set()
        for f in collection:
            if f["year"] and f["year"] > 0:
                decade = (f["year"] // 10) * 10
                decade_set.add(f"{decade}s")
        return sorted(decade_set)

    def genre_decade_combos(self) -> List[str]:
        """Returns validated 'genre film from the decade' combo strings."""
        collection = self._filtered_films()
        excluded = self._excluded_genres()
        combos: Set[str] = set()
        for f in collection:
            if not f["year"] or f["year"] <= 0:
                continue
            decade = f"{(f['year'] // 10) * 10}s"
            for g in f["genres"]:
                if g and g not in excluded:
                    combos.add(f"{g} film from the {decade}")
        return sorted(combos)

    def director_decade_combos(self) -> List[str]:
        """Returns validated 'film directed by X from the decade' combo strings."""
        collection = self._filtered_films()
        excluded = self._excluded_directors()
        combos: Set[str] = set()
        for f in collection:
            if not f["year"] or f["year"] <= 0:
                continue
            decade = f"{(f['year'] // 10) * 10}s"
            for d in f["directors"]:
                if d and d not in excluded:
                    combos.add(f"film directed by {d} from the {decade}")
        return sorted(combos)

    def runtime_categories(self) -> List[str]:
        """Returns available runtime categories."""
        collection = self._filtered_films()
        categories: Set[str] = set()
        for f in collection:
            runtime = f.get("runtime", 0)
            if runtime > 0:
                if runtime < 90:
                    categories.add("short (under 90 minutes)")
                elif runtime <= 120:
                    categories.add("standard-length (90-120 minutes)")
                elif runtime <= 150:
                    categories.add("long (120-150 minutes)")
                else:
                    categories.add("epic-length (over 150 minutes)")
        return sorted(categories)

    def rating_categories(self) -> List[str]:
        """Returns rating tier categories."""
        collection = self._filtered_films()
        categories: Set[str] = set()

        for f in collection:
            rating = f.get("rating", 0.0)
            if rating > 0:
                if f.get("source") == "imdb":
                    # IMDb uses 1-10 scale
                    if rating >= 8.0:
                        categories.add("highly-rated (8+)")
                    elif rating >= 6.0:
                        categories.add("well-rated (6-8)")
                    else:
                        categories.add("divisive (under 6)")
                else:
                    # Letterboxd uses 0.5-5.0 scale
                    if rating >= 4.0:
                        categories.add("highly-rated (4+ stars)")
                    elif rating >= 3.0:
                        categories.add("well-rated (3-4 stars)")
                    else:
                        categories.add("divisive (under 3 stars)")
        return sorted(categories)

    def title_types(self) -> List[str]:
        """Returns unique title types (movie, tvSeries, etc.) from IMDb exports."""
        collection = self._filtered_films()
        types: Set[str] = set()
        for f in collection:
            t = f.get("title_type", "")
            if t and t != "movie":
                types.add(t)
        if any(f.get("title_type") == "movie" for f in collection):
            types.add("movie")
        return sorted(types)

    # === Objective generation ===
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return []

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = []

        # If no films found, provide a fallback
        if not self._filtered_films():
            objectives.append(
                GameObjectiveTemplate(
                    label="Watch a film from your collection",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                )
            )
            return objectives

        # Primary: Watch a specific film
        if self.films():
            objectives.append(
                GameObjectiveTemplate(
                    label="Watch FILM",
                    data={"FILM": (self.films, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                )
            )

        # Director-based challenge
        if self.directors():
            objectives.append(
                GameObjectiveTemplate(
                    label="Watch a film directed by DIRECTOR",
                    data={"DIRECTOR": (self.directors, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                )
            )

        # Genre-based challenge
        if self.genres():
            objectives.append(
                GameObjectiveTemplate(
                    label="Watch a GENRE film from your collection",
                    data={"GENRE": (self.genres, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                )
            )

        # Decade-based challenge
        if self.decades():
            objectives.append(
                GameObjectiveTemplate(
                    label="Watch a film from the DECADE from your collection",
                    data={"DECADE": (self.decades, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Runtime-based challenge
        if self._include_runtime_challenges() and self.runtime_categories():
            objectives.append(
                GameObjectiveTemplate(
                    label="Watch a RUNTIME film from your collection",
                    data={"RUNTIME": (self.runtime_categories, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Rating-based challenge
        if self._include_rating_challenges() and self.rating_categories():
            objectives.append(
                GameObjectiveTemplate(
                    label="Watch a RATING film from your collection",
                    data={"RATING": (self.rating_categories, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Combo: genre + decade (pre-validated)
        if self.genre_decade_combos():
            objectives.append(
                GameObjectiveTemplate(
                    label="Watch a GENRE_DECADE in your collection",
                    data={"GENRE_DECADE": (self.genre_decade_combos, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                )
            )

        # Combo: director + decade (pre-validated)
        if self.director_decade_combos():
            objectives.append(
                GameObjectiveTemplate(
                    label="Watch a DIRECTOR_DECADE",
                    data={"DIRECTOR_DECADE": (self.director_decade_combos, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                )
            )

        # Title type filter (IMDb exports include TV series, shorts, etc.)
        types = self.title_types()
        if len(types) > 1:
            objectives.append(
                GameObjectiveTemplate(
                    label="Watch a TYPE from your collection",
                    data={"TYPE": (self.title_types, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                )
            )

        return objectives


# === Archipelago Option Classes ===
class FilmCollectionSource(TextChoice):
    """
    Which source(s) to read film data from.

    Place CSV files in the appropriate subfolder:
        film_collection/letterboxd/  <- Letterboxd exports
        film_collection/imdb/        <- IMDb exports

    Multiple CSVs per folder are supported and will be merged.
    """

    display_name = "Film Collection Source"
    option_letterboxd = 0
    option_imdb = 1
    option_both = 2
    default = 2


class FilmCollectionExcludedGenres(OptionSet):
    """
    Genres to exclude from challenge generation. Films where ALL genres
    are excluded will be filtered out.

    Common genres: Action, Comedy, Drama, Horror, Sci-Fi, Thriller,
    Romance, Documentary, Animation, Fantasy
    """

    display_name = "Film Collection Excluded Genres"
    default = []


class FilmCollectionExcludedDirectors(OptionSet):
    """
    Directors to exclude from challenge generation. Films where ALL directors
    are excluded will be filtered out.
    """

    display_name = "Film Collection Excluded Directors"
    default = []


class FilmCollectionIncludeRuntimeChallenges(Toggle):
    """
    Include challenges based on film runtime (short/standard/long/epic).
    Only works with IMDb exports which include runtime data.
    """

    display_name = "Film Collection Include Runtime Challenges"


class FilmCollectionIncludeRatingChallenges(Toggle):
    """
    Include challenges based on film ratings (highly-rated/well-rated/divisive).
    Requires rating data in your CSV export.
    """

    display_name = "Film Collection Include Rating Challenges"


class FilmCollectionFolder(FreeText):
    """
    Player folder name for locating film collection CSVs.
    Leave empty to use the default film_collection/ subfolder alongside this game file.

    For multiplayer setups, set this to the player's folder name (e.g., "eiron").
    The game will then look in: <game_folder>/eiron/film_collection/letterboxd/ and imdb/

    You can also provide an absolute path to a folder containing letterboxd/ and/or imdb/ subfolders.
    """

    display_name = "Film Collection Folder"
    default = ""
