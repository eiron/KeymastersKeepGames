from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import Toggle, DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DownwellArchipelagoOptions:
    downwell_include_style_objectives: DownwellIncludeStyleObjectives
    downwell_include_hard_mode_objectives: DownwellIncludeHardModeObjectives


class DownwellGame(Game):
    name = "Downwell"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.AND,
    ]

    is_adult_only_or_unrated = False

    options_cls = DownwellArchipelagoOptions

    @property
    def include_style_objectives(self) -> bool:
        return self.archipelago_options.downwell_include_style_objectives.value

    @property
    def include_hard_mode_objectives(self) -> bool:
        return self.archipelago_options.downwell_include_hard_mode_objectives.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = []

        constraints += [
            GameObjectiveTemplate(
                label="On 1-1, do not shoot your gunboots",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Hoard at least GEM_COUNT gems before the boss",
                data={"GEM_COUNT": (self.high_gem_targets, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Beat a whole area in under SPEEDRUN_TIME",
                data={"SPEEDRUN_TIME": (self.speedrun_times, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Beat STAGE_COUNT separate stages with full health",
                data={"STAGE_COUNT": (self.stage_counts, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Get a COMBO_COUNT combo outside of Limbo",
                data={"COMBO_COUNT": (self.combo_targets, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Beat a stage without killing enemies by shooting",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="For your first UPGRADE_COUNT upgrades, always pick the left option",
                data={"UPGRADE_COUNT": (self.early_upgrade_counts, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Avoid descriptive upgrades when possible",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Never pick up lasers",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Use the Zennyan color palette",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Have an enemy die from a side room's time void",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
        ]

        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Beat the game as STYLE",
                data={"STYLE": (self.styles, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Meet the Smiling Jelly as STYLE",
                data={"STYLE": (self.styles, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Beat 1-2 with fewer than GEM_COUNT gems",
                data={"GEM_COUNT": (self.low_gem_caps, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Achieve a combo of N kills",
                data={"N": (self.combo_objective_counts, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Beat WORLD without taking any damage",
                data={"WORLD": (self.worlds, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Beat a stage without shooting your gunboots at all",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Beat a stage without killing any enemies",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Beat a stage without entering any safe zone",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Survive the Aquifer without your breath reaching zero",
                data={},
                is_time_consuming=True,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Collect N gems in a single run",
                data={"N": (self.gem_collection_targets, 1)},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Complete a Tomato Run (reach the boss without entering any safe zone)",
                data={},
                is_time_consuming=True,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Beat the game using only the WEAPON",
                data={"WEAPON": (self.weapons, 1)},
                is_time_consuming=True,
                is_difficult=True,
            ),
        ]

        if self.include_style_objectives:
            templates.append(
                GameObjectiveTemplate(
                    label="Beat the game and meet the Smiling Jelly as STYLE in separate runs",
                    data={"STYLE": (self.styles, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
            )

        if self.include_hard_mode_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Beat 2-1 on Hard Mode as STYLE",
                    data={"STYLE": (self.styles, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Beat WORLD on Hard Mode",
                    data={"WORLD": (self.worlds, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Beat the game on Hard Mode as STYLE",
                    data={"STYLE": (self.styles, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
            ])

        return templates

    @staticmethod
    def styles() -> List[str]:
        return [
            "Usual Style",
            "Arm Spin Style",
            "Boulder Style",
            "Levitate Style",
            "Handstand Style",
        ]

    @staticmethod
    def worlds() -> List[str]:
        return [
            "the Caverns",
            "the Catacombs",
            "the Aquifer",
            "Limbo",
        ]

    @staticmethod
    def weapons() -> List[str]:
        return [
            "Machine Gun",
            "Noppy",
            "Laser",
            "Shotgun",
            "Burst",
            "Triple",
            "Puncher",
        ]

    @staticmethod
    def combo_objective_counts() -> List[int]:
        return [10, 30, 100]

    @staticmethod
    def gem_collection_targets() -> List[str]:
        return [
            "3,000",
            "5,000",
        ]

    @staticmethod
    def high_gem_targets() -> List[str]:
        return ["2222"]

    @staticmethod
    def low_gem_caps() -> List[str]:
        return ["222"]

    @staticmethod
    def speedrun_times() -> List[str]:
        return ["02:22:22"]

    @staticmethod
    def stage_counts() -> List[str]:
        return ["3"]

    @staticmethod
    def combo_targets() -> List[str]:
        return ["30"]

    @staticmethod
    def early_upgrade_counts() -> List[str]:
        return ["5"]


class DownwellIncludeStyleObjectives(DefaultOnToggle):
    """Include style-focused objectives from the card set."""
    display_name = "Downwell Include Style Objectives"


class DownwellIncludeHardModeObjectives(Toggle):
    """Include Hard Mode objective variants."""
    display_name = "Downwell Include Hard Mode Objectives"
    default = 0
