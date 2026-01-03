
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
from Options import NamedRange, FreeText, OptionSet, Toggle, Range  # type: ignore
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
    playnite_library_use_play_next: "PlayniteLibraryUsePlayNext"
    playnite_library_play_next_count: "PlayniteLibraryPlayNextCount"


class PlayniteLibraryGame(Game):
    # -------- Computation and caching --------
    def _ensure_computed(self) -> None:
        """Build and cache all derived lists/sets in one pass for this instance/options."""
        if getattr(self, "_computed_ready", False):
            return
        self._compute_all()

    def _compute_all(self) -> None:
        """Compute filtered games and all attribute sets in a single traversal."""
        # Defaults in case options are not yet available (during options JSON build)
        arch_opts = getattr(self, "archipelago_options", None)
        min_time_played = 0
        max_time_played = -1
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

        excluded_games_set = self.excluded_games()

        # Initialize caches
        self._filtered_games_display: List[str] = []
        self._filtered_games_items: List[Dict[str, Any]] = []
        self._cats: Set[str] = set()
        self._series: Set[str] = set()
        self._tags: Set[str] = set()
        self._genres: Set[str] = set()
        self._platforms: Set[str] = set()
        self._features: Set[str] = set()
        self._sources: Set[str] = set()
        self._years: Set[int] = set()
        self._tag_to_games: Dict[str, List[str]] = {}

        for game in self._get_library_games():
            # Playtime filter
            if game.get("playtime_minutes", 0) < min_time_played:
                continue
            if max_time_played != -1 and game.get("playtime_minutes", 0) > max_time_played:
                continue

            # Exclusion filter by name/id
            if game["name"] in excluded_games_set or str(game.get("id", "")) in excluded_games_set:
                continue

            # Completion status filter
            completion_status = game.get("completion_status")
            if completion_status and excluded_statuses and completion_status in excluded_statuses:
                continue

            # Release year filter
            try:
                release_year = int(game.get("release_year", 0) or 0)
            except (ValueError, TypeError):
                release_year = 0
            if release_year:
                if release_year < min_release_year or release_year > max_release_year:
                    continue

            # Score filters
            if game.get("user_score", 0) < min_user_score:
                continue
            if game.get("critic_score", 0) < min_critic_score:
                continue
            if game.get("community_score", 0) < min_community_score:
                continue

            # Passed all filters -> include
            display_name = game["name"]
            src = game.get("source")
            if src:
                display_name = f"{display_name} [Source: {src}]"

            self._filtered_games_display.append(display_name)
            self._filtered_games_items.append(game)

            # Attribute sets from filtered items
            # Categories
            for cat in game.get("Categories") or []:
                if isinstance(cat, dict) and "Name" in cat:
                    self._cats.add(cat["Name"])
                elif isinstance(cat, str):
                    self._cats.add(cat)
            # Series
            ser = game.get("Series")
            if isinstance(ser, list):
                for s in ser:
                    if isinstance(s, dict) and "Name" in s:
                        self._series.add(s["Name"])
                    elif isinstance(s, str) and s:
                        self._series.add(s)
            elif isinstance(ser, dict) and "Name" in ser:
                self._series.add(ser["Name"])
            elif isinstance(ser, str) and ser:
                self._series.add(ser)
            # Tags
            names_for_this_game: Set[str] = set()
            for t in game.get("Tags") or []:
                if isinstance(t, dict) and "Name" in t:
                    names_for_this_game.add(t["Name"])
                elif isinstance(t, str):
                    names_for_this_game.add(t)
            self._tags.update(names_for_this_game)
            # Genres
            for gname in game.get("Genres") or []:
                if isinstance(gname, dict) and "Name" in gname:
                    self._genres.add(gname["Name"])
                elif isinstance(gname, str):
                    self._genres.add(gname)
            # Platforms
            for plat in game.get("Platforms") or []:
                if isinstance(plat, dict) and "Name" in plat:
                    self._platforms.add(plat["Name"])
                elif isinstance(plat, str):
                    self._platforms.add(plat)
            # Features
            for feat in game.get("Features") or []:
                if isinstance(feat, dict) and "Name" in feat:
                    self._features.add(feat["Name"])
                elif isinstance(feat, str):
                    self._features.add(feat)
            # Source
            if src:
                self._sources.add(src)
            # Years
            if release_year:
                self._years.add(release_year)

        self._computed_ready = True
    def _get_library_games(self) -> List[Dict[str, Any]]:
        """Get the library games, using lru_cache on PlayniteLibraryHolder.games()."""
        json_path = self._get_json_path()
        if not json_path:
            return []
        return playnite_library.games(json_path)

    # === Attribute extraction helpers ===
    @property
    def categories(self) -> List[str]:
        self._ensure_computed()
        return sorted(self._cats)

    @property
    def series(self) -> List[str]:
        self._ensure_computed()
        return sorted(self._series)

    @property
    def tags(self) -> List[str]:
        self._ensure_computed()
        return sorted(self._tags)

    @property
    def genres(self) -> List[str]:
        self._ensure_computed()
        return sorted(self._genres)

    @property
    def sources(self) -> List[str]:
        self._ensure_computed()
        return sorted(self._sources)

    @property
    def platforms(self) -> List[str]:
        self._ensure_computed()
        return sorted(self._platforms)

    @property
    def features(self) -> List[str]:
        self._ensure_computed()
        return sorted(self._features)

    def play_next_nth_choices(self) -> List[str]:
        """Generate NTH ordinal choices for Play Next suggestions.
        
        Play Next is a Playnite plugin with its own internal display - we cannot access
        its data from JSON exports. This simply generates ordinal numbers (1st, 2nd, 3rd...)
        up to the configured play_next_count. The user manually looks at their Play Next
        list in Playnite and plays the Nth game from that list.
        
        Returns ordinals from 1 up to play_next_count.
        If Play Next is disabled, returns an empty list.
        """
        arch_opts = getattr(self, "archipelago_options", None)
        use_play_next = False
        play_next_count = 10
        
        if arch_opts is not None:
            try:
                # Toggle options are boolean
                use_play_next = bool(getattr(arch_opts.playnite_library_use_play_next, "value", False))
            except Exception:
                use_play_next = False
            try:
                # Range is 1-100, no "no limit" option
                play_next_count = int(getattr(arch_opts.playnite_library_play_next_count, "value", 10))
            except Exception:
                play_next_count = 10
        
        if not use_play_next:
            return []
        
        # Simply generate ordinals up to the configured count
        # User will manually check their Play Next list in Playnite
        return [self._ordinal(n) for n in range(1, play_next_count + 1)]

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

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        """Runs before generating this game's objectives when the game is selected.

        Use this hook to compute caches lazily so we don't touch the library
        unless Playnite is actually the chosen game.
        """
        # Keep this a no-op to preserve strict laziness across engines that might
        # probe all games. Actual data is resolved via callables at selection time.
        return []

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        """Generate all unique Playnite library challenge objectives.

        If the Playnite JSON is missing or unreadable, return a fallback objective
        that can be completed manually.
        """
        objectives: List[GameObjectiveTemplate] = []

        # Lazy-load safeguard: only proceed if a path (file or folder) exists on disk.
        # We DO NOT parse the JSON here; we only test for existence to avoid expensive IO.
        json_path = self._get_json_path()
        if not json_path:
            # No path configured - provide generic fallback
            objectives.append(
                GameObjectiveTemplate(
                    label="Play a random game from your Playnite library",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )
            return objectives
            
        json_path_obj = Path(json_path).expanduser()
        # If it's a directory, ensure games.json exists inside; if it's a file, ensure file exists.
        if json_path_obj.is_dir():
            if not (json_path_obj / "games.json").exists():
                # Path configured but file missing - provide generic fallback
                objectives.append(
                    GameObjectiveTemplate(
                        label="Play a random game from your Playnite library",
                        data={},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )
                return objectives
        else:
            if not json_path_obj.exists():
                # Path configured but file missing - provide generic fallback
                objectives.append(
                    GameObjectiveTemplate(
                        label="Play a random game from your Playnite library",
                        data={},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )
                return objectives

        # Check if library actually loads and has games
        # If it fails to load or is empty, provide generic fallback
        if not self.games():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play a random game from your Playnite library",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )
            return objectives

        # 1) Plain game pick from filtered Playnite library (deferred)
        objectives.append(
            GameObjectiveTemplate(
                label="Play GAME from your Playnite library",
                data={"GAME": (lambda: list(self.games()), 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            )
        )

        # 2) Play Next plugin – ordinal choice only (manual lookup in Playnite UI)
        #    - We cannot query the plugin list from JSON; users select an NTH (e.g., 1st/2nd/3rd)
        #      and then look at their Play Next panel in Playnite.
        #    - Only emitted when the Play Next feature is enabled and has at least one ordinal.
        # 2) Play Next – we must evaluate choices to know if feature enabled; this is inexpensive
        if self.play_next_nth_choices():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play the NTH game from your Playnite Play Next suggestions",
                    data={"NTH": (lambda: list(self.play_next_nth_choices()), 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                )
            )

        # 3) Series filter – choose any game in a selected series
        # 3) Series filter – defer actual series list until objective resolution
        objectives.append(
            GameObjectiveTemplate(
                label="Play a Playnite library game from the SERIES series",
                data={"SERIES": (lambda: list(self.series()), 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            )
        )

        # 4) Release year constraints – pick a specific year, and optionally a random pick within that year
        # 4) Release year constraints – defer evaluation
        objectives.append(
            GameObjectiveTemplate(
                label="Play a Playnite library game released in YEAR",
                data={"YEAR": (lambda: list(self.release_year_choices()), 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            )
        )
        objectives.append(
            GameObjectiveTemplate(
                label="Play a random Playnite library game released in YEAR",
                data={"YEAR": (lambda: list(self.release_year_choices()), 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            )
        )

        # Supported attribute filters and ordering options used below
        attribute_types = [
            ("TAG", lambda: list(self.tags)),
            ("GENRE", lambda: list(self.genres)),
            ("FEATURE", lambda: list(self.features)),
            ("PLATFORM", lambda: list(self.platforms)),
            ("CATEGORY", lambda: list(self.categories)),
            ("SOURCE", lambda: list(self.sources)),
        ]
        ordering_options = [
            "most recently added",
            "least recently added",
            "newest",
            "oldest",
            "highest-rated (UserScore)",
            "highest-rated (CriticScore)",
            "highest-rated (CommunityScore)",
            "alphabetical by name",
        ]

        # 5) Attribute-based filters – TAG/GENRE/FEATURE/PLATFORM/CATEGORY/SOURCE
        #    - Only include if attribute list is non-empty
        for attr_label, attr_func in attribute_types:
            # Only create templates for attributes that have values
            if not attr_func():
                continue
            attr_weight = 1
            objectives.append(
                GameObjectiveTemplate(
                    label=f"Play a Playnite library game with the {attr_label} {attr_label.lower()}",
                    data={attr_label: (lambda f=attr_func: list(f()), 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=attr_weight,
                )
            )
            objectives.append(
                GameObjectiveTemplate(
                    label=f"Play a random Playnite library game with the {attr_label} {attr_label.lower()}",
                    data={attr_label: (lambda f=attr_func: list(f()), 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=attr_weight,
                )
            )
        # 6) Ordering + NTH objectives – universal ordinal tokens applied to various subsets
        #    - Only add if there are games available
        for order_label in ordering_options:
            objectives.append(
                GameObjectiveTemplate(
                    label=f"Play your NTH {order_label} Playnite library game",
                    data={"NTH": (lambda: list(self.nth_choices()), 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )
            objectives.append(
                GameObjectiveTemplate(
                    label=f"Play your NTH {order_label} Playnite library game released in YEAR",
                    data={
                        "YEAR": (lambda: list(self.release_year_choices()), 1),
                        "NTH": (lambda: list(self.nth_choices()), 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )
            for attr_label, attr_func in attribute_types:
                # Only create templates for attributes that have values
                if not attr_func():
                    continue
                objectives.append(
                    GameObjectiveTemplate(
                        label=f"Play your NTH {order_label} Playnite library game with the {attr_label} {attr_label.lower()}",
                        data={
                            attr_label: (lambda f=attr_func: list(f()), 1),
                            "NTH": (lambda: list(self.nth_choices()), 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

        seen_labels = set()
        unique_objectives = []
        for obj in objectives:
            if obj.label not in seen_labels:
                unique_objectives.append(obj)
                seen_labels.add(obj.label)
        
        # Safety check: ensure at least one objective exists for players with default options
        if not unique_objectives:
            unique_objectives.append(
                GameObjectiveTemplate(
                    label="Play a random game from your Playnite library",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )
        
        return unique_objectives

    def nth_choices(self) -> List[str]:
        """Offer a universal NTH set (1st–10th) without subset counting.

        These are independent tokens used to construct the objective; the player applies
        the NTH to the chosen ordering and subset when executing the objective.
        """
        return [self._ordinal(n) for n in range(1, 11)]

    # Note: We intentionally do not compute per-subset caps for NTH to avoid costly counting
    # and to keep objectives broad and fast to generate.

    def _ordinal(self, n: int) -> str:
        # Grammar-correct ordinal: 1st, 2nd, 3rd, 4th, ... including 11th/12th/13th exceptions
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

    def release_year_choices(self) -> List[int]:
        self._ensure_computed()
        return sorted(self._years)

    def games(self) -> List[str]:
        # If no JSON path is available, return empty to avoid errors during option generation
        if not self._get_json_path():
            return []
        self._ensure_computed()
        return list(self._filtered_games_display)

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


class PlayniteLibraryUsePlayNext(Toggle):
    """
    Enable using Play Next plugin suggestions from your Playnite library.
    
    The Play Next plugin provides curated game suggestions based on your play history and preferences.
    When enabled, objectives can be generated from these suggestions.
    """

    display_name = "Playnite Library Use Play Next"


class PlayniteLibraryPlayNextCount(Range):
    """
    Number of Play Next suggestions to include when generating objectives.
    
    Only used if Play Next is enabled. Limits the pool of suggested games.
    The Play Next plugin provides its own curated list that cannot be accessed like tags,
    so this setting controls how many games from that list to consider.
    """

    display_name = "Playnite Library Play Next Count"
    default = 10
    range_start = 1
    range_end = 100


class PlayniteLibraryHolder:
    def __init__(self):
        self._printed_elements = False
        self._printed_filter_result = False
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
            # Print filter summary after statistics, only once per session
            from os import environ
            min_time_played = int(environ.get("PLAYNITE_LIBRARY_MIN_TIME_PLAYED", 0))
            max_time_played = int(environ.get("PLAYNITE_LIBRARY_MAX_TIME_PLAYED", -1))
            min_release_year = int(environ.get("PLAYNITE_LIBRARY_MIN_RELEASE_YEAR", 0))
            max_release_year = int(environ.get("PLAYNITE_LIBRARY_MAX_RELEASE_YEAR", 9999))
            min_user_score = int(environ.get("PLAYNITE_LIBRARY_MIN_USER_SCORE", 0))
            min_critic_score = int(environ.get("PLAYNITE_LIBRARY_MIN_CRITIC_SCORE", 0))
            min_community_score = int(environ.get("PLAYNITE_LIBRARY_MIN_COMMUNITY_SCORE", 0))
            excluded_statuses = environ.get("PLAYNITE_LIBRARY_EXCLUDED_COMPLETION_STATUSES", "")
            excluded_games = environ.get("PLAYNITE_LIBRARY_EXCLUDED_GAMES", "")
            print(
                "Filtering Playnite library with "
                f"min_time={min_time_played}, max_time={max_time_played}, "
                f"min_year={min_release_year}, max_year={max_release_year}, "
                f"min_user={min_user_score}, min_critic={min_critic_score}, min_community={min_community_score}, "
                f"excluded_statuses={excluded_statuses}, excluded_games={excluded_games}"
            )
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
        years: Set[int] = set()

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

            # Sources (normalized key)
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

            # Years (normalized key)
            year = g.get("release_year", 0)
            try:
                year_int = int(year)
                if year_int:
                    years.add(year_int)
            except (ValueError, TypeError):
                pass

        print("\n=== Playnite Library Statistics (Before Filtering) ===")
        print(f"Tags: {len(tags)}")
        print(f"Genres: {len(genres)}")
        print(f"Features: {len(features)}")
        print(f"Platforms: {len(platforms)}")
        print(f"Categories: {len(categories)}")
        print(f"Sources: {len(sources)}")
        print(f"Series: {len(series)}")
        print(f"Years: {len(years)}")
        print(f"Total Games: {len(normalized)}")
        print("=" * 55 + "\n")

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
            # Be permissive with encodings and formats (Playnite's games.json can be NDJSON)
            load_error: Exception | None = None
            data = None
            # 1) Try strict UTF-8 JSON
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e1:
                load_error = e1
                # 2) Try UTF-8 with BOM
                try:
                    with path.open("r", encoding="utf-8-sig") as f:
                        data = json.load(f)
                        load_error = None
                except Exception as e2:
                    load_error = e2
            # 3) If still failing, try a tolerant text read and handle NDJSON
            if data is None:
                try:
                    raw_text = path.read_text(encoding="utf-8", errors="replace")
                    raw = raw_text.strip()
                    # If it's a normal JSON container, try loading again
                    if raw.startswith("{") or raw.startswith("["):
                        try:
                            data = json.loads(raw)
                            load_error = None
                        except Exception as e3:
                            load_error = e3
                    # If not a normal container, treat as NDJSON (one JSON object per line)
                    if data is None:
                        lines = [ln.strip() for ln in raw_text.splitlines() if ln.strip()]
                        ndjson_items = []
                        ndjson_failed = False
                        for ln in lines:
                            try:
                                ndjson_items.append(json.loads(ln))
                            except Exception:
                                ndjson_failed = True
                                break
                        if not ndjson_failed and ndjson_items:
                            data = ndjson_items
                            load_error = None
                except Exception as e4:
                    load_error = e4

            if data is None:
                error_msg = str(load_error) if load_error else "Unknown error - file may be empty or severely malformed"
                raise RuntimeError(f"Failed to read Playnite library JSON: {error_msg}")

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