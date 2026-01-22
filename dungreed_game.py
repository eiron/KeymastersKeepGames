from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle, DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DungreedArchipelagoOptions:
    dungreed_include_difficulty_objectives: DungreedIncludeDifficultyObjectives
    dungreed_include_weapon_objectives: DungreedIncludeWeaponObjectives
    dungreed_include_boss_objectives: DungreedIncludeBossObjectives
    dungreed_include_character_objectives: DungreedIncludeCharacterObjectives
    dungreed_include_trial_objectives: DungreedIncludeTrialObjectives


class DungreedGame(Game):
    name = "Dungreed"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.PS4,
    ]

    is_adult_only_or_unrated = False

    options_cls = DungreedArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on Hard Mode",
                data={},
            ),
            GameObjectiveTemplate(
                label="Use only WEAPON_TYPE weapons",
                data={
                    "WEAPON_TYPE": (self.weapon_types, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Don't use any food items",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't upgrade any stats at the village",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a run without using any dash skills",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a run without buying from shops",
                data={},
            ),
            GameObjectiveTemplate(
                label="Use only RARITY_TIER rarity items",
                data={
                    "RARITY_TIER": (self.rarity_tiers, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Play as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Complete an area with only dash damage",
                data={},
            ),
            GameObjectiveTemplate(
                label="Only have 1 legendary accessory equipped at any time",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't enhance anything at a Magic Forge",
                data={},
            ),
            GameObjectiveTemplate(
                label="Only buy the cheapest food item at restaurants",
                data={},
            ),
            GameObjectiveTemplate(
                label="Sell or discard a weapon from your inventory every area (including boss areas)",
                data={},
            ),
            GameObjectiveTemplate(
                label="Sacrifice an accessory to the Altar before the first boss",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        objectives += self.base_objectives()
        
        if self.include_difficulty_objectives:
            objectives += self.difficulty_objectives()
            
        if self.include_weapon_objectives:
            objectives += self.weapon_objectives()
            
        if self.include_boss_objectives:
            objectives += self.boss_objectives()
            
        if self.include_character_objectives:
            objectives += self.character_objectives()
            
        if self.include_trial_objectives:
            objectives += self.trial_objectives()
        
        return objectives
    
    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a full dungeon run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Defeat Niflheim",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Reach Floor 5",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Collect 10,000 gold in a single run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat Ericha (Final Boss)",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=12,
            ),
            GameObjectiveTemplate(
                label="Complete a Trial",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Complete a run with 10+ weapon upgrades",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Clear all rooms on a single floor",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Rescue 3 NPCs in a single run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat a boss without taking damage",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Complete an area without taking damage",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Clear the Twilight Manor",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=9,
            ),
            GameObjectiveTemplate(
                label="Collect 5 RARITY_TIER rarity items in a single run",
                data={
                    "RARITY_TIER": (self.rarity_tiers, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
        ]
    
    def difficulty_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a run on Hard Mode",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Defeat Niflheim on Hard Mode",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Reach Floor 10 on Hard Mode",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Complete a Hard Mode run without using food",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=9,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS on Hard Mode without taking damage",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=9,
            ),
        ]
    
    def weapon_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a run using only WEAPON_TYPE weapons",
                data={
                    "WEAPON_TYPE": (self.weapon_types, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Defeat Niflheim using only WEAPON_TYPE weapons",
                data={
                    "WEAPON_TYPE": (self.weapon_types, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Complete a run with WEAPON_COMBO",
                data={
                    "WEAPON_COMBO": (self.weapon_combos, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Max upgrade a WEAPON_TYPE weapon in a single run",
                data={
                    "WEAPON_TYPE": (self.weapon_types, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
        ]
    
    def boss_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Defeat BOSS",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS without taking damage",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=9,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS using only WEAPON_TYPE weapons",
                data={
                    "BOSS": (self.bosses, 1),
                    "WEAPON_TYPE": (self.weapon_types, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS without using dash",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS using only dash damage",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=9,
            ),
            GameObjectiveTemplate(
                label="Defeat all bosses up to BOSS in a single run",
                data={
                    "BOSS": (self.progressive_bosses, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=9,
            ),
        ]
    
    def character_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a run as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Defeat Niflheim as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=7,
            ),
        ]
    
    def trial_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete TRIAL",
                data={
                    "TRIAL": (self.trials, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Complete TRIAL without taking damage",
                data={
                    "TRIAL": (self.trials, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Complete all 5 Trials",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
        ]
    
    @property
    def include_difficulty_objectives(self) -> bool:
        return self.archipelago_options.dungreed_include_difficulty_objectives.value
    
    @property
    def include_weapon_objectives(self) -> bool:
        return self.archipelago_options.dungreed_include_weapon_objectives.value
    
    @property
    def include_boss_objectives(self) -> bool:
        return self.archipelago_options.dungreed_include_boss_objectives.value
    
    @property
    def include_character_objectives(self) -> bool:
        return self.archipelago_options.dungreed_include_character_objectives.value
    
    @property
    def include_trial_objectives(self) -> bool:
        return self.archipelago_options.dungreed_include_trial_objectives.value
    
    @staticmethod
    def bosses() -> List[str]:
        return [
            "Asterios",
            "Belial (Dark Warden)",
            "Naglfar (Loyal Ark Vassal)",
            "Niflheim (The Ice Witch)",
            "Tunak (The King of Lizard Man)",
            "Envyrok (Little Devil Lord)",
            "Erta Ale (The Final Trial)",
            "Slime Maker (The Fused Machine)",
            "Lasley (Prisoner of the Dark Blade)",
            "Devana (Evil Cult Leader)",
            "Kaminela",
            "Ericha",
        ]
    
    @staticmethod
    def progressive_bosses() -> List[str]:
        return [
            "Asterios (01F)",
            "Belial (02F)",
            "Naglfar (03F)",
            "Niflheim (04F)",
            "Tunak (06F)",
            "Envyrok (08F)",
        ]

    @staticmethod
    def weapon_types() -> List[str]:
        return [
            "sword",
            "bow",
            "gun",
            "dagger",
            "hammer",
            "spear",
            "shield",
            "wand/staff",
        ]
    
    @staticmethod
    def specific_weapons() -> List[str]:
        return [
            "Devil Sword Elema",
            "Nastrond",
            "Zweihander",
            "Muramasa",
            "Isaac's Mask",
            "Ceres",
            "Dragon's Hammer",
            "Lara's Magic Wand",
            "Bounty Hunter",
            "Hecate",
            "Mini Slime Maker",
        ]
    
    @staticmethod
    def weapon_combos() -> List[str]:
        return [
            "dual swords",
            "sword and bow",
            "bow and dagger",
            "gun and magic",
            "hammer and shield",
            "dual guns",
            "spear and dagger",
            "staff and sword",
        ]

    @staticmethod
    def rarity_tiers() -> List[str]:
        return [
            "Common",
            "Uncommon",
            "Rare",
            "Legendary",
        ]
    
    @staticmethod
    def characters() -> List[str]:
        return [
            "Adventurer",
            "Armored Warrior",
            "Sunset Gunman",
            "Alice",
            "Lotus",
            "Ikina Bear",
            "Rider H",
            "Criminal Silhouette",
            "King of Pickaxes",
            "Fatso",
            "Devil Swordsman",
            "Human Lasley",
            "Master Chef",
            "Pandora",
            "Livna",
        ]
    
    @staticmethod
    def unlockable_characters() -> List[str]:
        return [
            "Armored Warrior",
            "Sunset Gunman",
            "Alice",
            "Lotus",
            "Ikina Bear",
            "Rider H",
            "Criminal Silhouette",
            "King of Pickaxes",
            "Fatso",
            "Devil Swordsman",
            "Human Lasley",
            "Master Chef",
            "Pandora",
            "Livna",
        ]
    
    @staticmethod
    def trials() -> List[str]:
        return [
            "1st Trial (Platforming with Dash)",
            "2nd Trial (Platforming without Dash)",
            "3rd Trial (Enemy Waves)",
            "4th Trial (Shoot 'em Up)",
            "5th Trial (Erta Ale Boss Fight)",
        ]


# Archipelago Options
class DungreedIncludeDifficultyObjectives(Toggle):
    """
    Indicates whether to include objectives that require playing on Hard Mode or higher difficulty levels.
    """
    display_name = "Dungreed: Include Difficulty Objectives"


class DungreedIncludeWeaponObjectives(DefaultOnToggle):
    """
    Indicates whether to include objectives that require using specific weapon types or weapon combinations.
    """
    display_name = "Dungreed: Include Weapon Objectives"


class DungreedIncludeBossObjectives(DefaultOnToggle):
    """
    Indicates whether to include objectives that focus on boss battles and boss-specific challenges.
    """
    display_name = "Dungreed: Include Boss Objectives"


class DungreedIncludeCharacterObjectives(Toggle):
    """
    Indicates whether to include objectives that require playing as specific characters.
    """
    display_name = "Dungreed: Include Character Objectives"


class DungreedIncludeTrialObjectives(Toggle):
    """
    Indicates whether to include objectives related to completing the game's 5 Trials.
    """
    display_name = "Dungreed: Include Trial Objectives"
