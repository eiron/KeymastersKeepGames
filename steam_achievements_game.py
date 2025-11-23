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
    steam_achievements_include_specific_achievements: SteamAchievementsIncludeSpecificAchievements
    steam_achievements_include_hidden_achievements: SteamAchievementsIncludeHiddenAchievements

class SteamAchievementsGame(Game):
    name = "Steam Achievements"
    platform = KeymastersKeepGamePlatforms.META
    is_adult_only_or_unrated = False
    options_cls = SteamAchievementsArchipelagoOptions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_specific_game = None
        self._cached_locked_achievements = None

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates = [
            GameObjectiveTemplate(
                label="Beat STEAM_GAME_NAME",
                data={
                    "STEAM_GAME_NAME": (self.games, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Unlock at least ACHIEVEMENT_PERCENTAGE% of the achievements in STEAM_GAME_NAME",
                data={
                    "STEAM_GAME_NAME": (self.games, 1),
                    "ACHIEVEMENT_PERCENTAGE": (self.percentages, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=9,
            ),
            GameObjectiveTemplate(
                label="Unlock all the achievements in STEAM_GAME_NAME",
                data={
                    "STEAM_GAME_NAME": (self.games, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

        if self.archipelago_options.steam_achievements_include_specific_achievements.value:
            templates.append(
                GameObjectiveTemplate(
                    label="Unlock the achievement 'ACHIEVEMENT_NAME' in SPECIFIC_GAME",
                    data={
                        "ACHIEVEMENT_NAME": (self.specific_game_achievements, 1),
                        "SPECIFIC_GAME": (self.specific_game_name, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                )
            )
            
        return templates

    def _get_eligible_games_data(self) -> List[Dict[str, any]]:
        min_time_played = self.archipelago_options.steam_achievements_min_time_played.value
        max_time_played = self.archipelago_options.steam_achievements_max_time_played.value
        steam_id = self.archipelago_options.steam_achievements_steam_id.value
        
        try:
            all_games = steam_library.games(steam_id)
        except Exception as e:
            print(f"Error fetching Steam games: {e}")
            return []
        
        filtered_games = []
        excluded = self.excluded_games()
        
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
        return filtered_games

    def games(self) -> List[str]:
        return sorted([g["name"] for g in self._get_eligible_games_data()])

    def _get_random_game_with_achievements(self):
        if self._cached_specific_game:
            return self._cached_specific_game, self._cached_locked_achievements
            
        eligible = self._get_eligible_games_data()
        if not eligible:
            return None, []
            
        # Shuffle eligible list to pick random ones
        shuffled = eligible[:]
        random.shuffle(shuffled)
        
        steam_id = self.archipelago_options.steam_achievements_steam_id.value
        include_hidden = self.archipelago_options.steam_achievements_include_hidden_achievements.value
        
        for game in shuffled[:5]: # Try up to 5 games
            achievements = steam_library.get_locked_achievements(steam_id, game["appid"], include_hidden)
            if achievements:
                self._cached_specific_game = game["name"]
                self._cached_locked_achievements = achievements
                return self._cached_specific_game, self._cached_locked_achievements
                
        return None, []

    def specific_game_name(self) -> List[str]:
        game, _ = self._get_random_game_with_achievements()
        return [game] if game else []

    def specific_game_achievements(self) -> List[str]:
        _, achs = self._get_random_game_with_achievements()
        return achs

    def excluded_games(self) -> Set[str]:
        return self.archipelago_options.steam_achievements_excluded_games.value

    def percentages(self) -> range:
        min_pct = self.archipelago_options.steam_achievements_percentage_min.value
        max_pct = self.archipelago_options.steam_achievements_percentage_max.value
        if min_pct > max_pct:
            return range(max_pct, min_pct + 1)
        return range(min_pct, max_pct + 1)

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

class SteamAchievementsIncludeSpecificAchievements(DefaultOnToggle):
    """
    Include objectives to unlock specific achievements from a random game in your library.
    """
    display_name = "Steam Achievements Include Specific Achievements"

class SteamAchievementsIncludeHiddenAchievements(Toggle):
    """
    Include hidden achievements when selecting specific achievements.
    """
    display_name = "Steam Achievements Include Hidden Achievements"

class SteamLibraryHolder:
    @functools.lru_cache(maxsize=None)
    def games(self, steam_id) -> List[Dict[str, any]]:
        key = environ.get("STEAM_API_KEY")
        if not key:
            raise RuntimeError("STEAM_API_KEY environment variable is not set")
        print("Fetching games from Steam library...")
        steam_response = requests.get("https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/",
                                      params={
                                          "key": key,
                                          "steamid": steam_id,
                                          "include_appinfo": True,
                                          "include_played_free_games": True,
                                      })
        if steam_response.status_code != 200:
            raise RuntimeError(f"Steam API returned {steam_response.status_code}")
        games_data = steam_response.json().get("response", {}).get("games", [])

        return games_data

    def get_locked_achievements(self, steam_id, app_id, include_hidden=True) -> List[str]:
        key = environ.get("STEAM_API_KEY")
        if not key:
            return []
        
        # 1. Get Player Achievements
        try:
            resp = requests.get("https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/",
                                params={"key": key, "steamid": steam_id, "appid": app_id})
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
        try:
            resp = requests.get("https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/",
                                params={"key": key, "appid": app_id})
            if resp.status_code != 200:
                return locked_apinames
            schema = resp.json()
        except Exception:
            return locked_apinames

        available_stats = schema.get("game", {}).get("availableGameStats", {}).get("achievements", [])
        
        name_map = {}
        for a in available_stats:
            if not include_hidden and a.get("hidden", 0) == 1:
                continue
            name_map[a["name"]] = a["displayName"]
        
        return [name_map.get(api, api) for api in locked_apinames if include_hidden or api in name_map]
steam_library = SteamLibraryHolder()
