from __future__ import annotations

import functools
from typing import List, Dict, Set

from dataclasses import dataclass

from Options import Toggle, Range, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

# Option Dataclass
@dataclass
class CookServeDelicious2ArchipelagoOptions:
    cook_serve_delicious_2_max_yum_level: CookServeDelicious2MaxYumLevel
    cook_serve_delicious_2_display_yum_level_requirements: CookServeDelicious2DisplayYumLevelRequirements
    cook_serve_delicious_2_include_locked_foods: CookServeDelicious2IncludeLockedFoods
    cook_serve_delicious_2_game_types: CookServeDelicious2GameTypes
    cook_serve_delicious_2_csd_modes: CookServeDelicious2CSDModes

# Main Class
class CookServeDelicious2Game(Game):
    name = "Cook, Serve, Delicious! 2!!"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE
    ]

    is_adult_only_or_unrated = False

    options_cls = CookServeDelicious2ArchipelagoOptions

    @property
    def game_types(self) -> Set[str]:
        return self.archipelago_options.cook_serve_delicious_2_game_types.value

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = []

        include_csd = "CSD" in self.game_types
        include_cfh = "Chef for Hire" in self.game_types

        if include_csd:
            objectives.extend(self.csd_objectives())

        if include_cfh:
            objectives.append(
                GameObjectiveTemplate(
                    label="Get a Perfect Day in SHIFT",
                    data={
                        "SHIFT": (self.shifts, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    # Set weight for 50/50 chance between Chef for Hire and CSD objectives
                    weight=max(sum(o.weight for o in objectives if self.archipelago_options.include_difficult_objectives or not o.is_difficult), 1),
                ),
            )

        return objectives

    def csd_objectives(self) -> List[GameObjectiveTemplate]:
        """ Based on the configuration, generates a list of objective templates for CSD mode. """
        objectives = []
        for entree_count in range(1, self.csd_max_entrees() + 1):
            for side_count in range(1, self.csd_max_sides() + 1):
                for drink_count in range(1, self.csd_max_drinks() + 1):
                    for mode in self.csd_modes():
                        objectives.append(GameObjectiveTemplate(
                            label=f"Get a Perfect Day in Cook Serve Delicious in {mode} mode with entrees: [ENTREES], sides: [SIDES], drinks: [DRINKS]",
                            data={
                                "ENTREES": (self.csd_entrees, entree_count),
                                "SIDES": (self.csd_sides, side_count),
                                "DRINKS": (self.csd_drinks, drink_count),
                            },
                            is_time_consuming=False,
                            is_difficult=mode == "Stress",
                            weight=entree_count, # Favor higher entree counts
                        ))
        return objectives

    @property
    def max_yum_level(self) -> int:
        return self.archipelago_options.cook_serve_delicious_2_max_yum_level.value

    @property
    def display_yum_level(self) -> int:
        return self.archipelago_options.cook_serve_delicious_2_display_yum_level_requirements.value

    def shifts(self) -> List[str]:
        result = []
        for restaurant, levels in self.chef_for_hire_level_requirements.items():
            for index, level in enumerate(levels):
                if level <= self.max_yum_level:
                    result.append(f"{restaurant} - Shift {index + 1}{ ' (Yum Level ' + str(level) + ')' if self.display_yum_level else ''}")
        return result

    @functools.cached_property
    def chef_for_hire_level_requirements(self) -> Dict[str, List[int]]:
        """A dictionary mapping each Chef for Hire restaurant to the required Yum Level for each shift."""
        return {
            "MAX Wieners": [0, 1, 2, 5, 8, 9, 10, 15],
            "Biggs Burger": [3, 4, 6, 9, 11, 13, 16, 18, 22],
            "Eaty's": [1, 3, 5, 7, 8, 13, 15, 17, 21, 22, 26, 29, 32, 33, 39, 40],
            "Chilly Bowl": [2, 6, 7, 12, 14, 17, 19, 23],
            "Chinese Food": [8, 10, 11, 12, 14, 16, 18, 19, 20, 23, 25, 27, 30, 34],
            "Breakfast & Breakloose": [8, 10, 11, 12, 13, 16, 18, 19, 20, 23, 24, 25, 27, 28, 30, 31],
            "Gree/Itali Casual Dining": [11, 12, 15, 16, 18, 20, 22, 24, 26, 28, 29, 31],
            "Pizza That!": [12, 13, 17, 19, 21, 22, 24, 26, 32],
            "All The Sports Grill": [9, 9, 11, 14, 17, 19, 20, 24, 25, 27, 30, 33, 36, 41],
            "Esteban's": [26, 28, 29, 31, 33, 35, 36, 38, 40, 42, 44, 45, 47, 49, 51],
            "Pie Right": [24, 25, 27, 30, 32, 34, 35, 37, 41, 46],
            "FireKickers": [19, 21, 23, 28, 29, 33, 35, 37, 39, 41, 43, 45, 46, 48],
            "Food Shackers": [20, 25, 26, 29, 31, 32, 34, 36, 38, 40, 42, 44],
            "Slammy's Old Fashioned BBQ": [22, 23, 27, 31, 34, 36, 39, 42, 45, 47, 49, 52, 54, 59],
            "Burrito Time": [16, 18, 22, 28, 35, 40, 46, 49, 50, 52, 53, 57],
            "Contrast Coffee Company": [6, 8, 10, 19, 23, 30, 37, 43, 49, 59, 64, 69, 72, 76],
            "Planet Blue": [34, 38, 47, 61, 63, 65, 73, 77, 78, 84],
            "SubSolutions": [17, 21, 26, 28, 37, 38, 41, 43, 44, 48],
            "The World Tour": [15, 16, 18, 30, 33, 35, 37, 39, 43, 46, 50, 53],
            "Oooh, Organic!": [30, 32, 35, 38, 42, 44, 47, 50],
            "Poppers & Crunchies": [27, 33, 36, 40, 43, 45, 50, 52, 55],
            "The Deep All-You-Can-Eat": [29, 35, 38, 46, 48, 51, 56, 58, 61, 64],
            "The Far East": [31, 37, 38, 45, 49, 53, 57, 60, 62, 67],
            "Good Japan": [32, 37, 40, 43, 48, 51, 55, 59, 63, 65, 70],
            "E": [33, 39, 42, 47, 49, 52, 54, 57, 60, 63, 68, 71, 73, 75, 77, 79],
            "Sushi Nest": [21, 31, 36, 41, 53, 58, 66, 69, 72, 78],
            "Welcome to Tasteville": [46, 50, 56, 61, 64, 69, 72, 74, 76, 80, 82, 84, 86, 89],
            "XLR Purple": [39, 41, 52, 54, 62, 65, 67, 70, 74, 81, 83, 87, 90, 92],
            "Secrets of the Deep": [44, 48, 51, 55, 57, 66, 68, 73, 75, 78, 80, 85, 88, 91],
            "Absolutely": [45, 47, 51, 54, 58, 66, 71, 76, 77, 79, 81, 82],
            "Sebucosto 1991": [48, 55, 56, 59, 62, 65, 68, 74, 80, 83, 86, 93],
            "UEIYAV": [56, 60, 63, 64, 67, 71, 75, 81, 82, 85, 87, 94, 95, 97, 98],
            "Executive's Decision": [70, 73, 79, 80, 84, 88, 89, 91, 92, 93, 95, 96, 97, 98, 99, 100]
        }

    def csd_modes(self) -> List[str]:
        return sorted(self.archipelago_options.cook_serve_delicious_2_csd_modes.value)

    def csd_max_entrees(self):
        """
        Returns the maximum number of entrees that can be served in a single shift.
        This is based on the maximum Yum Level.
        """
        if self.max_yum_level < 4:
            return 3
        elif self.max_yum_level < 14:
            return 4
        elif self.max_yum_level < 18:
            return 5
        else:
            return 6

    def csd_max_sides(self):
        """
        Returns the maximum number of sides that can be served in a single shift.
        This is based on the maximum Yum Level.
        """
        if self.max_yum_level < 7:
            return 1
        elif self.max_yum_level < 21:
            return 2
        else:
            return 3

    def csd_max_drinks(self):
        """
        Returns the maximum number of drinks that can be served in a single shift.
        This is based on the maximum Yum Level.
        """
        if self.max_yum_level < 11:
            return 1
        else:
            return 2

    def csd_entrees(self) -> List[str]:
        """
        Returns a list of entrees that will be included in the CSD food pool.
        This includes both initially unlocked and locked entrees based on the configuration.
        """
        if self.archipelago_options.cook_serve_delicious_2_include_locked_foods.value:
            return self.csd_unlocked_entrees + self.csd_locked_entrees
        else:
            return self.csd_unlocked_entrees

    def csd_sides(self) -> List[str]:
        """
        Returns a list of sides that will be included in the CSD food pool.
        This includes both initially unlocked and locked sides based on the configuration.
        """
        if self.archipelago_options.cook_serve_delicious_2_include_locked_foods.value:
            return self.csd_unlocked_sides + self.csd_locked_sides
        else:
            return self.csd_unlocked_sides

    def csd_drinks(self) -> List[str]:
        """
        Returns a list of drinks that will be included in the CSD food pool.
        This includes both initially unlocked and locked drinks based on the configuration.
        """
        if self.archipelago_options.cook_serve_delicious_2_include_locked_foods.value:
            return self.csd_unlocked_drinks + self.csd_locked_drinks
        else:
            return self.csd_unlocked_drinks

    @functools.cached_property
    def csd_unlocked_entrees(self) -> List[str]:
        """Entrees that are initially unlocked or can be purchased."""
        return [
            "Chili",
            "Chowder",
            "Gumbo",
            "Soup",
            "Stew",
            "Chicken Strips",
            "Corndogs",
            "Egg Drop Soup",
            "French Toast",
            "Fried Shrimp",
            "Lasagna",
            "Brisket Slices",
            "Turkey Slices",
            "Ham Slices",
            "Sausage Slices",
            "Muffins",
            "Oatmeal",
            "Pizza by the Slice",
            "Pretzel",
            "Steak Fingers",
            "Tiramisu",
            "Tres Leches",
            "Griddle Eggs",
            "Bean Burger",
            "Breakfast Sandwich",
            "Chicken Sandwich",
            "Chimichanga",
            "Funnel Cake",
            "Hamburger",
            "Hotdog",
            "Japanese Fried Rice",
            "Grilled Chicken Sandwich",
            "Lamb Chops",
            "Meatloaf",
            "Pancakes",
            "Quesadilla",
            "Ramen",
            "Ribs",
            "Salisbury Steak",
            "Sopapillas",
            "Spinach Veggie Pasta",
            "Steak",
            "Tacos",
            "Traditional Hot Wings",
            "Turkey Leg",
            "Wok Dish: Beef and Pork",
            "Wok Dish: Chicken",
            "Wok Dish: Shrimp and Veg.",
            "Baked Hot Wings",
            "Calzone",
            "Cereal",
            "Chicken Breast",
            "Club Sandwich",
            "Corn Chip Pie",
            "Crab Cakes",
            "Crab Legs",
            "Creme Brulee",
            "Dessert Shooters",
            "Fresh Fish",
            "Fried Chicken",
            "Hiyayakko Tofu",
            "Ice Cream Sundae",
            "Japanese Crepe",
            "Steamed Momos",
            "Okonomiyaki",
            "Pig's Blood Cake",
            "Pizza",
            "Pork Loin",
            "Salad",
            "Samosas",
            "Small Custom Sub",
            "Sushi",
            "Tabbouleh",
            "Tamales",
            "Taiwanese Shaved Ice",
            "Stadium Nachos",
            "Spaghetti",
            "Frozen Lattes",
            "Hot Lattes",
            "Iced Lattes",
            "Milkshakes",
            "Smoothies",
            "Espresso Shots",
            "Enchiladas",
            "Htapothi sti Skhara",
            "Rote Grutze",
            "Organic Salad",
            "Ice Cream Scoops",
            "Glazed Donut",
            "Specialty Donuts",
            "Frozen Bananas",
            "Cinnamon Buns",
            "Brownies",
        ]

    @functools.cached_property
    def csd_locked_entrees(self) -> List[str]:
        """Entrees that are locked and can only be acquired through randomized unlocks."""
        return [
            "Biscuit and Gravy",
            "Chicken Nuggets",
            "Chopped Brisket Sandwich",
            "Fried Fish",
            "Prime Rib",
            "Roast Beef Sandwich",
            "Slice of Pie",
            "Breakfast Burrito",
            "Burrito",
            "Cannoli",
            "Chicken Fried Meats",
            "Chow Mein",
            "Filet Mignon",
            "Veal Marsala",
            "Lobster",
            "Deluxe Nachos",
            "Omelette",
            "Pasta",
            "Pulled Pork Sandwich",
            "Sausage and Sauerkraut",
            "Sizzling Fajitas",
            "Sliders",
            "Stuffed Peppers",
            "Tostadas",
            "Waffles",
            "Yaki Tomorokoshi",
            "Bananas Foster",
            "Beef Wellington",
            "Carpaccio",
            "Eggplant Parmigiana",
            "Escargot",
            "Gazpacho",
            "Oysters",
            "Pies",
            "Pot Pie",
            "Quiche",
            "Risotto",
            "Sashimi",
            "Shish Kabob",
            "Souffle",
            "Steamed Mussels",
            "Sub Sandwich",
            "Whole Cakes",
            "Yakizakana",
            "Agedashi Tofu",
        ]

    @functools.cached_property
    def csd_unlocked_sides(self) -> List[str]:
        """Sides that are initially unlocked or can be purchased."""
        return [
            "Asparagus",
            "Bacon",
            "Baked Potato",
            "Black Beans",
            "Broccoli",
            "Brussels Sprouts",
            "Side Chow Mein",
            "Corn on the Cob",
            "Sauerkraut",
            "Dinner Rolls",
            "Edamame",
            "Side Egg Drop Soup",
            "Egg Rolls",
            "Fries",
            "Fried Okra",
            "Fruit Spread",
            "German Red Cabbage",
            "Green Beans",
            "Hash Browns",
            "Japanese Fried Rice Side",
            "Kale Chips",
            "Mac n' Cheese",
            "Mashed Potatoes",
            "Mexican Rice",
            "Onion Rings",
            "Pakora",
            "Peas",
            "Pinto Beans",
            "Potato Salad",
            "Black Rice",
            "Refried Beans",
            "Brown Rice",
            "Sausage Links",
            "Scrambled Eggs",
            "Side Chili",
            "Side Chowder",
            "Side Gumbo",
            "Side Soup",
            "Side Stew",
            "Side Salad",
            "Grits",
            "Steamed Vegetables",
            "Tater Tots",
            "Toast",
            "Tuscan Beans",
            "Cookies",
            "White Rice",
            "Wild Rice",
            "Marshmallow Squares",
            "Croissants",
            "Specialty Fries",
            "Side Oatmeal",
        ]

    @functools.cached_property
    def csd_locked_sides(self) -> List[str]:
        """Sides that are locked and can only be acquired through randomized unlocks."""
        return [
            "Grilled Fennel",
            "Kimchi",
            "Onigiri",
            "Roasted Cauliflower",
            "Stuffed Artichokes",
            "Tazukuri",
            "Boiled Eggs",
            "Fried Seafood Sides",
        ]

    @functools.cached_property
    def csd_unlocked_drinks(self) -> List[str]:
        """Drinks that are initially unlocked or can be purchased."""
        return [
            "Beer",
            "Coffee",
            "Iced Tea",
            "Juice Bar",
            "Fresh Lemonade",
            "Soda Fountain",
            "Horchata",
            "Hot Tea",
        ]

    @functools.cached_property
    def csd_locked_drinks(self) -> List[str]:
        """Drinks that are locked and can only be acquired through randomized unlocks."""
        return [
            "Craft Beer",
            "Pineapple Juice",
            "Red Wine",
            "White Wine",
        ]

class CookServeDelicious2MaxYumLevel(Range):
    """
    The maximum Yum Level that will be required for trials.

    You should either have a save with at least this Yum Level, or be willing to grind to this Yum Level.
    """
    display_name = "Max Yum Level"
    range_start = 10
    range_end = 125
    default = 50

class CookServeDelicious2DisplayYumLevelRequirements(Toggle):
    """
    Displays the Yum Level requirements for each Chef for Hire shift on the trial description.

    This may be considered spoilers but can be helpful for knowing what level you need to reach for each trial.
    """
    display_name = "Display Yum Level Requirements"
    default = False

class CookServeDelicious2IncludeLockedFoods(Toggle):
    """
    Include locked entrees, sides, and drinks in the pool for CSD mode trials.

    By default, only those foods you start with or can purchase are included, if you enable this option foods that are unlocked
    randomly at milestones will be included. It is recommended to only enable this if you have a save with all foods unlocked
    or are willing to grind to unlock them.
    """
    display_name = "Include Locked Foods"
    default = False

class CookServeDelicious2GameTypes(OptionSet):
    """
    Indicates which game types can appear in Cook, Serve, Delicious! 2!! objectives.

    CSD: Cook, Serve, Delicious mode where you build your own menu and serve customers.
    Chef for Hire: Work shifts at various restaurants around the city.
    """
    display_name = "Game Types"
    valid_keys = {
        "CSD",
        "Chef for Hire",
    }
    default = {
        "CSD",
        "Chef for Hire",
    }

class CookServeDelicious2CSDModes(OptionSet):
    """
    Indicates which CSD modes can appear in Cook, Serve, Delicious! objectives.
    """
    display_name = "CSD Modes"
    valid_keys = {
        "Classic",
        "Standard",
        "Stress",
        "Zen",
    }
    default = {
        "Classic",
        "Standard",
        "Stress",
        "Zen",
    }