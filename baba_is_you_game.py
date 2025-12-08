from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle, DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BabaIsYouArchipelagoOptions:
    baba_is_you_include_world_objectives: BabaIsYouIncludeWorldObjectives
    baba_is_you_include_transformation_objectives: BabaIsYouIncludeTransformationObjectives
    baba_is_you_include_custom_level_objectives: BabaIsYouIncludeCustomLevelObjectives


class BabaIsYouGame(Game):
    name = "Baba Is You"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.AND,
    ]

    is_adult_only_or_unrated = False

    options_cls = BabaIsYouArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Don't use the 'Undo' button",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't use the 'Restart' button (Exit to map to retry)",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        objectives += self.base_objectives()
        
        if self.include_world_objectives:
            objectives += self.world_objectives()
            
        if self.include_transformation_objectives:
            objectives += self.transformation_objectives()

        if self.include_custom_level_objectives:
            objectives += self.custom_level_objectives()
        
        return objectives
    
    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete 3 levels",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Complete a level with 'BABA IS YOU'",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
             GameObjectiveTemplate(
                label="Complete a level by reaching the FLAG",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]
    
    def world_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a level in WORLD",
                data={
                    "WORLD": (self.worlds, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
             GameObjectiveTemplate(
                label="Complete 3 levels in WORLD",
                data={
                    "WORLD": (self.worlds, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
        ]

    def transformation_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a level where CHARACTER is YOU",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
        ]

    def custom_level_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete custom level LEVEL_CODE (Attempt in < 15m)",
                data={
                    "LEVEL_CODE": (self.custom_levels, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
        ]
    
    @property
    def include_world_objectives(self) -> bool:
        return self.archipelago_options.baba_is_you_include_world_objectives.value
    
    @property
    def include_transformation_objectives(self) -> bool:
        return self.archipelago_options.baba_is_you_include_transformation_objectives.value

    @property
    def include_custom_level_objectives(self) -> bool:
        return self.archipelago_options.baba_is_you_include_custom_level_objectives.value
    
    @staticmethod
    def worlds() -> List[str]:
        return [
            "The Lake",
            "Solitary Island",
            "Temple Ruins",
            "Forest of Fall",
            "Deep Forest",
            "Rocket Trip",
            "Flower Garden",
            "Volcanic Cavern",
            "Chasm",
            "Mountaintop",
            "Meta",
            "Center",
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "BABA",
            "KEKE",
            "ME",
            "IT",
            "FOFO",
            "JIJI",
        ]

    @staticmethod
    def custom_levels() -> List[str]:
        return [
            "DHKX-G4ZP",
            "9GYD-KIQH",
            "7719-HWJZ",
            "GZLB-Z79F",
            "G4QV-7XT3",
            "3QV3-2ZN3",
            "6JHR-N84E",
            "2GW9-UIWK",
            "6QRN-1AH2",
            "874H-B47J",
            "CK2K-PQJF",
            "68NL-1CZM",
            "9XAN-P8WL",
            "Y71M-NIXK",
            "BXET-3RZY",
            "34ZH-X6WX",
            "VCA7-1FPZ",
            "RRF7-WFNA",
            "9H77-AUWD",
            "WIQX-QJ7K",
            "U23B-Y9NK",
            "3GIU-JWY7",
            "61QR-FVY4",
            "UPFH-IZJB",
            "ZAYF-FLWF",
            "BQ64-TM1A",
            "F843-AIP8",
            "9AXN-AAGW",
            "YXYT-DKNT",
            "7ZWP-77V2",
            "YM89-W9L7",
            "LDYL-C9GU",
            "AI9A-F4VR",
            "N3CV-YZA8",
            "C2AL-YFQG",
            "K7BJ-PYQT",
            "EUK2-Q3HK",
            "W4PF-9JHQ",
            "WA3C-PCQZ",
            "1HI4-NFT9",
        ]


# Archipelago Options
class BabaIsYouIncludeWorldObjectives(DefaultOnToggle):
    """
    Indicates whether to include objectives that require completing levels in specific worlds.
    """
    display_name = "Baba Is You: Include World Objectives"


class BabaIsYouIncludeTransformationObjectives(DefaultOnToggle):
    """
    Indicates whether to include objectives that require winning as specific characters.
    """
    display_name = "Baba Is You: Include Transformation Objectives"


class BabaIsYouIncludeCustomLevelObjectives(Toggle):
    """
    Indicates whether to include objectives that require completing specific custom levels.
    """
    display_name = "Baba Is You: Include Custom Level Objectives"
