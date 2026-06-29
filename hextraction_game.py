from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class HextractionArchipelagoOptions:
    hextraction_include_advanced_solo_objectives: HextractionIncludeAdvancedSoloObjectives
    hextraction_include_booster_pack_objectives: HextractionIncludeBoosterPackObjectives


class HextractionGame(Game):
    name = "Hextraction"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = HextractionArchipelagoOptions

    @property
    def include_advanced_solo_objectives(self) -> bool:
        return self.archipelago_options.hextraction_include_advanced_solo_objectives.value

    @property
    def include_booster_pack_objectives(self) -> bool:
        return self.archipelago_options.hextraction_include_booster_pack_objectives.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = []

        constraints += [
            GameObjectiveTemplate(
                label="Your hand size is reduced by one on your first turn",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Win on a turn where the ball passes through at least three effect tiles",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Win on a turn where you roll before placing a tile",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Always place your tile before rolling",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Activate the 3-ball rule at least once",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Flip a coin. If it's heads, you must only win in the leftmost goal zone. If it's tails, you must only win in the rightmost goal zone",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Have two balls fall through the same space in the board on the same turn",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Have a ball move from a lower space up to a higher one",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Don't play the same tile twice [if possible]",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
        ]

        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Win a game of Hextraction",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Win a game of Monkey Fight",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Win a game of Monkey Heaven",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Win a game of Puzzle Mode",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Win a game of Hextraction without triggering any effect tiles",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Trigger Break the Loop at least once during a game",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Have a tile successfully voted off the board during a game",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Overwrite a tile during a game",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Have the 3-ball tile destruction rule trigger during a game",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Win a game of Hextraction while Overdrive is active (every slot on the board is filled)",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
        ]

        if self.include_advanced_solo_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete Puzzle Mode in Hard Mode (10 tiles, 5 turns, no hand reload)",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Complete Puzzle Mode in Brutal Mode (reach the finish line on your final turn exactly)",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Complete Puzzle Mode without any tiles being destroyed",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Win a game of Monkey Fight on your very first turn",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Win a game of Monkey Heaven in Extra Hard Mode (you also lose if your ball falls off the side of the board)",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            ])

        if self.include_booster_pack_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Play a Combo tile during a game",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Use a Create effect to play a Virtual tile during a game",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Activate the Backrooms Tile's teleporter during a game",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Activate the Light Switch Tile during a game",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Activate the Rewind Tile during a game",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Activate the Pendulum Tile during a game",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Win a game where the Shrink Ray Tile was activated at least once",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            ])

        return templates


class HextractionIncludeAdvancedSoloObjectives(DefaultOnToggle):
    """Include advanced Puzzle Mode and harder solo mode objectives."""
    display_name = "Hextraction Include Advanced Solo Objectives"


class HextractionIncludeBoosterPackObjectives(DefaultOnToggle):
    """Include objectives for Booster Pack tiles (Hexceptions to the Rule, Time is of the Hexes, Practical F-Hex)."""
    display_name = "Hextraction Include Booster Pack Objectives"
