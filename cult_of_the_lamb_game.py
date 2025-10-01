from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, TextChoice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CultOfTheLambArchipelagoOptions:
    cotl_include_cult_management: COTLIncludeCultManagement
    cotl_include_crusade_objectives: COTLIncludeCrusadeObjectives
    cotl_include_follower_relationships: COTLIncludeFollowerRelationships
    cotl_include_base_building: COTLIncludeBaseBuilding
    cotl_include_boss_progression: COTLIncludeBossProgression
    cotl_include_ritual_ceremonies: COTLIncludeRitualCeremonies
    cotl_include_resource_collection: COTLIncludeResourceCollection
    cotl_include_doctrine_development: COTLIncludeDoctrineDevelopment
    cotl_management_style: COTLManagementStyle


class CultOfTheLambGame(Game):
    name = "Cult of the Lamb"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = CultOfTheLambArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective while maintaining FAITH_LEVEL faith",
                data={"FAITH_LEVEL": (self.faith_levels, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without losing any followers",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective using only DOCTRINE_TYPE doctrine",
                data={"DOCTRINE_TYPE": (self.doctrine_types, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective with FOLLOWER_COUNT or more followers",
                data={"FOLLOWER_COUNT": (self.follower_count_requirements, 1)},
            ),
        ])
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Cult Management
        if self.include_cult_management:
            management_templates = []
            
            if self.management_style in ["All", "Benevolent"]:
                management_templates.extend([
                    GameObjectiveTemplate(
                        label="Maintain maximum faith for DURATION days",
                        data={"DURATION": (self.duration_days, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Have FOLLOWER_COUNT happy followers simultaneously",
                        data={"FOLLOWER_COUNT": (self.follower_counts, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                ])
            
            if self.management_style in ["All", "Ruthless"]:
                management_templates.extend([
                    GameObjectiveTemplate(
                        label="Sacrifice SACRIFICE_COUNT followers in RITUAL",
                        data={
                            "SACRIFICE_COUNT": (self.sacrifice_counts, 1),
                            "RITUAL": (self.sacrifice_rituals, 1)
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Use PUNISHMENT_TYPE on PUNISHMENT_COUNT followers",
                        data={
                            "PUNISHMENT_TYPE": (self.punishments, 1),
                            "PUNISHMENT_COUNT": (self.punishment_counts, 1)
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])
            
            management_templates.extend([
                GameObjectiveTemplate(
                    label="Recruit RECRUIT_COUNT new followers",
                    data={"RECRUIT_COUNT": (self.recruit_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Successfully perform SERMON_COUNT sermons",
                    data={"SERMON_COUNT": (self.sermon_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Maintain a cult of CULT_SIZE followers",
                    data={"CULT_SIZE": (self.cult_sizes, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])
            
            game_objective_templates.extend(management_templates)

        # Crusade Objectives
        if self.include_crusade_objectives:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete a crusade in AREA without dying",
                    data={"AREA": (self.crusade_areas, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Defeat ENEMY_COUNT ENEMY_TYPE in crusades",
                    data={
                        "ENEMY_COUNT": (self.enemy_kill_counts, 1),
                        "ENEMY_TYPE": (self.enemy_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete a crusade using only WEAPON_TYPE weapons",
                    data={"WEAPON_TYPE": (self.weapon_types, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Collect TAROT_COUNT tarot cards in a single crusade",
                    data={"TAROT_COUNT": (self.tarot_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Find and rescue FOLLOWER_RESCUE_COUNT followers during crusades",
                    data={"FOLLOWER_RESCUE_COUNT": (self.rescue_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Follower Relationships
        if self.include_follower_relationships:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Max out loyalty with LOYALTY_COUNT followers",
                    data={"LOYALTY_COUNT": (self.loyalty_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Marry MARRIAGE_COUNT followers",
                    data={"MARRIAGE_COUNT": (self.marriage_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Give GIFT_COUNT gifts to followers",
                    data={"GIFT_COUNT": (self.gift_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Have followers produce RESOURCE_COUNT RESOURCE_TYPE through work",
                    data={
                        "RESOURCE_COUNT": (self.production_counts, 1),
                        "RESOURCE_TYPE": (self.producible_resources, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete QUEST_COUNT follower quests",
                    data={"QUEST_COUNT": (self.quest_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Base Building
        if self.include_base_building:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Build and place BUILDING_COUNT BUILDING_TYPE",
                    data={
                        "BUILDING_COUNT": (self.building_counts, 1),
                        "BUILDING_TYPE": (self.building_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Fully upgrade UPGRADE_BUILDING to maximum level",
                    data={"UPGRADE_BUILDING": (self.upgradeable_buildings, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Create a functional AREA_TYPE area in your cult",
                    data={"AREA_TYPE": (self.functional_areas, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Decorate your cult with DECORATION_COUNT decorations",
                    data={"DECORATION_COUNT": (self.decoration_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Boss Progression
        if self.include_boss_progression:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Defeat BISHOP",
                    data={"BISHOP": (self.bishops, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Defeat MINI_BOSS without taking damage",
                    data={"MINI_BOSS": (self.mini_bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete the main story campaign",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Unlock and defeat the final boss",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Ritual Ceremonies
        if self.include_ritual_ceremonies:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Perform RITUAL successfully",
                    data={"RITUAL": (self.rituals, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Hold CEREMONY_COUNT ceremonies in CEREMONY_DURATION days",
                    data={
                        "CEREMONY_COUNT": (self.ceremony_counts, 1),
                        "CEREMONY_DURATION": (self.ceremony_durations, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Unlock and perform all RITUAL_CATEGORY rituals",
                    data={"RITUAL_CATEGORY": (self.ritual_categories, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Resource Collection
        if self.include_resource_collection:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Collect RESOURCE_AMOUNT RESOURCE",
                    data={
                        "RESOURCE_AMOUNT": (self.resource_amounts, 1),
                        "RESOURCE": (self.resources, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Cook and serve MEAL_COUNT MEAL_TYPE meals",
                    data={
                        "MEAL_COUNT": (self.meal_counts, 1),
                        "MEAL_TYPE": (self.meal_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Farm and harvest CROP_COUNT CROP",
                    data={
                        "CROP_COUNT": (self.crop_counts, 1),
                        "CROP": (self.crops, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Doctrine Development
        if self.include_doctrine_development:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Unlock and implement DOCTRINE",
                    data={"DOCTRINE": (self.doctrines, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete a full DOCTRINE_TREE doctrine tree",
                    data={"DOCTRINE_TREE": (self.doctrine_trees, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Unlock COMMANDMENT_COUNT divine commandments",
                    data={"COMMANDMENT_COUNT": (self.commandment_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_cult_management(self) -> bool:
        return self.archipelago_options.cotl_include_cult_management.value

    @property
    def include_crusade_objectives(self) -> bool:
        return self.archipelago_options.cotl_include_crusade_objectives.value

    @property
    def include_follower_relationships(self) -> bool:
        return self.archipelago_options.cotl_include_follower_relationships.value

    @property
    def include_base_building(self) -> bool:
        return self.archipelago_options.cotl_include_base_building.value

    @property
    def include_boss_progression(self) -> bool:
        return self.archipelago_options.cotl_include_boss_progression.value

    @property
    def include_ritual_ceremonies(self) -> bool:
        return self.archipelago_options.cotl_include_ritual_ceremonies.value

    @property
    def include_resource_collection(self) -> bool:
        return self.archipelago_options.cotl_include_resource_collection.value

    @property
    def include_doctrine_development(self) -> bool:
        return self.archipelago_options.cotl_include_doctrine_development.value

    @property
    def management_style(self) -> str:
        return self.archipelago_options.cotl_management_style.value

    # Data lists
    @staticmethod
    def crusade_areas() -> List[str]:
        return ["Darkwood", "Anura", "Anchordeep", "Silk Cradle"]

    @staticmethod
    def bishops() -> List[str]:
        return ["Leshy", "Heket", "Kallamar", "Shamura", "The One Who Waits"]

    @staticmethod
    def mini_bosses() -> List[str]:
        return [
            "Amdusias", "Eligos", "Barbatos", "Zepar", "Focalor", "Vephar",
            "Hauras", "Allocer", "Bael", "Forneus", "Gusion", "Valefar"
        ]

    @staticmethod
    def enemy_types() -> List[str]:
        return [
            "Cultists", "Spiders", "Slugs", "Mushrooms", "Worms", "Frogs",
            "Squid", "Ancients", "Heretics", "Demons"
        ]

    @staticmethod
    def weapon_types() -> List[str]:
        return ["Swords", "Daggers", "Axes", "Hammers", "Curses", "Ranged"]

    @staticmethod
    def rituals() -> List[str]:
        return [
            "Ritual of Resurrection", "Feast", "Fast", "Sacrifice", "Wedding",
            "Funeral", "Enlightenment", "Brainwashing", "Holiday", "Ascend Follower",
            "Alms for the Poor", "Ritual of Enrichment", "Blood Moon Ritual"
        ]

    @staticmethod
    def ritual_categories() -> List[str]:
        return ["Sustenance", "Afterlife", "Law & Order", "Work & Worship", "Possessions"]

    @staticmethod
    def sacrifice_rituals() -> List[str]:
        return ["Sacrifice", "Ascend Follower", "Blood Moon Ritual"]

    @staticmethod
    def punishments() -> List[str]:
        return ["Stocks", "Re-education", "Intimidate", "Imprison", "Exile"]

    @staticmethod
    def building_types() -> List[str]:
        return [
            "Shrine", "Sleeping Bag", "Outhouse", "Farm Plot", "Lumber Yard",
            "Stone Mine", "Kitchen", "Healing Bay", "Prison", "Decoration",
            "Compost Bin", "Refinement", "Missionary", "Fertilizer"
        ]

    @staticmethod
    def upgradeable_buildings() -> List[str]:
        return ["Shrine", "Kitchen", "Sleeping Quarters", "Farm Plots", "Refinement"]

    @staticmethod
    def functional_areas() -> List[str]:
        return [
            "Farming Area", "Living Quarters", "Worship Area", "Kitchen Area",
            "Prison Area", "Mining Area", "Decoration Area", "Work Area"
        ]

    @staticmethod
    def resources() -> List[str]:
        return [
            "Wood", "Stone", "Gold Coins", "Grass", "Berries", "Bones",
            "Crystal", "Spider Silk", "Relic", "Camelia", "Mushroom",
            "Pumpkin", "Beetroot", "Cauliflower", "Fish", "Meat"
        ]

    @staticmethod
    def producible_resources() -> List[str]:
        return ["Wood", "Stone", "Grass", "Berries", "Camelia"]

    @staticmethod
    def crops() -> List[str]:
        return ["Berries", "Cauliflower", "Beetroot", "Pumpkin", "Camelia", "Mushroom"]

    @staticmethod
    def meal_types() -> List[str]:
        return [
            "Basic Meals", "Good Meals", "Great Meals", "Magnificent Meals",
            "Fish Meals", "Meat Meals", "Vegetarian Meals", "Mixed Meals"
        ]

    @staticmethod
    def doctrines() -> List[str]:
        return [
            "Ritual Fast", "Ritual Feast", "Belief in Afterlife", "Belief in Sacrifice",
            "Respect Your Elders", "Ascend Follower", "Natural Burial", "Ritual of Resurrection",
            "Work and Worship", "Devotee Work", "Holy Day", "Ritual Holiday",
            "Materialism", "False Idols", "Greed", "Alms for the Poor"
        ]

    @staticmethod
    def doctrine_trees() -> List[str]:
        return ["Sustenance", "Afterlife", "Law & Order", "Work & Worship", "Possessions"]

    @staticmethod
    def doctrine_types() -> List[str]:
        return ["Benevolent", "Ruthless", "Balanced"]

    @staticmethod
    def faith_levels() -> List[str]:
        return ["Low Faith", "Medium Faith", "High Faith", "Maximum Faith"]

    # Ranges
    @staticmethod
    def follower_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def cult_sizes() -> range:
        return range(10, 30, 5)

    @staticmethod
    def recruit_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def sermon_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def sacrifice_counts() -> range:
        return range(1, 10, 2)

    @staticmethod
    def punishment_counts() -> range:
        return range(2, 10, 2)

    @staticmethod
    def duration_days() -> range:
        return range(3, 14, 3)

    @staticmethod
    def enemy_kill_counts() -> range:
        return range(10, 100, 10)

    @staticmethod
    def tarot_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def rescue_counts() -> range:
        return range(2, 10, 2)

    @staticmethod
    def loyalty_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def marriage_counts() -> range:
        return range(1, 5)

    @staticmethod
    def gift_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def production_counts() -> range:
        return range(20, 100, 20)

    @staticmethod
    def quest_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def building_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def decoration_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def ceremony_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def ceremony_durations() -> range:
        return range(7, 21, 7)

    @staticmethod
    def resource_amounts() -> range:
        return range(50, 300, 50)

    @staticmethod
    def meal_counts() -> range:
        return range(10, 50, 10)

    @staticmethod
    def crop_counts() -> range:
        return range(20, 100, 20)

    @staticmethod
    def commandment_counts() -> range:
        return range(3, 12, 3)

    @staticmethod
    def follower_count_requirements() -> range:
        return range(10, 25, 5)


# Archipelago Options
class COTLIncludeCultManagement(DefaultOnToggle):
    """Include cult management objectives (followers, faith, sermons)."""
    display_name = "Include Cult Management"

class COTLIncludeCrusadeObjectives(DefaultOnToggle):
    """Include crusade objectives (combat, exploration, rescues)."""
    display_name = "Include Crusade Objectives"

class COTLIncludeFollowerRelationships(DefaultOnToggle):
    """Include follower relationship objectives (loyalty, marriage, quests)."""
    display_name = "Include Follower Relationships"

class COTLIncludeBaseBuilding(DefaultOnToggle):
    """Include base building objectives (construction, upgrades, decoration)."""
    display_name = "Include Base Building"

class COTLIncludeBossProgression(DefaultOnToggle):
    """Include boss and story progression objectives."""
    display_name = "Include Boss Progression"

class COTLIncludeRitualCeremonies(DefaultOnToggle):
    """Include ritual and ceremony objectives."""
    display_name = "Include Ritual Ceremonies"

class COTLIncludeResourceCollection(DefaultOnToggle):
    """Include resource collection and production objectives."""
    display_name = "Include Resource Collection"

class COTLIncludeDoctrineDevelopment(DefaultOnToggle):
    """Include doctrine and commandment objectives."""
    display_name = "Include Doctrine Development"

class COTLManagementStyle(TextChoice):
    """Focus cult management on specific leadership styles."""
    display_name = "Management Style"
    option_all = 0
    option_benevolent = 1
    option_ruthless = 2
    default = 0
