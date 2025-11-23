from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class AlinaOfTheArenaArchipelagoOptions:
    alina_of_the_arena_include_class_objectives: AlinaOfTheArenaIncludeClassObjectives
    alina_of_the_arena_include_challenge_objectives: AlinaOfTheArenaIncludeChallengeObjectives
    alina_of_the_arena_include_hardcore_difficulty: AlinaOfTheArenaIncludeHardcoreDifficulty


class AlinaOfTheArenaGame(Game):
    name = "Alina of the Arena"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = AlinaOfTheArenaArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on Hardcore Mode",
                data={},
            ),
            GameObjectiveTemplate(
                label="Play on Veteran difficulty",
                data={},
            ),
            GameObjectiveTemplate(
                label="Play as the CLASS class",
                data={
                    "CLASS": (self.classes, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Don't visit a shop until the Royal Arena (Mystery Shop is allowed)",
                data={},
            ),
            GameObjectiveTemplate(
                label="Skip the mystery shop",
                data={},
            ),
            GameObjectiveTemplate(
                label="Always choose the immoral choice in Events (stealing, hurting feelings, binding to cursed weapons)",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        objectives += self.base_objectives()
        
        if self.include_class_objectives:
            objectives += self.class_objectives()
            
        if self.include_challenge_objectives:
            objectives += self.challenge_objectives()
            
        if self.include_hardcore_difficulty:
            objectives += self.hardcore_objectives()
        
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
                label="Defeat the Demon of the Arena",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Defeat a Champion",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
        ]
    
    def class_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run as the CLASS",
                data={
                    "CLASS": (self.classes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
        ]
    
    def challenge_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run without equipping any Accessories",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Deal 300+ damage in a single attack",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Kill 6 enemies in a single turn",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Gain 200+ Block in a single fight",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Stack 30+ Bleed on a single target",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Stack 200+ Burn on a single target",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Possess 2000+ Gold at once",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Upgrade a single weapon 5 times",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear all Elite spaces in the Underground Arena",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear every space on the leftmost path for all three Arenas",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Kill an Elite enemy with a rock",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Finish a run with 20 or fewer cards in your deck",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Finish a run with one of your hands free",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat at least one Arena boss without taking damage",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get the crowd to boo you",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Upgrade a weapon at least once in each Arena",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Stun an enemy by shoving them into another enemy",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Drink at least three potions during a single Arena boss fight",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]
        
    def hardcore_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run on Hardcore Mode",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
        ]
    
    @property
    def include_class_objectives(self) -> bool:
        return self.archipelago_options.alina_of_the_arena_include_class_objectives.value
    
    @property
    def include_challenge_objectives(self) -> bool:
        return self.archipelago_options.alina_of_the_arena_include_challenge_objectives.value
        
    @property
    def include_hardcore_difficulty(self) -> bool:
        return self.archipelago_options.alina_of_the_arena_include_hardcore_difficulty.value
    
    @staticmethod
    def classes() -> List[str]:
        return [
            "Slave",
            "Warrior",
            "Mercenary",
            "Bandit",
            "Hunter",
            "Pyromancer",
            "Samurai",
            "Deprived",
        ]


# Archipelago Options
class AlinaOfTheArenaIncludeClassObjectives(Toggle):
    """
    Indicates whether to include objectives that require winning with specific classes.
    """
    display_name = "Alina of the Arena: Include Class Objectives"


class AlinaOfTheArenaIncludeChallengeObjectives(Toggle):
    """
    Indicates whether to include difficult challenge objectives (e.g. high damage, specific feats).
    """
    display_name = "Alina of the Arena: Include Challenge Objectives"


class AlinaOfTheArenaIncludeHardcoreDifficulty(Toggle):
    """
    Indicates whether to include objectives that require playing on Hardcore Mode.
    """
    display_name = "Alina of the Arena: Include Hardcore Difficulty"
