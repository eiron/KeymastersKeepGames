from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, OptionSet, TextChoice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class HarvestellaArchipelagoOptions:
    harvestella_include_farming: HarvestellaIncludeFarming
    harvestella_include_exploration: HarvestellaIncludeExploration
    harvestella_include_combat: HarvestellaIncludeCombat
    harvestella_include_relationships: HarvestellaIncludeRelationships
    harvestella_include_story: HarvestellaIncludeStory
    harvestella_include_crafting: HarvestellaIncludeCrafting
    harvestella_include_cooking: HarvestellaIncludeCooking
    harvestella_include_seasonal: HarvestellaIncludeSeasonalGoals
    harvestella_include_collection: HarvestellaIncludeCollection
    harvestella_difficulty_level: HarvestellaDifficultyLevel
    harvestella_crop_selection: HarvestellaCropSelection
    harvestella_job_selection: HarvestellaJobSelection
    harvestella_location_selection: HarvestellaLocationSelection
    harvestella_character_selection: HarvestellaCharacterSelection
    harvestella_monster_selection: HarvestellaMonsterSelection
    harvestella_recipe_selection: HarvestellaRecipeSelection
    harvestella_item_selection: HarvestellaItemSelection


class HarvestellaGame(Game):
    @staticmethod
    def all_farming_quantities() -> List[int]:
        return [10, 20, 30, 50, 100]

    @staticmethod
    def all_star_ratings() -> List[str]:
        return ["Gold"]

    @staticmethod
    def all_season_harvest_quantities() -> List[int]:
        return [50, 75, 100, 150]

    @staticmethod
    def all_field_sizes() -> List[int]:
        return [20, 30, 50, 100]

    @staticmethod
    def all_exploration_floors() -> List[int]:
        return [10, 20, 30, 50]

    @staticmethod
    def all_rare_material_quantities() -> List[int]:
        return [5, 10, 15, 25]

    @staticmethod
    def all_combat_quantities() -> List[int]:
        return [10, 25, 50, 100]

    @staticmethod
    def all_enemy_day_quantities() -> List[int]:
        return [20, 30, 50, 75]

    @staticmethod
    def all_relationship_levels() -> List[int]:
        return [3, 5, 7, 10]

    @staticmethod
    def all_story_chapters() -> List[int]:
        return [1, 2, 3, 4, 5, 6, 7, 8]

    @staticmethod
    def all_seaslight_crystals() -> List[int]:
        return [1, 2, 3, 4]

    @staticmethod
    def all_crafting_quantities() -> List[int]:
        return [5, 10, 20, 30]

    @staticmethod
    def all_equipment_levels() -> List[int]:
        return [3, 5, 7, 10]

    @staticmethod
    def all_rarities() -> List[str]:
        return ["Rare", "Epic", "Legendary"]

    @staticmethod
    def all_cooking_quantities() -> List[int]:
        return [10, 25, 50, 75]

    @staticmethod
    def all_dish_quantities() -> List[int]:
        return [5, 10, 20, 30]

    @staticmethod
    def all_quietus_events() -> List[int]:
        return [1, 2, 3, 4]

    @staticmethod
    def all_collection_quantities() -> List[int]:
        return [10, 25, 50, 75]

    @staticmethod
    def all_categories() -> List[str]:
        return ["seeds", "materials", "gems", "artifacts"]

    @staticmethod
    def all_inventory_categories() -> List[str]:
        return ["crop", "monster material", "gem", "artifact"]
    
    name = "Harvestella"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = HarvestellaArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        if self.difficulty_level in ["Hard", "Nightmare"]:
            constraints.extend([
                GameObjectiveTemplate(
                    label="Complete this objective within DAYS days",
                    data={"DAYS": (self.nightmare_day_limits, 1)},
                ),
                GameObjectiveTemplate(
                    label="Complete this objective without using revival items",
                    data={},
                ),
            ])
        
        if self.difficulty_level == "Nightmare":
            constraints.extend([
                GameObjectiveTemplate(
                    label="Complete this objective using only JOBCLASS job abilities",
                    data={"JOBCLASS": (self.jobs, 1)},
                ),
                GameObjectiveTemplate(
                    label="Complete this objective without purchasing any items from shops",
                    data={},
                ),
            ])
        
        return constraints

    @staticmethod
    def nightmare_day_limits() -> List[int]:
        return [30, 45, 60, 90]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = []

        # Farming objectives
        if self.include_farming:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Grow and harvest QUANTITY CROP",
                    data={
                        "QUANTITY": (self.all_farming_quantities, 1),
                        "CROP": (self.all_crops, 1)
                    },
                    is_time_consuming=True,
                ),
                GameObjectiveTemplate(
                    label="Achieve a Gold rating on CROP",
                    data={
                        "CROP": (self.all_crops, 1)
                    },
                ),
                GameObjectiveTemplate(
                    label="Harvest QUANTITY CROP in a single season",
                    data={
                        "QUANTITY": (self.all_season_harvest_quantities, 1),
                        "CROP": (self.all_crops, 1)
                    },
                ),
                GameObjectiveTemplate(
                    label="Create a farm field with at least SIZE plots of CROP",
                    data={
                        "SIZE": (self.all_field_sizes, 1),
                        "CROP": (self.all_crops, 1)
                    },
                ),
                # Pet objectives
                GameObjectiveTemplate(
                    label="Raise a Cluffowl",
                    data={},
                ),
                GameObjectiveTemplate(
                    label="Achieve maximum bond level with Cluffowl",
                    data={},
                ),
                GameObjectiveTemplate(
                    label="Unlock all Cluffowl skills",
                    data={},
                ),
                GameObjectiveTemplate(
                    label="Upgrade Cluffowl housing to highest level",
                    data={},
                ),
                GameObjectiveTemplate(
                    label="Raise a Woolum",
                    data={},
                ),
                GameObjectiveTemplate(
                    label="Achieve maximum bond level with Woolum",
                    data={},
                ),
                GameObjectiveTemplate(
                    label="Unlock all Woolum skills",
                    data={},
                ),
                GameObjectiveTemplate(
                    label="Upgrade Woolum housing to highest level",
                    data={},
                ),
                GameObjectiveTemplate(
                    label="Obtain and ride Totokaku",
                    data={},
                ),
                GameObjectiveTemplate(
                    label="Achieve maximum bond level with Totokaku (unlock all skills)",
                    data={},
                ),
            ])

        # Exploration and Adventure objectives
        if self.include_exploration:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Discover all treasure chests in LOCATION",
                    data={"LOCATION": (self.all_locations, 1)},
                ),
                GameObjectiveTemplate(
                    label="Reach floor FLOOR in DUNGEON",
                    data={
                        "FLOOR": (self.all_exploration_floors, 1),
                        "DUNGEON": (self.all_dungeons, 1)
                    },
                ),
                GameObjectiveTemplate(
                    label="Collect QUANTITY rare materials from LOCATION",
                    data={
                        "QUANTITY": (self.all_rare_material_quantities, 1),
                        "LOCATION": (self.all_locations, 1)
                    },
                ),
            ])

        # Combat objectives  
        if self.include_combat:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Defeat QUANTITY MONSTER",
                    data={
                        "QUANTITY": (self.all_combat_quantities, 1),
                        "MONSTER": (self.all_monsters, 1)
                    },
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSSES without taking damage",
                    data={"BOSSES": (self.all_boss_monsters, 1)},
                ),
                GameObjectiveTemplate(
                    label="Master the JOBCLASS job to level LEVEL",
                    data={
                        "JOBCLASS": (self.all_jobs, 1),
                        "LEVEL": (self.all_equipment_levels, 1)
                    },
                ),
                GameObjectiveTemplate(
                    label="Complete a dungeon using only JOBCLASS abilities",
                    data={"JOBCLASS": (self.all_jobs, 1)},
                ),
                GameObjectiveTemplate(
                    label="Defeat QUANTITY enemies in a single day",
                    data={"QUANTITY": (self.all_enemy_day_quantities, 1)},
                ),
            ])

        # Relationship objectives
        if self.include_relationships:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach relationship level LEVEL with CHARACTER",
                    data={
                        "LEVEL": (self.all_relationship_levels, 1),
                        "CHARACTER": (self.all_characters, 1)
                    },
                ),
                GameObjectiveTemplate(
                    label="Complete all relationship events for CHARACTER", 
                    data={"CHARACTER": (self.all_characters, 1)},
                ),
            ])

        # Story progression objectives
        if self.include_story:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete Chapter CHAPTER of the main story",
                    data={"CHAPTER": (self.all_story_chapters, 1)},
                ),
                GameObjectiveTemplate(
                    label="Unlock the SEASON_DUNGEON seasonal dungeon",
                    data={"SEASON_DUNGEON": (self.all_seasonal_dungeons, 1)},
                ),
                GameObjectiveTemplate(
                    label="Complete all side quests in LOCATION",
                    data={"LOCATION": (self.all_locations, 1)},
                ),
                GameObjectiveTemplate(
                    label="Restore QUANTITY Seaslight crystals",
                    data={"QUANTITY": (self.all_seaslight_crystals, 1)},
                ),
            ])

        # Crafting objectives
        if self.include_crafting:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Craft QUANTITY ITEM",
                    data={
                        "QUANTITY": (self.all_crafting_quantities, 1),
                        "ITEM": (self.all_craftable_items, 1)
                    },
                ),
                GameObjectiveTemplate(
                    label="Upgrade your EQUIPMENT to +LEVEL",
                    data={
                        "EQUIPMENT": (self.all_equipment, 1),
                        "LEVEL": (self.all_equipment_levels, 1)
                    },
                ),
                GameObjectiveTemplate(
                    label="Craft a RARITY rarity ITEM",
                    data={
                        "RARITY": (self.all_rarities, 1),
                        "ITEM": (self.all_craftable_items, 1)
                    },
                ),
            ])

        # Cooking objectives
        if self.include_cooking:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Cook QUANTITY different recipes",
                    data={"QUANTITY": (self.all_cooking_quantities, 1)},
                ),
                GameObjectiveTemplate(
                    label="Master the recipe for DISH",
                    data={"DISH": (self.all_recipes, 1)},
                ),
                GameObjectiveTemplate(
                    label="Cook QUANTITY DISH",
                    data={
                        "QUANTITY": (self.all_dish_quantities, 1),
                        "DISH": (self.all_recipes, 1)
                    },
                ),
            ])

        # Seasonal objectives
        if self.include_seasonal:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete all seasonal activities in SEASON",
                    data={"SEASON": (self.all_seasons, 1)},
                ),
                GameObjectiveTemplate(
                    label="Survive QUANTITY Quietus events",
                    data={"QUANTITY": (self.all_quietus_events, 1)},
                ),
                GameObjectiveTemplate(
                    label="Harvest CROP during its optimal season only",
                    data={"CROP": (self.all_seasonal_crops, 1)},
                ),
            ])

        # Collection objectives
        if self.include_collection:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Collect QUANTITY different CATEGORY items",
                    data={
                        "QUANTITY": (self.all_collection_quantities, 1),
                        "CATEGORY": (self.all_categories, 1)
                    },
                ),
                GameObjectiveTemplate(
                    label="Complete the CATEGORY collection in your inventory",
                    data={"CATEGORY": (self.all_inventory_categories, 1)},
                ),
                GameObjectiveTemplate(
                    label="Find all hidden items in LOCATION",
                    data={"LOCATION": (self.all_locations, 1)},
                ),
            ])

        return game_objective_templates

    # Properties for game options
    @property
    def include_farming(self) -> bool:
        return bool(self.archipelago_options.harvestella_include_farming.value)

    @property
    def include_exploration(self) -> bool:
        return bool(self.archipelago_options.harvestella_include_exploration.value)

    @property
    def include_combat(self) -> bool:
        return bool(self.archipelago_options.harvestella_include_combat.value)

    @property
    def include_relationships(self) -> bool:
        return bool(self.archipelago_options.harvestella_include_relationships.value)

    @property
    def include_story(self) -> bool:
        return bool(self.archipelago_options.harvestella_include_story.value)

    @property
    def include_crafting(self) -> bool:
        return bool(self.archipelago_options.harvestella_include_crafting.value)

    @property
    def include_cooking(self) -> bool:
        return bool(self.archipelago_options.harvestella_include_cooking.value)

    @property
    def include_seasonal(self) -> bool:
        return bool(self.archipelago_options.harvestella_include_seasonal.value)

    @property
    def include_collection(self) -> bool:
        return bool(self.archipelago_options.harvestella_include_collection.value)

    @property
    def difficulty_level(self) -> str:
        return self.archipelago_options.harvestella_difficulty_level.value

    # Cached properties for game content

    @staticmethod
    def all_crops() -> List[str]:
        return [
            "Turnip", "Cabbage", "Strawberry", "Potato", "Cucumber",
            "Tomato", "Corn", "Onion", "Eggplant", "Bell Pepper",
            "Pumpkin", "Sweet Potato", "Carrot", "Radish", "Spinach",
            "Lettuce", "Broccoli", "Cauliflower", "Asparagus", "Artichoke",
            "Nemean Tomato", "Morrocorn", "Lightalfa", "Colorful Carrot"
        ]

    @staticmethod
    def all_jobs() -> List[str]:
        return [
            "Fighter", "Mage", "Mechanic", "Assault Savant", "Sky Lancer",
            "Shadow Walker", "Woglinde", "Lunamancer", "Avenger", "Pilgrim",
            "Aristotle", "Samurai"
        ]

    @staticmethod
    def all_locations() -> List[str]:
        return [
            "Lethe Village", "Shatolla", "Holy Capital Argene", "Abandoned Eden",
            "Coral Shrine", "Jade Forest", "Seaside Cave", "Autumn Falls",
            "Emo Hot Springs", "Conellu", "Glacia Mountain", "Twilight Mine",
            "Floating Sanctum", "Avatar's Territory"
        ]

    @staticmethod
    def all_characters() -> List[str]:
        return [
            "Shrika", "Heine", "Asyl", "Aria", "Emo", "Istina", "Brakka", "Dianthus", "Cres", "Unicorn"
        ]

    @staticmethod
    def all_monsters() -> List[str]:
        return [
            "Goblin", "Gnome", "Dragon", "Unicorn", "Juggernaut", "Hornet", "Sahagin",
            "Slime", "Chloro Gel", "Cyano Gel", "Crawler", "Shadow Elemental", "Bone Dragon",
            "Ancient Golem", "Lorelei", "Malicid", "Mnemosyne", "Star Sleeper", "Venom Bouquet", "Writhing Kelpie"
        ]

    @staticmethod
    def all_recipes() -> List[str]:
        return [
            "Vegetable Stir-fry", "Herb-grilled Fish", "Meat and Potato Stew",
            "Tomato Salad", "Corn Soup", "Pumpkin Pie", "Strawberry Jam",
            "Grilled Vegetables", "Seafood Pasta", "Mushroom Risotto",
            "Fruit Smoothie"
        ]

    @staticmethod
    def all_craftable_items() -> List[str]:
        return [
            "Repair Kit", "Fertilizer", "Seed Maker", "Quality Fertilizer",
            "Sprinkler", "Chest", "Scarecrow", "Bridge", "Lamp",
            "Healing Potion", "Magic Potion", "Stamina Potion",
            "Iron Ingot", "Silver Ingot", "Gold Ingot", "Mythril Ingot"
        ]

    @staticmethod
    def all_dungeons() -> List[str]:
        return [
            "Abandoned Eden Dungeon",
            "Coral Shrine",
            "Wind Season Dungeon", 
            "Spring Season Dungeon",
            "Summer Season Dungeon",
            "Autumn Season Dungeon"
        ]

    @staticmethod
    def all_boss_monsters() -> List[str]:
        return [
            "Unicorn",
            "Giant Mushroom",
            "Bone Dragon",
            "Shadow Elemental",
            "Corrupted Fairy",
            "Ancient Golem"
        ]

    @staticmethod
    def all_seasonal_dungeons() -> List[str]:
        return [
            "Spring Seaslight Dungeon",
            "Summer Seaslight Dungeon", 
            "Autumn Seaslight Dungeon",
            "Wind Seaslight Dungeon"
        ]

    @staticmethod
    def all_seasons() -> List[str]:
        return ["Spring", "Summer", "Autumn", "Winter", "Quietus"]

    @staticmethod
    def all_seasonal_crops() -> List[str]:
        return [
            "Strawberry", "Turnip", "Cabbage",  # Spring
            "Tomato", "Corn", "Eggplant",       # Summer  
            "Pumpkin", "Sweet Potato", "Carrot", # Autumn
            "Nemean Tomato", "Morrocorn"        # Special seasonal crops
        ]

    @staticmethod
    def all_equipment() -> List[str]:
        return [
            "Fighter Sword",
            "Mechanic Wrench",
            "Assault Savate Shoes",
            "Sky Lancer Spear",
            "Shadow Walker Daggers",
            "Woglinde Bow",
            "Lunamancer Orb",
            "Avenger Gauntlets",
            "Pilgrim Scepter"
        ]


