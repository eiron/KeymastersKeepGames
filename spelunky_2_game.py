from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import List

from Options import OptionSet, Range, Toggle, DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class Spelunky2ArchipelagoOptions:
    spelunky2_allowed_biomes: "Spelunky2AllowedBiomes"
    spelunky2_allowed_characters: "Spelunky2AllowedCharacters"
    spelunky2_include_sunken_city_objectives: "Spelunky2IncludeSunkenCityObjectives"
    spelunky2_include_eggplant_runs: "Spelunky2IncludeEggplantRuns"
    spelunky2_include_no_gold_runs: "Spelunky2IncludeNoGoldRuns"
    spelunky2_include_cosmic_ocean_objectives: "Spelunky2IncludeCosmicOceanObjectives"
    spelunky2_run_count: "Spelunky2RunCount"


class Spelunky2Game(Game):
    name = "Spelunky 2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = Spelunky2ArchipelagoOptions

    @functools.cached_property
    def biomes(self) -> List[str]:
        return sorted(self.archipelago_options.spelunky2_allowed_biomes.value)

    @property
    def include_sunken_city(self) -> bool:
        return self.archipelago_options.spelunky2_include_sunken_city_objectives.value

    @property
    def include_eggplant(self) -> bool:
        return self.archipelago_options.spelunky2_include_eggplant_runs.value

    @property
    def include_no_gold(self) -> bool:
        return self.archipelago_options.spelunky2_include_no_gold_runs.value

    @property
    def include_cosmic_ocean(self) -> bool:
        return self.archipelago_options.spelunky2_include_cosmic_ocean_objectives.value

    def run_count_range(self) -> range:
        step = self.archipelago_options.spelunky2_run_count.value
        return range(step, step * 2 + 1, step)

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Do not rob shops (no stealing, no aggroing shopkeepers)",
                data={},
            ),
            GameObjectiveTemplate(
                label="Pacifist: Do not directly kill any enemies (indirect kills allowed)",
                data={},
            ),
            GameObjectiveTemplate(
                label="No bombs (cannot place bombs)",
                data={},
            ),
            GameObjectiveTemplate(
                label="No ropes (cannot use ropes)",
                data={},
            ),
            GameObjectiveTemplate(
                label="No items purchased from shops",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a level without taking any damage",
                data={},
            ),
            GameObjectiveTemplate(
                label="Speedrun: Finish a full run under 25 minutes",
                data={},
            ),
            GameObjectiveTemplate(
                label="No gold collected in an entire run",
                data={},
            ),
            GameObjectiveTemplate(
                label="Do not pick up a shotgun on the run",
                data={},
            ),
            GameObjectiveTemplate(
                label="Do not use a jetpack",
                data={},
            ),
            GameObjectiveTemplate(
                label="Spend at least 4 minutes on one floor",
                data={},
            ),
            GameObjectiveTemplate(
                label="Do not harm any turkeys",
                data={},
            ),
            GameObjectiveTemplate(
                label="Never collect more than 50,000 gold throughout the run",
                data={},
            ),
            GameObjectiveTemplate(
                label="Never carry more than 20 bombs at once",
                data={},
            ),
            GameObjectiveTemplate(
                label="Stay in a non-boss level for at least 4:45 without a clover",
                data={},
            ),
            GameObjectiveTemplate(
                label="Blow up the first Kali altar you encounter",
                data={},
            ),
            GameObjectiveTemplate(
                label="Get the Ankh and then die on spikes to resurrect",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = []

        # Core progression
        objectives.extend([
            GameObjectiveTemplate(
                label="Complete COUNT successful runs by defeating Tiamat",
                data={
                    "COUNT": (self.run_count_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Defeat Tiamat while playing as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Reach Olmec's Lair and defeat Olmec",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Defeat Tiamat while still holding the Ankh",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
        ])

        # Sunken City and Hundun
        if self.include_sunken_city:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Reach the Sunken City and defeat Hundun",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Reach the Sunken City without using the Temple/Tide Pool shortcut",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
            ])

        # Eggplant
        if self.include_eggplant:
            objectives.append(
                GameObjectiveTemplate(
                    label="Complete an Eggplant run (deliver the Eggplant Child to Hundun)",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                )
            )

        # No gold
        if self.include_no_gold:
            objectives.append(
                GameObjectiveTemplate(
                    label="Complete a No-Gold run",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                )
            )

        # Cosmic Ocean (optional, very challenging)
        if self.include_cosmic_ocean:
            objectives.append(
                GameObjectiveTemplate(
                    label="Reach the Cosmic Ocean and clear at least 10 levels",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                )
            )

        # Character + biome combination challenge
        objectives.append(
            GameObjectiveTemplate(
                label="Beat Tiamat as CHARACTER, visiting BIOME_COMBO",
                data={
                    "CHARACTER": (self.available_characters, 1),
                    "BIOME_COMBO": (self.biome_pairs, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=6,
            )
        )

        # Biome-specific tasks
        objectives.extend([
            GameObjectiveTemplate(
                label="Clear BIOME without taking damage",
                data={
                    "BIOME": (self.biomes, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Collect a Golden Idol in BIOME",
                data={
                    "BIOME": (self.biomes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Pick up at least COUNT Golden Idols on the run",
                data={
                    "COUNT": (self.idol_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
        ])

        # Rescue and economy
        objectives.extend([
            GameObjectiveTemplate(
                label="Rescue COUNT pets in a single run",
                data={
                    "COUNT": (self.pet_rescue_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Acquire COUNT hearts from Kali sacrifices in one run",
                data={
                    "COUNT": (self.kali_health_rewards, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Accumulate at least GOLD gold in a single run",
                data={
                    "GOLD": (self.gold_targets, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Finish a run with at least GOLD gold",
                data={
                    "GOLD": (self.score_targets, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Ghost at least one gem during the run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Finish the run with at least BOMB_COUNT bombs in inventory",
                data={
                    "BOMB_COUNT": (self.bomb_inventory_targets, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Kill a shopkeeper",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
        ])

        # Exploration and side content
        objectives.extend([
            GameObjectiveTemplate(
                label="Find the Black Market",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a Moon Challenge",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Visit Vlad's Castle and obtain the Crown",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Steal from a vault",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Steal an idol from 3 different areas in one run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
        ])

        # Advanced challenges
        objectives.extend([
            GameObjectiveTemplate(
                label="Finish a run with at least 500,000 gold",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Kill at least COUNT NPCs in a single run",
                data={
                    "COUNT": (self.npc_kill_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Sacrifice at least COUNT items/enemies on Kali Altars in one run",
                data={
                    "COUNT": (self.kali_sacrifice_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Kill Qilin",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Kill a yeti with the bow from the Moon Challenge",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
        ])

        return objectives

    # Data helpers
    @staticmethod
    def pet_rescue_counts() -> List[int]:
        return [2, 4, 6]

    @staticmethod
    def kali_health_rewards() -> List[int]:
        return [1, 2, 3]

    @staticmethod
    def gold_targets() -> List[int]:
        return [50000, 100000, 150000]

    @staticmethod
    def score_targets() -> List[int]:
        return [300000, 500000, 1000000]

    @staticmethod
    def bomb_inventory_targets() -> List[int]:
        return [10, 15, 20]

    @staticmethod
    def idol_counts() -> List[int]:
        return [2, 3]

    @staticmethod
    def npc_kill_counts() -> List[int]:
        return [5, 10, 15]

    @staticmethod
    def kali_sacrifice_counts() -> List[int]:
        return [5, 8, 12]

    # Logical biome sets for path pairing
    def world2_biomes(self) -> List[str]:
        allowed = set(self.biomes)
        return [b for b in ["Volcana", "Jungle"] if b in allowed]

    def world3_biomes(self) -> List[str]:
        allowed = set(self.biomes)
        return [b for b in ["Tide Pool", "Temple"] if b in allowed]

    def biome_pairs(self) -> List[str]:
        a = self.world2_biomes()
        b = self.world3_biomes()
        return [f"{x} and {y}" for x in a for y in b]

    @staticmethod
    def characters() -> List[str]:
        # Core roster (includes unlockables)
        return [
            "Ana Spelunky",
            "Margaret Tunnel",
            "Colin Northward",
            "Roffy D. Sloth",
            "Liz Mutton",
            "Alto Singh",
            "Nekka Plissken",
            "Coco Von Diamonds",
            "Little Jay",
            "Tina Flan",
            "Valerie Crump",
            "Au",
            "Demi Von Diamonds",
            "Dirk Yamaoka",
        ]

    @functools.cached_property
    def available_characters(self) -> List[str]:
        allowed = set(self.archipelago_options.spelunky2_allowed_characters.value)
        roster = self.characters()
        filtered = [character for character in roster if character in allowed]
        return filtered or roster


# Archipelago Options
class Spelunky2AllowedBiomes(OptionSet):
    """Which biomes can be targeted for biome-specific objectives."""

    display_name = "Spelunky 2 Allowed Biomes"
    valid_keys = [
        "Dwelling",
        "Jungle",
        "Volcana",
        "Tide Pool",
        "Temple",
        "Neo Babylon",
        "Sunken City",
        "Abzu",
        "Duat",
    ]

    default = valid_keys


class Spelunky2AllowedCharacters(OptionSet):
    """Which characters can be targeted for character-specific objectives."""

    display_name = "Spelunky 2 Allowed Characters"
    valid_keys = Spelunky2Game.characters()
    default = valid_keys


class Spelunky2IncludeSunkenCityObjectives(DefaultOnToggle):
    """Include objectives that reach the Sunken City and defeat Hundun."""

    display_name = "Include Sunken City Objectives"


class Spelunky2IncludeEggplantRuns(DefaultOnToggle):
    """Include the Eggplant Child run objective."""

    display_name = "Include Eggplant Child Run"


class Spelunky2IncludeNoGoldRuns(DefaultOnToggle):
    """Include the No-Gold run objective."""

    display_name = "Include No-Gold Run"


class Spelunky2IncludeCosmicOceanObjectives(Toggle):
    """Include objectives related to reaching/clearing Cosmic Ocean."""

    display_name = "Include Cosmic Ocean Objectives"


class Spelunky2RunCount(Range):
    """How many successful runs are expected for core progression objectives."""

    display_name = "Spelunky 2 Run Count"
    range_start = 1
    range_end = 5
    default = 3
