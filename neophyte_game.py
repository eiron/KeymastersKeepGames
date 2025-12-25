from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle, DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class NeophyteArchipelagoOptions:
    neophyte_include_difficulty_objectives: NeophyteIncludeDifficultyObjectives
    neophyte_include_loadout_objectives: NeophyteIncludeLoadoutObjectives


class NeophyteGame(Game):
    name = "Neophyte"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = NeophyteArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a run without upgrading weapons",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a run without using any special abilities",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a run taking minimal damage (less than 25% health lost)",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a run on maximum difficulty",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a run using only melee weapons",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a run using only ranged weapons",
                data={},
            ),
            GameObjectiveTemplate(
                label="Collect all upgrades in a single run",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a run without visiting any shops",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a run with LOADOUT only",
                data={
                    "LOADOUT": (self.loadouts, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS_NAME without taking any damage",
                data={
                    "BOSS_NAME": (self.bosses, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        objectives += self.base_objectives()
        
        if self.include_difficulty_objectives:
            objectives += self.difficulty_objectives()
            
        if self.include_loadout_objectives:
            objectives += self.loadout_objectives()
        
        return objectives
    
    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a full run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Defeat the final boss",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Complete a run collecting 50+ gold",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Complete a run with 5+ weapon upgrades",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat all boss encounters without dying",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Complete a run visiting all available rooms",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Defeat ENEMY_TYPE boss",
                data={
                    "ENEMY_TYPE": (self.bosses, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
        ]
    
    def difficulty_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a run on Hard difficulty",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Complete a run on Hard difficulty without upgrading weapons",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Complete a run on Hard difficulty taking minimal damage",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=7,
            ),
        ]
    
    def loadout_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a run using only LOADOUT equipment",
                data={
                    "LOADOUT": (self.loadouts, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat the final boss using LOADOUT equipment",
                data={
                    "LOADOUT": (self.loadouts, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Beat the game on Challenge Level CHALLENGE_LEVEL. Start with SPELL_COMBO",
                data={
                    "CHALLENGE_LEVEL": (self.challenge_levels, 1),
                    "SPELL_COMBO": (self.spell_locations, 2),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="CONDITION. Beat the game on Challenge Level CHALLENGE_LEVEL. Start with SPELL_COMBO",
                data={
                    "CONDITION": (self.run_conditions, 1),
                    "CHALLENGE_LEVEL": (self.challenge_levels, 1),
                    "SPELL_COMBO": (self.spell_locations, 2),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=9,
            ),
            GameObjectiveTemplate(
                label="Beat Challenge Level CHALLENGE_LEVEL without taking any damage",
                data={
                    "CHALLENGE_LEVEL": (self.challenge_levels, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Collect all RARITY spells in a single Challenge Level CHALLENGE_LEVEL run",
                data={
                    "RARITY": (self.spell_rarities, 1),
                    "CHALLENGE_LEVEL": (self.challenge_levels, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Complete Challenge Level CHALLENGE_LEVEL collecting all available emblems",
                data={
                    "CHALLENGE_LEVEL": (self.challenge_levels, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=7,
            ),
        ]
    
    @property
    def include_difficulty_objectives(self) -> bool:
        return self.archipelago_options.neophyte_include_difficulty_objectives.value
    
    @property
    def include_loadout_objectives(self) -> bool:
        return self.archipelago_options.neophyte_include_loadout_objectives.value
    
    @staticmethod
    def bosses() -> List[str]:
        return [
            "Wraith",
            "Construct",
            "Shadow Knight",
            "Ancient Guardian",
            "Final Boss",
        ]

    @staticmethod
    def loadouts() -> List[str]:
        return [
            "Sword and Shield",
            "Dual Blades",
            "Bow and Arrow",
            "Magic Staff",
            "Spear",
            "Hammer",
            "Heavy Armor",
            "Light Armor",
        ]

    @staticmethod
    def challenge_levels() -> List[str]:
        return [
            "1",
            "2",
            "3",
            "4",
            "5",
        ]

    @staticmethod
    def spell_locations() -> List[str]:
        return [
            "leftmost",
            "centre",
            "rightmost",
        ]

    @staticmethod
    def spell_rarities() -> List[str]:
        return [
            "common",
            "uncommon",
            "rare",
            "legendary",
        ]

    @staticmethod
    def run_conditions() -> List[str]:
        return [
            "Without rerolling in the first or third arenas",
            "Taking all mana or mana per second increases",
            "Surviving a wave in the second or third arena using only 2 of your equipped spells",
            "Without taking any duplicate emblems",
            "Defeating at least four waves without taking any damage",
            "Keeping your first two spells equipped for the entire run",
            "Hitting the reroll statue at least once whenever you see it, before taking any items",
            "Choosing the leftmost reward for the first 4 times you are given choices of rewards",
            "Without upgrading weapons",
            "Without visiting any shops",
            "Taking minimal damage (less than 25% health lost)",
        ]


# Archipelago Options
class NeophyteIncludeDifficultyObjectives(Toggle):
    """
    Indicates whether to include objectives that require playing on higher difficulty levels.
    """
    display_name = "Neophyte: Include Difficulty Objectives"


class NeophyteIncludeLoadoutObjectives(DefaultOnToggle):
    """
    Indicates whether to include objectives that require using specific loadouts or equipment combinations.
    """
    display_name = "Neophyte: Include Loadout Objectives"
