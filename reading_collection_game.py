"""
Reading Collection game for Keymaster's Keep.

Parses Goodreads and/or StoryGraph CSV exports and generates reading challenges
based on the books, authors, genres/shelves, publication years, and page counts
in the player's collection.

CSV files should be placed in the reading_collection/ subfolder alongside this file:
    reading_collection/
        goodreads/    <- Drop Goodreads CSV exports here
        storygraph/   <- Drop StoryGraph CSV exports here

Multiple CSVs per source are supported; all files in each subfolder are merged.
Supports filtering by shelf (e.g., only "to-read" books) so players can focus
on their backlog.
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
class ReadingCollectionArchipelagoOptions:
    reading_collection_folder: "ReadingCollectionFolder"
    reading_collection_source: "ReadingCollectionSource"
    reading_collection_included_goodreads_shelves: "ReadingCollectionIncludedGoodreadsShelves"
    reading_collection_included_storygraph_statuses: "ReadingCollectionIncludedStorygraphStatuses"
    reading_collection_excluded_authors: "ReadingCollectionExcludedAuthors"
    reading_collection_include_shelf_challenges: "ReadingCollectionIncludeShelfChallenges"
    reading_collection_include_length_challenges: "ReadingCollectionIncludeLengthChallenges"


# === Module-level CSV holder with caching ===
_READING_COLLECTION_DIR = Path(__file__).parent / "reading_collection"


class _ReadingCollectionHolder:
    """Caches parsed CSV data keyed by source name."""

    def __init__(self):
        self._notice_printed = False

    @functools.lru_cache(maxsize=4)
    def parse_source(self, source: str, base_dir: str = "") -> List[Dict[str, Any]]:
        """Parse all CSVs for the given source(s).

        source: "goodreads", "storygraph", or "both"
        base_dir: custom folder path (empty = use default)

        Returns a list of book dicts with normalized keys:
        title, author, shelves (list), genres (list), year, pages, rating, source
        """
        books: List[Dict[str, Any]] = []
        collection_dir = Path(base_dir) if base_dir else _READING_COLLECTION_DIR

        sources_to_load: List[str] = []
        if source == "both":
            sources_to_load = ["goodreads", "storygraph"]
        else:
            sources_to_load = [source]

        for src in sources_to_load:
            src_dir = collection_dir / src
            if not src_dir.is_dir():
                if not self._notice_printed:
                    print(f"[Reading Collection] Source folder not found: {src_dir}")
                    self._notice_printed = True
                continue

            csv_files = sorted(src_dir.glob("*.csv"))
            if not csv_files:
                if not self._notice_printed:
                    print(f"[Reading Collection] No CSV files found in: {src_dir}")
                    self._notice_printed = True
                continue

            for csv_file in csv_files:
                books.extend(self._parse_csv_file(csv_file, src))

        # Deduplicate by title+author, preferring entries with more data
        if len(sources_to_load) > 1:
            seen: Dict[tuple, int] = {}
            for i, book in enumerate(books):
                key = (book["title"].lower(), book["author"].lower())
                if key in seen:
                    existing = books[seen[key]]
                    # Keep the entry with more data (year/pages)
                    existing_score = (1 if existing.get("year", 0) else 0) + (1 if existing.get("pages", 0) else 0)
                    new_score = (1 if book.get("year", 0) else 0) + (1 if book.get("pages", 0) else 0)
                    if new_score > existing_score:
                        # Merge shelves from existing into new entry
                        for s in existing.get("shelves", []):
                            if s not in book.get("shelves", []):
                                book["shelves"].append(s)
                        books[seen[key]] = book
                    else:
                        # Merge shelves from new into existing
                        for s in book.get("shelves", []):
                            if s not in existing.get("shelves", []):
                                existing["shelves"].append(s)
                else:
                    seen[key] = i

            books = [books[i] for i in sorted(seen.values())]

        return books

    def _parse_csv_file(self, path: Path, csv_format: str) -> List[Dict[str, Any]]:
        """Parse a single CSV file in the given format."""
        try:
            with open(path, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    return []

                normalized_fields = {h.strip().lower(): h for h in reader.fieldnames}

                if csv_format == "storygraph":
                    return self._parse_storygraph(reader, normalized_fields)
                else:
                    return self._parse_goodreads(reader, normalized_fields)

        except Exception as e:
            if not self._notice_printed:
                print(f"[Reading Collection] Error reading CSV '{path.name}': {e}")
                self._notice_printed = True
            return []

    def _parse_goodreads(self, reader: csv.DictReader, field_map: Dict[str, str]) -> List[Dict[str, Any]]:
        """Parse Goodreads CSV format."""
        books: List[Dict[str, Any]] = []

        # Goodreads column mappings (case-insensitive lookup)
        title_key = field_map.get("title", "")
        author_key = field_map.get("author", "")
        shelves_key = field_map.get("bookshelves", "")
        exclusive_shelf_key = field_map.get("exclusive shelf", "")
        orig_year_key = field_map.get("original publication year", "")
        pub_year_key = field_map.get("year published", "")
        pages_key = field_map.get("number of pages", "") or field_map.get("pages", "")
        rating_key = field_map.get("my rating", "")
        avg_rating_key = field_map.get("average rating", "")

        for row in reader:
            title = (row.get(title_key, "") or "").strip()
            if not title:
                continue

            author = (row.get(author_key, "") or "").strip()

            # Build shelves list from both exclusive shelf and bookshelves
            shelves: List[str] = []
            exclusive = (row.get(exclusive_shelf_key, "") or "").strip()
            if exclusive:
                shelves.append(exclusive)
            bookshelves_raw = (row.get(shelves_key, "") or "").strip()
            if bookshelves_raw:
                for s in bookshelves_raw.split(","):
                    s = s.strip()
                    if s and s not in shelves:
                        shelves.append(s)

            # Year (prefer original publication year, fall back to year published)
            year = 0
            year_raw = (row.get(orig_year_key, "") or "").strip()
            if not year_raw:
                year_raw = (row.get(pub_year_key, "") or "").strip()
            try:
                year = int(year_raw) if year_raw else 0
            except ValueError:
                year = 0

            # Pages
            pages = 0
            pages_raw = (row.get(pages_key, "") or "").strip()
            try:
                pages = int(pages_raw) if pages_raw else 0
            except ValueError:
                pages = 0

            # Rating
            rating = 0.0
            rating_raw = (row.get(rating_key, "") or row.get(avg_rating_key, "") or "").strip()
            try:
                rating = float(rating_raw) if rating_raw else 0.0
            except ValueError:
                rating = 0.0

            books.append({
                "title": title,
                "author": author,
                "shelves": shelves,
                "genres": [],  # Goodreads doesn't export genre data
                "year": year,
                "pages": pages,
                "rating": rating,
            })

        return books

    def _parse_storygraph(self, reader: csv.DictReader, field_map: Dict[str, str]) -> List[Dict[str, Any]]:
        """Parse StoryGraph CSV format."""
        books: List[Dict[str, Any]] = []

        # StoryGraph column mappings
        title_key = field_map.get("title", "")
        author_key = field_map.get("author(s)", "") or field_map.get("authors", "") or field_map.get("author", "")
        status_key = field_map.get("status", "") or field_map.get("read status", "")
        year_key = field_map.get("publication year", "") or field_map.get("year published", "")
        pages_key = field_map.get("page count", "") or field_map.get("pages", "") or field_map.get("number of pages", "")
        rating_key = field_map.get("user rating", "") or field_map.get("star rating", "") or field_map.get("my rating", "")
        genres_key = field_map.get("genres", "") or field_map.get("tags", "")
        moods_key = field_map.get("storygraph moods", "") or field_map.get("moods", "")

        for row in reader:
            title = (row.get(title_key, "") or "").strip()
            if not title:
                continue

            author = (row.get(author_key, "") or "").strip()

            # StoryGraph uses "status" as the shelf equivalent
            shelves: List[str] = []
            status = (row.get(status_key, "") or "").strip()
            if status:
                shelves.append(status)

            # Genres stored separately (not mixed into shelves)
            genres: List[str] = []
            genres_raw = (row.get(genres_key, "") or "").strip()
            if genres_raw:
                for g in genres_raw.split(","):
                    g = g.strip()
                    if g:
                        genres.append(g)

            # Year
            year = 0
            year_raw = (row.get(year_key, "") or "").strip()
            try:
                year = int(year_raw) if year_raw else 0
            except ValueError:
                year = 0

            # Pages
            pages = 0
            pages_raw = (row.get(pages_key, "") or "").strip()
            try:
                pages = int(pages_raw) if pages_raw else 0
            except ValueError:
                pages = 0

            # Rating
            rating = 0.0
            rating_raw = (row.get(rating_key, "") or "").strip()
            try:
                rating = float(rating_raw) if rating_raw else 0.0
            except ValueError:
                rating = 0.0

            books.append({
                "title": title,
                "author": author,
                "shelves": shelves,
                "genres": genres,
                "year": year,
                "pages": pages,
                "rating": rating,
            })

        return books


_reading_holder = _ReadingCollectionHolder()


# === Main Game Class ===
class ReadingCollectionGame(Game):
    name = "Reading Collection"
    platform = KeymastersKeepGamePlatforms.META
    is_adult_only_or_unrated = False
    options_cls = ReadingCollectionArchipelagoOptions

    def _get_collection_dir(self) -> str:
        """Get collection folder path, accounting for player subfolder.

        If a player folder is set (e.g., "eiron"), resolves to:
            <game_file_parent>/eiron/reading_collection/
        If an absolute path is given, uses it directly.
        If empty, uses the default reading_collection/ alongside this file.
        """
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return ""
        try:
            val = (opts.reading_collection_folder.value or "").strip()
            if not val:
                return ""
            p = Path(val)
            if p.is_absolute():
                return val
            # Treat as a player subfolder name relative to game file parent
            return str(Path(__file__).parent / val / "reading_collection")
        except Exception:
            return ""

    def _get_source(self) -> str:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return "both"
        try:
            val = opts.reading_collection_source.value
            if val == 1:
                return "storygraph"
            elif val == 2:
                return "both"
            return "goodreads"
        except Exception:
            return "both"

    def _get_included_shelves(self) -> Set[str]:
        """Get combined included shelves/statuses from both source-specific options."""
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return set()
        shelves: Set[str] = set()
        try:
            goodreads_shelves = opts.reading_collection_included_goodreads_shelves.value
            if goodreads_shelves:
                shelves.update(goodreads_shelves)
        except Exception:
            pass
        try:
            storygraph_statuses = opts.reading_collection_included_storygraph_statuses.value
            if storygraph_statuses:
                shelves.update(storygraph_statuses)
        except Exception:
            pass
        return shelves

    def _get_excluded_authors(self) -> Set[str]:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return set()
        try:
            authors = opts.reading_collection_excluded_authors.value
            return set(authors) if authors else set()
        except Exception:
            return set()

    def _include_length_challenges(self) -> bool:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return True
        try:
            return bool(getattr(opts.reading_collection_include_length_challenges, "value", True))
        except Exception:
            return True

    def _include_shelf_challenges(self) -> bool:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return True
        try:
            return bool(getattr(opts.reading_collection_include_shelf_challenges, "value", True))
        except Exception:
            return True

    def _get_raw_books(self) -> List[Dict[str, Any]]:
        source = self._get_source()
        return _reading_holder.parse_source(source, self._get_collection_dir())

    def _filtered_books(self) -> List[Dict[str, Any]]:
        """Apply shelf inclusion and author exclusion filters."""
        raw = self._get_raw_books()
        included_shelves = self._get_included_shelves()
        excluded_authors = self._get_excluded_authors()

        filtered = []
        for book in raw:
            # Shelf filter: if included_shelves is non-empty, book must be on at least one
            if included_shelves:
                book_shelves_lower = {s.lower() for s in book["shelves"]}
                included_lower = {s.lower() for s in included_shelves}
                if not book_shelves_lower.intersection(included_lower):
                    continue

            # Author exclusion
            if excluded_authors and book["author"] in excluded_authors:
                continue

            filtered.append(book)

        return filtered

    # === Attribute extraction ===
    def books(self) -> List[str]:
        """Returns 'Title by Author' strings."""
        collection = self._filtered_books()
        book_list = []
        for b in collection:
            if b["author"]:
                book_list.append(f"{b['title']} by {b['author']}")
            else:
                book_list.append(b["title"])
        return sorted(set(book_list))

    def authors(self) -> List[str]:
        """Returns unique author names."""
        collection = self._filtered_books()
        authors: Set[str] = set()
        for b in collection:
            if b["author"]:
                authors.add(b["author"])
        return sorted(authors)

    def shelves(self) -> List[str]:
        """Returns unique shelf/status names from the filtered collection.

        Only returns shelves that are within the included shelves set (if specified),
        so challenges won't ask the player to read from shelves they haven't opted into.
        """
        collection = self._filtered_books()
        included_shelves = self._get_included_shelves()
        included_lower = {s.lower() for s in included_shelves} if included_shelves else set()
        shelf_set: Set[str] = set()
        for b in collection:
            for s in b["shelves"]:
                if s:
                    # If we have an inclusion filter, only return shelves within it
                    if included_lower and s.lower() not in included_lower:
                        continue
                    shelf_set.add(s)
        return sorted(shelf_set)

    def genres(self) -> List[str]:
        """Returns unique genres from StoryGraph exports."""
        collection = self._filtered_books()
        genre_set: Set[str] = set()
        for b in collection:
            for g in b.get("genres", []):
                if g:
                    genre_set.add(g)
        return sorted(genre_set)

    def years(self) -> List[str]:
        """Returns unique publication years as strings."""
        collection = self._filtered_books()
        year_set: Set[str] = set()
        for b in collection:
            if b["year"] and b["year"] > 0:
                year_set.add(str(b["year"]))
        return sorted(year_set)

    def decades(self) -> List[str]:
        """Returns decade strings like '1980s', '2000s'."""
        collection = self._filtered_books()
        decade_set: Set[str] = set()
        for b in collection:
            if b["year"] and b["year"] > 0:
                decade = (b["year"] // 10) * 10
                decade_set.add(f"{decade}s")
        return sorted(decade_set)

    def author_decade_combos(self) -> List[str]:
        """Returns validated 'book by Author from the decade' combo strings."""
        collection = self._filtered_books()
        combos: Set[str] = set()
        for b in collection:
            if not b["author"] or not b["year"] or b["year"] <= 0:
                continue
            decade = f"{(b['year'] // 10) * 10}s"
            combos.add(f"book by {b['author']} from the {decade}")
        return sorted(combos)

    def length_categories(self) -> List[str]:
        """Returns available length categories based on page counts."""
        collection = self._filtered_books()
        categories: Set[str] = set()
        for b in collection:
            pages = b.get("pages", 0)
            if pages > 0:
                if pages < 200:
                    categories.add("short (under 200 pages)")
                elif pages <= 400:
                    categories.add("medium-length (200-400 pages)")
                else:
                    categories.add("long (over 400 pages)")
        return sorted(categories)

    # === Objective generation ===
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return []

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = []
        objectives.append(
            GameObjectiveTemplate(
                label='Read one chapter from your reading collection',
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
        )

        # If no books found, provide a fallback
        if not self._filtered_books():
            objectives.append(
                GameObjectiveTemplate(
                    label="Read a book from your reading collection",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                )
            )
            return objectives

        # Primary: Read a specific book
        if self.books():
            objectives.append(
                GameObjectiveTemplate(
                    label="Read BOOK",
                    data={"BOOK": (self.books, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                )
            )

        # Author-based challenge
        if self.authors():
            objectives.append(
                GameObjectiveTemplate(
                    label="Read a book by AUTHOR",
                    data={"AUTHOR": (self.authors, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                )
            )

        # Shelf-based challenge
        if self._include_shelf_challenges() and self.shelves():
            objectives.append(
                GameObjectiveTemplate(
                    label="Read a book from your SHELF shelf",
                    data={"SHELF": (self.shelves, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Genre-based challenge (StoryGraph exports include genre data)
        if self.genres():
            objectives.append(
                GameObjectiveTemplate(
                    label="Read a GENRE book from your collection",
                    data={"GENRE": (self.genres, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Decade-based challenge
        if self.decades():
            objectives.append(
                GameObjectiveTemplate(
                    label="Read a book published in the DECADE",
                    data={"DECADE": (self.decades, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Year-based challenge
        if self.years():
            objectives.append(
                GameObjectiveTemplate(
                    label="Read a book published in YEAR",
                    data={"YEAR": (self.years, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                )
            )

        # Length-based challenge
        if self._include_length_challenges() and self.length_categories():
            objectives.append(
                GameObjectiveTemplate(
                    label="Read a LENGTH book from your collection",
                    data={"LENGTH": (self.length_categories, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Combo: author + decade (pre-validated)
        if self.author_decade_combos():
            objectives.append(
                GameObjectiveTemplate(
                    label="Read a AUTHOR_DECADE",
                    data={"AUTHOR_DECADE": (self.author_decade_combos, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                )
            )

        return objectives


# === Archipelago Option Classes ===
class ReadingCollectionSource(TextChoice):
    """
    Which reading collection source(s) to use.

    Place CSV exports in the reading_collection/ subfolder:
        reading_collection/goodreads/   <- Goodreads exports
        reading_collection/storygraph/  <- StoryGraph exports

    For Goodreads: Export from https://www.goodreads.com/review/import
    For StoryGraph: Export from your StoryGraph library settings.
    """

    display_name = "Reading Collection Source"
    option_goodreads = 0
    option_storygraph = 1
    option_both = 2
    default = 2


class ReadingCollectionIncludedGoodreadsShelves(OptionSet):
    """
    Only include books on these Goodreads shelves in challenge generation.
    Leave empty to include ALL books from Goodreads regardless of shelf.

    Common Goodreads shelves: to-read, currently-reading, read
    """

    display_name = "Reading Collection Included Goodreads Shelves"
    default = ["to-read"]


class ReadingCollectionIncludedStorygraphStatuses(OptionSet):
    """
    Only include books with these StoryGraph statuses in challenge generation.
    Leave empty to include ALL books from StoryGraph regardless of status.

    Common StoryGraph statuses: to-read, currently-reading, read, did-not-finish
    """

    display_name = "Reading Collection Included StoryGraph Statuses"
    default = ["to-read"]


class ReadingCollectionExcludedAuthors(OptionSet):
    """
    Authors to exclude from challenge generation.
    Use exact name as it appears in your CSV export.
    """

    display_name = "Reading Collection Excluded Authors"
    default = []


class ReadingCollectionIncludeShelfChallenges(Toggle):
    """
    Include challenges based on shelf/status (e.g., "Read a book from your to-read shelf").
    Disable this if you find shelf-based challenges too vague or redundant.
    """

    display_name = "Reading Collection Include Shelf Challenges"


class ReadingCollectionIncludeLengthChallenges(Toggle):
    """
    Include challenges based on book length (short/medium/long).
    Requires page count data in your CSV export.
    """

    display_name = "Reading Collection Include Length Challenges"


class ReadingCollectionFolder(FreeText):
    """
    Player folder name for locating reading collection CSVs.
    Leave empty to use the default reading_collection/ subfolder alongside this game file.

    For multiplayer setups, set this to the player's folder name (e.g., "eiron").
    The game will then look in: <game_folder>/eiron/reading_collection/goodreads/ and storygraph/

    You can also provide an absolute path to a folder containing goodreads/ and/or storygraph/ subfolders.
    """

    display_name = "Reading Collection Folder"
    default = ""
