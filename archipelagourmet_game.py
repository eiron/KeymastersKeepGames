from __future__ import annotations

import functools
from typing import List, Dict, Set

from dataclasses import dataclass

from Options import Range, OptionList

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


# Option Dataclass
@dataclass
class ArchipelagourmetArchipelagoOptions:
    archipelagourmet_recipes: ArchipelagourmetRecipes
    archipelagourmet_recipes_weight: ArchipelagourmetRecipesWeight
    archipelagourmet_takeaway_options: ArchipelagourmetTakeawayOptions
    archipelagourmet_takeaway_options_weight: ArchipelagourmetTakeawayOptionsWeight
    archipelagourmet_restaurant_options: ArchipelagourmetRestaurantOptions
    archipelagourmet_restaurant_options_weight: ArchipelagourmetRestaurantOptionsWeight

# Main Class
class ArchipelagourmetGame(Game):
    name = "Archipelagourmet"
    platform = KeymastersKeepGamePlatforms.META

    is_adult_only_or_unrated = False

    options_cls = ArchipelagourmetArchipelagoOptions

    # Main Objectives
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        if self.recipes:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="Make and eat the following dish: RECIPES",
                    data={
                        "RECIPES": (self.recipes, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.recipesweight,
                ),
            )

        if self.takeaways:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="Order the following takeaway option: TAKEAWAYS",
                    data={
                        "TAKEAWAYS": (self.takeaways, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.takeawaysweight,
                ),
            )

        if self.restaurants:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="Order the following restaurant option: RESTAURANTS",
                    data={
                        "RESTAURANTS": (self.restaurants, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.restaurantsweight,
                ),
    )
        
        return game_objective_templates

    @property
    def recipesweight(self) -> int:
        return self.archipelago_options.archipelagourmet_recipes_weight.value
    
    @property
    def takeawaysweight(self) -> int:
        return self.archipelago_options.archipelagourmet_takeaway_options_weight.value
    
    @property
    def restaurantsweight(self) -> int:
        return self.archipelago_options.archipelagourmet_restaurant_options_weight.value

    def recipes(self) -> List[str]:
        recipes: List[str] = list(self.archipelago_options.archipelagourmet_recipes.value)
        return sorted(recipes)
    
    def takeaways(self) -> List[str]:
        takeaways: List[str] = list(self.archipelago_options.archipelagourmet_takeaway_options.value)
        return sorted(takeaways)
    
    def restaurants(self) -> List[str]:
        restaurants: List[str] = list(self.archipelago_options.archipelagourmet_restaurant_options.value)
        return sorted(restaurants)

# Archipelago Options
class ArchipelagourmetRecipes(OptionList):
    """
    Indicates which recipes the player could make.
    The player is free to add or remove any options they like. Multiple appearances will function as weightings for the options provided.
    """

    display_name = "Archipelagourmet Recipes"
    default = [
        "Spaghetti Carbonara",
        "Chicken Tikka Masala",
        "Beef Stroganoff",
        "Vegetable Stir Fry",
    ]

class ArchipelagourmetTakeawayOptions(OptionList):
    """
    Indicates which takeaway options the player could order.
    The player is free to add or remove any options they like. Multiple appearances will function as weightings for the options provided.
    """

    display_name = "Archipelagourmet Takeaway Options"
    default = [
        "Pizza",
        "Sushi",
        "Chinese Takeout",
        "Indian Curry",
    ]

class ArchipelagourmetRestaurantOptions(OptionList):
    """
    Indicates which restaurant options the player could order.
    The player is free to add or remove any options they like. Multiple appearances will function as weightings for the options provided.
    """

    display_name = "Archipelagourmet Restaurant Options"
    default = [
        "Italian Bistro",
        "Sushi Bar",
        "Chinese Restaurant",
        "Indian Restaurant",
    ]

class ArchipelagourmetRecipesWeight(Range):
    """
    The weighting for recipes you have to make yourself (0-100).
    """
    display_name = "Archipelagourmet Recipes Weight"
    default = 25
    range_start = 0
    range_end = 100

class ArchipelagourmetTakeawayOptionsWeight(Range):
    """
    The weighting for takeaway options (0-100).
    """
    display_name = "Archipelagourmet Takeaway Options Weight"
    default = 3
    range_start = 0
    range_end = 100

class ArchipelagourmetRestaurantOptionsWeight(Range):
    """
    The weighting for restaurant options (0-100).
    """
    display_name = "Archipelagourmet Restaurant Options Weight"
    default = 2
    range_start = 0
    range_end = 100
