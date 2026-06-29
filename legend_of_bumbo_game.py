from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class LegendOfBumboArchipelagoOptions:
    legend_of_bumbo_include_jackpot_objectives: LegendOfBumboIncludeJackpotObjectives
    legend_of_bumbo_include_difficult_character_objectives: LegendOfBumboIncludeDifficultCharacterObjectives


class LegendOfBumboGame(Game):
    name = "The Legend of Bum-Bo"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XSX,
        KeymastersKeepGamePlatforms.AND,
    ]

    is_adult_only_or_unrated = False

    options_cls = LegendOfBumboArchipelagoOptions

    @property
    def include_jackpot_objectives(self) -> bool:
        return self.archipelago_options.legend_of_bumbo_include_jackpot_objectives.value

    @property
    def include_difficult_character_objectives(self) -> bool:
        return self.archipelago_options.legend_of_bumbo_include_difficult_character_objectives.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = []

        constraints += [
            GameObjectiveTemplate(
                label="Do not use the shell game in casinos",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Finish with at least one soul heart",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Match at least five 7 combos",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Skip one spell in an item room",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Do not spend any coins in the second casino",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Flawless a boss",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Finish without upgrading spells in the casino",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Go down to half a heart at least once on the run",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Never have more than 3 poops out at a given time",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
        ]

        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = []

        templates += [
            GameObjectiveTemplate(
                label="Beat the game as CHARACTER",
                data={"CHARACTER": (self.standard_characters, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Beat CHAPTER without taking any damage",
                data={"CHAPTER": (self.chapters, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Get a 7+ combo using TILE tiles",
                data={"TILE": (self.tile_types, 1)},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Beat the game without spending coins at any Wooden Nickel shop",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Beat the game while holding at least COIN_TARGET coins",
                data={"COIN_TARGET": (self.coin_targets, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Beat the game without picking up any spells from Treasure Rooms",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Complete a run without casting any Defense or Puzzle spells",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
        ]

        if self.include_jackpot_objectives:
            templates += [
                GameObjectiveTemplate(
                    label="Win the Jackpot Ending",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Win the Jackpot Ending COUNT times",
                    data={"COUNT": (self.jackpot_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                ),
            ]

        if self.include_difficult_character_objectives:
            templates += [
                GameObjectiveTemplate(
                    label="Beat the game as Bum-Bo the Dead",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Beat the game as Bum-Bo the Lost",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Beat the game as Bum-Bo the Empty",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Beat the game as CHARACTER while holding at least 45 coins",
                    data={"CHARACTER": (self.characters, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
            ]

        return templates

    @staticmethod
    def standard_characters() -> List[str]:
        return [
            "Bum-Bo the Brave",
            "Bum-Bo the Nimble",
            "Bum-Bo the Stout",
            "Bum-Bo the Weird",
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Bum-Bo the Brave",
            "Bum-Bo the Nimble",
            "Bum-Bo the Stout",
            "Bum-Bo the Weird",
            "Bum-Bo the Dead",
            "Bum-Bo the Lost",
            "Bum-Bo the Empty",
        ]

    @staticmethod
    def chapters() -> List[str]:
        return [
            "the Sewers of Dross",
            "the Forlorn Hollow",
            "the Halls of Belial",
            "the Basement",
        ]

    @staticmethod
    def tile_types() -> List[str]:
        return [
            "Tooth",
            "Bone",
            "Pee",
            "Poop",
            "Booger",
            "Heart",
            "Curse",
        ]

    @staticmethod
    def coin_targets() -> List[int]:
        return [30, 45]

    @staticmethod
    def jackpot_counts() -> List[int]:
        return [3, 5, 10]


class LegendOfBumboIncludeJackpotObjectives(DefaultOnToggle):
    """
    Indicates whether to include objectives that require achieving jackpots.
    """

    display_name = "Legend of Bumbo Include Jackpot Objectives"


class LegendOfBumboIncludeDifficultCharacterObjectives(DefaultOnToggle):
    """
    Indicates whether to include objectives that involve difficult characters.
    """

    display_name = "Legend of Bumbo Include Difficult Character Objectives"

