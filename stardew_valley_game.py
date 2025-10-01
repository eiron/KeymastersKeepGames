from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, TextChoice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class StardewValleyArchipelagoOptions:
    stardew_include_farming: StardewIncludeFarming
    stardew_include_mining: StardewIncludeMining
    stardew_include_fishing: StardewIncludeFishing
    stardew_include_foraging: StardewIncludeForaging
    stardew_include_relationships: StardewIncludeRelationships
    stardew_include_community_center: StardewIncludeCommunityCenterBundles
    stardew_include_collections: StardewIncludeCollections
    stardew_include_cooking: StardewIncludeCooking
    stardew_include_seasonal_goals: StardewIncludeSeasonalGoals
    stardew_difficulty_level: StardewDifficultyLevel


class StardewValleyGame(Game):
    name = "Stardew Valley"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
    ]

    is_adult_only_or_unrated = False

    options_cls = StardewValleyArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        if self.difficulty_level in ["Hard", "Expert"]:
            constraints.append(
                GameObjectiveTemplate(
                    label="Complete this objective before the end of Year YEAR",
                    data={"YEAR": (self.year_limits, 1)},
                )
            )
        
        if self.difficulty_level == "Expert":
            constraints.append(
                GameObjectiveTemplate(
                    label="Complete this objective without using any purchased items",
                    data={},
                )
            )
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Farming objectives
        if self.include_farming:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Grow and harvest QUANTITY CROP",
                    data={
                        "QUANTITY": (self.crop_quantities, 1),
                        "CROP": (self.crops, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Earn PROFIT gold from selling CROP",
                    data={
                        "PROFIT": (self.profit_amounts, 1),
                        "CROP": (self.crops, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete the ANIMAL_TYPE barn/coop with QUANTITY animals",
                    data={
                        "ANIMAL_TYPE": (self.animal_types, 1),
                        "QUANTITY": (self.animal_quantities, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Mining objectives
        if self.include_mining:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach floor FLOOR in the mines",
                    data={"FLOOR": (self.mine_floors, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Collect QUANTITY ORE_TYPE ore",
                    data={
                        "QUANTITY": (self.ore_quantities, 1),
                        "ORE_TYPE": (self.ore_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Defeat MONSTER_COUNT MONSTER in the mines",
                    data={
                        "MONSTER_COUNT": (self.monster_counts, 1),
                        "MONSTER": (self.monsters, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Fishing objectives
        if self.include_fishing:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Catch FISH_COUNT FISH",
                    data={
                        "FISH_COUNT": (self.fish_counts, 1),
                        "FISH": (self.fish, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Catch a legendary fish: LEGENDARY_FISH",
                    data={"LEGENDARY_FISH": (self.legendary_fish, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete CRAB_POT_COUNT crab pot catches",
                    data={"CRAB_POT_COUNT": (self.crab_pot_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Foraging objectives
        if self.include_foraging:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Forage QUANTITY FORAGE_ITEM",
                    data={
                        "QUANTITY": (self.forage_quantities, 1),
                        "FORAGE_ITEM": (self.forage_items, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Tap TREE_COUNT TREE_TYPE trees",
                    data={
                        "TREE_COUNT": (self.tree_counts, 1),
                        "TREE_TYPE": (self.tree_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Relationship objectives
        if self.include_relationships:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach HEART_LEVEL hearts with VILLAGER",
                    data={
                        "HEART_LEVEL": (self.heart_levels, 1),
                        "VILLAGER": (self.villagers, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Marry BACHELOR",
                    data={"BACHELOR": (self.marriage_candidates, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Give GIFT_COUNT gifts to VILLAGER",
                    data={
                        "GIFT_COUNT": (self.gift_counts, 1),
                        "VILLAGER": (self.villagers, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Community Center objectives
        if self.include_community_center:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the BUNDLE_ROOM bundles",
                    data={"BUNDLE_ROOM": (self.bundle_rooms, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete BUNDLE_COUNT community center bundles",
                    data={"BUNDLE_COUNT": (self.bundle_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ])

        # Collection objectives
        if self.include_collections:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the COLLECTION collection",
                    data={"COLLECTION": (self.collections, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Find ARTIFACT_COUNT artifacts for the museum",
                    data={"ARTIFACT_COUNT": (self.artifact_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Cooking objectives
        if self.include_cooking:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Cook DISH_COUNT different DISH recipes",
                    data={
                        "DISH_COUNT": (self.dish_counts, 1),
                        "DISH": (self.dish_categories, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Learn the recipe for RECIPE",
                    data={"RECIPE": (self.recipes, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Seasonal objectives
        if self.include_seasonal_goals:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete FESTIVAL during SEASON",
                    data={
                        "FESTIVAL": (self.festivals, 1),
                        "SEASON": (self.seasons, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Earn SEASONAL_PROFIT gold during SEASON",
                    data={
                        "SEASONAL_PROFIT": (self.seasonal_profits, 1),
                        "SEASON": (self.seasons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_farming(self) -> bool:
        return self.archipelago_options.stardew_include_farming.value

    @property
    def include_mining(self) -> bool:
        return self.archipelago_options.stardew_include_mining.value

    @property
    def include_fishing(self) -> bool:
        return self.archipelago_options.stardew_include_fishing.value

    @property
    def include_foraging(self) -> bool:
        return self.archipelago_options.stardew_include_foraging.value

    @property
    def include_relationships(self) -> bool:
        return self.archipelago_options.stardew_include_relationships.value

    @property
    def include_community_center(self) -> bool:
        return self.archipelago_options.stardew_include_community_center.value

    @property
    def include_collections(self) -> bool:
        return self.archipelago_options.stardew_include_collections.value

    @property
    def include_cooking(self) -> bool:
        return self.archipelago_options.stardew_include_cooking.value

    @property
    def include_seasonal_goals(self) -> bool:
        return self.archipelago_options.stardew_include_seasonal_goals.value

    @property
    def difficulty_level(self) -> str:
        return self.archipelago_options.stardew_difficulty_level.value

    # Data lists
    @staticmethod
    def crops() -> List[str]:
        return [
            "Parsnips", "Cauliflower", "Coffee Beans", "Kale", "Tulip Bulbs", "Potatoes", "Garlic",
            "Tomatoes", "Blueberries", "Hot Peppers", "Radishes", "Wheat", "Hops", "Corn",
            "Eggplant", "Pumpkins", "Bok Choy", "Yam", "Beets", "Cranberries", "Sunflowers",
            "Ancient Fruit", "Sweet Gem Berry", "Cactus Fruit", "Starfruit"
        ]

    @staticmethod
    def animal_types() -> List[str]:
        return ["Chicken", "Duck", "Rabbit", "Cow", "Goat", "Sheep", "Pig"]

    @staticmethod
    def ore_types() -> List[str]:
        return ["Copper", "Iron", "Gold", "Iridium", "Coal", "Quartz", "Geodes"]

    @staticmethod
    def fish() -> List[str]:
        return [
            "Sardine", "Carp", "Sunfish", "Catfish", "Largemouth Bass", "Salmon", "Tuna",
            "Red Mullet", "Herring", "Eel", "Octopus", "Red Snapper", "Squid", "Sea Cucumber",
            "Super Cucumber", "Ghostfish", "Stonefish", "Ice Pip", "Lava Eel"
        ]

    @staticmethod
    def legendary_fish() -> List[str]:
        return ["Legend", "Crimsonfish", "Angler", "Glacierfish", "Mutant Carp"]

    @staticmethod
    def forage_items() -> List[str]:
        return [
            "Wild Horseradish", "Daffodil", "Leek", "Dandelion", "Salmonberry", "Spring Onion",
            "Grape", "Spice Berry", "Sweet Pea", "Red Mushroom", "Purple Mushroom", "Fiddlehead Fern",
            "Blackberry", "Wild Plum", "Hazelnut", "Common Mushroom", "Winter Root", "Crystal Fruit",
            "Snow Yam", "Crocus", "Holly", "Coconut", "Cactus Fruit", "Cave Carrot"
        ]

    @staticmethod
    def tree_types() -> List[str]:
        return ["Oak", "Maple", "Pine", "Mahogany"]

    @staticmethod
    def villagers() -> List[str]:
        return [
            "Abigail", "Alex", "Caroline", "Clint", "Demetrius", "Dwarf", "Elliott", "Emily",
            "Evelyn", "George", "Gus", "Haley", "Harvey", "Jas", "Jodi", "Kent", "Krobus",
            "Leah", "Lewis", "Linus", "Marnie", "Maru", "Pam", "Penny", "Pierre", "Robin",
            "Sam", "Sebastian", "Shane", "Vincent", "Willy", "Wizard"
        ]

    @staticmethod
    def marriage_candidates() -> List[str]:
        return [
            "Abigail", "Alex", "Elliott", "Emily", "Haley", "Harvey",
            "Leah", "Maru", "Penny", "Sam", "Sebastian", "Shane"
        ]

    @staticmethod
    def bundle_rooms() -> List[str]:
        return ["Pantry", "Crafts Room", "Fish Tank", "Boiler Room", "Vault", "Bulletin Board"]

    @staticmethod
    def collections() -> List[str]:
        return ["Artifacts", "Minerals", "Fish", "Shipping"]

    @staticmethod
    def dish_categories() -> List[str]:
        return ["Breakfast", "Lunch", "Dinner", "Dessert", "Drink", "Snack"]

    @staticmethod
    def recipes() -> List[str]:
        return [
            "Fried Egg", "Omelet", "Salad", "Cheese Cauliflower", "Baked Fish", "Parsnip Soup",
            "Vegetable Medley", "Complete Breakfast", "Fried Calamari", "Strange Bun", "Lucky Lunch",
            "Fried Mushroom", "Pizza", "Bean Hotpot", "Glazed Yams", "Carp Surprise", "Hashbrowns",
            "Pancakes", "Salmon Dinner", "Fish Taco", "Crispy Bass", "Pepper Poppers", "Bread",
            "Tom Kha Soup", "Trout Soup", "Chocolate Cake", "Pink Cake", "Rhubarb Pie",
            "Cookie", "Spaghetti", "Fried Eel", "Spicy Eel", "Sashimi"
        ]

    @staticmethod
    def festivals() -> List[str]:
        return [
            "Egg Festival", "Flower Dance", "Luau", "Dance of the Moonlight Jellies",
            "Stardew Valley Fair", "Spirit's Eve", "Festival of Ice", "Feast of the Winter Star"
        ]

    @staticmethod
    def seasons() -> List[str]:
        return ["Spring", "Summer", "Fall", "Winter"]

    @staticmethod
    def monsters() -> List[str]:
        return [
            "Green Slime", "Frost Jelly", "Dust Spirit", "Bat", "Stone Golem", "Grub",
            "Fly", "Bug", "Rock Crab", "Lava Crab", "Shadow Brute", "Shadow Shaman",
            "Skeleton", "Metal Head", "Squid Kid"
        ]

    # Ranges
    @staticmethod
    def crop_quantities() -> range:
        return range(5, 50, 5)

    @staticmethod
    def profit_amounts() -> range:
        return range(1000, 10000, 1000)

    @staticmethod
    def animal_quantities() -> range:
        return range(2, 12, 2)

    @staticmethod
    def mine_floors() -> range:
        return range(20, 120, 20)

    @staticmethod
    def ore_quantities() -> range:
        return range(10, 100, 10)

    @staticmethod
    def monster_counts() -> range:
        return range(5, 50, 5)

    @staticmethod
    def fish_counts() -> range:
        return range(3, 20, 2)

    @staticmethod
    def crab_pot_counts() -> range:
        return range(10, 50, 5)

    @staticmethod
    def forage_quantities() -> range:
        return range(10, 50, 5)

    @staticmethod
    def tree_counts() -> range:
        return range(5, 30, 5)

    @staticmethod
    def heart_levels() -> range:
        return range(2, 10, 2)

    @staticmethod
    def gift_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def bundle_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def artifact_counts() -> range:
        return range(5, 30, 5)

    @staticmethod
    def dish_counts() -> range:
        return range(3, 15, 2)

    @staticmethod
    def seasonal_profits() -> range:
        return range(5000, 50000, 5000)

    @staticmethod
    def year_limits() -> range:
        return range(1, 4)


# Archipelago Options
class StardewIncludeFarming(DefaultOnToggle):
    """Include farming objectives (crops, animals, profit goals)."""
    display_name = "Include Farming Objectives"

class StardewIncludeMining(DefaultOnToggle):
    """Include mining objectives (floors, ores, monsters)."""
    display_name = "Include Mining Objectives"

class StardewIncludeFishing(DefaultOnToggle):
    """Include fishing objectives (fish catches, legendary fish, crab pots)."""
    display_name = "Include Fishing Objectives"

class StardewIncludeForaging(DefaultOnToggle):
    """Include foraging objectives (wild items, tree tapping)."""
    display_name = "Include Foraging Objectives"

class StardewIncludeRelationships(DefaultOnToggle):
    """Include relationship objectives (villager hearts, marriage, gifts)."""
    display_name = "Include Relationship Objectives"

class StardewIncludeCommunityCenterBundles(DefaultOnToggle):
    """Include Community Center bundle objectives."""
    display_name = "Include Community Center Bundles"

class StardewIncludeCollections(DefaultOnToggle):
    """Include collection objectives (museum, artifacts, minerals)."""
    display_name = "Include Collection Objectives"

class StardewIncludeCooking(DefaultOnToggle):
    """Include cooking objectives (recipes, dishes)."""
    display_name = "Include Cooking Objectives"

class StardewIncludeSeasonalGoals(DefaultOnToggle):
    """Include seasonal objectives (festivals, seasonal profits)."""
    display_name = "Include Seasonal Goals"

class StardewDifficultyLevel(TextChoice):
    """Sets the difficulty level for objectives and constraints."""
    display_name = "Difficulty Level"
    option_easy = 0
    option_normal = 1  
    option_hard = 2
    option_expert = 3
    default = 1
