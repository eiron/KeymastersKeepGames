from __future__ import annotations

import functools
import random
from os import environ
import requests
from typing import List, Set, Dict

from dataclasses import dataclass

from Options import NamedRange, OptionSet, FreeText, Range, DefaultOnToggle, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms

@dataclass
class SteamAchievementsArchipelagoOptions:
    steam_achievements_min_time_played: SteamAchievementsMinTimePlayed
    steam_achievements_max_time_played: SteamAchievementsMaxTimePlayed
    steam_achievements_steam_id: SteamAchievementsSteamID
    steam_achievements_excluded_games: SteamAchievementsExcludedGames
    steam_achievements_percentage_min: SteamAchievementsPercentageMin
    steam_achievements_percentage_max: SteamAchievementsPercentageMax
    steam_achievements_include_play_game: SteamAchievementsIncludePlayGame
    steam_achievements_include_unlock_any_achievement: SteamAchievementsIncludeUnlockAnyAchievement
    steam_achievements_include_beat_game: SteamAchievementsIncludeBeatGame
    steam_achievements_include_all_achievements: SteamAchievementsIncludeAllAchievements
    steam_achievements_include_percentage: SteamAchievementsIncludePercentage
    steam_achievements_include_specific_achievements: SteamAchievementsIncludeSpecificAchievements
    steam_achievements_include_hidden_achievements: SteamAchievementsIncludeHiddenAchievements
    steam_achievements_time_consuming_threshold: SteamAchievementsTimeConsumingThreshold
    steam_achievements_difficulty_threshold: SteamAchievementsDifficultyThreshold
    steam_achievements_include_redo_achievements: SteamAchievementsIncludeRedoAchievements

