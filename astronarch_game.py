from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class AstronarchArchipelagoOptions:
    astronarch_include_ascension_objectives: AstronarchIncludeAscensionObjectives
    astronarch_include_hero_objectives: AstronarchIncludeHeroObjectives


class AstronarchGame(Game):
    name = "Astronarch"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = AstronarchArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on Ascension 20",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't buy any items from shops",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't heal at Rest Sites",
                data={},
            ),
            GameObjectiveTemplate(
                label="Only recruit heroes of the CLASS class",
                data={
                    "CLASS": (self.hero_classes, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Have at least 1 Potion Slot empty at all times",
                data={},
            ),
            GameObjectiveTemplate(
                label="Visit as many Shops as possible",
                data={},
            ),
            GameObjectiveTemplate(
                label="Restock every shop you visit",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        objectives += self.base_objectives()
        
        if self.include_ascension_objectives:
            objectives += self.ascension_objectives()
            
        if self.include_hero_objectives:
            objectives += self.hero_objectives()
        
        return objectives
    
    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Defeat the final boss",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Collect 5 Legendary Items",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Have a party of 5 heroes",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat the King. Your starting party must include: CLASSES",
                data={
                    "CLASSES": (self.hero_classes, 2),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat the King. Your starting party must include: CLASSES",
                data={
                    "CLASSES": (self.hero_classes, 3),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Fight 9 or more Elites",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Collect every Key",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Sell at least 5 non-potion items at a single Shop",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]
    
    def ascension_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run on Ascension 5+",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a run on Ascension 10+",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a run on Ascension 20",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
        ]
    
    def hero_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run with HERO in your party",
                data={
                    "HERO": (self.heroes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
        ]
    
    @property
    def include_ascension_objectives(self) -> bool:
        return self.archipelago_options.astronarch_include_ascension_objectives.value
    
    @property
    def include_hero_objectives(self) -> bool:
        return self.archipelago_options.astronarch_include_hero_objectives.value
    
    @staticmethod
    def hero_classes() -> List[str]:
        return [
            "Warrior",
            "Rogue",
            "Mage",
            "Support",
        ]

    @staticmethod
    def heroes() -> List[str]:
        return [
            "Knight", "Berserker", "Paladin", "Gladiator",
            "Archer", "Assassin", "Hunter", "Thief",
            "Wizard", "Sorcerer", "Warlock", "Necromancer",
            "Cleric", "Priest", "Druid", "Bard",
            # Add more specific heroes as needed
        ]


# Archipelago Options
class AstronarchIncludeAscensionObjectives(Toggle):
    """
    Indicates whether to include objectives that require playing on higher Ascension levels.
    """
    display_name = "Astronarch: Include Ascension Objectives"


class AstronarchIncludeHeroObjectives(DefaultOnToggle):
    """
    Indicates whether to include objectives that require winning with specific heroes.
    """
    display_name = "Astronarch: Include Hero Objectives"
