from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class AtomicropsArchipelagoOptions:
    atomicrops_include_character_objectives: AtomicropsIncludeCharacterObjectives
    atomicrops_include_year_objectives: AtomicropsIncludeYearObjectives


class AtomicropsGame(Game):
    name = "Atomicrops"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = AtomicropsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on Year 10",
                data={},
            ),
            GameObjectiveTemplate(
                label="Play on Year 5+",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't buy any guns (Stick with the Peashooter)",
                data={},
            ),
            GameObjectiveTemplate(
                label="Only buy new guns if you can afford both",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't get married",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't use any Tractors",
                data={},
            ),
            GameObjectiveTemplate(
                label="Purchase a new Tractor after each Season",
                data={},
            ),
            GameObjectiveTemplate(
                label="If you can afford it, gamble at least once after every season",
                data={},
            ),
            GameObjectiveTemplate(
                label="Take Scarecrows whenever they are offered at camps",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't harvest any plants until dawn of Day 1",
                data={},
            ),
            GameObjectiveTemplate(
                label="Have no Trees on your farm at the end of the run",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        objectives += self.base_objectives()
        
        if self.include_character_objectives:
            objectives += self.character_objectives()
            
        if self.include_year_objectives:
            objectives += self.year_objectives()
        
        return objectives
    
    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return []
    
    def character_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat the Corpse-a-Copia (Nuclear Winter Boss) as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Clear a Tier 1 Biome (Desert or Plains) as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Clear a Tier 2 Biome (Tundra or Jungle) as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Get Married as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Harvest a Mega Crop as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
             GameObjectiveTemplate(
                label="Collect 1000 Cashews in a single run as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat Deervil as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
        ]
    
    def year_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run on Year 5+",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a run on Year 10",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
        ]
    
    @property
    def include_character_objectives(self) -> bool:
        return self.archipelago_options.atomicrops_include_character_objectives.value
    
    @property
    def include_year_objectives(self) -> bool:
        return self.archipelago_options.atomicrops_include_year_objectives.value
    
    @staticmethod
    def characters() -> List[str]:
        return [
            "Lavender",
            "Rye",
            "Robusta",
            "Thyme",
            "Dandelion",
            "Crow",
        ]


# Archipelago Options
class AtomicropsIncludeCharacterObjectives(Toggle):
    """
    Indicates whether to include objectives that require winning with specific characters.
    """
    display_name = "Atomicrops: Include Character Objectives"


class AtomicropsIncludeYearObjectives(Toggle):
    """
    Indicates whether to include objectives that require playing on higher Years (difficulty).
    """
    display_name = "Atomicrops: Include Year Objectives"
