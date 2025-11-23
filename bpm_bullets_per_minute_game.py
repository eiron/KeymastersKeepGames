from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BPMBulletsPerMinuteArchipelagoOptions:
    pass


class BPMBulletsPerMinuteGame(Game):
    name = "BPM: BULLETS PER MINUTE"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = BPMBulletsPerMinuteArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="No ultimate ability usage",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="No health pickups allowed",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use any special weapons (only starter weapon)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot purchase any items from shops",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must maintain perfect rhythm (no missed beats)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Leave one item slot empty",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Skip all Altars on a floor",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Skip a Treasure Room",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never buy items from the two rightmost pedestals at Huggin's Shop",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never buy consumables from the front pedestal at Muninn's Armory",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never buy weapons from the leftmost pedestal at Muninn's Armory",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Turn on Strict Rhythm Timing",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a run on DIFFICULTY as CHARACTER",
                data={
                    "DIFFICULTY": (self.difficulties_easy_medium, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a run on DIFFICULTY as CHARACTER",
                data={
                    "DIFFICULTY": (self.difficulties_hard_hellish, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS as CHARACTER",
                data={
                    "BOSS": (self.bosses, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach DUNGEON_LEVEL without dying",
                data={
                    "DUNGEON_LEVEL": (self.dungeon_levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a full run using only WEAPON_TYPE weapons",
                data={
                    "WEAPON_TYPE": (self.weapon_types, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Achieve COIN_COUNT coins in a single run",
                data={
                    "COIN_COUNT": (self.coin_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete ROOM_COUNT rooms without taking damage",
                data={
                    "ROOM_COUNT": (self.room_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat ENEMY_COUNT ENEMY enemies in a single run",
                data={
                    "ENEMY_COUNT": (self.enemy_counts, 1),
                    "ENEMY": (self.common_enemies, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect ABILITY_COUNT abilities in a single run",
                data={
                    "ABILITY_COUNT": (self.ability_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a run with ITEM_RESTRICTION item restriction",
                data={
                    "ITEM_RESTRICTION": (self.item_restrictions, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Clear DUNGEON_LEVEL on DIFFICULTY difficulty",
                data={
                    "DUNGEON_LEVEL": (self.dungeon_levels, 1),
                    "DIFFICULTY": (self.difficulties_easy_medium, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear DUNGEON_LEVEL on DIFFICULTY difficulty",
                data={
                    "DUNGEON_LEVEL": (self.dungeon_levels, 1),
                    "DIFFICULTY": (self.difficulties_hard_hellish, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Göll",
            "Freyr",
            "Hildr",
            "Njord",
            "Yrsa",
            "Rún",
            "Huginn",
            "Muninn",
            "Njal",
            "Stig",
        ]

    @staticmethod
    def difficulties_easy_medium() -> List[str]:
        return [
            "Easy",
            "Medium",
        ]

    @staticmethod
    def difficulties_hard_hellish() -> List[str]:
        return [
            "Hard",
            "Hellish",
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Draugr",
            "Hel",
            "Surt",
            "Nidhogg",
            "Yggdrasil Guardian",
            "Fenrir",
            "Jormungandr",
        ]

    @staticmethod
    def dungeon_levels() -> List[str]:
        return [
            "Asgard (Floor 1)",
            "Asgard (Floor 2)",
            "Asgard (Floor 3)",
            "Vanaheim (Floor 4)",
            "Vanaheim (Floor 5)",
            "Helheim (Floor 6)",
            "Helheim (Floor 7)",
        ]

    @staticmethod
    def weapon_types() -> List[str]:
        return [
            "Pistol",
            "Shotgun",
            "Revolver",
            "Grenade Launcher",
            "Rocket Launcher",
        ]

    @staticmethod
    def common_enemies() -> List[str]:
        return [
            "Skeleton Warrior",
            "Fire Demon",
            "Ice Wraith",
            "Dark Valkyrie",
            "Hell Hound",
            "Draugr Archer",
            "Berserker",
        ]

    @staticmethod
    def item_restrictions() -> List[str]:
        return [
            "no damage upgrades",
            "no armor upgrades",
            "no ultimate abilities",
            "no healing items",
            "no stat boosts",
        ]

    @staticmethod
    def coin_counts() -> range:
        return range(100, 500, 100)

    @staticmethod
    def room_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def enemy_counts() -> range:
        return range(50, 200, 50)

    @staticmethod
    def ability_counts() -> range:
        return range(3, 10)


# Archipelago Options
# ...
