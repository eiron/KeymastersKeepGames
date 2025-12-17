from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class JustKingArchipelagoOptions:
    just_king_campaign: JustKingCampaign
    just_king_army_objectives: JustKingArmyObjectives
    just_king_challenge_objectives: JustKingChallengeObjectives


class JustKingGame(Game):
    name = "Just King"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = JustKingArchipelagoOptions

    # Properties
    @property
    def include_campaign(self) -> bool:
        return self.archipelago_options.just_king_campaign.value

    @property
    def include_army_objectives(self) -> bool:
        return self.archipelago_options.just_king_army_objectives.value

    @property
    def include_challenge_objectives(self) -> bool:
        return self.archipelago_options.just_king_challenge_objectives.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(label="Have the SYNERGY synergy active at some point on your run and complete 3 fights", data={"SYNERGY": (self.synergies, 1)}),
            GameObjectiveTemplate(label="Have a HERO on your team at the end of your run", data={"HERO": (self.heroes, 1)}),
            GameObjectiveTemplate(label="Have a unit with at least ARMOR armor at the end of your run", data={"ARMOR": (self.armor_thresholds, 1)}),
            GameObjectiveTemplate(label="Sell a Level 3 unit at some point on your run", data={}),
            GameObjectiveTemplate(label="Have at least GOLD gold in hand at some point on your run", data={"GOLD": (self.gold_thresholds, 1)}),
            GameObjectiveTemplate(label="Fight at least ELITE_COUNT elite battles", data={"ELITE_COUNT": (self.elite_battle_counts, 1)}),
            GameObjectiveTemplate(label="Have four synergies active at one time, for at least 2 fights on your run", data={}),
            GameObjectiveTemplate(label="The first unit you buy, immediately sell", data={}),
            GameObjectiveTemplate(label="Have SYNERGY_COUNT different synergies active simultaneously for at least one fight", data={"SYNERGY_COUNT": (self.synergy_counts, 1)}),
            GameObjectiveTemplate(label="Sell a Level 2 unit at some point on your run", data={}),
            GameObjectiveTemplate(label="Have at least 2 units of the same HERO type at the end of your run", data={"HERO": (self.heroes, 1)}),
            GameObjectiveTemplate(label="Have a unit with at least ATTACK attack at the end of your run", data={"ATTACK": (self.attack_thresholds, 1)}),
            GameObjectiveTemplate(label="Complete a run without selling any units", data={}),
            GameObjectiveTemplate(label="Sell at least 5 units during your run", data={}),
            GameObjectiveTemplate(label="Have at least 20 gold at the end of your run", data={}),
            GameObjectiveTemplate(label="Never reroll the shop during your run", data={}),
            GameObjectiveTemplate(label="Reroll the shop at least 10 times during your run", data={}),
            GameObjectiveTemplate(label="Buy every unit from at least one shop", data={}),
            GameObjectiveTemplate(label="Complete a run with exactly 5 units on your team", data={}),
            GameObjectiveTemplate(label="Have at least 3 Level 3 units at the end of your run", data={}),
            GameObjectiveTemplate(label="No unit upgrades during battle", data={}),
            GameObjectiveTemplate(label="Use only UNIT_TYPE units", data={"UNIT_TYPE": (self.unit_types, 1)}),
            GameObjectiveTemplate(label="Don't use any spells", data={}),
            GameObjectiveTemplate(label="Win with GOLD_LIMIT or less gold spent", data={"GOLD_LIMIT": (self.gold_limits, 1)}),
            GameObjectiveTemplate(label="Complete without using BUILDING", data={"BUILDING": (self.buildings, 1)}),
            GameObjectiveTemplate(label="Limit army to ARMY_SIZE units maximum", data={"ARMY_SIZE": (self.army_size_limits, 1)}),
            GameObjectiveTemplate(label="Don't lose any units during battles", data={}),
            GameObjectiveTemplate(label="Win without using any ranged units", data={}),
            GameObjectiveTemplate(label="Win without using any melee units", data={}),
            GameObjectiveTemplate(label="Complete with at least 3 legendary units", data={}),
            GameObjectiveTemplate(label="Don't use the same unit type more than twice", data={}),
            GameObjectiveTemplate(label="Use only units costing 2 gold or less", data={}),
            GameObjectiveTemplate(label="Win with at least 5 different unit types", data={}),
            GameObjectiveTemplate(label="Don't use any hero units", data={}),
            GameObjectiveTemplate(label="Lose no more than 2 units total during your run", data={}),
            GameObjectiveTemplate(label="Win without retreating any units", data={}),
            GameObjectiveTemplate(label="Use at least one unit from each tier", data={}),
            GameObjectiveTemplate(label="Win with army value under 50 gold", data={}),
            GameObjectiveTemplate(label="Don't use any support units", data={}),
            GameObjectiveTemplate(label="Complete your first fight without buying any units", data={}),
            GameObjectiveTemplate(label="Never have more than 3 gold at the start of a fight", data={}),
            GameObjectiveTemplate(label="Win a fight with only one unit on your team", data={}),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives = []

        if self.include_campaign:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Complete ZONE",
                    data={"ZONE": (self.zones, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Complete LEVEL",
                    data={"LEVEL": (self.campaign_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Complete CHAPTER",
                    data={"CHAPTER": (self.campaign_chapters, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSS",
                    data={"BOSS": (self.boss_enemies, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Win a run using HERO",
                    data={"HERO": (self.heroes, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Win ZONE with HERO as your first hero",
                    data={"ZONE": (self.zones, 1), "HERO": (self.heroes, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Complete the full campaign",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        if self.include_army_objectives:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Unlock UNIT",
                    data={"UNIT": (self.unlockable_units, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Fully upgrade UNIT",
                    data={"UNIT": (self.upgradeable_units, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Collect all FACTION units",
                    data={"FACTION": (self.factions, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Build an army worth at least VALUE gold",
                    data={"VALUE": (self.army_value_targets, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
            ])

        if self.include_challenge_objectives:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Win CHALLENGE_COUNT CHALLENGE_MODE challenges",
                    data={
                        "CHALLENGE_COUNT": (self.challenge_counts, 1),
                        "CHALLENGE_MODE": (self.challenge_modes, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Achieve RATING or higher rating in ranked mode",
                    data={"RATING": (self.rating_targets, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win STREAK consecutive battles without losing",
                    data={"STREAK": (self.win_streaks, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=5,
                ),
            ])

        return objectives

    # Static providers
    @staticmethod
    def heroes() -> List[str]:
        return [
            "Archer", "Bard", "Berserker", "Captain", "Cleric", "Hoplite",
            "Imp", "Knight", "Paladin", "Ranger", "Rogue", "Wizard"
        ]

    @staticmethod
    def zones() -> List[str]:
        return ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"]

    @staticmethod
    def campaign_levels() -> List[str]:
        return [
            "The First Battle", "Defense of the Village", "Forest Ambush", "River Crossing",
            "Mountain Pass", "Siege of the Castle", "Valley of Shadows", "The Lost Temple",
            "Desert Outpost", "Frozen Wasteland", "Volcanic Rift", "The Dark Tower",
            "Swamp of Despair", "Highland Fortress", "Coastal Raid", "Underground Cavern",
            "Sky Citadel", "Cursed Battlefield", "The Final Stand", "Throne Room Assault"
        ]

    @staticmethod
    def campaign_chapters() -> List[str]:
        return [
            "Chapter 1: The Rising Conflict",
            "Chapter 2: Trials of War",
            "Chapter 3: The Dark Alliance",
            "Chapter 4: Turning the Tide",
            "Chapter 5: The Final Campaign"
        ]

    @staticmethod
    def boss_enemies() -> List[str]:
        return [
            "The Corrupted General", "Shadow Lord", "Dragon King", "Necromancer Supreme",
            "Demon Warlord", "Ice Tyrant", "Fire Sovereign", "The Usurper King"
        ]

    @staticmethod
    def unlockable_units() -> List[str]:
        return [
            "Elite Knight", "Arcane Mage", "Shadow Assassin", "Dragon Rider",
            "Paladin", "War Elephant", "Siege Golem", "Phoenix Guard",
            "Berserker", "Priestess", "Sniper", "Battle Mage",
            "Cavalry Commander", "Necromancer", "Demon Hunter", "Royal Guard"
        ]

    @staticmethod
    def upgradeable_units() -> List[str]:
        return [
            "Swordsman", "Archer", "Spearman", "Mage", "Knight", "Crossbowman",
            "Pike", "Cleric", "Scout", "Cavalry", "Trebuchet", "Guard"
        ]

    @staticmethod
    def factions() -> List[str]:
        return ["Kingdom", "Empire", "Horde", "Alliance", "Legion", "Confederation"]

    @staticmethod
    def unit_types() -> List[str]:
        return ["Infantry", "Cavalry", "Ranged", "Siege", "Magic", "Support"]

    @staticmethod
    def buildings() -> List[str]:
        return [
            "Barracks", "Archery Range", "Stables", "Siege Workshop",
            "Mage Tower", "Temple", "Forge", "Market", "Wall", "Watchtower"
        ]

    @staticmethod
    def commanders() -> List[str]:
        return [
            "Lord Commander", "Battle Tactician", "War Sage", "Defensive Strategist",
            "Aggressive General", "Balanced Leader", "Economic Advisor", "Siege Master"
        ]

    @staticmethod
    def strategies() -> List[str]:
        return [
            "Rush Strategy", "Defensive Formation", "Economic Build", "Siege Focus",
            "Magic Superiority", "Cavalry Charge", "Ranged Dominance", "Balanced Approach"
        ]

    @staticmethod
    def challenge_modes() -> List[str]:
        return ["Survival", "Time Attack", "Limited Resources", "Boss Rush", "Endless"]

    @staticmethod
    def army_size_limits() -> List[int]:
        return [5, 8, 10, 12]

    @staticmethod
    def turn_limits() -> List[int]:
        return [5, 8, 10, 12, 15]

    @staticmethod
    def gold_limits() -> List[int]:
        return [30, 50, 75, 100]

    @staticmethod
    def resource_thresholds() -> List[int]:
        return [10, 20, 30, 50]

    @staticmethod
    def army_value_targets() -> List[int]:
        return [100, 150, 200, 250]

    @staticmethod
    def challenge_counts() -> range:
        return range(3, 11)

    @staticmethod
    def rating_targets() -> List[int]:
        return [1200, 1400, 1600, 1800]

    @staticmethod
    def win_streaks() -> range:
        return range(3, 11)

    @staticmethod
    def synergies() -> List[str]:
        return [
            "Shady Business", "Hot Hands", "Knight's Valor", "Arcane Focus",
            "Beast Mastery", "Divine Shield", "Shadow Strike", "Battle Cry",
            "Ranger's Mark", "Cleric's Blessing", "Berserker Rage", "Bard's Song"
        ]

    @staticmethod
    def armor_thresholds() -> List[int]:
        return [4, 6, 8, 10]

    @staticmethod
    def attack_thresholds() -> List[int]:
        return [5, 7, 10, 12]

    @staticmethod
    def gold_thresholds() -> List[int]:
        return [15, 20, 25, 30]

    @staticmethod
    def elite_battle_counts() -> range:
        return range(3, 6)

    @staticmethod
    def synergy_counts() -> range:
        return range(3, 6)


# Archipelago Options
class JustKingCampaign(DefaultOnToggle):
    """
    Include campaign objectives.
    """
    display_name = "Just King Campaign"


class JustKingArmyObjectives(DefaultOnToggle):
    """
    Include army building and unit collection objectives.
    """
    display_name = "Just King Army Objectives"


class JustKingChallengeObjectives(DefaultOnToggle):
    """
    Include challenge mode and competitive objectives.
    """
    display_name = "Just King Challenge Objectives"
