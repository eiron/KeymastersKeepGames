from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import Toggle, Range


@dataclass
class DiceyDungeonsArchipelagoOptions:
    dicey_dungeons_include_tennis_mod: DiceyDungeonsIncludeTennisMod


class DiceyDungeonsGame(Game):
    name = "Dicey Dungeons"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
    ]

    is_adult_only_or_unrated = False

    options_cls = DiceyDungeonsArchipelagoOptions

    @property
    def include_tennis_mod(self) -> Toggle:
        return self.archipelago_options.dicey_dungeons_include_tennis_mod.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="End a run with at least 10 coins",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Leave at least 3 apples on the floor",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Buy at least 1 item from each shop",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Play on hard mode",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't open any chests on the second floor",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Choose a random rule at least twice",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Do not play anything on your first round of your first fight on the first floor",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Do not use any healing equipment",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Defeat all optional encounters",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Use only purchased equipment, no found equipment",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Use status effects on enemies at least 10 times",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Defeat an opponent without taking any damage",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives = [
            GameObjectiveTemplate(
                label="Complete chapter CHAPTER_NUMBER as CHARACTER",
                data={
                    "CHAPTER_NUMBER": (self.chapters, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a run as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete the Halloween Special as CHARACTER",
                data={
                    "CHARACTER": (self.halloween_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete the Reunion episode as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find and defeat ENEMY_TYPE",
                data={
                    "ENEMY_TYPE": (self.enemies, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat Lady Luck as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]
        
        if self.include_tennis_mod:
            objectives.append(
                GameObjectiveTemplate(
                    label="Win a run in the Tennis mod as CHARACTER",
                    data={
                        "CHARACTER": (self.tennis_mod_characters, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                )
            )
        
        return objectives

    @staticmethod
    def chapters() -> List[int]:
        return [1, 2, 3, 4, 5, 6]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Warrior",
            "Thief",
            "Robot",
            "Inventor",
            "Witch",
            "Jester",
        ]

    @staticmethod
    def halloween_characters() -> List[str]:
        return [
            "Warrior",
            "Inventor",
            "Witch",
        ]

    @staticmethod
    def tennis_mod_characters() -> List[str]:
        return [
            "Warrior",
            "Thief",
            "Robot",
            "Inventor",
            "Witch",
        ]

    @staticmethod
    def enemies() -> List[str]:
        return [
            "Alchemist",
            "Aoife",
            "Audrey",
            "Aurora",
            "Baby Squid",
            "Banshee",
            "Beatrice",
            "Bounty Hunter",
            "Bully",
            "Buster",
            "Cactus",
            "Copycat",
            "Cornelius",
            "Cowboy",
            "Crystalina",
            "Dire Wolf",
            "Drake",
            "Dryad",
            "Fireman",
            "Frog",
            "Gardener",
            "Gargoyle",
            "Handyman",
            "Haunted Jar",
            "Hothead",
            "Keymaster",
            "Kraken",
            "Loud Bird",
            "Madison",
            "Magician",
            "Marshmallow",
            "Mimic",
            "Paper Knight",
            "Pirate",
            "Rat King",
            "Rhino Beetle",
            "Robobot",
            "Rose",
            "Rotten Apple",
            "Scathach",
            "Singer",
            "Skeleton",
            "Slime",
            "Sneezy",
            "Snowman",
            "Sorceress",
            "Space Marine",
            "Stereohead",
            "Sticky Hands",
            "Vacuum",
            "Warlock",
            "Wicker Man",
            "Wisp",
            "Wizard",
            "Wolf Puppy",
            "Yeti",
        ]


# Archipelago Options
class DiceyDungeonsIncludeTennisMod(Toggle):
    """If enabled, adds objectives for the Tennis mod. Requires the mod to be installed."""
    display_name = "Dicey Dungeons Include Tennis Mod"
    default = 0