# Archipelago Options
class HarvestellaIncludeFarming(DefaultOnToggle):
    """Include farming-related objectives (growing crops, managing fields, etc.)"""
    display_name = "Harvestella Include Farming Objectives"


class HarvestellaIncludeExploration(DefaultOnToggle):
    """Include exploration objectives (discovering areas, collecting treasures, etc.)"""
    display_name = "Harvestella Include Exploration Objectives"


class HarvestellaIncludeCombat(DefaultOnToggle):
    """Include combat objectives (defeating monsters, mastering jobs, etc.)"""
    display_name = "Harvestella Include Combat Objectives"


class HarvestellaIncludeRelationships(DefaultOnToggle):
    """Include relationship objectives (befriending characters, completing events, etc.)"""
    display_name = "Harvestella Include Relationship Objectives"


class HarvestellaIncludeStory(DefaultOnToggle):
    """Include story progression objectives (completing chapters, restoring Seaslights, etc.)"""
    display_name = "Harvestella Include Story Objectives"


class HarvestellaIncludeCrafting(DefaultOnToggle):
    """Include crafting objectives (creating items, upgrading equipment, etc.)"""
    display_name = "Harvestella Include Crafting Objectives"


class HarvestellaIncludeCooking(DefaultOnToggle):
    """Include cooking objectives (learning recipes, preparing meals, etc.)"""
    display_name = "Harvestella Include Cooking Objectives"


