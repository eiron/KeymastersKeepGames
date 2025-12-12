from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RevitaArchipelagoOptions:
    revita_include_area_progress: RevitaIncludeAreaProgress
    revita_include_boss_clears: RevitaIncludeBossClears
    revita_include_shard_difficulty: RevitaIncludeShardDifficulty


class RevitaGame(Game):
    name = "Revita"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.SW,  # Revita is on Switch
    ]

    is_adult_only_or_unrated = False

    options_cls = RevitaArchipelagoOptions

    # Properties
    @property
    def include_area_progress(self) -> bool:
        return self.archipelago_options.revita_include_area_progress.value

    @property
    def include_boss_clears(self) -> bool:
        return self.archipelago_options.revita_include_boss_clears.value

    @property
    def include_shard_difficulty(self) -> bool:
        return self.archipelago_options.revita_include_shard_difficulty.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(label="No shop purchases during the run", data={}),
            GameObjectiveTemplate(label="Do not buy max health", data={}),
            GameObjectiveTemplate(label="Beat a floor without taking damage", data={}),
            GameObjectiveTemplate(label="Beat an area without using relic actives", data={}),
            GameObjectiveTemplate(label="Flawless a boss (no damage)", data={}),
            GameObjectiveTemplate(label="Clear an area without shrines", data={}),
            GameObjectiveTemplate(label="Clear an area without picking up relics", data={}),
            GameObjectiveTemplate(label="Spend hearts at a shrine exactly once", data={}),
            GameObjectiveTemplate(label="Trade health for a relic three times in one run", data={}),
            GameObjectiveTemplate(label="Reach the boss with at least 3 curses active", data={}),
            GameObjectiveTemplate(label="Beat an area with only basic weapon (no mods)", data={}),
            GameObjectiveTemplate(label="Defeat a boss under 90 seconds", data={}),
            GameObjectiveTemplate(label="Clear an area without dashing", data={}),
            GameObjectiveTemplate(label="Clear an area without using your active ability", data={}),
            GameObjectiveTemplate(label="Enter the Void", data={}),
            GameObjectiveTemplate(label="Complete a Black Market shop purchase", data={}),
            GameObjectiveTemplate(label="Hold at least 5 curses at once", data={}),
            GameObjectiveTemplate(label="Clear an area with 1 heart or less", data={}),
            GameObjectiveTemplate(label="Buy exactly one item per shop", data={}),
            # Area-specific constraints
            GameObjectiveTemplate(label="Go to the Calm Caldarium and use the statue for 6 or more hearts", data={}),
            GameObjectiveTemplate(label="Go to the Hollow Hives and Sacrifice your rarest Relic to the Queen Bee", data={}),
            # Custom Shard constraints
            GameObjectiveTemplate(label="Activate Custom Shards and play with Max Level Rough Rivals and Max Level Miniature", data={}),
            GameObjectiveTemplate(label="Activate Custom Shards and play with Level 2 Cursed Relics and Max Level Local Customs", data={}),
            GameObjectiveTemplate(label="Activate Custom Shards and play with the Attachment Modifier turned on", data={}),
            GameObjectiveTemplate(label="Activate Custom Shards with Level 3 Enemy Speed Up and Level 3 Tricky Tactics", data={}),
            GameObjectiveTemplate(label="Activate Custom Shards with Max Level Brutal Bosses and Level 2 Strained Security", data={}),
            GameObjectiveTemplate(label="Activate Custom Shards with Level 3 Lowered Max HP and Level 2 Blood Pressure", data={}),
            GameObjectiveTemplate(label="Activate Custom Shards with Level 2 Expansions and Max Level Wave Rooms", data={}),
            GameObjectiveTemplate(label="Activate Custom Shards with Max Level Chestless and Max Level Sold Out", data={}),
            GameObjectiveTemplate(label="Activate Custom Shards with Level 3 Cursed Start and Level 2 Abandoned Artifacts", data={}),
            GameObjectiveTemplate(label="Activate Custom Shards with Level 2 Drained and Level 2 Untrained", data={}),
            GameObjectiveTemplate(label="Activate Custom Shards with Expensive Shops and Expensive Repairs active", data={}),
            GameObjectiveTemplate(label="Activate Custom Shards with Level 2 Relic-Lock and Level 2 Lowered Max Soul", data={}),
            GameObjectiveTemplate(label="Activate Custom Shards with Level 3 Enemy HP Up and Level 3 Visitors", data={}),
            # Dynamic Custom Shard combinations - unified approach with pre-combined shard+level strings
            GameObjectiveTemplate(
                label="Activate Custom Shards with SHARD_COMBO_A and SHARD_COMBO_B",
                data={
                    "SHARD_COMBO_A": (self.all_shard_combinations, 1),
                    "SHARD_COMBO_B": (self.all_shard_combinations, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Activate Custom Shards with SHARD_COMBO_A, SHARD_COMBO_B, and SHARD_COMBO_C",
                data={
                    "SHARD_COMBO_A": (self.all_shard_combinations, 1),
                    "SHARD_COMBO_B": (self.all_shard_combinations, 1),
                    "SHARD_COMBO_C": (self.all_shard_combinations, 1),
                },
            ),
            # Equipment and resource constraints
            GameObjectiveTemplate(label="Swap your Celestial Weapon at every chance", data={}),
            GameObjectiveTemplate(label="Spend as many hearts as you can on your first shrine", data={}),
            GameObjectiveTemplate(label="Never buy health from shops", data={}),
            GameObjectiveTemplate(label="Upgrade your Celestial Weapon to max level", data={}),
            # Ticket modifiers
            GameObjectiveTemplate(label="Enable the Chaos Ticket", data={}),
            GameObjectiveTemplate(label="Complete a run using only the free key ticket", data={}),
            GameObjectiveTemplate(label="Use all available Tickets in one run", data={}),
            # Curse constraints
            GameObjectiveTemplate(label="Pick up a curse whenever you have an opportunity to do so", data={}),
            GameObjectiveTemplate(label="Clear an area while holding only negative curses", data={}),
            # Combat style constraints
            GameObjectiveTemplate(label="Defeat a boss using only your active ability damage", data={}),
            GameObjectiveTemplate(label="Complete an entire area without using your Celestial Weapon", data={}),
            # Achievement-inspired challenges
            GameObjectiveTemplate(label="Clear five shops in a single run", data={}),
            GameObjectiveTemplate(label="Steal from a shop", data={}),
            GameObjectiveTemplate(label="Empty a claw machine without failing", data={}),
            GameObjectiveTemplate(label="Use a reroll machine three times in one shop", data={}),
            GameObjectiveTemplate(label="Beat a room without touching the ground after your first jump", data={}),
            GameObjectiveTemplate(label="Finish a boss fight at half a heart", data={}),
            GameObjectiveTemplate(label="Defeat Bargaining while they are spinning on the ground", data={}),
            GameObjectiveTemplate(label="Defeat Denial by shooting while its eye is open", data={}),
            GameObjectiveTemplate(label="Defeat three minibosses in a single run", data={}),
            GameObjectiveTemplate(label="Pet the cat ten times this run", data={}),
            GameObjectiveTemplate(label="Finish a run without disturbing any critters", data={}),
            GameObjectiveTemplate(label="Collect three Celestial Weapons in one run", data={}),
            GameObjectiveTemplate(label="Beat a full run in under 20 minutes", data={}),
            GameObjectiveTemplate(label="Beat a full run without taking a hit", data={}),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = []

        if self.include_area_progress:
            templates.extend([
                GameObjectiveTemplate(
                    label="Reach AREA_NAME",
                    data={"AREA_NAME": (self.area_names, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Clear AREA_NAME",
                    data={"AREA_NAME": (self.area_names, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=9,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSS_NAME in AREA_NAME",
                    data={
                        "BOSS_NAME": (self.boss_names, 1),
                        "AREA_NAME": (self.area_names, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Clear AREA_NAME without taking damage",
                    data={"AREA_NAME": (self.area_names, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Reach AREA_NAME within ROOM_TARGET rooms",
                    data={
                        "AREA_NAME": (self.area_names, 1),
                        "ROOM_TARGET": (self.room_targets, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
            ])

        if self.include_boss_clears:
            templates.extend([
                GameObjectiveTemplate(
                    label="Defeat BOSS_NAME",
                    data={"BOSS_NAME": (self.boss_names, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSS_NAME with RELIC_COUNT relics equipped",
                    data={
                        "BOSS_NAME": (self.boss_names, 1),
                        "RELIC_COUNT": (self.relic_count_targets, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Flawless BOSS_NAME (no damage)",
                    data={"BOSS_NAME": (self.boss_names, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSS_NAME at SHARD_LEVEL shards",
                    data={
                        "BOSS_NAME": (self.boss_names, 1),
                        "SHARD_LEVEL": (self.shard_levels, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Defeat Anger without killing any of its spawns",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Defeat Depression without dashing",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=7,
                ),
            ])

        # Progression and meta objectives
        templates.extend([
            GameObjectiveTemplate(
                label="Complete the Strange Key and Open the Bedroom Chest",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Loop at least one time",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=9,
            ),
            GameObjectiveTemplate(
                label="Find at least three secret rooms",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Finish a run with at least 6 max HP",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Fully upgrade at least three relics",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Finish a run with at least 8 relics equipped",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Complete a run with at least 10 curses collected",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Defeat three bosses in a row without taking damage",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Give the Crown to the Frog King in The Caldarium and finish the run at Acceptance",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=9,
            ),
        ])

        if self.include_shard_difficulty:
            templates.extend([
                GameObjectiveTemplate(
                    label="Clear AREA_NAME at SHARD_LEVEL shards",
                    data={
                        "AREA_NAME": (self.area_names, 1),
                        "SHARD_LEVEL": (self.shard_levels, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSS_NAME at SHARD_LEVEL shards",
                    data={
                        "BOSS_NAME": (self.boss_names, 1),
                        "SHARD_LEVEL": (self.shard_levels_high, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=9,
                ),
                GameObjectiveTemplate(
                    label="Clear AREA_NAME without taking damage at SHARD_LEVEL shards",
                    data={
                        "AREA_NAME": (self.area_names, 1),
                        "SHARD_LEVEL": (self.shard_levels, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Reach Last Refuge at SHARD_LEVEL shards",
                    data={
                        "SHARD_LEVEL": (self.shard_levels, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Unlock and defeat Mother",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Unlock and defeat Regret",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Complete the True Ending with VARIANT_TYPE on SHARD_LEVEL shards or higher without shortcuts, imprisoned items, or more than one free key ticket",
                    data={
                        "VARIANT_TYPE": (self.variant_types, 1),
                        "SHARD_LEVEL": (self.shard_levels_true_ending_min, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Defeat Mother with VARIANT_TYPE at SHARD_LEVEL shards without shortcuts, imprisoned items, or more than one free key ticket",
                    data={
                        "VARIANT_TYPE": (self.variant_types, 1),
                        "SHARD_LEVEL": (self.shard_levels_true_ending_min, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=9,
                ),
                GameObjectiveTemplate(
                    label="Flawless Mother (no damage) at SHARD_LEVEL shards",
                    data={
                        "SHARD_LEVEL": (self.shard_levels_high, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=9,
                ),
                GameObjectiveTemplate(
                    label="Defeat Regret with VARIANT_TYPE at SHARD_LEVEL shards under 120 seconds",
                    data={
                        "VARIANT_TYPE": (self.variant_types, 1),
                        "SHARD_LEVEL": (self.shard_levels_high, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=9,
                ),
                GameObjectiveTemplate(
                    label="Flawless Regret (no damage)",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=8,
                ),
            ])

        return templates

    # Data lists (conservative defaults; can adjust after wiki verification)
    @staticmethod
    def area_names() -> List[str]:
        return [
            "Gazing Grove",
            "Fungated Funnels",
            "Hollow Hives",
            "Forgotten Station",
            "Arid Athenaeum",
            "Somber Sepulcher",
            "Calm Caldarium",
            "Ticking Tower Top",
            "Last Refuge",
            "Void",
        ]

    @staticmethod
    def boss_names() -> List[str]:
        return [
            "Denial",
            "Anger",
            "Bargaining",
            "Depression",
            "Enigma",
            "Mother",
            "Regret",
            "Acceptance",
        ]

    @staticmethod
    def shard_levels() -> List[str]:
        return ["0", "5", "10"]

    @staticmethod
    def shard_levels_high() -> List[str]:
        return ["15", "20"]

    @staticmethod
    def shard_levels_true_ending_min() -> List[str]:
        return ["5", "10", "15"]

    @staticmethod
    def relic_count_targets() -> List[str]:
        return ["3", "5", "7"]

    @staticmethod
    def room_targets() -> List[str]:
        return ["6", "8", "10"]

    @staticmethod
    def variant_types() -> List[str]:
        return [
            "Soul Gun",
            "Rocket Launcher",
            "Blast Gun",
            "Charge Gun",
            "Machine Gun",
            "Shotgun",
            "Orbit Gun",
            "Sniper",
        ]

    @staticmethod
    def custom_shards_1_level() -> List[str]:
        """Shards with only 1 level."""
        return [
            "Expensive Shops",
            "Expensive Repairs",
            "Forsaken",
            "Attachment",
            "Enraged",
        ]

    @staticmethod
    def custom_shards_2_levels() -> List[str]:
        """Shards with 2 levels."""
        return [
            "Cheap Monsters",
            "Cheap Bosses",
            "Lowered Max Soul",
            "Lowered Soul Amount",
            "Blood Pressure",
            "Drained",
            "Relic-Lock",
            "Secluded Statues",
            "Abandoned Artifacts",
        ]

    @staticmethod
    def custom_shards_3_levels() -> List[str]:
        """Shards with 3 levels."""
        return [
            "Enemy Damage Up",
            "Enemy HP Up",
            "Enemy Amount Up",
            "Trap Amount Up",
            "Wave Rooms",
            "Rough Rivals",
            "Lowered HP",
            "Lowered Max HP",
            "Untrained",
            "Setback",
            "Expansions",
            "Miniature",
            "Strained Security",
            "Chestless",
            "Sold Out",
            "No Repairs",
            "Cursed Start",
            "Local Customs",
            "Cursed Relics",
        ]

    @staticmethod
    def custom_shards_4_levels() -> List[str]:
        """Shards with 4 levels."""
        return [
            "Enemy Speed Up",
            "Enemy Shotspeed Up",
            "Tricky Tactics",
            "Visitors",
            "Brutal Bosses",
        ]

    @staticmethod
    def shard_levels_1_to_2() -> List[str]:
        return ["1", "2"]

    @staticmethod
    def shard_levels_1_to_3() -> List[str]:
        return ["1", "2", "3"]

    @staticmethod
    def shard_levels_1_to_4() -> List[str]:
        return ["1", "2", "3", "4"]

    @staticmethod
    def all_shard_combinations() -> List[str]:
        """All possible shard+level combinations for smart template generation."""
        combinations = []
        
        # 1-level shards (no level notation needed)
        for shard in RevitaGame.custom_shards_1_level():
            combinations.append(shard)
        
        # 2-level shards
        for shard in RevitaGame.custom_shards_2_levels():
            for level in ["1", "2"]:
                combinations.append(f"{shard} at Level {level}")
        
        # 3-level shards
        for shard in RevitaGame.custom_shards_3_levels():
            for level in ["1", "2", "3"]:
                combinations.append(f"{shard} at Level {level}")
        
        # 4-level shards
        for shard in RevitaGame.custom_shards_4_levels():
            for level in ["1", "2", "3", "4"]:
                combinations.append(f"{shard} at Level {level}")
        
        return combinations


# Archipelago Options
class RevitaIncludeAreaProgress(DefaultOnToggle):
    """Include objectives for reaching/clearing areas."""
    display_name = "Revita Include Area Progress"


class RevitaIncludeBossClears(DefaultOnToggle):
    """Include boss defeat objectives."""
    display_name = "Revita Include Boss Clears"


class RevitaIncludeShardDifficulty(DefaultOnToggle):
    """Include shard difficulty objectives."""
    display_name = "Revita Include Shard Difficulty"
