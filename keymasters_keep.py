"""
Keymaster's Keep Challenges Module

The ultimate meta module for generating challenges to play Keymaster's Keep itself!
This module creates objectives for playing Keymaster's Keep in its two game modes:
- Keymaster's Challenge: Collect artifacts and face the ultimate challenge
- Magic Key Heist: Gather keys and escape the keep

Features a comprehensive list of games from the Keymaster's Keep game selection pool.
"""

from __future__ import annotations
from typing import List, Dict, Set
from dataclasses import dataclass
import functools
import random

from Options import Range, OptionList, Toggle, Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


# Option Dataclass
@dataclass
class KeymastersKeepArchipelagoOptions:
    keymasters_keep_game_selection: KeymastersKeepGameSelection
    keymasters_keep_minimum_game_count: KeymastersKeepMinimumGameCount
    keymasters_keep_maximum_game_count: KeymastersKeepMaximumGameCount
    keymasters_keep_challenge_type_selection: KeymastersKeepChallengeTypeSelection


# Main Class
class KeymastersKeepGame(Game):
    name = "Keymaster's Keep"
    platform = KeymastersKeepGamePlatforms.META

    is_adult_only_or_unrated = False

    options_cls = KeymastersKeepArchipelagoOptions

    # Main Objectives
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = []

        if self.game_selection:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="Complete a CHALLENGE_TYPE including the games: GAMES",
                    data={
                        "CHALLENGE_TYPE": (self.challenge_types, 1),
                        "GAMES": (self.game_selection, self.number_of_games),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=50,
                ),
            )
        
        return game_objective_templates

    @functools.cached_property
    def challenge_types(self) -> List[str]:
        """Get available challenge types based on user selection."""
        challenge_types = []
        selection = self.archipelago_options.keymasters_keep_challenge_type_selection.value
        
        if "keymasters_challenge" in selection:
            challenge_types.append("Keymaster's Challenge")
        if "magic_key_heist" in selection:
            challenge_types.append("Magic Key Heist")
            
        return challenge_types

    def game_selection(self) -> List[str]:
        """Get the player's game selection."""
        games: List[str] = list(self.archipelago_options.keymasters_keep_game_selection.value)
        return sorted(games)
    
    @property
    def number_of_games(self) -> int:
        """Get a random number of games between min and max."""
        min_games = self.archipelago_options.keymasters_keep_minimum_game_count.value
        max_games = self.archipelago_options.keymasters_keep_maximum_game_count.value
        return random.randint(min_games, max_games)


# Archipelago Options
class KeymastersKeepGameSelection(OptionList):
    """
    Indicates which games can be selected for Keymaster's Keep challenges.
    The player is free to add or remove any options they like. Multiple appearances will function as weightings for the options provided.
    Defaults to the comprehensive game selection from the Keymaster's Keep YAML configuration.
    """
    display_name = "Keymaster's Keep Game Selection"
    default = [
        "A Dance of Fire and Ice",
        "Adventure/Experience Challenges",
        "Any Game Bingo",
        "Any Game Tasks",
        "Archipelago Multiworld Randomizer",
        "Archipelagourmet",
        "Awaria",
        "Balatro",
        "Bloons TD 6",
        "Blue Prince",
        "Caveblazers",
        "Celeste",
        "Christmas Holiday Challenges",
        "Cook, Serve, Delicious! 2!!",
        "Creative Challenges",
        "Crush Crush",
        "Cuphead",
        "Custom",
        "Custom Medley",
        "Cytus II",
        "Dead By Daylight",
        "Deep Rock Galactic",
        "DemonCrawl",
        "Descenders",
        "Destiny 2",
        "Dome Keeper",
        "Dungeon Defenders",
        "Ensemble Stars!! Music",
        "Enter the Gungeon",
        "FTL: Multiverse",
        "Fall Guys",
        "Fortnite",
        "Freedom Planet 2",
        "Game Backlog",
        "God Eater Resurrection",
        "Guild Wars 2",
        "Hollow Knight",
        "HoloCure: Save the Fans!",
        "Hotline Miami",
        "Hyperspace Dogfights",
        "Identity V",
        "Jackbox Party Packs",
        "Keymaster's Keep",
        "League of Legends",
        "Left 4 Dead 2",
        "Lethal Company",
        "Little Inferno",
        "MONSTER HUNTER RISE",
        "Made in Abyss: Binary Star Falling into Darkness",
        "Mages of Mystralia",
        "Magic the Gathering",
        "Mario Kart 8",
        "Mario Kart World",
        "Mario Party",
        "Mario Party 2",
        "Mario Party 3",
        "Marvel Rivals",
        "Mega Man",
        "Mega Man 11",
        "Mega Man 2",
        "Mega Man 3",
        "Mega Man 4",
        "Melatonin",
        "Melvor Idle",
        "Minecraft MCParks Server",
        "Monster Hunter World",
        "Music Listening",
        "NiGHTS into Dreams...",
        "Nickelodeon All-Star Brawl 2",
        "Nubby's Number Factory",
        "Octodad: Dadliest Catch",
        "OldTV",
        "OpenRCT2",
        "Ori and the Will of the Wisps",
        "Overwatch 2",
        "PEAK",
        "Paperball",
        "Peggle Deluxe",
        "Physical/Health Challenges",
        "Pinball FX3",
        "Placid Plastic Duck Simulator",
        "Plants vs. Zombies",
        "Pokemon Go",
        "Project Sekai: Colorful Stage",
        "Reading Backlog",
        "Realm of the Mad God",
        "RetroAchievements",
        "Rhythm Doctor",
        "Risk of Rain 2",
        "Rock of Ages 2: Bigger & Boulder",
        "Sea of Thieves",
        "Shiny Pokémon Hunt",
        "Sid Meier's Pirates",
        "Slay the Spire",
        "Smite 2",
        "Sonic Mania",
        "Sonic R",
        "Splatoon 3",
        "Spyro Reignited Trilogy",
        "Star Wars: Battlefront II (Classic)",
        "Steam Library",
        "Stellaris",
        "Super Hexagon",
        "Super Mario Galaxy",
        "Super Mario Sunshine",
        "Super Smash Bros. Ultimate",
        "Synthetik: Legion Rising",
        "Terraria",
        "The Bazaar",
        "The Binding of Isaac: Rebirth",
        "The Elder Scrolls V: Skyrim - Special Edition",
        "The Finals",
        "The Void Rains Upon Her Heart",
        "Tower Unite",
        "Trombone Champ",
        "ULTRAKILL",
        "Ultimate Custom Night",
        "Universal Studios Experience (Minecraft Bedrock)",
        "Vampire Survivors",
        "Watchlist",
        "Wingspan",
        "Worms Armageddon",
    ]


class KeymastersKeepChallengeTypeSelection(OptionList):
    """
    Indicates which challenge types (game modes) can be selected for Keymaster's Keep challenges.
    """
    display_name = "Keymaster's Keep Challenge Type Selection"
    default = [
        "keymasters_challenge",
        "magic_key_heist",
    ]


class KeymastersKeepMinimumGameCount(Range):
    """
    The minimum number of games to include when generating Keymaster's Keep challenges (1-10).
    """
    display_name = "Keymaster's Keep Minimum Game Count"
    default = 2
    range_start = 1
    range_end = 10
    

class KeymastersKeepMaximumGameCount(Range):
    """
    The maximum number of games to include when generating Keymaster's Keep challenges (1-10).
    """
    display_name = "Keymaster's Keep Maximum Game Count"
    default = 6
    range_start = 1
    range_end = 10


# For convenience, create a Game class alias that matches the old pattern
Game = KeymastersKeepGame
