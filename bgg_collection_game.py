"""
BoardGameGeek Collection game for Keymaster's Keep.

Parses BGG CSV exports and generates board gaming challenges based on games,
player counts, play times, complexity weights, decades, and ratings in the
player's collection.

CSV files should be placed in the bgg_collection/ subfolder alongside this file:
    bgg_collection/
        *.csv   <- Drop BGG CSV exports here

Export your collection from BGG:
    https://boardgamegeek.com/geekcollection.php?action=exportcsv&subtype=boardgame&username=YOURUSERNAME

Multiple CSV files are supported; all files in the folder are merged.
"""

from __future__ import annotations

import csv
import functools
from pathlib import Path
from typing import Dict, List, Set, Any

from dataclasses import dataclass

from Options import FreeText, OptionSet, Toggle  # type: ignore
from ..game import Game  # type: ignore
from ..game_objective_template import GameObjectiveTemplate  # type: ignore
from ..enums import KeymastersKeepGamePlatforms  # type: ignore


# === Options Dataclass ===
@dataclass
class BGGCollectionArchipelagoOptions:
    bgg_collection_folder: "BGGCollectionFolder"
    bgg_collection_include_player_count_challenges: "BGGCollectionIncludePlayerCountChallenges"
    bgg_collection_include_playtime_challenges: "BGGCollectionIncludePlaytimeChallenges"
    bgg_collection_include_solo_challenges: "BGGCollectionIncludeSoloChallenges"
    bgg_collection_include_weight_challenges: "BGGCollectionIncludeWeightChallenges"
    bgg_collection_excluded_games: "BGGCollectionExcludedGames"


# === Module-level CSV holder with caching ===
_BGG_COLLECTION_DIR = Path(__file__).parent / "bgg_collection"