class SteamAchievementsGame(Game):
    name = "Steam Achievements"
    platform = KeymastersKeepGamePlatforms.META
    is_adult_only_or_unrated = False
    options_cls = SteamAchievementsArchipelagoOptions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._eligible_games_cache: List[Dict[str, any]] | None = None

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        eligible_games = self._get_eligible_games_data()

        # Fallback when no Steam data is available with defaults
        if not eligible_games:
            return [
                GameObjectiveTemplate(
                    label="Play any game from your Steam library",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            ]

        played_count = sum(1 for g in eligible_games if g.get("playtime_forever", 0) > 0)
        print(f"  Steam Achievements: {len(eligible_games)} eligible games ({played_count} played)")

        templates = []

        if self.archipelago_options.steam_achievements_include_play_game.value:
            templates.append(
                GameObjectiveTemplate(
                    label="Play STEAM_GAME_NAME",
                    data={
                        "STEAM_GAME_NAME": (self.games, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=9,
                )
            )

        if self.archipelago_options.steam_achievements_include_unlock_any_achievement.value:
            templates.append(
                GameObjectiveTemplate(
                    label="Unlock any achievement in STEAM_GAME_NAME",
                    data={
                        "STEAM_GAME_NAME": (self.games, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=12,
                )
            )

        if self.archipelago_options.steam_achievements_include_beat_game.value:
            templates.append(
                GameObjectiveTemplate(
                    label="Beat STEAM_GAME_NAME",
                    data={
                        "STEAM_GAME_NAME": (self.games, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=9,
                )
            )

        if self.archipelago_options.steam_achievements_include_percentage.value:
            print("  Steam Achievements: [Percentage] Checking...")
            pct_objectives = self.percentage_objectives()
            if pct_objectives:
                templates.append(
                    GameObjectiveTemplate(
                        label="PERCENTAGE_OBJECTIVE",
                        data={
                            "PERCENTAGE_OBJECTIVE": (self.percentage_objectives, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=18,
                    )
                )

        if self.archipelago_options.steam_achievements_include_all_achievements.value:
            templates.append(
                GameObjectiveTemplate(
                    label="Unlock all the achievements in STEAM_GAME_NAME",
                    data={
                        "STEAM_GAME_NAME": (self.games, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                )
            )

        if self.archipelago_options.steam_achievements_include_redo_achievements.value:
            print("  Steam Achievements: [Redo] Checking quick...")
            quick_redo = self.quick_redo_achievements_with_games()
            if quick_redo:
                templates.append(
                    GameObjectiveTemplate(
                        label="QUICK_REDO_ACHIEVEMENT_WITH_GAME",
                        data={
                            "QUICK_REDO_ACHIEVEMENT_WITH_GAME": (self.quick_redo_achievements_with_games, 1)
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=3,
                    )
                )
            print("  Steam Achievements: [Redo] Checking medium...")
            medium_redo = self.medium_redo_achievements_with_games()
            if medium_redo:
                templates.append(
                    GameObjectiveTemplate(
                        label="MEDIUM_REDO_ACHIEVEMENT_WITH_GAME",
                        data={
                            "MEDIUM_REDO_ACHIEVEMENT_WITH_GAME": (self.medium_redo_achievements_with_games, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    )
                )
            print("  Steam Achievements: [Redo] Checking hard...")
            hard_redo = self.hard_redo_achievements_with_games()
            if hard_redo:
                templates.append(
                    GameObjectiveTemplate(
                        label="HARD_REDO_ACHIEVEMENT_WITH_GAME",
                        data={
                            "HARD_REDO_ACHIEVEMENT_WITH_GAME": (self.hard_redo_achievements_with_games, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=1,
                    )
                )

        if self.archipelago_options.steam_achievements_include_specific_achievements.value:
            # Quick achievements (global unlock % >= time consuming threshold)
            templates.append(
                GameObjectiveTemplate(
                    label="QUICK_ACHIEVEMENT_WITH_GAME",
                    data={
                        "QUICK_ACHIEVEMENT_WITH_GAME": (self.quick_specific_achievements_with_games, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=15,
                )
            )
            # Medium achievements (>= difficulty threshold but < time consuming threshold)
            templates.append(
                GameObjectiveTemplate(
                    label="MEDIUM_ACHIEVEMENT_WITH_GAME",
                    data={
                        "MEDIUM_ACHIEVEMENT_WITH_GAME": (self.medium_specific_achievements_with_games, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=12,
                )
            )
            # Hard achievements (global unlock % < difficulty threshold)
            templates.append(
                GameObjectiveTemplate(
                    label="HARD_ACHIEVEMENT_WITH_GAME",
                    data={
                        "HARD_ACHIEVEMENT_WITH_GAME": (self.hard_specific_achievements_with_games, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=9,
                )
            )
            
        return templates

    def _get_eligible_games_data(self) -> List[Dict[str, any]]:
        if self._eligible_games_cache is not None:
            return self._eligible_games_cache

        min_time_played = self.archipelago_options.steam_achievements_min_time_played.value
        max_time_played = self.archipelago_options.steam_achievements_max_time_played.value
        steam_id = self.archipelago_options.steam_achievements_steam_id.value
        
        try:
            all_games = steam_library.games(steam_id)
        except Exception as e:
            print(f"Error fetching Steam games: {e}")
            return []
        
        filtered_games = []
        excluded = self.excluded_games
        
        for game in all_games:
            if game.get("playtime_forever", 0) < min_time_played:
                continue
            if max_time_played != -1 and game.get("playtime_forever", 0) > max_time_played:
                continue
            
            if game["name"] in excluded or str(game["appid"]) in excluded:
                continue

            if not game.get("has_community_visible_stats", False):
                continue
                
            filtered_games.append(game)

        self._eligible_games_cache = filtered_games
        return filtered_games

    def games(self) -> List[str]:
        return sorted([g["name"] for g in self._get_eligible_games_data()])

    def _get_achievements_by_tier(self, tier: str) -> List[str]:
        """
        Picks a random eligible game and fetches its achievements via the Steam API.
        Splits achievements into tiers based on global unlock percentages:
          - "quick": unlock % >= time_consuming_threshold (not time consuming, not difficult)
          - "medium": unlock % >= difficulty_threshold but < time_consuming_threshold (time consuming, not difficult)
          - "hard": unlock % < difficulty_threshold (time consuming, difficult)
        Returns list of formatted strings like "Unlock the achievement 'Achievement Name' in Game Name"
        """
        eligible = self._get_eligible_games_data()
        if not eligible:
            return []
        
        shuffled = eligible[:]
        random.shuffle(shuffled)
        
        steam_id = self.archipelago_options.steam_achievements_steam_id.value
        include_hidden = self.archipelago_options.steam_achievements_include_hidden_achievements.value
        time_threshold = float(self.archipelago_options.steam_achievements_time_consuming_threshold.value)
        diff_threshold = float(self.archipelago_options.steam_achievements_difficulty_threshold.value)
        
        for i, game in enumerate(shuffled, 1):
            achievements = steam_library.get_locked_achievements(steam_id, game["appid"], include_hidden)
            if not achievements:
                continue
            
            global_pcts = steam_library.get_global_achievement_percentages(game["appid"])
            
            filtered = []
            for achievement in achievements:
                pct = float(global_pcts.get(achievement, 50.0))  # Default to 50% if unknown
                
                if tier == "quick" and pct >= time_threshold:
                    filtered.append(f"Unlock the achievement '{achievement}' in {game['name']}")
                elif tier == "medium" and diff_threshold <= pct < time_threshold:
                    filtered.append(f"Unlock the achievement '{achievement}' in {game['name']}")
                elif tier == "hard" and pct < diff_threshold:
                    filtered.append(f"Unlock the achievement '{achievement}' in {game['name']}")
            
            if filtered:
                print(f"    [{tier}] Found match after checking {i} game(s)")
                return filtered
        
        print(f"    [{tier}] No match found after checking {len(shuffled)} games")
        return []

    def quick_specific_achievements_with_games(self) -> List[str]:
        return self._get_achievements_by_tier(tier="quick")

    def medium_specific_achievements_with_games(self) -> List[str]:
        return self._get_achievements_by_tier(tier="medium")

    def hard_specific_achievements_with_games(self) -> List[str]:
        return self._get_achievements_by_tier(tier="hard")

    def _get_redo_achievements_by_tier(self, tier: str) -> List[str]:
        """Like _get_achievements_by_tier but for already-unlocked achievements."""
        eligible = self._get_eligible_games_data()
        if not eligible:
            return []

        played = [g for g in eligible if g.get("playtime_forever", 0) > 0]
        if not played:
            return []

        shuffled = played[:]
        random.shuffle(shuffled)

        steam_id = self.archipelago_options.steam_achievements_steam_id.value
        include_hidden = self.archipelago_options.steam_achievements_include_hidden_achievements.value
        time_threshold = float(self.archipelago_options.steam_achievements_time_consuming_threshold.value)
        diff_threshold = float(self.archipelago_options.steam_achievements_difficulty_threshold.value)

        for i, game in enumerate(shuffled, 1):
            achievements = steam_library.get_unlocked_achievements(steam_id, game["appid"], include_hidden)
            if not achievements:
                continue

            global_pcts = steam_library.get_global_achievement_percentages(game["appid"])

            filtered = []
            for achievement in achievements:
                pct = float(global_pcts.get(achievement, 50.0))

                if tier == "quick" and pct >= time_threshold:
                    filtered.append(f"Re-do the achievement '{achievement}' in {game['name']}")
                elif tier == "medium" and diff_threshold <= pct < time_threshold:
                    filtered.append(f"Re-do the achievement '{achievement}' in {game['name']}")
                elif tier == "hard" and pct < diff_threshold:
                    filtered.append(f"Re-do the achievement '{achievement}' in {game['name']}")

            if filtered:
                print(f"    [{tier} redo] Found match after checking {i} game(s)")
                return filtered

        print(f"    [{tier} redo] No match found after checking {len(shuffled)} games")
        return []

    def quick_redo_achievements_with_games(self) -> List[str]:
        return self._get_redo_achievements_by_tier(tier="quick")

    def medium_redo_achievements_with_games(self) -> List[str]:
        return self._get_redo_achievements_by_tier(tier="medium")

    def hard_redo_achievements_with_games(self) -> List[str]:
        return self._get_redo_achievements_by_tier(tier="hard")

    @property
    def excluded_games(self) -> Set[str]:
        return self.archipelago_options.steam_achievements_excluded_games.value

    def percentages(self) -> range:
        min_pct = self.archipelago_options.steam_achievements_percentage_min.value
        max_pct = self.archipelago_options.steam_achievements_percentage_max.value
        return range(min(min_pct, max_pct), max(min_pct, max_pct) + 1)

    def percentage_objectives(self) -> List[str]:
        """Pick a random game, check its progress with one API call, return valid percentages above current."""
        eligible = self._get_eligible_games_data()
        if not eligible:
            return []

        min_pct = self.archipelago_options.steam_achievements_percentage_min.value
        max_pct = self.archipelago_options.steam_achievements_percentage_max.value
        steam_id = self.archipelago_options.steam_achievements_steam_id.value

        played = [g for g in eligible if g.get("playtime_forever", 0) > 0]
        if not played:
            return []

        shuffled = played[:]
        random.shuffle(shuffled)

        for i, game in enumerate(shuffled, 1):
            counts = steam_library.get_achievement_counts(steam_id, game["appid"])
            if counts is None:
                continue
            unlocked, total = counts
            if total == 0:
                continue
            current_pct = (unlocked / total) * 100
            effective_min = max(min_pct, int(current_pct) + 1)
            if effective_min > max_pct:
                continue
            print(f"    [percentage] Found match after checking {i} game(s)")
            return [
                f"Unlock at least {pct}% of the achievements in {game['name']}"
                for pct in range(effective_min, max_pct + 1)
            ]

        print(f"    [percentage] No match found after checking {len(shuffled)} games")
        return []

# Define options specifically for this game to avoid confusion in YAML
class SteamAchievementsMinTimePlayed(NamedRange):
    """
    Only include games from your steam library that have been played at least this many minutes.

    Use -1 or "no_limit" for no minimum.
    """
    display_name = "Steam Achievements Min-Time Played"
    default = 0
    range_start = 0
    range_end = 5256000
    special_range_names = {
        "no_limit": 0
    }

class SteamAchievementsMaxTimePlayed(NamedRange):
    """
    Only include games from your steam library that have been played at most this many minutes.

    Use -1 or "no_limit" for no maximum.
    """
    display_name = "Steam Achievements Max-Time Played"
    default = -1
    range_start = -1
    range_end = 5256000
    special_range_names = {
        "no_limit": -1,
        "never_played": 0,
    }

class SteamAchievementsSteamID(FreeText):
    """
    Steam ID to use for fetching the library.
    """
    display_name = "Steam Achievements Steam ID"

class SteamAchievementsExcludedGames(OptionSet):
    """
    List of game names (must be an exact match) or Steam App IDs to exclude from the Steam library.
    """
    display_name = "Steam Achievements Excluded Games"

class SteamAchievementsPercentageMin(Range):
    """
    Minimum percentage of achievements to require.
    """
    display_name = "Steam Achievements Min Percentage"
    default = 10
    range_start = 1
    range_end = 100

class SteamAchievementsPercentageMax(Range):
    """
    Maximum percentage of achievements to require.
    """
    display_name = "Steam Achievements Max Percentage"
    default = 75
    range_start = 1
    range_end = 100
    
class SteamAchievementsIncludePlayGame(DefaultOnToggle):
    """
    Include objectives to play a game from your Steam library.
    """
    display_name = "Steam Achievements Include Play Game"

class SteamAchievementsIncludeUnlockAnyAchievement(DefaultOnToggle):
    """
    Include objectives to unlock any single achievement in a game from your Steam library.
    """
    display_name = "Steam Achievements Include Unlock Any Achievement"

class SteamAchievementsIncludeBeatGame(DefaultOnToggle):
    """
    Include objectives to beat a game from your Steam library.
    """
    display_name = "Steam Achievements Include Beat Game"

class SteamAchievementsIncludeAllAchievements(DefaultOnToggle):
    """
    Include objectives to unlock all achievements in a game from your Steam library.
    """
    display_name = "Steam Achievements Include All Achievements"

class SteamAchievementsIncludeSpecificAchievements(DefaultOnToggle):
    """
    Include objectives to unlock specific achievements from a random game in your library.
    """
    display_name = "Steam Achievements Include Specific Achievements"

class SteamAchievementsIncludePercentage(DefaultOnToggle):
    """
    Include objectives to unlock a certain percentage of achievements in a game from your Steam library.
    """
    display_name = "Steam Achievements Include Percentage"

class SteamAchievementsIncludeHiddenAchievements(Toggle):
    """
    Include hidden achievements when selecting specific achievements.
    """
    display_name = "Steam Achievements Include Hidden Achievements"

class SteamAchievementsIncludeRedoAchievements(Toggle):
    """
    Include low-priority objectives to re-do achievements the player has already unlocked.
    """
    display_name = "Steam Achievements Include Redo Achievements"

class SteamAchievementsTimeConsumingThreshold(Range):
    """
    Global unlock percentage threshold for time-consuming achievements.
    Achievements unlocked by at least this percentage of players globally are considered quick (not time consuming).
    Achievements below this but above the difficulty threshold are considered time consuming but not difficult.
    For example, a value of 50 means achievements unlocked by 50%+ of players are quick objectives.
    """
    display_name = "Steam Achievements Time Consuming Threshold"
    default = 50
    range_start = 1
    range_end = 100

class SteamAchievementsDifficultyThreshold(Range):
    """
    Global unlock percentage threshold for achievement difficulty.
    Achievements unlocked by fewer than this percentage of players globally are considered difficult.
    For example, a value of 10 means achievements unlocked by less than 10% of players are difficult.
    """
    display_name = "Steam Achievements Difficulty Threshold"
    default = 10
    range_start = 1
    range_end = 100

class SteamLibraryHolder:
    def __init__(self):
        self._schema_cache: Dict[int, List[Dict]] = {}

    def _get_schema(self, app_id: int) -> List[Dict]:
        """Fetch and cache the achievement schema for a game."""
        if app_id in self._schema_cache:
            return self._schema_cache[app_id]
        key = environ.get("STEAM_API_KEY")
        if not key:
            self._schema_cache[app_id] = []
            return []
        try:
            resp = requests.get(
                "https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/",
                params={"key": key, "appid": app_id},
                timeout=10,
            )
            if resp.status_code == 200:
                result = resp.json().get("game", {}).get("availableGameStats", {}).get("achievements", [])
            else:
                result = []
        except Exception:
            result = []
        self._schema_cache[app_id] = result
        return result

    @functools.lru_cache(maxsize=None)
    def games(self, steam_id) -> List[Dict[str, any]]:
        key = environ.get("STEAM_API_KEY")
        if not key:
            # Fall back to a small, static set of well-known games
            # Ensures CI tests have valid entries without requiring a Steam API key
            return self._default_games()
        try:
            print("Fetching games from Steam library...")
            steam_response = requests.get(
                "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/",
                params={
                    "key": key,
                    "steamid": steam_id,
                    "include_appinfo": True,
                    "include_played_free_games": True,
                },
                timeout=10,
            )
            if steam_response.status_code != 200:
                # Fall back instead of raising to keep objectives generation resilient
                return self._default_games()
            games_data = steam_response.json().get("response", {}).get("games", [])
            return games_data
        except Exception:
            # Any network or parse issue → fallback
            return self._default_games()

    def get_locked_achievements(self, steam_id, app_id, include_hidden=True) -> List[str]:
        key = environ.get("STEAM_API_KEY")
        if not key:
            # Provide placeholder achievement names respecting the hidden toggle
            return self._default_achievements(include_hidden=include_hidden)
        
        # 1. Get Player Achievements
        try:
            resp = requests.get(
                "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/",
                params={"key": key, "steamid": steam_id, "appid": app_id},
                timeout=10,
            )
            if resp.status_code != 200:
                return []
            data = resp.json()
        except Exception:
            return []

        if not data.get("playerstats", {}).get("success"):
            return []
            
        achievements = data["playerstats"].get("achievements", [])
        locked_apinames = [a["apiname"] for a in achievements if a["achieved"] == 0]
        
        if not locked_apinames:
            return []

        # 2. Get Schema for Display Names
        available_stats = self._get_schema(app_id)
        if not available_stats:
            return locked_apinames
        
        name_map = {}
        for a in available_stats:
            if not include_hidden and a.get("hidden", 0) == 1:
                continue
            name_map[a["name"]] = a.get("displayName") or a.get("name")
        
        return [name_map.get(api, api) for api in locked_apinames if include_hidden or api in name_map]

    def get_unlocked_achievements(self, steam_id, app_id, include_hidden=True) -> List[str]:
        key = environ.get("STEAM_API_KEY")
        if not key:
            return self._default_achievements(include_hidden=include_hidden)

        try:
            resp = requests.get(
                "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/",
                params={"key": key, "steamid": steam_id, "appid": app_id},
                timeout=10,
            )
            if resp.status_code != 200:
                return []
            data = resp.json()
        except Exception:
            return []

        if not data.get("playerstats", {}).get("success"):
            return []

        achievements = data["playerstats"].get("achievements", [])
        unlocked_apinames = [a["apiname"] for a in achievements if a["achieved"] == 1]

        if not unlocked_apinames:
            return []

        available_stats = self._get_schema(app_id)
        if not available_stats:
            return unlocked_apinames

        name_map = {}
        for a in available_stats:
            if not include_hidden and a.get("hidden", 0) == 1:
                continue
            name_map[a["name"]] = a.get("displayName") or a.get("name")

        return [name_map.get(api, api) for api in unlocked_apinames if include_hidden or api in name_map]

    @functools.lru_cache(maxsize=None)
    def get_global_achievement_percentages(self, app_id) -> Dict[str, float]:
        """Returns a dict mapping achievement display name to global unlock percentage."""
        key = environ.get("STEAM_API_KEY")
        if not key:
            return self._default_global_percentages()
        try:
            resp = requests.get(
                "https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/",
                params={"gameid": app_id},
                timeout=10,
            )
            if resp.status_code != 200:
                return {}
            data = resp.json()
        except Exception:
            return {}

        achievements = data.get("achievementpercentages", {}).get("achievements", [])
        
        # This endpoint returns api names; map to display names using schema
        pct_by_api = {a["name"]: float(a["percent"]) for a in achievements}
        
        # Try to get display names from cached schema
        available = self._get_schema(app_id)
        if available:
            result = {}
            for a in available:
                display = a.get("displayName") or a.get("name")
                result[display] = pct_by_api.get(a["name"], 50.0)
            return result
        
        # Fallback: return api name mapping
        return pct_by_api

    def _default_global_percentages(self) -> Dict[str, float]:
        return {
            "Example Achievement": 75.0,
            "Example Hidden Achievement": 5.0,
        }

    @functools.lru_cache(maxsize=None)
    def get_achievement_counts(self, steam_id, app_id):
        """Returns (unlocked_count, total_count) for a player's achievements in a game, or None on failure."""
        key = environ.get("STEAM_API_KEY")
        if not key:
            return (0, 2)
        try:
            resp = requests.get(
                "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/",
                params={"key": key, "steamid": steam_id, "appid": app_id},
                timeout=10,
            )
            if resp.status_code != 200:
                return None
            data = resp.json()
        except Exception:
            return None

        if not data.get("playerstats", {}).get("success"):
            return None

        achievements = data["playerstats"].get("achievements", [])
        total = len(achievements)
        unlocked = sum(1 for a in achievements if a["achieved"] == 1)
        return (unlocked, total)

    def _default_games(self) -> List[Dict[str, any]]:
        # Minimal fields used by filtering and formatting: name, appid, playtime_forever, has_community_visible_stats
        return [
            {"appid": 1000, "name": "Example Game", "playtime_forever": 60, "has_community_visible_stats": True},
        ]

    def _default_achievements(self, include_hidden: bool = True) -> List[str]:
        # Generic placeholders used when Steam API isn't available
        base = ["Example Achievement"]
        hidden = ["Example Hidden Achievement"]
        return base + (hidden if include_hidden else [])

steam_library = SteamLibraryHolder()