class HarvestellaIncludeSeasonalGoals(DefaultOnToggle):
    """Include seasonal objectives (seasonal activities, Quietus events, etc.)"""
    display_name = "Harvestella Include Seasonal Objectives"


class HarvestellaIncludeCollection(DefaultOnToggle):
    """Include collection objectives (gathering items, completing sets, etc.)"""
    display_name = "Harvestella Include Collection Objectives"


class HarvestellaDifficultyLevel(TextChoice):
    """Difficulty level affects objective complexity and constraints"""
    display_name = "Harvestella Difficulty Level"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_nightmare = 3
    default = 1


class HarvestellaCropSelection(OptionSet):
    """Select which crops can appear in farming objectives"""
    display_name = "Harvestella Crop Selection"
    default = [
        "Turnip", "Cabbage", "Strawberry", "Potato", "Cucumber",
        "Tomato", "Corn", "Onion", "Eggplant", "Bell Pepper",
        "Pumpkin", "Sweet Potato", "Carrot", "Radish", "Spinach",
        "Lettuce", "Broccoli", "Cauliflower", "Asparagus", "Artichoke",
        "Nemean Tomato", "Morrocorn", "Lightalfa", "Colorful Carrot"
    ]


class HarvestellaJobSelection(OptionSet):
    """Select which jobs can appear in combat objectives"""
    display_name = "Harvestella Job Selection"  
    default = [
        "Fighter", "Mage", "Mechanic", "Assault Savant", "Sky Lancer",
        "Shadow Walker", "Woglinde", "Lunamancer", "Avenger", "Pilgrim",
        "Aristotle", "Samurai"
    ]