class _BGGCollectionHolder:
    """Caches parsed BGG CSV data."""

    def __init__(self):
        self._notice_printed = False

    @functools.lru_cache(maxsize=4)
    def parse_collection(self, folder_path: str = "") -> List[Dict[str, Any]]:
        """Parse all CSV files in the given folder (or the default bgg_collection folder).

        Returns a list of game dicts with normalized keys:
        name, id, year, min_players, max_players, playing_time,
        user_rating, avg_rating, weight, num_plays, own
        """
        collection_dir = Path(folder_path) if folder_path else _BGG_COLLECTION_DIR

        if not collection_dir.is_dir():
            if not self._notice_printed:
                print(f"[BGG Collection] Folder not found: {collection_dir}")
                self._notice_printed = True
            return []

        csv_files = sorted(collection_dir.glob("*.csv"))
        if not csv_files:
            if not self._notice_printed:
                print(f"[BGG Collection] No CSV files found in: {collection_dir}")
                self._notice_printed = True
            return []

        games: List[Dict[str, Any]] = []
        seen_ids: Set[int] = set()

        for csv_file in csv_files:
            for game in self._parse_csv_file(csv_file):
                game_id = game.get("id", 0)
                if game_id and game_id not in seen_ids:
                    seen_ids.add(game_id)
                    games.append(game)
                elif not game_id:
                    games.append(game)

        return games

    def _parse_csv_file(self, path: Path) -> List[Dict[str, Any]]:
        """Parse a single BGG CSV export."""
        games: List[Dict[str, Any]] = []

        try:
            with open(path, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    return []

                field_map = {h.strip().lower(): h for h in reader.fieldnames}

                name_key = field_map.get("objectname", "") or field_map.get("name", "")
                id_key = field_map.get("objectid", "") or field_map.get("object id", "")
                year_key = field_map.get("yearpublished", "") or field_map.get("year published", "")
                min_players_key = field_map.get("minplayers", "") or field_map.get("min players", "")
                max_players_key = field_map.get("maxplayers", "") or field_map.get("max players", "")
                playtime_key = field_map.get("playingtime", "") or field_map.get("playing time", "")
                rating_key = field_map.get("rating", "")
                avg_key = field_map.get("average", "") or field_map.get("bgg_rating", "")
                weight_key = field_map.get("avgweight", "") or field_map.get("weight", "")
                numplays_key = field_map.get("numplays", "") or field_map.get("plays", "")
                own_key = field_map.get("own", "")

                for row in reader:
                    name = (row.get(name_key, "") or "").strip()
                    if not name:
                        continue

                    # Only include owned games if the 'own' column exists
                    if own_key:
                        own_val = (row.get(own_key, "") or "").strip()
                        if own_val == "0":
                            continue

                    game_id = 0
                    id_raw = (row.get(id_key, "") or "").strip()
                    try:
                        game_id = int(id_raw) if id_raw else 0
                    except ValueError:
                        game_id = 0

                    year = 0
                    year_raw = (row.get(year_key, "") or "").strip()
                    try:
                        year = int(year_raw) if year_raw else 0
                    except ValueError:
                        year = 0

                    min_players = 0
                    min_raw = (row.get(min_players_key, "") or "").strip()
                    try:
                        min_players = int(min_raw) if min_raw else 0
                    except ValueError:
                        min_players = 0

                    max_players = 0
                    max_raw = (row.get(max_players_key, "") or "").strip()
                    try:
                        max_players = int(max_raw) if max_raw else 0
                    except ValueError:
                        max_players = 0

                    playing_time = 0
                    pt_raw = (row.get(playtime_key, "") or "").strip()
                    try:
                        playing_time = int(pt_raw) if pt_raw else 0
                    except ValueError:
                        playing_time = 0

                    user_rating = 0.0
                    rating_raw = (row.get(rating_key, "") or "").strip()
                    if rating_raw and rating_raw.lower() not in ("n/a", ""):
                        try:
                            user_rating = float(rating_raw)
                        except ValueError:
                            user_rating = 0.0

                    avg_rating = 0.0
                    avg_raw = (row.get(avg_key, "") or "").strip()
                    try:
                        avg_rating = float(avg_raw) if avg_raw else 0.0
                    except ValueError:
                        avg_rating = 0.0

                    weight = 0.0
                    weight_raw = (row.get(weight_key, "") or "").strip()
                    try:
                        weight = float(weight_raw) if weight_raw else 0.0
                    except ValueError:
                        weight = 0.0

                    num_plays = 0
                    plays_raw = (row.get(numplays_key, "") or "").strip()
                    try:
                        num_plays = int(plays_raw) if plays_raw else 0
                    except ValueError:
                        num_plays = 0

                    games.append({
                        "id": game_id,
                        "name": name,
                        "year": year,
                        "min_players": min_players,
                        "max_players": max_players,
                        "playing_time": playing_time,
                        "user_rating": user_rating,
                        "avg_rating": avg_rating,
                        "weight": weight,
                        "num_plays": num_plays,
                    })

        except Exception as e:
            if not self._notice_printed:
                print(f"[BGG Collection] Error reading CSV '{path.name}': {e}")
                self._notice_printed = True

        return games


_bgg_holder = _BGGCollectionHolder()


# === Main Game Class ===
class BGGCollectionGame(Game):
    name = "BGG Collection"
    platform = KeymastersKeepGamePlatforms.META
    is_adult_only_or_unrated = False
    options_cls = BGGCollectionArchipelagoOptions

    def _get_collection_dir(self) -> str:
        """Get collection folder path, accounting for player subfolder.

        If a player folder is set (e.g., "eiron"), resolves to:
            <game_file_parent>/eiron/bgg_collection/
        If an absolute path is given, uses it directly.
        If empty, uses the default bgg_collection/ alongside this file.
        """
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return ""
        try:
            val = (opts.bgg_collection_folder.value or "").strip()
            if not val:
                return ""
            p = Path(val)
            if p.is_absolute():
                return val
            # Treat as a player subfolder name relative to game file parent
            return str(Path(__file__).parent / val / "bgg_collection")
        except Exception:
            return ""

    def _excluded_games(self) -> Set[str]:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return set()
        try:
            return set(opts.bgg_collection_excluded_games.value or [])
        except Exception:
            return set()

    def _include_player_count_challenges(self) -> bool:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return True
        try:
            return bool(getattr(opts.bgg_collection_include_player_count_challenges, "value", True))
        except Exception:
            return True

    def _include_playtime_challenges(self) -> bool:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return True
        try:
            return bool(getattr(opts.bgg_collection_include_playtime_challenges, "value", True))
        except Exception:
            return True

    def _include_solo_challenges(self) -> bool:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return True
        try:
            return bool(getattr(opts.bgg_collection_include_solo_challenges, "value", True))
        except Exception:
            return True

    def _include_weight_challenges(self) -> bool:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            return True
        try:
            return bool(getattr(opts.bgg_collection_include_weight_challenges, "value", True))
        except Exception:
            return True

    def _filtered_games(self) -> List[Dict[str, Any]]:
        """Apply game exclusion filter."""
        collection = _bgg_holder.parse_collection(self._get_collection_dir())
        excluded = self._excluded_games()

        if not excluded:
            return collection

        return [g for g in collection if g["name"] not in excluded]

    # === Attribute extraction ===
    def games(self) -> List[str]:
        """Returns game names."""
        return sorted({g["name"] for g in self._filtered_games() if g["name"]})

    def player_counts(self) -> List[str]:
        """Returns unique player count descriptions."""
        collection = self._filtered_games()
        counts: Set[str] = set()
        for g in collection:
            min_p = g.get("min_players", 0)
            max_p = g.get("max_players", 0)
            if min_p == 1:
                counts.add("solo (1 player)")
            if min_p <= 2 and max_p >= 2:
                counts.add("2 players")
            if min_p <= 3 and max_p >= 3:
                counts.add("3 players")
            if min_p <= 4 and max_p >= 4:
                counts.add("4 players")
            if max_p >= 5:
                counts.add("5+ players")
        return sorted(counts)

    def playtime_categories(self) -> List[str]:
        """Returns playtime category descriptions."""
        collection = self._filtered_games()
        categories: Set[str] = set()
        for g in collection:
            pt = g.get("playing_time", 0)
            if pt > 0:
                if pt <= 30:
                    categories.add("quick (30 min or less)")
                elif pt <= 60:
                    categories.add("medium (30-60 min)")
                elif pt <= 120:
                    categories.add("long (1-2 hours)")
                else:
                    categories.add("epic (2+ hours)")
        return sorted(categories)

    def weight_categories(self) -> List[str]:
        """Returns complexity/weight categories based on BGG weight rating."""
        collection = self._filtered_games()
        categories: Set[str] = set()
        for g in collection:
            w = g.get("weight", 0.0)
            if w > 0:
                if w < 2.0:
                    categories.add("light (weight < 2.0)")
                elif w < 3.0:
                    categories.add("medium (weight 2.0-3.0)")
                elif w < 4.0:
                    categories.add("heavy (weight 3.0-4.0)")
                else:
                    categories.add("very heavy (weight 4.0+)")
        return sorted(categories)

    def solo_games(self) -> List[str]:
        """Returns games that support solo play."""
        collection = self._filtered_games()
        return sorted({g["name"] for g in collection if g.get("min_players", 0) == 1 and g["name"]})

    def decades(self) -> List[str]:
        """Returns decade strings."""
        collection = self._filtered_games()
        decade_set: Set[str] = set()
        for g in collection:
            year = g.get("year", 0)
            if year and year >= 1900:
                decade = (year // 10) * 10
                decade_set.add(f"{decade}s")
        return sorted(decade_set)

    def unplayed_games(self) -> List[str]:
        """Returns games with 0 recorded plays (shame pile!)."""
        collection = self._filtered_games()
        return sorted({g["name"] for g in collection if g.get("num_plays", 0) == 0 and g["name"]})

    def highly_rated_games(self) -> List[str]:
        """Returns games with a BGG average rating of 7.5+."""
        collection = self._filtered_games()
        return sorted({g["name"] for g in collection if g.get("avg_rating", 0) >= 7.5 and g["name"]})

    def player_count_game_combos(self) -> List[str]:
        """Returns validated 'GAME at N players' combo strings."""
        collection = self._filtered_games()
        combos: Set[str] = set()
        for g in collection:
            name = g.get("name", "")
            if not name:
                continue
            min_p = g.get("min_players", 0)
            max_p = g.get("max_players", 0)
            if min_p <= 2 and max_p >= 2:
                combos.add(f"{name} with 2 players")
            if min_p <= 3 and max_p >= 3:
                combos.add(f"{name} with 3 players")
            if min_p <= 4 and max_p >= 4:
                combos.add(f"{name} with 4 players")
            if max_p >= 5:
                combos.add(f"{name} with 5+ players")
        return sorted(combos)

    # === Objective generation ===
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return []

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = []

        # Fallback if no games found
        if not self._filtered_games():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play a board game from your BGG collection",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )
            return objectives

        # Primary: Play a specific game
        if self.games():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play GAME",
                    data={"GAME": (self.games, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                )
            )

        # Player count challenge
        if self._include_player_count_challenges() and self.player_counts():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play a game with PLAYER_COUNT from your collection",
                    data={"PLAYER_COUNT": (self.player_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            )

        # Playtime challenge
        if self._include_playtime_challenges() and self.playtime_categories():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play a PLAYTIME game from your collection",
                    data={"PLAYTIME": (self.playtime_categories, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Weight/complexity challenge
        if self._include_weight_challenges() and self.weight_categories():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play a WEIGHT complexity game from your collection",
                    data={"WEIGHT": (self.weight_categories, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Solo challenge
        if self._include_solo_challenges() and self.solo_games():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play GAME solo",
                    data={"GAME": (self.solo_games, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Decade-based challenge
        if self.decades():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play a game from the DECADE from your collection",
                    data={"DECADE": (self.decades, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )

        # Shame pile: unplayed games
        if self.unplayed_games():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play GAME from your shelf of shame (never played!)",
                    data={"GAME": (self.unplayed_games, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                )
            )

        # Highly rated games
        if self.highly_rated_games():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play GAME (rated 7.5+ on BGG)",
                    data={"GAME": (self.highly_rated_games, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        # Combo: specific game at specific player count (pre-validated)
        if self._include_player_count_challenges() and self.player_count_game_combos():
            objectives.append(
                GameObjectiveTemplate(
                    label="Play GAME_PLAYER_COUNT",
                    data={"GAME_PLAYER_COUNT": (self.player_count_game_combos, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        return objectives


# === Archipelago Option Classes ===
class BGGCollectionIncludePlayerCountChallenges(Toggle):
    """
    Include challenges that specify a player count (e.g., 'Play a game at 3 players').
    """

    display_name = "BGG Collection Include Player Count Challenges"


class BGGCollectionIncludePlaytimeChallenges(Toggle):
    """
    Include challenges based on estimated play time
    (quick/medium/long/epic categories).
    """

    display_name = "BGG Collection Include Playtime Challenges"


class BGGCollectionIncludeSoloChallenges(Toggle):
    """
    Include solo play challenges for games that support 1 player.
    """

    display_name = "BGG Collection Include Solo Challenges"


class BGGCollectionIncludeWeightChallenges(Toggle):
    """
    Include challenges based on BGG complexity weight
    (light/medium/heavy/very heavy categories).
    """

    display_name = "BGG Collection Include Weight Challenges"


class BGGCollectionExcludedGames(OptionSet):
    """
    Games to exclude from challenge generation.
    Use the exact name as it appears in your BGG CSV export.
    """

    display_name = "BGG Collection Excluded Games"
    default = []


class BGGCollectionFolder(FreeText):
    """
    Player folder name for locating BGG CSV exports.
    Leave empty to use the default bgg_collection/ subfolder alongside this game file.

    For multiplayer setups, set this to the player's folder name (e.g., "eiron").
    The game will then look for CSVs in: <game_folder>/eiron/bgg_collection/

    You can also provide an absolute path to a folder containing CSV files directly.
    """

    display_name = "BGG Collection Folder"
    default = ""
