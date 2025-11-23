from __future__ import annotations

from typing import List

from dataclasses import dataclass
from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CryptOfTheNecrodancerArchipelagoOptions:
    cotn_include_amplified_dlc: NecrodancerIncludeAmplifiedDLC
    cotn_include_synchrony_dlc: NecrodancerIncludeSynchronyDLC
    cotn_include_hatsune_miku_dlc: NecrodancerIncludeHatsuneMikuDLC
    cotn_include_shovel_knight_dlc: NecrodancerIncludeShovelKnightDLC


class CryptOfTheNecrodancerGame(Game):
    name = "Crypt of the NecroDancer"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
    ]

    is_adult_only_or_unrated = False

    options_cls = CryptOfTheNecrodancerArchipelagoOptions

    @property
    def include_amplified_dlc(self) -> bool:
        return self.archipelago_options.cotn_include_amplified_dlc.value

    @property
    def include_synchrony_dlc(self) -> bool:
        return self.archipelago_options.cotn_include_synchrony_dlc.value

    @property
    def include_hatsune_miku_dlc(self) -> bool:
        return self.archipelago_options.cotn_include_hatsune_miku_dlc.value

    @property
    def include_shovel_knight_dlc(self) -> bool:
        return self.archipelago_options.cotn_include_shovel_knight_dlc.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Never purchase items from shops",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never use bombs",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never pick up gold",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never use spells or scrolls",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never kill enemies (pacifist run)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Use only the starting weapon (no weapon pickups)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never use shrines",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must destroy every chest before opening",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never take armor or health upgrades",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must miss at least one beat per floor",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Use only torch as light source (no other light items)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never use healing consumables",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never let a floor song end (finish each floor before track ends)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Do not kill any skeleton-type enemies (except bosses) for the full run",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates = [
            GameObjectiveTemplate(
                label="Complete ZONE",
                data={
                    "ZONE": (self.zones, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
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
                label="Complete a full run with CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a full run with CHARACTER",
                data={
                    "CHARACTER": (self.characters_hard, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete ZONE with CHARACTER",
                data={
                    "ZONE": (self.zones, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete ZONE with CHARACTER",
                data={
                    "ZONE": (self.zones, 1),
                    "CHARACTER": (self.characters_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a zone without missing a beat",
                data={
                    "ZONE": (self.zones_short, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Collect GOLD gold in a single run",
                data={
                    "GOLD": (self.gold_thresholds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Unlock CHARACTER",
                data={
                    "CHARACTER": (self.unlockable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a run using only WEAPON_TYPE weapons",
                data={
                    "WEAPON_TYPE": (self.weapon_types, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Achieve a MULTIPLIER coin multiplier",
                data={
                    "MULTIPLIER": (self.coin_multipliers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Kill KILL_COUNT enemies in a single zone",
                data={
                    "KILL_COUNT": (self.kill_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete ZONE without taking damage",
                data={
                    "ZONE": (self.zones_short, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete DAILY_CHALLENGE daily challenge",
                data={
                    "DAILY_CHALLENGE": (self.daily_challenge_types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Use SPELL spell successfully USAGE_COUNT times in one run",
                data={
                    "SPELL": (self.spells, 1),
                    "USAGE_COUNT": (self.spell_usage_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a zone while maintaining CHAIN_LENGTH enemy kill chain",
                data={
                    "CHAIN_LENGTH": (self.chain_lengths, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find and use ITEM",
                data={
                    "ITEM": (self.rare_items, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete MODE mode",
                data={
                    "MODE": (self.game_modes, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat MINIBOSS miniboss",
                data={
                    "MINIBOSS": (self.minibosses, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Skip at least 2 minibosses using trap doors",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Kill a shopkeeper by the end of the run",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="End the run at full HP",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Leave ZONE without killing a single enemy",
                data={"ZONE": (self.zones_short, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Perfect a boss fight (no damage) against BOSS",
                data={"BOSS": (self.bosses, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat ZONE without collecting any gold",
                data={"ZONE": (self.zones_short, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Kill BOSS using a SPELL spell",
                data={"BOSS": (self.bosses, 1), "SPELL": (self.spells, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Kill MINIBOSS using bombs",
                data={"MINIBOSS": (self.minibosses, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish the run while holding a healing item",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat the game in under 30 minutes",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Kill your first MINIBOSS by throwing your dagger",
                data={"MINIBOSS": (self.minibosses, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

        # DLC-specific objectives appended conditionally so they only appear if toggles enabled
        if self.include_amplified_dlc:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete Zone 5 without missing a beat",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                )
            )
            templates.append(
                GameObjectiveTemplate(
                    label="Complete Zone 5 with AMPLIFIED_CHARACTER",
                    data={"AMPLIFIED_CHARACTER": (self.characters_amplified_dlc, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                )
            )
            templates.append(
                GameObjectiveTemplate(
                    label="Achieve a 15x coin multiplier in Zone 5",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                )
            )

        if self.include_synchrony_dlc:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete a full run with SYNCHRONY_CHARACTER",
                    data={"SYNCHRONY_CHARACTER": (self.characters_synchrony_dlc, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                )
            )
            templates.append(
                GameObjectiveTemplate(
                    label="Maintain a CHAIN_LENGTH kill chain as Tempo",
                    data={"CHAIN_LENGTH": (self.chain_lengths, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                )
            )
            templates.append(
                GameObjectiveTemplate(
                    label="Complete ZONE flawless with SYNCHRONY_CHARACTER",
                    data={
                        "ZONE": (self.zones_short, 1),
                        "SYNCHRONY_CHARACTER": (self.characters_synchrony_dlc, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                )
            )

        if self.include_hatsune_miku_dlc:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete a zone without missing a beat as Hatsune Miku",
                    data={"ZONE": (self.zones_short, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                )
            )
            templates.append(
                GameObjectiveTemplate(
                    label="Complete a full run as Hatsune Miku",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                )
            )

        if self.include_shovel_knight_dlc:
            templates.append(
                GameObjectiveTemplate(
                    label="Collect 1000+ gold as Shovel Knight",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )
            templates.append(
                GameObjectiveTemplate(
                    label="Defeat BOSS using only the starting shovel as Shovel Knight",
                    data={"BOSS": (self.bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                )
            )
            templates.append(
                GameObjectiveTemplate(
                    label="Complete a full run as Shovel Knight",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                )
            )

        return templates

    def zones(self) -> List[str]:
        zones = [
            "Zone 1",
            "Zone 2",
            "Zone 3",
            "Zone 4",
        ]
        if self.include_amplified_dlc:
            zones.append("Zone 5")
        return zones

    @staticmethod
    def zones_short() -> List[str]:
        return [
            "Zone 1",
            "Zone 2",
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "King Conga",
            "Death Metal",
            "Deep Blues",
            "Coral Riff",
            "Dead Ringer",
        ]

    @staticmethod
    def minibosses() -> List[str]:
        return [
            "Shopkeeper",
            "Fortissimole",
            "Nightmare",
            "Mimic",
        ]

    def characters(self) -> List[str]:
        chars = self.characters_base()
        if self.include_amplified_dlc:
            chars.extend(self.characters_amplified_dlc())
        if self.include_synchrony_dlc:
            chars.extend(self.characters_synchrony_dlc())
        if self.include_hatsune_miku_dlc:
            chars.extend(self.characters_hatsune_miku_dlc())
        if self.include_shovel_knight_dlc:
            chars.extend(self.characters_shovel_knight_dlc())
        return chars

    @staticmethod
    def characters_hard() -> List[str]:
        return [
            "Aria",
            "Coda",
            "Monk",
        ]

    def unlockable_characters(self) -> List[str]:
        chars = [c for c in self.characters_base() if c != "Cadence"]
        if self.include_amplified_dlc:
            chars.extend(self.characters_amplified_dlc())
        if self.include_synchrony_dlc:
            chars.extend(self.characters_synchrony_dlc())
        if self.include_hatsune_miku_dlc:
            chars.extend(self.characters_hatsune_miku_dlc())
        if self.include_shovel_knight_dlc:
            chars.extend(self.characters_shovel_knight_dlc())
        return chars

    @staticmethod
    def characters_base() -> List[str]:
        return [
            "Cadence",
            "Melody",
            "Aria",
            "Dorian",
            "Eli",
            "Monk",
            "Dove",
            "Coda",
            "Bolt",
            "Bard",
        ]

    @staticmethod
    def characters_amplified_dlc() -> List[str]:
        return [
            "Nocturna",
            "Diamond",
            "Mary",
        ]

    @staticmethod
    def characters_synchrony_dlc() -> List[str]:
        return [
            "Tempo",
            "Chaunter",
            "Suzu",
            "Klarinet",
        ]

    @staticmethod
    def characters_hatsune_miku_dlc() -> List[str]:
        return [
            "Hatsune Miku",
        ]

    @staticmethod
    def characters_shovel_knight_dlc() -> List[str]:
        return [
            "Shovel Knight",
        ]

    @staticmethod
    def weapon_types() -> List[str]:
        return [
            "Dagger",
            "Broadsword",
            "Rapier",
            "Spear",
            "Whip",
            "Flail",
        ]

    @staticmethod
    def gold_thresholds() -> List[int]:
        return [500, 1000, 2000]

    @staticmethod
    def coin_multipliers() -> List[str]:
        return [
            "5x",
            "10x",
            "15x",
        ]

    @staticmethod
    def kill_counts() -> List[int]:
        return [30, 50, 75]

    @staticmethod
    def daily_challenge_types() -> List[str]:
        return [
            "Standard",
            "Hard Mode",
            "Seeded",
        ]

    @staticmethod
    def spells() -> List[str]:
        return [
            "Fireball",
            "Freeze",
            "Transmute",
            "Earthquake",
            "Shield",
        ]

    @staticmethod
    def spell_usage_counts() -> List[int]:
        return [5, 10, 15]

    @staticmethod
    def chain_lengths() -> List[int]:
        return [10, 20, 30]

    @staticmethod
    def rare_items() -> List[str]:
        return [
            "Ring of Courage",
            "Ring of Shadows",
            "Boots of Levitation",
            "Crown of Greed",
            "Glass Jaw",
            "Ring of War",
        ]

    @staticmethod
    def game_modes() -> List[str]:
        return [
            "All Zones Mode",
            "Hard Mode",
            "Phasing Mode",
        ]


# Archipelago Options
class NecrodancerIncludeAmplifiedDLC(Toggle):
    """If enabled, includes Amplified DLC content (Zone 5 + Nocturna, Diamond, Mary)."""
    display_name = "Crypt of the NecroDancer Include Amplified DLC"


class NecrodancerIncludeSynchronyDLC(Toggle):
    """If enabled, includes Synchrony DLC characters (Tempo, Chaunter, Suzu, Klarinet)."""
    display_name = "Crypt of the NecroDancer Include Synchrony DLC"


class NecrodancerIncludeHatsuneMikuDLC(Toggle):
    """If enabled, includes Hatsune Miku DLC character."""
    display_name = "Crypt of the NecroDancer Include Hatsune Miku DLC"


class NecrodancerIncludeShovelKnightDLC(Toggle):
    """If enabled, includes Shovel Knight DLC character."""
    display_name = "Crypt of the NecroDancer Include Shovel Knight DLC"