from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle, Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class AnimalCrossingNewHorizonsArchipelagoOptions:
    acnh_include_daily_activities: ACNHIncludeDailyActivities
    acnh_include_collections: ACNHIncludeCollections
    acnh_include_island_development: ACNHIncludeIslandDevelopment
    acnh_include_villager_interactions: ACNHIncludeVillagerInteractions
    acnh_include_shopping: ACNHIncludeShopping
    acnh_include_crafting: ACNHIncludeCrafting
    acnh_include_seasonal_events: ACNHIncludeSeasonalEvents
    acnh_include_decorating: ACNHIncludeDecorating
    acnh_collection_focus: ACNHCollectionFocus


class AnimalCrossingNewHorizonsGame(Game):
    name = "Animal Crossing: New Horizons"
    platform = KeymastersKeepGamePlatforms.SW

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = AnimalCrossingNewHorizonsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective within TIMEFRAME",
                data={"TIMEFRAME": (self.timeframes, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective while wearing CLOTHING_TYPE",
                data={"CLOTHING_TYPE": (self.clothing_categories, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective during WEATHER weather",
                data={"WEATHER": (self.weather_types, 1)},
            ),
        ])
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Daily Activities
        if self.include_daily_activities:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Collect DAILY_COUNT DAILY_ITEM for COUNT consecutive days",
                    data={
                        "DAILY_COUNT": (self.daily_counts, 1),
                        "DAILY_ITEM": (self.daily_items, 1),
                        "COUNT": (self.consecutive_days, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete COUNT daily Nook Miles+ tasks",
                    data={"COUNT": (self.nook_miles_task_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Shake TREE_COUNT trees and collect COUNT TREE_ITEM",
                    data={
                        "TREE_COUNT": (self.tree_shake_counts, 1),
                        "COUNT": (self.tree_item_counts, 1),
                        "TREE_ITEM": (self.tree_items, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Collections
        if self.include_collections:
            collection_templates = []
            
            if self.collection_focus in ["All", "Bugs"]:
                collection_templates.append(
                    GameObjectiveTemplate(
                        label="Catch BUG and donate it to the museum",
                        data={"BUG": (self.bugs, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    )
                )
            
            if self.collection_focus in ["All", "Fish"]:
                collection_templates.append(
                    GameObjectiveTemplate(
                        label="Catch FISH and donate it to the museum",
                        data={"FISH": (self.fish, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    )
                )
            
            if self.collection_focus in ["All", "Sea Creatures"]:
                collection_templates.append(
                    GameObjectiveTemplate(
                        label="Dive for SEA_CREATURE and donate it to the museum",
                        data={"SEA_CREATURE": (self.sea_creatures, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    )
                )
            
            if self.collection_focus in ["All", "Fossils"]:
                collection_templates.append(
                    GameObjectiveTemplate(
                        label="Find and assess FOSSIL_COUNT fossils",
                        data={"FOSSIL_COUNT": (self.fossil_counts, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    )
                )
            
            collection_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the COLLECTION_TYPE section of the museum",
                    data={"COLLECTION_TYPE": (self.collection_types, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Collect COUNT different DIY recipes",
                    data={"COUNT": (self.diy_recipe_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])
            
            game_objective_templates.extend(collection_templates)

        # Island Development
        if self.include_island_development:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Build and place BUILDING on your island",
                    data={"BUILDING": (self.buildings, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create INFRASTRUCTURE_COUNT pieces of infrastructure",
                    data={"INFRASTRUCTURE_COUNT": (self.infrastructure_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Plant and grow FLOWER_COUNT FLOWER_TYPE flowers",
                    data={
                        "FLOWER_COUNT": (self.flower_counts, 1),
                        "FLOWER_TYPE": (self.flower_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Achieve STAR_RATING star island rating",
                    data={"STAR_RATING": (self.star_ratings, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Villager Interactions
        if self.include_villager_interactions:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach best friend status with VILLAGER",
                    data={"VILLAGER": (self.villager_personalities, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Give COUNT gifts to your villagers",
                    data={"COUNT": (self.gift_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Help VILLAGER_COUNT villagers with their requests",
                    data={"VILLAGER_COUNT": (self.villager_help_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Invite PERSONALITY_TYPE villager to your island",
                    data={"PERSONALITY_TYPE": (self.villager_personalities, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Shopping
        if self.include_shopping:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Purchase ITEM_COUNT items from SHOP",
                    data={
                        "ITEM_COUNT": (self.shopping_counts, 1),
                        "SHOP": (self.shops, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Spend BELLS_AMOUNT bells on CATEGORY items",
                    data={
                        "BELLS_AMOUNT": (self.spending_amounts, 1),
                        "CATEGORY": (self.item_categories, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Buy the complete FURNITURE_SET furniture set",
                    data={"FURNITURE_SET": (self.furniture_sets, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Crafting
        if self.include_crafting:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Craft COUNT CRAFT_CATEGORY items",
                    data={
                        "COUNT": (self.craft_counts, 1),
                        "CRAFT_CATEGORY": (self.craft_categories, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Craft CRAFT_ITEM using materials you collected yourself",
                    data={"CRAFT_ITEM": (self.craftable_items, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Customize COUNT items at a workbench",
                    data={"COUNT": (self.customization_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Seasonal Events
        if self.include_seasonal_events:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Participate in EVENT and collect EVENT_ITEM",
                    data={
                        "EVENT": (self.seasonal_events, 1),
                        "EVENT_ITEM": (self.event_items, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Collect COUNT seasonal DIY recipes during SEASON",
                    data={
                        "COUNT": (self.seasonal_diy_counts, 1),
                        "SEASON": (self.seasons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Decorating
        if self.include_decorating:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Design a ROOM_TYPE room with THEME theme",
                    data={
                        "ROOM_TYPE": (self.room_types, 1),
                        "THEME": (self.decoration_themes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create an outdoor area with OUTDOOR_THEME theme",
                    data={"OUTDOOR_THEME": (self.outdoor_themes, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Achieve HHA_SCORE HHA points in your home",
                    data={"HHA_SCORE": (self.hha_scores, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_daily_activities(self) -> bool:
        return self.archipelago_options.acnh_include_daily_activities.value

    @property
    def include_collections(self) -> bool:
        return self.archipelago_options.acnh_include_collections.value

    @property
    def include_island_development(self) -> bool:
        return self.archipelago_options.acnh_include_island_development.value

    @property
    def include_villager_interactions(self) -> bool:
        return self.archipelago_options.acnh_include_villager_interactions.value

    @property
    def include_shopping(self) -> bool:
        return self.archipelago_options.acnh_include_shopping.value

    @property
    def include_crafting(self) -> bool:
        return self.archipelago_options.acnh_include_crafting.value

    @property
    def include_seasonal_events(self) -> bool:
        return self.archipelago_options.acnh_include_seasonal_events.value

    @property
    def include_decorating(self) -> bool:
        return self.archipelago_options.acnh_include_decorating.value

    @property
    def collection_focus(self) -> str:
        return self.archipelago_options.acnh_collection_focus.value

    # Data lists
    @staticmethod
    def daily_items() -> List[str]:
        return [
            "Wood", "Softwood", "Hardwood", "Stone", "Clay", "Iron Nugget", 
            "Weeds", "Tree Branches", "Shells", "Fruit"
        ]

    @staticmethod
    def tree_items() -> List[str]:
        return ["Bells", "Furniture", "Wasps", "Tree Branches"]

    @staticmethod
    def bugs() -> List[str]:
        return [
            "Common Butterfly", "Yellow Butterfly", "Tiger Butterfly", "Peacock Butterfly",
            "Common Bluebottle", "Paper Kite Butterfly", "Great Purple Emperor", "Monarch Butterfly",
            "Emperor Butterfly", "Agrias Butterfly", "Rajah Brooke's Birdwing", "Queen Alexandra's Birdwing",
            "Moth", "Atlas Moth", "Madagascan Sunset Moth", "Long Locust", "Migratory Locust",
            "Rice Grasshopper", "Grasshopper", "Cricket", "Bell Cricket", "Mantis", "Orchid Mantis",
            "Honeybee", "Wasp", "Brown Cicada", "Robust Cicada", "Giant Cicada", "Walker Cicada",
            "Evening Cicada", "Cicada Shell", "Red Dragonfly", "Darner Dragonfly", "Banded Dragonfly",
            "Damselfly", "Firefly", "Mole Cricket", "Pondskater", "Diving Beetle", "Giant Water Bug",
            "Stinkbug", "Man-faced Stink Bug", "Ladybug", "Tiger Beetle", "Jewel Beetle", "Violin Beetle",
            "Citrus Long-horned Beetle", "Rosalia Batesi Beetle", "Blue Weevil Beetle", "Dung Beetle",
            "Earth-boring Dung Beetle", "Scarab Beetle", "Drone Beetle", "Goliath Beetle", "Saw Stag",
            "Miyama Stag", "Giant Stag", "Rainbow Stag", "Cyclommatus Stag", "Golden Stag",
            "Giraffe Stag", "Horned Dynastid", "Horned Atlas", "Horned Elephant", "Horned Hercules",
            "Walking Stick", "Walking Leaf", "Bagworm", "Ant", "Hermit Crab", "Wharf Roach",
            "Fly", "Mosquito", "Flea", "Snail", "Pill Bug", "Centipede", "Spider", "Tarantula", "Scorpion"
        ]

    @staticmethod
    def fish() -> List[str]:
        return [
            "Bitterling", "Pale Chub", "Crucian Carp", "Dace", "Carp", "Koi", "Goldfish", "Pop-eyed Goldfish",
            "Ranchu Goldfish", "Killifish", "Crawfish", "Soft-shelled Turtle", "Snapping Turtle", "Tadpole",
            "Frog", "Freshwater Goby", "Loach", "Catfish", "Giant Snakehead", "Bluegill", "Yellow Perch",
            "Black Bass", "Tilapia", "Pike", "Pond Smelt", "Sweetfish", "Cherry Salmon", "Char", "Golden Trout",
            "Stringfish", "Salmon", "King Salmon", "Mitten Crab", "Guppy", "Nibble Fish", "Angelfish",
            "Betta", "Neon Tetra", "Rainbowfish", "Piranha", "Arowana", "Dorado", "Gar", "Arapaima",
            "Saddled Bichir", "Sturgeon", "Sea Butterfly", "Sea Horse", "Clown Fish", "Surgeonfish",
            "Butterfly Fish", "Napoleonfish", "Zebra Turkeyfish", "Blowfish", "Puffer Fish", "Anchovy",
            "Horse Mackerel", "Barred Knifejaw", "Sea Bass", "Red Snapper", "Dab", "Olive Flounder",
            "Squid", "Moray Eel", "Ribbon Eel", "Tuna", "Blue Marlin", "Giant Trevally", "Mahi-mahi",
            "Ocean Sunfish", "Ray", "Saw Shark", "Hammerhead Shark", "Great White Shark", "Whale Shark",
            "Suckerfish", "Football Fish", "Oarfish", "Barreleye", "Coelacanth"
        ]

    @staticmethod
    def sea_creatures() -> List[str]:
        return [
            "Seaweed", "Sea Grapes", "Sea Cucumber", "Sea Pig", "Sea Star", "Sea Urchin",
            "Slate Pencil Urchin", "Sea Anemone", "Moon Jellyfish", "Sea Slug", "Pearl Oyster",
            "Mussel", "Oyster", "Scallop", "Whelk", "Turban Shell", "Abalone", "Gigas Giant Clam",
            "Chambered Nautilus", "Octopus", "Umbrella Octopus", "Vampire Squid", "Firefly Squid",
            "Gazami Crab", "Dungeness Crab", "Snow Crab", "Red King Crab", "Acorn Barnacle",
            "Spider Crab", "Tiger Prawn", "Sweet Shrimp", "Mantis Shrimp", "Spiny Lobster",
            "Lobster", "Giant Isopod", "Horseshoe Crab", "Sea Pineapple", "Spotted Garden Eel",
            "Flatworm"
        ]

    @staticmethod
    def villager_personalities() -> List[str]:
        return ["Lazy", "Jock", "Cranky", "Smug", "Normal", "Peppy", "Snooty", "Uchi"]

    @staticmethod
    def buildings() -> List[str]:
        return [
            "Nook's Cranny", "Able Sisters", "Museum", "Campsite", "Bridge", "Incline", 
            "Villager House", "Player House", "Resident Services"
        ]

    @staticmethod
    def flower_types() -> List[str]:
        return [
            "Tulips", "Pansies", "Cosmos", "Hyacinths", "Windflowers", 
            "Mums", "Lilies", "Roses"
        ]

    @staticmethod
    def shops() -> List[str]:
        return ["Nook's Cranny", "Able Sisters", "Kicks", "Redd's Treasure Trawler", "Nook Shopping"]

    @staticmethod
    def furniture_sets() -> List[str]:
        return [
            "Antique", "Cute", "Diner", "Imperial", "Ironwood", "Log", "Rattan", "Wooden",
            "Shell", "Bamboo", "Cherry Blossom", "Mushroom", "Frozen", "Golden"
        ]

    @staticmethod
    def craft_categories() -> List[str]:
        return ["Tools", "Furniture", "Decorations", "Clothing", "Equipment"]

    @staticmethod
    def craftable_items() -> List[str]:
        return [
            "Fishing Rod", "Net", "Axe", "Shovel", "Slingshot", "Watering Can", "DIY Workbench",
            "Simple Wooden Fence", "Wooden Chair", "Log Stool", "Campfire", "Tiki Torch"
        ]

    @staticmethod
    def seasonal_events() -> List[str]:
        return [
            "Bunny Day", "Cherry Blossom Festival", "May Day", "Wedding Season", "Summer Solstice",
            "Fireworks Festival", "Halloween", "Harvest Festival", "Turkey Day", "Toy Day",
            "New Year's", "Festivale"
        ]

    @staticmethod
    def event_items() -> List[str]:
        return [
            "Bunny Day Eggs", "Cherry Blossom Petals", "Summer Shells", "Acorns", "Pine Cones",
            "Snowflakes", "Ornaments", "Festivale Feathers"
        ]

    @staticmethod
    def room_types() -> List[str]:
        return ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Study", "Music Room", "Gym"]

    @staticmethod
    def decoration_themes() -> List[str]:
        return [
            "Modern", "Rustic", "Elegant", "Cute", "Cool", "Spooky", "Natural", "Sci-Fi",
            "Retro", "Traditional", "Tropical", "Winter", "Zen", "Gothic"
        ]

    @staticmethod
    def outdoor_themes() -> List[str]:
        return [
            "Garden", "Playground", "Cafe", "Market", "Beach", "Forest", "Orchard", 
            "Park", "Museum Area", "Residential Area"
        ]

    @staticmethod
    def collection_types() -> List[str]:
        return ["Bugs", "Fish", "Sea Creatures", "Fossils", "Art"]

    @staticmethod
    def item_categories() -> List[str]:
        return ["Furniture", "Clothing", "Tools", "Materials", "Food", "Decorations"]

    @staticmethod
    def seasons() -> List[str]:
        return ["Spring", "Summer", "Fall", "Winter"]

    @staticmethod
    def timeframes() -> List[str]:
        return ["1 day", "3 days", "1 week", "2 weeks"]

    @staticmethod
    def clothing_categories() -> List[str]:
        return ["Hat", "Dress", "Shirt", "Pants", "Shoes", "Accessories", "Full Outfit"]

    @staticmethod
    def weather_types() -> List[str]:
        return ["Sunny", "Cloudy", "Rainy", "Snowy"]

    # Ranges
    @staticmethod
    def daily_counts() -> range:
        return range(5, 30, 5)

    @staticmethod
    def consecutive_days() -> range:
        return range(3, 14, 2)

    @staticmethod
    def nook_miles_task_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def tree_shake_counts() -> range:
        return range(10, 50, 5)

    @staticmethod
    def tree_item_counts() -> range:
        return range(1, 5)

    @staticmethod
    def fossil_counts() -> range:
        return range(3, 15, 2)

    @staticmethod
    def diy_recipe_counts() -> range:
        return range(10, 50, 5)

    @staticmethod
    def infrastructure_counts() -> range:
        return range(3, 15, 2)

    @staticmethod
    def flower_counts() -> range:
        return range(10, 50, 5)

    @staticmethod
    def star_ratings() -> range:
        return range(3, 6)

    @staticmethod
    def gift_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def villager_help_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def shopping_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def spending_amounts() -> range:
        return range(10000, 100000, 10000)

    @staticmethod
    def craft_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def customization_counts() -> range:
        return range(3, 15, 2)

    @staticmethod
    def seasonal_diy_counts() -> range:
        return range(3, 12, 2)

    @staticmethod
    def hha_scores() -> range:
        return range(50000, 200000, 25000)


# Archipelago Options
class ACNHIncludeDailyActivities(Toggle):
    """Include daily activity objectives (resource gathering, tasks)."""
    display_name = "Include Daily Activities"
    default = True

class ACNHIncludeCollections(Toggle):
    """Include collection objectives (museum donations, critterpedia)."""
    display_name = "Include Collection Activities"
    default = True

class ACNHIncludeIslandDevelopment(Toggle):
    """Include island development objectives (buildings, infrastructure, rating)."""
    display_name = "Include Island Development"
    default = True

class ACNHIncludeVillagerInteractions(Toggle):
    """Include villager interaction objectives (friendship, gifts, help)."""
    display_name = "Include Villager Interactions"
    default = True

class ACNHIncludeShopping(Toggle):
    """Include shopping objectives (purchases, collections, sets)."""
    display_name = "Include Shopping Activities"
    default = True

class ACNHIncludeCrafting(Toggle):
    """Include crafting objectives (DIY recipes, customization)."""
    display_name = "Include Crafting Activities"
    default = True

class ACNHIncludeSeasonalEvents(Toggle):
    """Include seasonal event objectives (limited-time activities)."""
    display_name = "Include Seasonal Events"
    default = False  # Keep as False - seasonal events are more specialized/harder

class ACNHIncludeDecorating(Toggle):
    """Include decorating objectives (room design, themes, HHA scoring)."""
    display_name = "Include Decorating Activities"
    default = True

class ACNHCollectionFocus(Choice):
    """Focus collection objectives on specific categories."""
    display_name = "Collection Focus"
    option_all = "All"
    option_bugs = "Bugs"
    option_fish = "Fish"
    option_sea_creatures = "Sea Creatures"
    option_fossils = "Fossils"
    default = option_all
