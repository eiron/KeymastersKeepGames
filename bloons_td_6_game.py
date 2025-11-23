from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BloonsTD6ArchipelagoOptions:
    pass


class BloonsTD6Game(Game):
    name = "Bloons TD 6"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = BloonsTD6ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Cannot use Heroes",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use Tier 5 Upgrades",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Disable all Monkey Knowledge",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot sell any towers",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Maximum of 10 towers placed",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use Powers or Insta-Monkeys",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only use one tower type (can place multiple of that type)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use any Magic Monkeys",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use any Military Monkeys",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must start with a Banana Farm as your first tower",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Have at least six towers within range of a single Monkey Village",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Include exactly one Ninja Monkey - no more, no less",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't place any towers along the last third of the path",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Place at least five Heli Pilots and/or Dartling Gunners, keeping all their targeting options set to Normal/Follow Mouse",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="During the first 3 Rounds, have only 1 tower on screen",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete LEVEL on Normal Mode without using PRIMARY, MILITARY, MAGIC, SUPPORT",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                    "PRIMARY": (self.monkeys_primary, 1),
                    "MILITARY": (self.monkeys_military, 1),
                    "MAGIC": (self.monkeys_magic, 1),
                    "SUPPORT": (self.monkeys_support, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Hard Mode without using PRIMARY, MILITARY, MAGIC, SUPPORT",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                    "PRIMARY": (self.monkeys_primary, 1),
                    "MILITARY": (self.monkeys_military, 1),
                    "MAGIC": (self.monkeys_magic, 1),
                    "SUPPORT": (self.monkeys_support, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Normal Mode without using PRIMARY, MILITARY, MAGIC, SUPPORT",
                data={
                    "LEVEL": (self.levels_intermediate, 1),
                    "PRIMARY": (self.monkeys_primary, 1),
                    "MILITARY": (self.monkeys_military, 1),
                    "MAGIC": (self.monkeys_magic, 1),
                    "SUPPORT": (self.monkeys_support, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Hard Mode without using PRIMARY, MILITARY, MAGIC, SUPPORT",
                data={
                    "LEVEL": (self.levels_intermediate, 1),
                    "PRIMARY": (self.monkeys_primary, 1),
                    "MILITARY": (self.monkeys_military, 1),
                    "MAGIC": (self.monkeys_magic, 1),
                    "SUPPORT": (self.monkeys_support, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Normal Mode without using PRIMARY, MILITARY, MAGIC, SUPPORT",
                data={
                    "LEVEL": (self.levels_advanced, 1),
                    "PRIMARY": (self.monkeys_primary, 1),
                    "MILITARY": (self.monkeys_military, 1),
                    "MAGIC": (self.monkeys_magic, 1),
                    "SUPPORT": (self.monkeys_support, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Hard Mode without using PRIMARY, MILITARY, MAGIC, SUPPORT",
                data={
                    "LEVEL": (self.levels_advanced, 1),
                    "PRIMARY": (self.monkeys_primary, 1),
                    "MILITARY": (self.monkeys_military, 1),
                    "MAGIC": (self.monkeys_magic, 1),
                    "SUPPORT": (self.monkeys_support, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Normal Mode without using PRIMARY, MILITARY, MAGIC, SUPPORT",
                data={
                    "LEVEL": (self.levels_expert, 1),
                    "PRIMARY": (self.monkeys_primary, 1),
                    "MILITARY": (self.monkeys_military, 1),
                    "MAGIC": (self.monkeys_magic, 1),
                    "SUPPORT": (self.monkeys_support, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat LEVEL on Normal Mode using only MONKEY (disable Monkey Knowledge)",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                    "MONKEY": (self.all_monkeys, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat LEVEL on Hard Mode using only MONKEY (disable Monkey Knowledge)",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                    "MONKEY": (self.all_monkeys, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat LEVEL on Normal Mode using only SQUAD",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                    "SQUAD": (self.squads, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat LEVEL on Hard Mode using only SQUAD",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                    "SQUAD": (self.squads, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Normal Mode using only PRIMARY, MILITARY, MAGIC, SUPPORT",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                    "PRIMARY": (self.monkeys_primary, 1),
                    "MILITARY": (self.monkeys_military, 1),
                    "MAGIC": (self.monkeys_magic, 1),
                    "SUPPORT": (self.monkeys_support, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Hard Mode using only PRIMARY, MILITARY, MAGIC, SUPPORT",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                    "PRIMARY": (self.monkeys_primary, 1),
                    "MILITARY": (self.monkeys_military, 1),
                    "MAGIC": (self.monkeys_magic, 1),
                    "SUPPORT": (self.monkeys_support, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Normal Mode using only non-Monkey towers (including Engineer)",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Hard Mode using only non-Monkey towers (including Engineer)",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Normal Mode using only Dart-Shooting Towers",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Hard Mode using only Dart-Shooting Towers",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Normal Mode using only Non-Dart-Projectile-Shooting Towers",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on Hard Mode using only Non-Dart-Projectile-Shooting Towers",
                data={
                    "LEVEL": (self.levels_beginner, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Fully upgrade one of the Super Monkey's paths",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    @staticmethod
    def monkeys_primary() -> List[str]:
        return [
            "Dart Monkey",
            "Boomerang",
            "Bomb Shooter",
            "Tack Shooter",
            "Ice Monkey",
            "Glue Gunner",
        ]

    @staticmethod
    def monkeys_military() -> List[str]:
        return [
            "Sniper Monkey",
            "Monkey Sub",
            "Monkey Buccaneer",
            "Monkey Ace",
            "Heli Pilot",
            "Mortar Monkey",
            "Dartling Gunner",
        ]

    @staticmethod
    def monkeys_magic() -> List[str]:
        return [
            "Wizard Monkey",
            "Super Monkey",
            "Ninja Monkey",
            "Alchemist",
            "Druid",
            "Mermonkey",
        ]

    @staticmethod
    def monkeys_support() -> List[str]:
        return [
            "Banana Farm",
            "Spike Factory",
            "Monkey Village",
            "Engineer Monkey",
            "Beast Handler",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Normal Mode",
            "Hard Mode",
        ]

    def all_monkeys(self) -> List[str]:
        return (
            self.monkeys_primary()
            + self.monkeys_military()
            + self.monkeys_magic()
            + self.monkeys_support()
        )

    @staticmethod
    def squads() -> List[str]:
        return [
            "Primary Monkeys",
            "Military Monkeys",
            "Magic Monkeys",
            "Support Monkeys",
        ]

    @staticmethod
    def levels_beginner() -> List[str]:
        return [
            "Monkey Meadow",
            "Tree Stump",
            "Scrapyard",
            "Alpine Run",
            "Hedge",
            "In The Loop",
            "Middle Of The Road",
            "Tinkerton",
            "Town Center",
            "One Two Tree",
            "The Cabin",
            "Resort",
            "Skates",
            "Lotus Island",
            "Candy Falls",
            "Winter Park",
            "Carved",
            "Park Path",
            "Frozen Over",
            "Cubism",
            "Four Circles",
            "End Of The Road",
            "Logs",
        ]

    @staticmethod
    def levels_intermediate() -> List[str]:
        return [
            "Kartsndarts",
            "Moon Landing",
            "Luminous Cove",
            "Sulfur Springs",
            "Water Park",
            "Polyphemus",
            "Covered Garden",
            "Quarry",
            "Quiet Street",
            "Bloonarius Prime",
            "Balance",
            "Encrypted",
            "Bazaar",
            "Adora's Temple",
            "Spring Spring",
            "Haunted",
            "Downstream",
            "Firing Range",
            "Cracked",
            "Streambed",
            "Chutes",
            "Rake",
            "Spice Islands",
        ]

    @staticmethod
    def levels_advanced() -> List[str]:
        return [
            "Last Resort",
            "Ancient Portal",
            "Castle Revenge",
            "Dark Path",
            "Erosion",
            "Midnight Mansion",
            "Sunken Columns",
            "X Factor",
            "Mesa",
            "Geared",
            "Spillway",
            "Cargo",
            "Pat's Pond Peninsula",
            "High Finance",
            "Another Brick",
            "Off The Coast",
            "Cornfield",
            "Underground",
        ]

    @staticmethod
    def levels_expert() -> List[str]:
        return [
            "Glacial Trail",
            "Dark Dungeons",
            "Sanctuary",
            "Ravine",
            "Flooded Valley",
            "Infernal",
            "Bloody Puddles",
            "Workshop",
            "Quad",
            "Dark Castle",
            "Muddy Puddles",
            "#Ouch",
        ]


# Archipelago Options
# ...
