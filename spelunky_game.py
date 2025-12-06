from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import List

from Options import OptionSet, Range, DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SpelunkyArchipelagoOptions:
    spelunky_allowed_biomes: SpelunkyAllowedBiomes
    spelunky_allowed_characters: SpelunkyAllowedCharacters
    spelunky_include_hell_objectives: SpelunkyIncludeHellObjectives
    spelunky_include_eggplant_runs: SpelunkyIncludeEggplantRuns
    spelunky_include_no_gold_runs: SpelunkyIncludeNoGoldRuns
    spelunky_run_count: SpelunkyRunCount


class SpelunkyGame(Game):
    name = "Spelunky"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.VITA,
        KeymastersKeepGamePlatforms.X360,
    ]

    is_adult_only_or_unrated = False

    options_cls = SpelunkyArchipelagoOptions

    @functools.cached_property
    def biomes(self) -> List[str]:
        return sorted(self.archipelago_options.spelunky_allowed_biomes.value)

    @property
    def include_hell(self) -> bool:
        return self.archipelago_options.spelunky_include_hell_objectives.value

    @property
    def include_eggplant(self) -> bool:
        return self.archipelago_options.spelunky_include_eggplant_runs.value

    @property
    def include_no_gold(self) -> bool:
        return self.archipelago_options.spelunky_include_no_gold_runs.value

    @property
    def run_count_range(self) -> range:
        step = self.archipelago_options.spelunky_run_count.value
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
                label="Speedrun: Finish a full run under 20 minutes",
                data={},
            ),
            GameObjectiveTemplate(
                label="No damsels harmed (do not deal damage to pets)",
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
                label="Kill every single possible shopkeeper",
                data={},
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Spend at least 4 minutes on one floor",
                data={},
            ),
            GameObjectiveTemplate(
                label="On 1-1, use no bombs or ropes and take the first totem you see",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = []

        # Core progression
        objectives.extend([
            GameObjectiveTemplate(
                label="Complete COUNT successful runs by defeating Olmec",
                data={
                    "COUNT": (self.run_count_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Defeat Olmec while playing as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Complete a run reaching the Temple (4-4) and defeat Olmec",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Complete a run without using the Ankh (no death through sacrifice)",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Defeat Olmec while still holding the Ankh",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
        ])

        # Hell and Yama
        if self.include_hell:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Reach Hell and defeat Yama",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Reach Hell without using the shortcut to 4-1",
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
                    label="Complete an Eggplant run (deliver Eggplant to Yama)",
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
            GameObjectiveTemplate(
                label="Defeat the area boss in Temple (Olmec) without taking damage",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
        ])

        # Rescue and economy
        objectives.extend([
            GameObjectiveTemplate(
                label="Rescue COUNT damsels in a single run",
                data={
                    "COUNT": (self.damsel_rescue_counts, 1),
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
            GameObjectiveTemplate(
                label="Kill every shopkeeper you can encounter on the run",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
        ])

        # Utility / shortcuts
        objectives.extend([
            GameObjectiveTemplate(
                label="Unlock the Jungle shortcut",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Unlock the Ice Caves shortcut",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Unlock the Temple shortcut",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Visit the Black Market",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat the Worm level",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat the Mothership level",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Spend at least 4 minutes on a single floor",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Reach 6 or more HP at any point during the run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
        ])

        return objectives

    # Data helpers
    @staticmethod
    def damsel_rescue_counts() -> List[int]:
        return [3, 5, 7]

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
    def characters() -> List[str]:
        # Full roster, includes unlockables
        return [
            "Spelunky Guy",
            "Spelunky Gal",
            "Yellow",
            "Purple",
            "Green",
            "Cyan",
            "Yang",
            "Round Boy",
            "Round Girl",
            "Van Helsing",
            "Eskimo",
            "Ninja",
            "Robot",
            "Meat Boy",
        ]

    @functools.cached_property
    def available_characters(self) -> List[str]:
        # Preserve roster order while respecting the OptionSet selection; fall back to full roster if empty
        allowed = set(self.archipelago_options.spelunky_allowed_characters.value)
        roster = self.characters()
        filtered = [character for character in roster if character in allowed]
        return filtered or roster


# Archipelago Options
class SpelunkyAllowedBiomes(OptionSet):
    """Which biomes can be targeted for biome-specific objectives."""

    display_name = "Spelunky Allowed Biomes"
    valid_keys = [
        "Mines",
        "Jungle",
        "Ice Caves",
        "Temple",
        "Hell",
    ]

    default = valid_keys


class SpelunkyAllowedCharacters(OptionSet):
    """Which characters can be targeted for character-specific objectives."""

    display_name = "Spelunky Allowed Characters"
    valid_keys = SpelunkyGame.characters()
    default = valid_keys


class SpelunkyIncludeHellObjectives(DefaultOnToggle):
    """Include objectives that reach Hell and defeat Yama."""

    display_name = "Include Hell Objectives"


class SpelunkyIncludeEggplantRuns(DefaultOnToggle):
    """Include the Eggplant run objective."""

    display_name = "Include Eggplant Run"


class SpelunkyIncludeNoGoldRuns(DefaultOnToggle):
    """Include the No-Gold run objective."""

    display_name = "Include No-Gold Run"


class SpelunkyRunCount(Range):
    """How many successful runs are expected for core progression objectives."""

    display_name = "Spelunky Run Count"
    range_start = 1
    range_end = 5
    default = 3
