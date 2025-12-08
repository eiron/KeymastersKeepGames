from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BackpackHeroArchipelagoOptions:
    backpack_hero_include_character_objectives: BackpackHeroIncludeCharacterObjectives
    backpack_hero_include_challenge_objectives: BackpackHeroIncludeChallengeObjectives


class BackpackHeroGame(Game):
    name = "Backpack Hero"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = BackpackHeroArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Don't use any Consumables",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't rearrange your inventory during combat",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't visit the Healer",
                data={},
            ),
            GameObjectiveTemplate(
                label="Only take three keys on the entire run",
                data={},
            ),
            GameObjectiveTemplate(
                label="If offered a bow in an event, you must take it. Replace your primary objective 'item' to hold with a bow instead",
                data={},
            ),
            GameObjectiveTemplate(
                label="Fully expand your backpack to the far left before you expand up or down",
                data={},
            ),
            GameObjectiveTemplate(
                label="Skip a non-combat room at least 3 times",
                data={},
            ),
            GameObjectiveTemplate(
                label="Never have a Legendary item in your backpack",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        objectives += self.base_objectives()
        
        if self.include_character_objectives:
            objectives += self.character_objectives()
            
        if self.include_challenge_objectives:
            objectives += self.challenge_objectives()
        
        return objectives
    
    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return []
    
    def character_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run (Defeat the Grandmaster) as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Reach Floor 9 (Magma Core) as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat a Boss without taking damage as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Have 5 Legendary items in your backpack as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
        ]

    def challenge_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run as CHARACTER on Hard Mode",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Win a run as CHARACTER with 0 Energy remaining at the end of every turn",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Generate at least 20 passive block per turn at some point as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Reorganise your inventory during battle at least five times as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Have at least 1 'herbs' in your backpack at the end of the run as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Have five fish in your inventory at one time at some point as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Carry two of the same type of clothing in your backpack (e.g. two boots, two helmets, etc.) as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Kill an enemy with an empty cup as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
        ]
    
    @property
    def include_character_objectives(self) -> bool:
        return self.archipelago_options.backpack_hero_include_character_objectives.value
    
    @property
    def include_challenge_objectives(self) -> bool:
        return self.archipelago_options.backpack_hero_include_challenge_objectives.value
    
    @staticmethod
    def characters() -> List[str]:
        return [
            "Purse",
            "Satchel",
            "Tote",
            "CR-8",
            "Pochette",
        ]


# Archipelago Options
class BackpackHeroIncludeCharacterObjectives(DefaultOnToggle):
    """
    Indicates whether to include objectives that require winning with specific characters.
    """
    display_name = "Backpack Hero: Include Character Objectives"


class BackpackHeroIncludeChallengeObjectives(DefaultOnToggle):
    """
    Indicates whether to include difficult challenge objectives.
    """
    display_name = "Backpack Hero: Include Challenge Objectives"
