from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class VoidRainsUponHerHeartArchipelagoOptions:
    void_rains_upon_her_heart_hearts: VoidRainsUponHerHeartHearts
    void_rains_upon_her_heart_mode: VoidRainsUponHerHeartMode
    void_rains_upon_her_heart_boss_challenges: VoidRainsUponHerHeartBossChallenges


class VoidRainsUponHerHeartGame(Game):
    name = "The Void Rains Upon Her Heart"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = VoidRainsUponHerHeartArchipelagoOptions

    # Properties
    @property
    def include_hearts(self) -> bool:
        return self.archipelago_options.void_rains_upon_her_heart_hearts.value

    @property
    def include_modes(self) -> bool:
        return self.archipelago_options.void_rains_upon_her_heart_mode.value

    @property
    def include_boss_challenges(self) -> bool:
        return self.archipelago_options.void_rains_upon_her_heart_boss_challenges.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = list()

        templates.extend([
            GameObjectiveTemplate(label="Defeat BOSS without taking damage", data={"BOSS": (self.named_bosses, 1)}),
            GameObjectiveTemplate(label="Defeat BOSS using only basic shots (no panic attacks)", data={"BOSS": (self.named_bosses, 1)}),
            GameObjectiveTemplate(label="Defeat 5 randomly selected bosses in a single run without restarting", data={}),
            GameObjectiveTemplate(label="Collect 3 different Upgrade Gifts in a single run", data={}),
            GameObjectiveTemplate(label="Reach wave 10 in Endless Nightmare mode", data={}),
            GameObjectiveTemplate(label="Defeat 2 Shiny variant bosses", data={}),
            GameObjectiveTemplate(label="Complete a full boss run using only power gifts", data={}),
            GameObjectiveTemplate(label="Never panic attack during an entire run", data={}),
            GameObjectiveTemplate(label="Accumulate 50 total motes of a single color type", data={}),
            GameObjectiveTemplate(label="Defeat BOSS back-to-back in the same run", data={"BOSS": (self.named_bosses, 2)}),
            GameObjectiveTemplate(label="Complete a Quickplay run from start to finish", data={}),
            GameObjectiveTemplate(label="Defeat The Void and reach the true ending", data={}),
            GameObjectiveTemplate(label="Play a complete run as HEART", data={"HEART": (self.playable_hearts, 1)}),
            GameObjectiveTemplate(label="Defeat BOSS in sequence without healing between battles", data={"BOSS": (self.named_bosses, 3)}),
            GameObjectiveTemplate(label="Collect every type of mote color in a single run", data={}),
            GameObjectiveTemplate(label="Always pick the right-most boss", data={}),
            GameObjectiveTemplate(label="Get at least 3 100% full combos", data={}),
            GameObjectiveTemplate(label="Complete at least six challenges", data={}),
            GameObjectiveTemplate(label="Complete 2 cycles of Endless Nightmare", data={}),
            GameObjectiveTemplate(label="Spend all possible panic attacks before going into the final boss fight", data={}),
            GameObjectiveTemplate(label="Get a 100% full combo while in Focus Mode for an entire fight after the first two fights", data={}),
            GameObjectiveTemplate(label="Get a 100% full combo without using any charge shots", data={}),
            GameObjectiveTemplate(label="Do not use any Active Gifts on odd-numbered fights", data={}),
            GameObjectiveTemplate(label="At least once, lose your 100% full combo in the last segment of the combo bar", data={}),
            GameObjectiveTemplate(label="Spend at least five seconds behind a boss", data={}),
            GameObjectiveTemplate(label="End a run with no power gifts, by giving them all away before the final boss", data={}),
            GameObjectiveTemplate(label="Complete a run with at least 21 total battles by extending the run with events", data={}),
        ])

        return templates

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = list()

        # Boss progression objectives
        templates.extend([
            GameObjectiveTemplate(
                label="Defeat the following bosses: BOSS",
                data={"BOSS": (self.named_bosses, 2)},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Defeat the following bosses: BOSS",
                data={"BOSS": (self.named_bosses, 3)},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete 3 dream challenges for BOSS",
                data={"BOSS": (self.named_bosses, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
        ])

        # Heart character objectives
        if self.include_hearts:
            templates.extend([
                GameObjectiveTemplate(
                    label="Play a full run as HEART",
                    data={"HEART": (self.playable_hearts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat the Void using HEART as your character",
                    data={"HEART": (self.playable_hearts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete story progression with HEART",
                    data={"HEART": (self.playable_hearts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Win a Story run on DIFFICULTY as HEART",
                    data={"DIFFICULTY": (self.difficulty_levels, 1), "HEART": (self.playable_hearts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
            ])

        # Game mode objectives
        if self.include_modes:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete MODE successfully",
                    data={"MODE": (self.game_modes_list, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Reach wave NUM in Endless Nightmare mode",
                    data={"NUM": (self.nightmare_waves, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Boss challenge objectives
        if self.include_boss_challenges:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete 2 dream challenges across different bosses",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSS at high difficulty",
                    data={"BOSS": (self.named_bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Collect all 7 mote color types",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        return templates

    # Static data providers

    @staticmethod
    def playable_hearts() -> List[str]:
        return [
            "Her Heart",
            "Defect",
            "Twin Heart",
            "The Devil",
            "Her Heart Alter",
            "Defect Alter",
            "Twin Heart Alter",
            "The Devil Alter",
        ]

    @staticmethod
    def named_bosses() -> List[str]:
        return [
            "Rendy",
            "Roundsaw",
            "Lila",
            "Shanx",
            "Stella",
            "Chroma",
            "Trinity",
            "Anomaly",
            "Vex",
            "Grimace",
            "Spinal",
            "Prism",
            "Nexus",
            "Echo",
            "Cyclone",
            "Radiant",
            "Vesper",
            "Torrent",
            "Hollow",
            "Surge",
            "Void Guardian",
            "The Void",
        ]

    @staticmethod
    def game_modes_list() -> List[str]:
        return [
            "Story Mode",
            "Quickplay",
            "Endless Nightmare",
            "The Towers",
            "Campaign",
        ]

    @staticmethod
    def nightmare_waves() -> range:
        return range(5, 51, 5)

    @staticmethod
    def mote_colors() -> List[str]:
        return [
            "Green Motes (Shambles)",
            "Red Motes (Guardians)",
            "Yellow Motes (Eyeric Glyphs)",
            "Blue Motes (Zaramechs)",
            "Orange Motes (Glass Flora)",
            "Purple Motes (Veyerals)",
            "Rainbow Motes (Special)",
        ]

    @staticmethod
    def difficulty_levels() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
            "Nightmare",
            "Despair",
        ]


# Archipelago Options
class VoidRainsUponHerHeartHearts(DefaultOnToggle):
    """Include objectives related to unlocking and playing as different heart characters."""
    display_name = "Heart Unlocks & Character Play"


class VoidRainsUponHerHeartMode(DefaultOnToggle):
    """Include objectives related to unlocking and completing different game modes."""
    display_name = "Game Modes"


class VoidRainsUponHerHeartBossChallenges(DefaultOnToggle):
    """Include objectives related to boss challenges and dream completions."""
    display_name = "Boss Challenges & Dreams"
