from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CircadianDiceArchipelagoOptions:
    pass


class CircadianDiceGame(Game):
    name = "Circadian Dice"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = CircadianDiceArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Never reroll dice during battle",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never use healing items or abilities",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never sell or discard dice",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Can only use dice with odd face values (1, 3, 5)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Can only use dice with even face values (2, 4, 6)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Maximum inventory of 6 dice (no more than 6 at any time)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never upgrade dice at shops",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must always choose the top option in events when given a choice",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never use support dice (only attack dice allowed)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must discard one die after every boss battle",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="End the run with at least 5 chain faces",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="End the run with at least 6 gold left",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Open all but two chests you encounter on your run",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Use a maximum of one ability per turn",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="End the run with a maximum of 3 fear",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Keep at least 3 attacks but do not use them",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only open chests with keys",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Finish the run with at least 4 stars",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Use at least one relic suggested by the 'Suggest relics' button",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="As long as you have rerolls left, you must reroll",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only buy and install upgrades on your first die",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Your first upgrade must cost 6 or more",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Defeat BOSS",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a full run with CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a full run on DIFFICULTY difficulty",
                data={
                    "DIFFICULTY": (self.difficulties_normal, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a full run with CHARACTER on DIFFICULTY difficulty",
                data={
                    "CHARACTER": (self.characters, 1),
                    "DIFFICULTY": (self.difficulties_normal, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a full run on DIFFICULTY difficulty",
                data={
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a full run with CHARACTER on DIFFICULTY difficulty",
                data={
                    "CHARACTER": (self.characters, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach ACT",
                data={
                    "ACT": (self.acts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a run using only DICE_TYPE dice",
                data={
                    "DICE_TYPE": (self.dice_types, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS without taking damage",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Collect DICE_COUNT different dice in a single run",
                data={
                    "DICE_COUNT": (self.dice_collection_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach floor FLOOR",
                data={
                    "FLOOR": (self.floors, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a battle by dealing exactly DAMAGE damage in one turn",
                data={
                    "DAMAGE": (self.damage_thresholds, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat ENEMY_COUNT enemies in a single run",
                data={
                    "ENEMY_COUNT": (self.enemy_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a run without using any STATUS dice",
                data={
                    "STATUS": (self.status_types, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Upgrade a single die to LEVEL",
                data={
                    "LEVEL": (self.upgrade_levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win CONSECUTIVE_WINS battles in a row without resting",
                data={
                    "CONSECUTIVE_WINS": (self.consecutive_win_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a run with exactly DICE_TOTAL dice in inventory at the end",
                data={
                    "DICE_TOTAL": (self.final_dice_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach GOLD gold in a single run",
                data={
                    "GOLD": (self.gold_thresholds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat a boss with only STARTING_DICE starting dice (no new dice acquired)",
                data={
                    "STARTING_DICE": (self.starting_dice_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a run after visiting every shop node in ACT",
                data={
                    "ACT": (self.acts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete CHARACTER's unlock requirements",
                data={
                    "CHARACTER": (self.unlockable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete SCENARIO scenario",
                data={
                    "SCENARIO": (self.scenarios, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete SCENARIO scenario on DIFFICULTY difficulty",
                data={
                    "SCENARIO": (self.scenarios, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete SCENARIO scenario with CHARACTER",
                data={
                    "SCENARIO": (self.scenarios, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Lady Luck",
            "Grotesque Monster",
            "Inventor",
            "Angry Sun",
            "Midnight",
            "Final Boss",
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Fei",
            "Shan",
            "Selene",
            "Iris",
            "Aurora",
            "Jae",
        ]

    @staticmethod
    def unlockable_characters() -> List[str]:
        return [
            "Selene",
            "Iris",
            "Aurora",
            "Jae",
        ]

    @staticmethod
    def difficulties_normal() -> List[str]:
        return [
            "Normal",
            "Easy",
        ]

    @staticmethod
    def difficulties_hard() -> List[str]:
        return [
            "Hard",
            "Hell",
        ]

    @staticmethod
    def acts() -> List[str]:
        return [
            "Act 1",
            "Act 2",
            "Act 3",
        ]

    @staticmethod
    def dice_types() -> List[str]:
        return [
            "Attack",
            "Defense",
            "Support",
            "Special",
        ]

    @staticmethod
    def dice_collection_counts() -> List[int]:
        return [8, 12, 15]

    @staticmethod
    def floors() -> List[int]:
        return [10, 15, 20, 25]

    @staticmethod
    def damage_thresholds() -> List[int]:
        return [50, 75, 100]

    @staticmethod
    def enemy_counts() -> List[int]:
        return [20, 30, 40]

    @staticmethod
    def status_types() -> List[str]:
        return [
            "Poison",
            "Burn",
            "Freeze",
            "Stun",
        ]

    @staticmethod
    def upgrade_levels() -> List[str]:
        return [
            "Level 2",
            "Level 3",
            "Max Level",
        ]

    @staticmethod
    def consecutive_win_counts() -> List[int]:
        return [5, 8, 10]

    @staticmethod
    def final_dice_counts() -> List[int]:
        return [6, 10, 15]

    @staticmethod
    def gold_thresholds() -> List[int]:
        return [300, 500, 800]

    @staticmethod
    def starting_dice_counts() -> List[int]:
        return [3, 4]

    @staticmethod
    def scenarios() -> List[str]:
        return [
            "Bandit Raid",
            "Vampire Nest",
            "Sunken Ghost Ship",
            "Cursed Forest",
            "Dragon's Lair",
            "Necromancer's Tower",
        ]


# Archipelago Options
# ...
