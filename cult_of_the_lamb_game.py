from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, Toggle, TextChoice

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
    cotl_include_woolhaven_dlc: COTLIncludeWoolhavenDLC
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
            GameObjectiveTemplate(
                label="Skip at least 2 Tarot Readings during a Crusade",
                data={},
            ),
            GameObjectiveTemplate(
                label="Clear every room on your chosen path during a single Crusade loop",
                data={},
            ),
            GameObjectiveTemplate(
                label="Only change your starting weapon once",
                data={},
            ),
            GameObjectiveTemplate(
                label="Only change your starting curse once",
                data={},
            ),
            GameObjectiveTemplate(
                label="Do not use a roll for a single Crusade loop",
                data={},
            ),
            GameObjectiveTemplate(
                label="Recruit all possible followers during a single Crusade loop",
                data={},
            ),
            GameObjectiveTemplate(
                label="Skip a Heart room once if possible",
                data={},
            ),
            GameObjectiveTemplate(
                label="Enter a Random room at least once if possible",
                data={},
            ),
            GameObjectiveTemplate(
                label="Only use a curse once per room (does not apply to Boss fights)",
                data={},
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

            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Appoint DISCIPLE_COUNT followers as Disciples",
                    data={"DISCIPLE_COUNT": (self.disciple_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Hatch EGG_COUNT eggs",
                    data={"EGG_COUNT": (self.egg_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

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
                    label="Collect at least TAROT_COUNT tarot cards in a single crusade",
                    data={"TAROT_COUNT": (self.tarot_counts_difficult, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Find and rescue FOLLOWER_RESCUE_COUNT followers during crusades",
                    data={"FOLLOWER_RESCUE_COUNT": (self.rescue_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete a crusade in AREA wearing FLEECE",
                    data={
                        "AREA": (self.crusade_areas, 1),
                        "FLEECE": (self.fleeces, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete a full row in the Purgatory Dungeon Gauntlet",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Catch FISH_COUNT fish at Pilgrim's Passage",
                    data={"FISH_COUNT": (self.fish_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win a game of Knucklebones",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
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
                    label="Defeat MINI_BOSS",
                    data={"MINI_BOSS": (self.mini_bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Defeat BISHOP without taking damage",
                    data={"BISHOP": (self.no_damage_bishops, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ])

            if self.include_woolhaven_dlc:
                game_objective_templates.extend([
                    GameObjectiveTemplate(
                        label="Defeat Marchosias",
                        data={},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Defeat Yngya without attacking her",
                        data={},
                        is_time_consuming=False,
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
                    label="Perform RITUAL_COUNT rituals",
                    data={"RITUAL_COUNT": (self.ritual_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
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

            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Have GOLD_AMOUNT gold coins at once",
                    data={"GOLD_AMOUNT": (self.gold_amounts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Doctrine Development
        if self.include_doctrine_development:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Have proclaimed DOCTRINE",
                    data={"DOCTRINE": (self.doctrines, 1)},
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
    def include_woolhaven_dlc(self) -> bool:
        return self.archipelago_options.cotl_include_woolhaven_dlc.value

    @property
    def management_style(self) -> str:
        return self.archipelago_options.cotl_management_style.value

    # Data lists
    def crusade_areas(self) -> List[str]:
        areas = ["Darkwood", "Anura", "Anchordeep", "Silk Cradle"]

        if self.include_woolhaven_dlc:
            areas.extend(["Ewefall", "The Rot"])

        return areas

    @staticmethod
    def bishops() -> List[str]:
        return ["Leshy", "Heket", "Kallamar", "Shamura", "The One Who Waits"]

    @staticmethod
    def no_damage_bishops() -> List[str]:
        return ["Leshy", "Heket", "Kallamar", "Shamura"]

    def fleeces(self) -> List[str]:
        fleeces = [
            "Fleece of the Lamb", "Golden Fleece", "Fleece of the Glass Cannon",
            "Fleece of the Diseased Heart", "Fleece of the Fates",
            "Fleece of Fragile Fortitude", "Fleece of a Cursed Crusade",
            "Fleece of the Berserker", "Fleece of Fervor's Favor",
            "Fleece of the Hobbled Heels", "Cowboy", "God of Death Fleece"
        ]

        if self.include_woolhaven_dlc:
            fleeces.extend(["Ratau's Cloak", "Yngya's Fleece"])

        return fleeces

    @staticmethod
    def mini_bosses() -> List[str]:
        return [
            "Amdusias", "Valefar", "Barbatos", "Gusion", "Eligos", "Zepar",
            "Saleos", "Haborym", "Baalzebub", "Focalor", "Vephar", "Hauras"
        ]

    @staticmethod
    def enemy_types() -> List[str]:
        return [
            "Cultists", "Spiders", "Slugs", "Mushrooms", "Worms", "Frogs",
            "Squid", "Ancients", "Heretics", "Demons"
        ]

    def weapon_types(self) -> List[str]:
        weapons = ["Swords", "Daggers", "Axes", "Gauntlets", "Hammers", "Blunderbusses"]

        if self.include_woolhaven_dlc:
            weapons.append("Flails")

        return weapons

    @staticmethod
    def rituals() -> List[str]:
        return [
            "Bonfire Ritual", "The Sacrifice of the Flesh", "Brainwashing Ritual",
            "Feasting Ritual", "Ritual Fast", "Ritual of the Harvest",
            "Ritual of the Ocean's Bounty", "Funeral", "Ritual of Resurrection",
            "Ritual of Enlightenment", "The Glory of Construction",
            "Glory Through Toil", "Holy Day", "Ascend Follower Ritual",
            "Ritualistic Fight Pit", "Wedding", "Loyalty Enforcer", "Tax Enforcer",
            "Alms for the Poor", "Ritual of Enrichment", "Blood Moon Ritual",
            "Rite of Lust", "Rite of Wrath", "Sinner's Pride", "Gluttony of Cannibals"
        ]

    def ritual_categories(self) -> List[str]:
        categories = ["Sustenance", "Afterlife", "Law & Order", "Work & Worship", "Possessions", "Sins"]

        if self.include_woolhaven_dlc:
            categories.append("Winter")

        return categories

    @staticmethod
    def sacrifice_rituals() -> List[str]:
        return ["The Sacrifice of the Flesh", "Ascend Follower Ritual", "Gluttony of Cannibals"]

    @staticmethod
    def punishments() -> List[str]:
        return ["Murder", "Imprison", "Intimidate", "Ritualistic Fight Pit"]

    def building_types(self) -> List[str]:
        buildings = [
            "Temple", "Shrine", "Sleeping Bag", "Shelter", "Outhouse",
            "Farm Plot", "Farmer Station", "Scarecrow", "Seed Silo", "Fertiliser Silo",
            "Cooking Fire", "Kitchen", "Lumberyard", "Stone Mine", "Refinery",
            "Healing Bay", "Prison", "Compost Bin", "Missionary",
            "Tabernacle", "Confession Booth", "Demonic Summoning Circle",
            "Propaganda Speakers", "Body Pit", "Morgue", "Janitor Station",
            "Offering Statue", "Knucklebones Table"
        ]

        if self.include_woolhaven_dlc:
            buildings.extend([
                "Ranch", "Trough", "Hutch", "Butcher's Block",
                "Work Tent", "Medic Station", "Carpentry Station",
                "Exorcism Altar", "Weather Vane", "Baptismal Bath",
                "Lightning Rod", "Rotburn Furnace", "Rotburn Mine", "Heater"
            ])

        return buildings

    def upgradeable_buildings(self) -> List[str]:
        buildings = [
            "Shelter", "Outhouse", "Kitchen", "Lumberyard", "Stone Mine",
            "Refinery", "Healing Bay", "Missionary", "Tabernacle",
            "Demonic Summoning Circle", "Farmer Station", "Scarecrow",
            "Morgue", "Janitor Station", "Crypt"
        ]

        if self.include_woolhaven_dlc:
            buildings.extend([
                "Ranch", "Exorcism Altar", "Rotburn Furnace",
                "Rotburn Mine", "Hatchery"
            ])

        return buildings

    @staticmethod
    def functional_areas() -> List[str]:
        return [
            "Farming Area", "Living Quarters", "Worship Area", "Kitchen Area",
            "Prison Area", "Mining Area", "Work Area"
        ]

    @staticmethod
    def resources() -> List[str]:
        return [
            "Lumber", "Stone", "Gold Coins", "Grass", "Berries", "Bones",
            "Crystal Shards", "Spider Silk", "Camellia", "Mushroom",
            "Pumpkin", "Beetroot", "Cauliflower", "Fish", "Meat",
            "Wooden Planks", "Stone Blocks", "Gold Bars"
        ]

    @staticmethod
    def producible_resources() -> List[str]:
        return ["Lumber", "Stone", "Grass", "Berries", "Camellia"]

    @staticmethod
    def crops() -> List[str]:
        return ["Berries", "Cauliflower", "Beetroot", "Pumpkin", "Camellia", "Mushroom"]

    def meal_types(self) -> List[str]:
        meals = [
            "Basic Berry Bowl", "Grassy Gruel",
            "Paltry Pumpkin Soup", "Cheery Cauliflower Chowder",
            "Splendid Vegetable Feast",
            "Stringy Meat Gruel", "Hearty Meat Broth", "Mighty Meat Feast",
            "Pungent Fish Stew", "Tasty Fish Meal", "Delicious Fish Feast",
            "Meager Mixed Meal", "Modest Mixed Meal", "Magnificent Mixed Meal",
            "Minced Follower Meat", "Bowl of Poop", "Deadly Dish"
        ]

        if self.include_woolhaven_dlc:
            meals.extend([
                "Egg Meal", "Hot Chili Mash", "Spoiled Milk Curd",
                "Cheese Fondue", "Shepherd's Pie", "Snow Fruit Sundae"
            ])

        return meals

    @staticmethod
    def doctrines() -> List[str]:
        return [
            "Ritual Fast", "Feasting Ritual", "Cannibal Trait", "Grass Eater Trait",
            "Ritual of the Harvest", "Ritual of the Ocean's Bounty",
            "Substances Encouraged", "Belief in Prohibition",
            "Belief in Sacrifice", "Belief in Afterlife",
            "Ritual of Resurrection", "Funeral",
            "Respect Your Elders", "Good Die Young",
            "Return to the Earth", "Grieve the Fallen",
            "Faithful", "Industrious", "Inspire", "Intimidate",
            "The Glory of Construction", "Ritual of Enlightenment",
            "Glory Through Toil", "Holy Day",
            "Murder Follower", "Ascend Follower Ritual",
            "Ritualistic Fight Pit", "Wedding",
            "Belief in Original Sin", "Belief in Absolution",
            "Loyalty Enforcer", "Tax Enforcer",
            "Extort Tithes", "Bribe Follower",
            "Belief in Materialism", "Belief in False Idols",
            "Alms for the Poor", "Ritual of Enrichment",
            "Sacral Architecture", "Devotee",
            "Rite of Lust", "Rite of Wrath",
            "Sinner's Pride", "Gluttony of Cannibals",
            "Doctrinal Extremist", "Violent Extremist",
            "Born of Sin", "Blind Allegiance"
        ]

    def doctrine_trees(self) -> List[str]:
        trees = ["Sustenance", "Afterlife", "Law & Order", "Work & Worship", "Possessions", "Sins"]

        if self.include_woolhaven_dlc:
            trees.append("Winter")

        return trees

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
        return range(3, 7)

    @staticmethod
    def tarot_counts_difficult() -> range:
        return range(8, 11)

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

    @staticmethod
    def gold_amounts() -> range:
        return range(200, 800, 200)

    @staticmethod
    def disciple_counts() -> range:
        return range(4, 13, 2)

    @staticmethod
    def egg_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def fish_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def ritual_counts() -> range:
        return range(3, 12, 3)


# Archipelago Options
class COTLIncludeCultManagement(DefaultOnToggle):
    """Include cult management objectives (followers, faith, sermons)."""
    display_name = "Cult of the Lamb Include Cult Management"

class COTLIncludeCrusadeObjectives(DefaultOnToggle):
    """Include crusade objectives (combat, exploration, rescues)."""
    display_name = "Cult of the Lamb Include Crusade Objectives"

class COTLIncludeFollowerRelationships(DefaultOnToggle):
    """Include follower relationship objectives (loyalty, marriage, quests)."""
    display_name = "Cult of the Lamb Include Follower Relationships"

class COTLIncludeBaseBuilding(DefaultOnToggle):
    """Include base building objectives (construction, upgrades, decoration)."""
    display_name = "Cult of the Lamb Include Base Building"

class COTLIncludeBossProgression(DefaultOnToggle):
    """Include boss and story progression objectives."""
    display_name = "Cult of the Lamb Include Boss Progression"

class COTLIncludeRitualCeremonies(DefaultOnToggle):
    """Include ritual and ceremony objectives."""
    display_name = "Cult of the Lamb Include Ritual Ceremonies"

class COTLIncludeResourceCollection(DefaultOnToggle):
    """Include resource collection and production objectives."""
    display_name = "Cult of the Lamb Include Resource Collection"

class COTLIncludeDoctrineDevelopment(DefaultOnToggle):
    """Include doctrine and commandment objectives."""
    display_name = "Cult of the Lamb Include Doctrine Development"

class COTLIncludeWoolhavenDLC(Toggle):
    """Include content from the Woolhaven paid DLC (Flails, Winter doctrines, ranching buildings, additional meals)."""
    display_name = "Cult of the Lamb Include Woolhaven DLC"

class COTLManagementStyle(TextChoice):
    """Focus cult management on specific leadership styles."""
    display_name = "Cult of the Lamb Management Style"
    option_all = 0
    option_benevolent = 1
    option_ruthless = 2
    default = 0
