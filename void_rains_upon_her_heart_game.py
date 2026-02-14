from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class VoidRainsUponHerHeartArchipelagoOptions:
    void_rains_upon_her_heart_hearts: VoidRainsUponHerHeartHearts
    void_rains_upon_her_heart_mode: VoidRainsUponHerHeartMode
    void_rains_upon_her_heart_boss_challenges: VoidRainsUponHerHeartBossChallenges
    void_rains_upon_her_heart_difficult_challenges: VoidRainsUponHerHeartDifficultChallenges


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

    @property
    def include_difficult_challenges(self) -> bool:
        return self.archipelago_options.void_rains_upon_her_heart_difficult_challenges.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = list()

        templates.extend([
            GameObjectiveTemplate(label="Play as HEART", data={"HEART": (self.playable_hearts, 1)}),
            GameObjectiveTemplate(label="Never use a panic attack during the entire run", data={}),
            GameObjectiveTemplate(label="Using only basic shots (no panic attacks)", data={}),
            GameObjectiveTemplate(label="Always pick the right-most monster at selection", data={}),
            GameObjectiveTemplate(label="Get at least 3 100% full combos in a single run", data={}),
            GameObjectiveTemplate(label="Spend all panic attacks before the final boss fight", data={}),
            GameObjectiveTemplate(label="Get a 100% full combo while in Focus Mode for an entire fight after the first two fights", data={}),
            GameObjectiveTemplate(label="Get a 100% full combo without using any charge shots", data={}),
            GameObjectiveTemplate(label="Do not use any Active Gifts on odd-numbered fights", data={}),
            GameObjectiveTemplate(label="At least once, lose your 100% full combo in the last segment of the combo bar", data={}),
            GameObjectiveTemplate(label="Spend at least five seconds behind a monster during a battle", data={}),
            GameObjectiveTemplate(label="Collect every basic mote color type in a single run", data={}),
            GameObjectiveTemplate(label="Score at least 2000 motes in a single battle", data={}),
            GameObjectiveTemplate(label="Collect at least 3 power gifts in a single Story run", data={}),
            GameObjectiveTemplate(label="Trigger at least 3 events in a single Story run", data={}),
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
                label="Complete both dream challenges for BOSS",
                data={"BOSS": (self.named_bosses, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Love at least 5 monsters in a single Story run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Love a Shiny variant monster in any mode",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a Story run and defeat a final boss",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete at least 3 dreams",
                data={},
                is_time_consuming=True,
                is_difficult=False,
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
                GameObjectiveTemplate(
                    label="Earn a medal on BOSS in Quickplay",
                    data={"BOSS": (self.named_bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Love BOSS in Quickplay and earn at least a Silver Medal",
                    data={"BOSS": (self.named_bosses, 1)},
                    is_time_consuming=False,
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
                    label="Collect all 6 basic tetrid color types in a single run",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSS without taking damage",
                    data={"BOSS": (self.named_bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSS using only basic shots (no panic attacks)",
                    data={"BOSS": (self.named_bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Love BOSS without using any panic attacks",
                    data={"BOSS": (self.named_bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Very difficult challenges
        if self.include_difficult_challenges:
            templates.extend([
                GameObjectiveTemplate(
                    label="Love BOSS at level 8 or higher in Quickplay",
                    data={"BOSS": (self.named_bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="End an Altered Story run with no power gifts by sacrificing them all to Abyss",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete an Altered Story run with 21 total battles",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
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
            "Alter Heart",
            "Alter Defect",
            "Alter Twin",
            "Alter Devil",
        ]

    @staticmethod
    def named_bosses() -> List[str]:
        return [
            # Shambles (Green Motes)
            "Scrambla",
            "Shy Scrambla",
            "Boiler",
            "Rage Boiler",
            "Knot Knott",
            "Shiny Knot Knott",
            "Blot",
            "Avoidant Blot",
            "Null Blot",
            "Amalga",
            "Calorie",
            "Joule",
            "Shiny Joule",
            "Emerald",
            "Moss",
            "Shamra",
            # Guardians (Red Motes)
            "Rendy",
            "Shiny Rendy",
            "Snowball",
            "Shiny Snowball",
            "Roundsaw",
            "Alter Roundsaw",
            "Null Roundsaw",
            "Lila",
            "Shy Lila",
            "Sandrome",
            "Voladrome",
            "Shanx",
            "Alter Shanx",
            "Ruby",
            "Scarlet",
            "Guardian Soul",
            # Eyeric Glyphs (Yellow Motes)
            "Photoxai",
            "Dendrohai",
            "Hematoren",
            "Ombroah",
            "Lavalin",
            "Heliola",
            "Chemory",
            "Hadesoh",
            "Chionotoh",
            "Astrayo",
            "Monovai",
            "Philolu",
            "Topaz",
            "Dandy",
            "Oudenai",
            # Zaramechs (Blue Motes)
            "Unit Lulu",
            "Null Unit",
            "Prisma",
            "Rage Prisma",
            "Dual Prisma",
            "Syncron",
            "Alter Syncron",
            "Shiny Syncron",
            "Flip Flap",
            "Sentinel 4X",
            "Sentinel 0X",
            "Ventra",
            "Sapphire",
            "Indigo",
            "Default",
            # Glass Flora (Orange Motes)
            "Dot",
            "Glacia",
            "Alter Glacia",
            "Null Glacia",
            "Vitrea",
            "Avoidant Vitrea",
            "Rage Duet",
            "Pearl",
            "Momo",
            "Shy Momo",
            "Shiny Momo",
            "Kiwi",
            "Citrine",
            "Amber",
            "Echo",
            # Veyerals (Purple Motes)
            "Split Veyeral",
            "Burning Veyeral",
            "Voltage Veyeral",
            "Venom Veyeral",
            "Frozen Veyeral",
            "Vibrant Veyeral",
            "Veyeral Quartet",
            "Veyeral Rain",
            "Shiny Veyerals",
            "Storm Veyeral",
            "Molten Veyeral",
            "Blizzard Veyeral",
            "Amethyst",
            "Violet",
            "Forma",
            "The Void",
            "Totaria",
            "Blue Veyeral",
            # Special Monsters
            "Wisp",
            "Anomaly",
            "Shiny Anomaly",
            "Stella",
            "Celestia",
            "Unity",
            "Chroma",
            "Duality",
            "Trinity",
            "Nix Polyps",
            "Ember Polyps",
            "Volt Polyps",
            "Tox Polyps",
            "Nova",
            "Limbo",
        ]

    @staticmethod
    def game_modes_list() -> List[str]:
        return [
            "Story Mode",
            "Quickplay",
            "Altered Story",
            "The Towers",
            "Endless Nightmare",
        ]

    @staticmethod
    def nightmare_waves() -> range:
        return range(1, 5)

    @staticmethod
    def mote_colors() -> List[str]:
        return [
            "Green Motes (Shambles)",
            "Red Motes (Guardians)",
            "Yellow Motes (Eyeric Glyphs)",
            "Blue Motes (Zaramechs)",
            "Orange Motes (Glass Flora)",
            "Purple Motes (Veyerals)",
            "Radiant Motes (Special)",
        ]

    @staticmethod
    def difficulty_levels() -> List[str]:
        return [
            "Mist Rain",
            "Light Rain",
            "Heavy Rain",
            "Torrent Rain",
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


class VoidRainsUponHerHeartDifficultChallenges(Toggle):
    """Include very difficult challenge objectives such as max-level Quickplay, full Altered Story runs, and Abyss sacrifice runs. Disabled by default."""
    display_name = "Very Difficult Challenges"
