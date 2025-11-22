from __future__ import annotations

import functools
from os import environ
import requests
from typing import List, Set, Dict

from dataclasses import dataclass

from Options import NamedRange, OptionSet, FreeText, Range

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

class SteamAchievementsGame(Game):
    name = "Steam Achievements"
    platform = KeymastersKeepGamePlatforms.META
    is_adult_only_or_unrated = False
    options_cls = SteamAchievementsArchipelagoOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
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

    def games(self) -> List[str]:
        min_time_played = self.archipelago_options.steam_achievements_min_time_played.value
        max_time_played = self.archipelago_options.steam_achievements_max_time_played.value
        steam_id = self.archipelago_options.steam_achievements_steam_id.value
        
        # Reuse the steam_library holder to fetch games
        try:
            all_games = steam_library.games(steam_id)
        except Exception as e:
            print(f"Error fetching Steam games: {e}")
            return []
        
        filtered_games = []
        for game in all_games:
            # Filter by playtime
            if game.get("playtime_forever", 0) < min_time_played:
                continue
            if max_time_played != -1 and game.get("playtime_forever", 0) > max_time_played:
                continue
            
            # Filter excluded games
            if game["name"] in self.excluded_games() or str(game["appid"]) in self.excluded_games():
                continue

            # Filter for achievements presence
            # has_community_visible_stats is usually true for games with achievements/stats
            if not game.get("has_community_visible_stats", False):
                continue
                
            filtered_games.append(game["name"])
            
        return sorted(filtered_games)

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
steam_library = SteamLibraryHolder()
