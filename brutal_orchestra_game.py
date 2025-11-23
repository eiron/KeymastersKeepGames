from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BrutalOrchestraArchipelagoOptions:
    pass


class BrutalOrchestraGame(Game):
    name = "Brutal Orchestra"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = BrutalOrchestraArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="No using items during combat",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot skip enemy encounters",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="No healing between fights",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use support abilities",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must keep first party member alive throughout the run",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Do not let any of your party members die in the first two acts",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Kill a boss with a 'Slap'",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Buy out an entire item shop then discard at least three of the items",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Get Nowak's Refresh ability to trigger at least once",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Get a non-Nowak party member down to 1HP and then heal them to full HP in the same fight",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Win a fight without personally dealing any direct damage to any enemies",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Kill Nowak at least 10 times during a run",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Every time you take direct damage from an enemy for the first time in combat, you must call somebody and tell them you love them. You cannot elaborate further until you have finished the run",
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
                label="Complete a run with PARTY_MEMBER in your party",
                data={
                    "PARTY_MEMBER": (self.party_members, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat ENEMY_COUNT enemies in a single run",
                data={
                    "ENEMY_COUNT": (self.enemy_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a run using only PARTY_SIZE party members",
                data={
                    "PARTY_SIZE": (self.party_sizes, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win BATTLE_COUNT battles without losing any party members",
                data={
                    "BATTLE_COUNT": (self.battle_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat a boss with CONDITION condition",
                data={
                    "CONDITION": (self.win_conditions, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete ZONE",
                data={
                    "ZONE": (self.zones, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Unlock PARTY_MEMBER",
                data={
                    "PARTY_MEMBER": (self.unlockable_members, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a DIFFICULTY run with a full random party",
                data={
                    "DIFFICULTY": (self.difficulties_normal, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a DIFFICULTY run with a full random party",
                data={
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a DIFFICULTY run with a COLOUR character in your party",
                data={
                    "DIFFICULTY": (self.difficulties_normal, 1),
                    "COLOUR": (self.colors, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a DIFFICULTY run with a COLOUR character in your party",
                data={
                    "DIFFICULTY": (self.difficulties_hard, 1),
                    "COLOUR": (self.colors, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat the final boss with Mung in your party",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def party_members() -> List[str]:
        return [
            "Boyle",
            "Hans",
            "Anton",
            "Splig",
            "Pearl",
            "Burnout",
            "Fennec",
            "Thype",
            "Griffin",
            "Arnold",
            "Dimitri",
            "LongLiver",
            "Clive",
            "Kleiver",
            "Cranes",
            "Agon",
            "Rags",
            "Smoke Stacks",
            "Leviat",
            "Bimini",
            "Gospel",
            "Mordrake",
        ]

    @staticmethod
    def unlockable_members() -> List[str]:
        return [
            "Anton",
            "Splig",
            "Pearl",
            "Burnout",
            "Fennec",
            "Thype",
            "Griffin",
            "Arnold",
            "Dimitri",
            "LongLiver",
            "Clive",
            "Kleiver",
            "Cranes",
            "Agon",
            "Rags",
            "Smoke Stacks",
            "Leviat",
            "Bimini",
            "Gospel",
            "Mordrake",
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Boomie",
            "The Shack Dweller",
            "Mad Taxi",
            "The Witness",
            "The Soprano",
            "The Broken Wheel",
            "The Conductor",
        ]

    @staticmethod
    def zones() -> List[str]:
        return [
            "The Outskirts",
            "The Terrace",
            "Downtown",
            "The Stage",
            "The Finale",
        ]

    @staticmethod
    def difficulties_normal() -> List[str]:
        return [
            "Normal",
        ]

    @staticmethod
    def difficulties_hard() -> List[str]:
        return [
            "Hard",
            "Hellmode",
        ]

    @staticmethod
    def colors() -> List[str]:
        return [
            "Red",
            "Blue",
            "Purple",
        ]

    @staticmethod
    def win_conditions() -> List[str]:
        return [
            "no party members below 50% health",
            "in under 5 turns",
            "without using items",
            "with only 3 party members",
            "without anyone dying",
        ]

    @staticmethod
    def party_sizes() -> List[int]:
        return [2, 3, 4]

    @staticmethod
    def battle_counts() -> range:
        return range(5, 16, 5)

    @staticmethod
    def enemy_counts() -> range:
        return range(20, 61, 20)


# Archipelago Options
# ...
