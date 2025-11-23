from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import Toggle


@dataclass
class BrotatoArchipelagoOptions:
    brotato_include_dlc_characters: BrotatoIncludeDlcCharacters


class BrotatoGame(Game):
    name = "Brotato"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = BrotatoArchipelagoOptions

    @property
    def include_dlc_characters(self) -> Toggle:
        return self.archipelago_options.brotato_include_dlc_characters.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="No rerolling the shop",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="No combining items",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot lock items in the shop",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot sell items",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only pick up one item per wave",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Keep at least one item locked at the end of each shop wave",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Reroll at least once inbetween each wave",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Go the first three waves without spending any materials",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never take the rightmost level-up reward",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Take every Weird Ghost you see",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Enable Manual Aim in the settings",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Have at least 3 negative stats at the end of the run",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Do not buy any passive items",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Take every item reducing your max HP and ignore every item increasing your max HP",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Recycle all of your current weapons at every shop",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Finish the run with a screwdriver in hand",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run as CHARACTER on DIFFICULTY difficulty",
                data={
                    "CHARACTER": (self.characters, 1),
                    "DIFFICULTY": (self.difficulties_normal, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a run as CHARACTER on DIFFICULTY difficulty",
                data={
                    "CHARACTER": (self.characters, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach Wave WAVE with CHARACTER",
                data={
                    "WAVE": (self.waves, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a run using only WEAPON_TYPE weapons",
                data={
                    "WEAPON_TYPE": (self.weapon_types, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Collect ITEM_COUNT items in a single run",
                data={
                    "ITEM_COUNT": (self.item_counts, 1),
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
                label="Win a run with STAT_FOCUS stat focus",
                data={
                    "STAT_FOCUS": (self.stat_focuses, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete Wave 20 with CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def characters_base() -> List[str]:
        return [
            "Well Rounded",
            "Brawler",
            "Crazy",
            "Ranger",
            "Mage",
            "Chunky",
            "Old",
            "Lucky",
            "Mutant",
            "Generalist",
            "Loud",
            "Multitasker",
            "Wildling",
            "Pacifist",
            "Gladiator",
            "Saver",
            "Sick",
            "Farmer",
            "Ghost",
            "Speedy",
            "Entrepreneur",
            "Engineer",
            "Explorer",
            "Doctor",
            "Hunter",
            "Artificer",
            "Arms Dealer",
            "Streamer",
            "Cyborg",
            "Glutton",
            "Jack",
            "Lich",
            "Apprentice",
            "Cryptid",
            "Fisherman",
            "Golem",
            "King",
            "Renegade",
            "One Armed",
            "Bull",
            "Soldier",
            "Masochist",
            "Knight",
            "Demon",
            "Baby",
            "Vagabond",
            "Technomage",
            "Vampire",
        ]

    @staticmethod
    def characters_dlc() -> List[str]:
        return [
            "Sailor",
            "Curious",
            "Builder",
            "Captain",
            "Creature",
            "Chef",
            "Druid",
            "Dwarf",
            "Gangster",
            "Diver",
            "Hiker",
            "Buccaneer",
            "Ogre",
            "Romantic",
        ]

    def characters(self) -> List[str]:
        chars = self.characters_base()
        if self.include_dlc_characters:
            chars += self.characters_dlc()
        return chars

    @staticmethod
    def difficulties_normal() -> List[str]:
        return [
            "Easy",
            "Medium",
        ]

    @staticmethod
    def difficulties_hard() -> List[str]:
        return [
            "Hard",
            "Extreme",
            "Impossible",
        ]

    @staticmethod
    def weapon_types() -> List[str]:
        return [
            "Melee",
            "Ranged",
            "Explosive",
            "Elemental",
        ]

    @staticmethod
    def stat_focuses() -> List[str]:
        return [
            "max HP only",
            "damage only",
            "speed only",
            "range only",
            "armor only",
            "crit chance only",
            "engineering only",
            "luck only",
        ]

    @staticmethod
    def waves() -> range:
        return range(5, 16, 5)

    @staticmethod
    def item_counts() -> range:
        return range(20, 51, 10)

    @staticmethod
    def enemy_counts() -> range:
        return range(1000, 4001, 1000)


# Archipelago Options
class BrotatoIncludeDlcCharacters(Toggle):
    """If enabled, adds DLC characters to the Brotato character pool for objectives."""
    display_name = "Brotato Include DLC Characters"