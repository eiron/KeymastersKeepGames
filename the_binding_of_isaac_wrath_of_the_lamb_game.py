from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet, DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TheBindingOfIsaacWrathOfTheLambArchipelagoOptions:
    the_binding_of_isaac_wrath_of_the_lamb_include_wrath_of_the_lamb_dlc: TheBindingOfIsaacWrathOfTheLambIncludeWrathOfTheLambDLC
    the_binding_of_isaac_wrath_of_the_lamb_include_eternal_edition: TheBindingOfIsaacWrathOfTheLambIncludeEternalEdition
    the_binding_of_isaac_wrath_of_the_lamb_characters: TheBindingOfIsaacWrathOfTheLambCharacters


class TheBindingOfIsaacWrathOfTheLambGame(Game):
    name = "The Binding of Isaac: Wrath of the Lamb"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = TheBindingOfIsaacWrathOfTheLambArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Cannot take any Pills",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use any Cards",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            # Basic in-run achievements
            GameObjectiveTemplate(
                label="Have 7 or more Red Heart Containers at one time",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Hold 55 Coins at one time",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Have 3 or more Soul Hearts at one time",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Blow up 10 Slot Machines in a single run",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect Mom's Eye and any other Mom's item in a single run",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect 2 'dead items' (Bob's Rotten Head, Dead Cat, Max's Head, Tammy's Head) in a single run",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat Mom or Mom's Heart with The Bible",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Kill 4 Horsemen of the Apocalypse in a single run",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect 2 'Common Cold' items (Roid Rage, The Virus, Growth Hormones) in a single run",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat the Basement without taking damage",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat the Caves without taking damage",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat the Depths without taking damage",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat the Womb without taking damage",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Pick up 3 familiars in a single run",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat COUNT of the following specific chapter bosses in one run: CHAPTER_BOSSES",
                data={
                    "COUNT": (self.specific_bosses_range, 1),
                    "CHAPTER_BOSSES": (self.chapter_bosses, 5),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            # Endgame objectives
            GameObjectiveTemplate(
                label="Defeat BOSS as CHARACTER",
                data={
                    "BOSS": (self.bosses, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
        ]

        # Wrath of the Lamb DLC content
        if self.has_wrath_of_the_lamb:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete Challenge #CHALLENGE",
                    data={
                        "CHALLENGE": (self.challenges, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat all 7 Deadly Sins in separate runs",
                    data=dict(),
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Skip two Treasure Rooms and defeat Mom",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Make 2 deals with the devil in a single run",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Transform into Guppy",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Defeat Krampus",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Defeat Ultra Pride",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Eternal Edition content (requires Wrath of the Lamb)
        if self.has_eternal_edition:
            templates.extend([
                GameObjectiveTemplate(
                    label="Gain 7 health upgrades from Eternal Hearts",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Defeat Mom in Hard Mode",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat Mom's Heart/It Lives in Hard Mode",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat Satan in Hard Mode",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat Isaac in the Cathedral in Hard Mode",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete The Chest as CHARACTER in Hard Mode",
                    data={
                        "CHARACTER": (self.characters, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
            ])

        return templates

    @staticmethod
    def specific_bosses_range() -> range:
        return range(2, 4)

    @property
    def has_wrath_of_the_lamb(self) -> bool:
        return self.archipelago_options.the_binding_of_isaac_wrath_of_the_lamb_include_wrath_of_the_lamb_dlc.value

    @property
    def has_eternal_edition(self) -> bool:
        # Eternal Edition requires Wrath of the Lamb
        return self.has_wrath_of_the_lamb and self.archipelago_options.the_binding_of_isaac_wrath_of_the_lamb_include_eternal_edition.value

    def characters(self) -> List[str]:
        chars = list(self.archipelago_options.the_binding_of_isaac_wrath_of_the_lamb_characters.value)
        # Filter out DLC characters if DLC is not enabled
        if not self.has_wrath_of_the_lamb:
            chars = [c for c in chars if c in self.characters_base]
        return chars

    @functools.cached_property
    def characters_base(self) -> List[str]:
        """Characters available in the base game"""
        return [
            "Isaac",
            "Magdalene",
            "Cain",
            "Judas",
            "Eve",
            "Samson",
        ]

    @functools.cached_property
    def characters_wrath_of_the_lamb(self) -> List[str]:
        """Characters added in Wrath of the Lamb DLC"""
        return [
            "???",  # Blue Baby
        ]

    @functools.cached_property
    def bosses_base(self) -> List[str]:
        """Final bosses in the base game"""
        return [
            "Mom",
            "Mom's Heart/It Lives",
        ]

    @functools.cached_property
    def bosses_wrath_of_the_lamb(self) -> List[str]:
        """Final bosses added in Wrath of the Lamb"""
        return [
            "Satan",  # Sheol boss
            "Isaac",  # Cathedral boss
            "???",    # Chest boss
        ]

    def bosses(self) -> List[str]:
        """All available final bosses"""
        bosses = self.bosses_base[:]
        if self.has_wrath_of_the_lamb:
            bosses.extend(self.bosses_wrath_of_the_lamb)
        return bosses

    def chapter_bosses(self) -> List[str]:
        """Regular chapter bosses (not final bosses)"""
        base_bosses = [
            "Monstro",
            "Larry Jr.",
            "Chub",
            "The Duke of Flies",
            "Gemini",
            "Steven",
            "Fistula",
            "Peep",
            "Gurdy Jr.",
            "Gurdy",
            "Loki",
            "Blastocyst",
            "Monstro II",
            "The Haunt",
            "Pin",
            "Famine",
            "Pestilence",
            "War",
            "Death",
            "The Bloat",
            "Lokii",
            "Scolex",
            "Blighted Ovum",
            "Widow",
            "The Carrion Queen",
            "Daddy Long Legs",
            "Teratoma",
            "The Cage",
            "The Hollow",
        ]
        
        wrath_bosses = [
            "Pride",
            "Wrath",
            "Envy",
            "Gluttony",
            "Lust",
            "Greed",
            "Sloth",
            "The Fallen",
            "Headless Horseman",
            "Conquest",
        ]
        
        if self.has_wrath_of_the_lamb:
            return base_bosses + wrath_bosses
        return base_bosses

    def challenges(self) -> List[str]:
        """Challenge names from Wrath of the Lamb"""
        return [
            "1 (Dark Was the Night)",
            "2 (7 Years Bad Luck)",
            "3 (Large Marge)",
            "4 (9 Deaths)",
            "5 (Lord of the Flies)",
            "6 (The Doctors Revenge!)",
            "7 (Meat 4 Evar!)",
            "8 (Spider Boy!)",
            "9 (Isaac Was Good Today)",
            "10 (The Purist)",
        ]


# Archipelago Options
class TheBindingOfIsaacWrathOfTheLambIncludeWrathOfTheLambDLC(DefaultOnToggle):
    """
    Include content from the Wrath of the Lamb DLC expansion.
    """
    display_name = "The Binding of Isaac Wrath of the Lamb Include Wrath of the Lamb DLC"


class TheBindingOfIsaacWrathOfTheLambIncludeEternalEdition(DefaultOnToggle):
    """
    Include content from the Eternal Edition expansion (Hard Mode).
    Requires Wrath of the Lamb DLC to be enabled.
    """
    display_name = "The Binding of Isaac Wrath of the Lamb Include Eternal Edition"


class TheBindingOfIsaacWrathOfTheLambCharacters(OptionSet):
    """
    Indicates which The Binding of Isaac characters can be selected when generating objectives.

    All characters from the base game and Wrath of the Lamb are listed.
    """

    display_name = "The Binding of Isaac Wrath of the Lamb Characters"
    valid_keys = [
        "Isaac",
        "Magdalene",
        "Cain",
        "Judas",
        "???",  # Blue Baby (Wrath of the Lamb)
        "Eve",
        "Samson",
    ]

    default = [
        "Isaac",
        "Magdalene",
        "Cain",
        "Judas",
        "???",
        "Eve",
        "Samson",
    ]
