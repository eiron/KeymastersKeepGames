from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, OptionList, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ArchipelagoMultiworldRandomizerWithMultiplayerArchipelagoOptions:
    archipelago_multiworld_randomizer_multiplayer_game_selection: ArchipelagoMultiworldRandomizerWithMultiplayerGameSelection
    archipelago_multiworld_randomizer_multiplayer_objective_types: ArchipelagoMultiworldRandomizerWithMultiplayerObjectiveTypes
    archipelago_multiworld_randomizer_multiplayer_bingo_release_always_off: ArchipelagoMultiworldRandomizerWithMultiplayerBingoReleaseAlwaysOff

class ArchipelagoMultiworldRandomizerWithMultiplayerGame(Game):
    name = "Archipelago Multiworld Randomizer with Multiplayer"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = ArchipelagoMultiworldRandomizerWithMultiplayerArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        if self.include_solo_randomizer_objectives:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%] Complete a solo randomizer with GAME",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "GAME": (self.games, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            )

        if self.include_small_multiworld_randomizer_objectives:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiworld randomizer with GAMES",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 2)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiworld randomizer with GAMES",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 3)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
            ])

        if self.include_medium_multiworld_randomizer_objectives:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiworld randomizer with GAMES",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 4)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        if self.include_large_multiworld_randomizer_objectives:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiworld randomizer with GAMES",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 5)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiworld randomizer with GAMES",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 6)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        if self.include_small_multiworld_randomizer_with_apbingo_objectives:
            bingo_label: str = (
                "[Hints: HINT_COST%  Release: RELEASE] Get COUNT bingo(s) on a SIZExSIZE APBingo board in a multiworld "
                "randomizer with GAMES"
            )
            blackout_label: str = (
                "[Hints: HINT_COST%  Release: RELEASE] Blackout a SIZExSIZE APBingo board in a multiworld "
                "randomizer with GAMES"
            )

            if self.apbingo_release_always_off:
                bingo_label = bingo_label.replace("Release: RELEASE", "Release: Off")
                blackout_label = blackout_label.replace("Release: RELEASE", "Release: Off")

            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label=bingo_label,
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 2),
                        "COUNT": (self.bingo_counts, 1),
                        "SIZE": (self.bingo_board_sizes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label=bingo_label,
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 3),
                        "COUNT": (self.bingo_counts, 1),
                        "SIZE": (self.bingo_board_sizes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ])

            if self.include_apbingo_blackout_objectives:
                game_objective_templates.extend([
                    GameObjectiveTemplate(
                        label=blackout_label,
                        data={
                            "HINT_COST": (self.hint_costs, 1),
                            "RELEASE": (self.release, 1),
                            "GAMES": (self.games, 2),
                            "SIZE": (self.bingo_board_sizes, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label=blackout_label,
                        data={
                            "HINT_COST": (self.hint_costs, 1),
                            "RELEASE": (self.release, 1),
                            "GAMES": (self.games, 3),
                            "SIZE": (self.bingo_board_sizes, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

        if self.include_medium_multiworld_randomizer_with_apbingo_objectives:
            bingo_label = (
                "[Hints: HINT_COST%  Release: RELEASE] Get COUNT bingo(s) on a SIZExSIZE APBingo board in a multiworld "
                "randomizer with GAMES"
            )
            blackout_label = (
                "[Hints: HINT_COST%  Release: RELEASE] Blackout a SIZExSIZE APBingo board in a multiworld "
                "randomizer with GAMES"
            )

            if self.apbingo_release_always_off:
                bingo_label = bingo_label.replace("Release: RELEASE", "Release: Off")
                blackout_label = blackout_label.replace("Release: RELEASE", "Release: Off")

            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label=bingo_label,
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 4),
                        "COUNT": (self.bingo_counts, 1),
                        "SIZE": (self.bingo_board_sizes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

            if self.include_apbingo_blackout_objectives:
                game_objective_templates.extend([
                    GameObjectiveTemplate(
                        label=blackout_label,
                        data={
                            "HINT_COST": (self.hint_costs, 1),
                            "RELEASE": (self.release, 1),
                            "GAMES": (self.games, 4),
                            "SIZE": (self.bingo_board_sizes, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

        if self.include_large_multiworld_randomizer_with_apbingo_objectives:
            bingo_label = (
                "[Hints: HINT_COST%  Release: RELEASE] Get COUNT bingo(s) on a SIZExSIZE APBingo board in a multiworld "
                "randomizer with GAMES"
            )
            blackout_label = (
                "[Hints: HINT_COST%  Release: RELEASE] Blackout a SIZExSIZE APBingo board in a multiworld "
                "randomizer with GAMES"
            )

            if self.apbingo_release_always_off:
                bingo_label = bingo_label.replace("Release: RELEASE", "Release: Off")
                blackout_label = blackout_label.replace("Release: RELEASE", "Release: Off")

            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label=bingo_label,
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 5),
                        "COUNT": (self.bingo_counts, 1),
                        "SIZE": (self.bingo_board_sizes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label=bingo_label,
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 6),
                        "COUNT": (self.bingo_counts, 1),
                        "SIZE": (self.bingo_board_sizes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

            if self.include_apbingo_blackout_objectives:
                game_objective_templates.extend([
                    GameObjectiveTemplate(
                        label=blackout_label,
                        data={
                            "HINT_COST": (self.hint_costs, 1),
                            "RELEASE": (self.release, 1),
                            "GAMES": (self.games, 5),
                            "SIZE": (self.bingo_board_sizes, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

        if self.include_small_multiworld_randomizer_with_slotlock_objectives:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiworld randomizer with GAMES using Slotlock",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 2)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiworld randomizer with GAMES using Slotlock",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 3)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
            ])
        
        if self.include_medium_multiworld_randomizer_with_slotlock_objectives:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiworld randomizer with GAMES using Slotlock",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 4)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ])

        if self.include_large_multiworld_randomizer_with_slotlock_objectives:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiworld randomizer with GAMES using Slotlock",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 5)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiworld randomizer with GAMES using Slotlock",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 6)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        if self.include_multiplayer_multiworld_objectives:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiplayer multiworld randomizer with GAME",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAME": (self.games, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiplayer multiworld randomizer with GAMES",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 2)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="[Hints: HINT_COST%  Release: RELEASE] Complete a multiplayer multiworld randomizer with GAMES",
                    data={
                        "HINT_COST": (self.hint_costs, 1),
                        "RELEASE": (self.release, 1),
                        "GAMES": (self.games, 3)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        return game_objective_templates

    @property
    def objective_types(self) -> List[str]:
        return sorted(self.archipelago_options.archipelago_multiworld_randomizer_multiplayer_objective_types.value)

    @property
    def include_solo_randomizer_objectives(self) -> bool:
        return "Solo Randomizer" in self.objective_types

    @property
    def include_small_multiworld_randomizer_objectives(self) -> bool:
        return "Small Multiworld Randomizer" in self.objective_types

    @property
    def include_medium_multiworld_randomizer_objectives(self) -> bool:
        return "Medium Multiworld Randomizer" in self.objective_types

    @property
    def include_large_multiworld_randomizer_objectives(self) -> bool:
        return "Large Multiworld Randomizer" in self.objective_types

    @property
    def include_small_multiworld_randomizer_with_apbingo_objectives(self) -> bool:
        return "Small Multiworld Randomizer with APBingo" in self.objective_types

    @property
    def include_medium_multiworld_randomizer_with_apbingo_objectives(self) -> bool:
        return "Medium Multiworld Randomizer with APBingo" in self.objective_types

    @property
    def include_large_multiworld_randomizer_with_apbingo_objectives(self) -> bool:
        return "Large Multiworld Randomizer with APBingo" in self.objective_types

    @property
    def include_apbingo_blackout_objectives(self) -> bool:
        return "APBingo Blackout" in self.objective_types

    @property
    def include_small_multiworld_randomizer_with_slotlock_objectives(self) -> bool:
        return "Small Multiworld Randomizer with Slotlock" in self.objective_types

    @property
    def include_medium_multiworld_randomizer_with_slotlock_objectives(self) -> bool:
        return "Medium Multiworld Randomizer with Slotlock" in self.objective_types

    @property
    def include_large_multiworld_randomizer_with_slotlock_objectives(self) -> bool:
        return "Large Multiworld Randomizer with Slotlock" in self.objective_types

    @property
    def include_multiplayer_multiworld_objectives(self) -> bool:
        return "Multiplayer Multiworld Randomizer" in self.objective_types
    
    @property
    def apbingo_release_always_off(self) -> bool:
        return self.archipelago_options.archipelago_multiworld_randomizer_multiplayer_bingo_release_always_off.value

    @staticmethod
    def hint_costs() -> List[int]:
        return list(range(0, 26)) + [100]

    @staticmethod
    def number_of_games() -> List[int]:
        return list(range(0, 2))

    @staticmethod
    def release() -> List[str]:
        return ["Off", "On", "On", "On", "On"]

    def games(self) -> List[str]:
        games: List[str] = list(self.archipelago_options.archipelago_multiworld_randomizer_multiplayer_game_selection.value)
        return sorted(games)

    @staticmethod
    def bingo_board_sizes() -> List[int]:
        return list(range(3, 11))

    @staticmethod
    def bingo_counts() -> List[int]:
        return list(range(1, 7))


# Archipelago Options
class ArchipelagoMultiworldRandomizerWithMultiplayerGameSelection(OptionList):
    """
    Defines which APWorlds to select from.

    You can customize this list to your liking. Defaults to all currently supported core games.

    You are allowed to add the same game multiple times here. This will act as a weighted pool.
    """

    display_name = "Archipelago Multiworld Randomizer Game Selection"

    default = [
        "A Hat in Time",
        "A Short Hike",
        "Adventure",
        "APQuest",
        "Aquaria",
        "Blasphemous",
        "Bomb Rush Cyberfunk",
        "Bumper Stickers",
        "Castlevania 64",
        "Castlevania: Circle of the Moon",
        "Celeste 64",
        "Celeste (Open World)",
        "ChecksFinder",
        "Choo-Choo Charles",
        "Dark Souls III",
        "DLC Quest",
        "Donkey Kong Country 3: Dixie Kong's Double Trouble!",
        "DOOM 1993",
        "DOOM II",
        "Factorio",
        "Faxanadu",
        "Final Fantasy",
        "Final Fantasy: Mystic Quest",
        "Heretic",
        "Hollow Knight",
        "Hylics 2",
        "Inscryption",
        "Jak and Daxter: The Precursor Legacy",
        "KINGDOM HEARTS FINAL MIX",
        "KINGDOM HEARTS II FINAL MIX",
        "Kirby's Dream Land 3",
        "Landstalker - The Treasures of King Nole",
        "Lingo",
        "Lufia II: Rise of the Sinistrals",
        "Mario & Luigi: Superstar Saga",
        "Mega Man 2",
        "Mega Man Battle Network 3 Blue",
        "Meritous",
        "Muse Dash",
        "Noita",
        "Old School Runescape",
        "Overcooked! 2",
        "Paint",
        "Pokémon Emerald",
        "Pokémon Red and Blue",
        "Raft",
        "Risk of Rain 2",
        "Saving Princess",
        "Secret of Evermore",
        "shapez",
        "Shivers",
        "Sid Meier's Civilization VI",
        "SMZ3",
        "Sonic Adventure 2: Battle",
        "StarCraft II",
        "Stardew Valley",
        "Subnautica",
        "Sudoku",
        "Super Mario 64",
        "Super Mario Land 2",
        "Super Mario World",
        "Super Mario World 2: Yoshi's Island",
        "Super Metroid",
        "Terraria",
        "The Legend of Zelda",
        "The Legend of Zelda: A Link to the Past",
        "The Legend of Zelda: Link's Awakening DX",
        "The Legend of Zelda: Ocarina of Time",
        "The Legend of Zelda: The Wind Waker",
        "The Messenger",
        "The Witness",
        "Timespinner",
        "TUNIC",
        "Undertale",
        "VVVVVV",
        "Wargroove",
        "Yacht Dice",
        "Yu-Gi-Oh! Ultimate Masters: WCT 2006",
        "Zillion",
    ]


class ArchipelagoMultiworldRandomizerWithMultiplayerObjectiveTypes(OptionSet):
    """
    Defines which types of Archipelago Multiworld Randomizer objectives to use when generating.
    """

    display_name = "Archipelago Multiworld Randomizer Objective Types"

    valid_keys = [
        "Solo Randomizer",
        "Small Multiworld Randomizer",
        "Medium Multiworld Randomizer",
        "Large Multiworld Randomizer",
        "Small Multiworld Randomizer with APBingo",
        "Medium Multiworld Randomizer with APBingo",
        "Large Multiworld Randomizer with APBingo",
        "APBingo Blackout",
        "Small Multiworld Randomizer with Slotlock",
        "Medium Multiworld Randomizer with Slotlock",
        "Large Multiworld Randomizer with Slotlock",
        "Multiplayer Multiworld Randomizer",
    ]

    default = valid_keys

class ArchipelagoMultiworldRandomizerWithMultiplayerBingoReleaseAlwaysOff(DefaultOnToggle):
    """
    Indicates whether to force the release parameter to always be "Off" for APBingo objectives.
    """

    display_name = "Archipelago Multiworld Randomizer Bingo Release Always Off"