class HarvestellaLocationSelection(OptionSet):
    """Select which locations can appear in exploration objectives"""
    display_name = "Harvestella Location Selection"
    default = [
        "Lethe Village", "Shatolla", "Holy Capital Argene", "Abandoned Eden",
        "Coral Shrine", "Jade Forest", "Seaside Cave", "Autumn Falls",
        "Emo Hot Springs", "Conellu", "Glacia Mountain", "Twilight Mine",
        "Floating Sanctum", "Avatar's Territory"
    ]


class HarvestellaCharacterSelection(OptionSet):
    """Select which characters can appear in relationship objectives"""
    display_name = "Harvestella Character Selection"
    default = [
        "Shrika", "Heine", "Asyl", "Aria", "Emo", "Istina", "Brakka", "Dianthus", "Cres", "Unicorn"
    ]


class HarvestellaMonsterSelection(OptionSet):
    """Select which monsters can appear in combat objectives"""
    display_name = "Harvestella Monster Selection"
    default = [
        "Goblin", "Gnome", "Dragon", "Unicorn", "Juggernaut", "Hornet", "Sahagin",
        "Slime", "Chloro Gel", "Cyano Gel", "Crawler", "Shadow Elemental", "Bone Dragon",
        "Ancient Golem", "Lorelei", "Malicid", "Mnemosyne", "Star Sleeper", "Venom Bouquet", "Writhing Kelpie"
    ]


class HarvestellaRecipeSelection(OptionSet):
    """Select which recipes can appear in cooking objectives"""
    display_name = "Harvestella Recipe Selection"
    default = [
        "Vegetable Stir-fry", "Herb-grilled Fish", "Meat and Potato Stew",
        "Tomato Salad", "Corn Soup", "Pumpkin Pie", "Strawberry Jam",
        "Grilled Vegetables", "Seafood Pasta", "Mushroom Risotto",
        "Fruit Smoothie"
    ]


class HarvestellaItemSelection(OptionSet):
    """Select which items can appear in crafting objectives"""
    display_name = "Harvestella Craftable Item Selection"
    default = [
        "Repair Kit", "Fertilizer", "Seed Maker", "Quality Fertilizer",
        "Sprinkler", "Chest", "Scarecrow", "Bridge", "Lamp",
        "Healing Potion", "Magic Potion", "Stamina Potion",
        "Iron Ingot", "Silver Ingot", "Gold Ingot", "Mythril Ingot"
    ]
