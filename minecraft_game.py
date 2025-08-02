from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle, Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MinecraftArchipelagoOptions:
    minecraft_include_survival_basics: MinecraftIncludeSurvivalBasics
    minecraft_include_building_projects: MinecraftIncludeBuildingProjects
    minecraft_include_exploration: MinecraftIncludeExploration
    minecraft_include_redstone_engineering: MinecraftIncludeRedstoneEngineering
    minecraft_include_farming_automation: MinecraftIncludeFarmingAutomation
    minecraft_include_boss_progression: MinecraftIncludeBossProgression
    minecraft_include_collection_goals: MinecraftIncludeCollectionGoals
    minecraft_include_challenge_runs: MinecraftIncludeChallengeRuns
    minecraft_game_mode_focus: MinecraftGameModeFocus
    minecraft_difficulty_preference: MinecraftDifficultyPreference


class MinecraftGame(Game):
    name = "Minecraft"
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

    options_cls = MinecraftArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective in GAME_MODE mode",
                data={"GAME_MODE": (self.game_modes, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without using RESTRICTED_MATERIAL",
                data={"RESTRICTED_MATERIAL": (self.restriction_materials, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective in a BIOME_TYPE biome only",
                data={"BIOME_TYPE": (self.biome_restrictions, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective using only TOOL_TYPE tools",
                data={"TOOL_TYPE": (self.tool_types, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective within DAY_LIMIT in-game days",
                data={"DAY_LIMIT": (self.day_limits, 1)},
            ),
        ])
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Survival Basics
        if self.include_survival_basics:
            survival_templates = []
            
            if self.difficulty_preference in ["All", "Hard"]:
                survival_templates.extend([
                    GameObjectiveTemplate(
                        label="Survive NIGHT_COUNT nights without sleeping",
                        data={"NIGHT_COUNT": (self.night_survival_counts, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Defeat HOSTILE_COUNT hostile mobs in one night",
                        data={"HOSTILE_COUNT": (self.hostile_mob_counts, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    ),
                ])
            
            survival_templates.extend([
                GameObjectiveTemplate(
                    label="Craft and use TOOL_SET tools",
                    data={"TOOL_SET": (self.tool_sets, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Build a shelter with ROOM_COUNT rooms",
                    data={"ROOM_COUNT": (self.room_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Establish a sustainable food source producing FOOD_AMOUNT food",
                    data={"FOOD_AMOUNT": (self.food_amounts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Mine and collect ORE_AMOUNT MATERIAL_TYPE",
                    data={
                        "ORE_AMOUNT": (self.ore_amounts, 1),
                        "MATERIAL_TYPE": (self.mineable_materials, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Reach the Nether and establish a base",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])
            
            game_objective_templates.extend(survival_templates)

        # Building Projects
        if self.include_building_projects:
            building_templates = []
            
            if self.game_mode_focus in ["All", "Creative"]:
                building_templates.extend([
                    GameObjectiveTemplate(
                        label="Build a massive STRUCTURE using BLOCK_COUNT+ blocks",
                        data={
                            "STRUCTURE": (self.massive_structures, 1),
                            "BLOCK_COUNT": (self.massive_block_counts, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Create a detailed replica of REPLICA_SUBJECT",
                        data={"REPLICA_SUBJECT": (self.replica_subjects, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                ])
            
            building_templates.extend([
                GameObjectiveTemplate(
                    label="Build a functional BUILDING_TYPE",
                    data={"BUILDING_TYPE": (self.functional_buildings, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Construct a ARCHITECTURAL_STYLE style building",
                    data={"ARCHITECTURAL_STYLE": (self.architectural_styles, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create a themed area dedicated to THEME",
                    data={"THEME": (self.building_themes, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Build a multi-level structure with LEVEL_COUNT levels",
                    data={"LEVEL_COUNT": (self.level_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])
            
            game_objective_templates.extend(building_templates)

        # Exploration
        if self.include_exploration:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Discover and explore BIOME_COUNT different biomes",
                    data={"BIOME_COUNT": (self.biome_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Find and loot STRUCTURE_COUNT STRUCTURE_TYPE structures",
                    data={
                        "STRUCTURE_COUNT": (self.structure_counts, 1),
                        "STRUCTURE_TYPE": (self.lootable_structures, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Travel DISTANCE blocks from spawn",
                    data={"DISTANCE": (self.travel_distances, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Locate and map LANDMARK_COUNT natural landmarks",
                    data={"LANDMARK_COUNT": (self.landmark_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Explore the DIMENSION dimension completely",
                    data={"DIMENSION": (self.dimensions, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Find and tame ANIMAL_COUNT ANIMAL_TYPE",
                    data={
                        "ANIMAL_COUNT": (self.animal_counts, 1),
                        "ANIMAL_TYPE": (self.tameable_animals, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Redstone Engineering
        if self.include_redstone_engineering:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Build a working REDSTONE_CONTRAPTION",
                    data={"REDSTONE_CONTRAPTION": (self.redstone_contraptions, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create an automated AUTOMATION_TYPE system",
                    data={"AUTOMATION_TYPE": (self.automation_systems, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Build a redstone computer that performs COMPUTATION",
                    data={"COMPUTATION": (self.redstone_computations, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Design a compact redstone circuit in CIRCUIT_SIZE blocks",
                    data={"CIRCUIT_SIZE": (self.circuit_sizes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create a redstone-powered transportation system",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Farming & Automation
        if self.include_farming_automation:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Build a fully automated CROP_TYPE farm",
                    data={"CROP_TYPE": (self.farmable_crops, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create a MOB_TYPE mob farm producing ITEM_RATE items per hour",
                    data={
                        "MOB_TYPE": (self.farmable_mobs, 1),
                        "ITEM_RATE": (self.production_rates, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Establish a breeding operation with ANIMAL_BREEDING_COUNT BREEDING_ANIMAL",
                    data={
                        "ANIMAL_BREEDING_COUNT": (self.breeding_counts, 1),
                        "BREEDING_ANIMAL": (self.breedable_animals, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Build an item sorting system with SORT_CATEGORY_COUNT categories",
                    data={"SORT_CATEGORY_COUNT": (self.sorting_categories, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create a renewable resource system for RENEWABLE_RESOURCE",
                    data={"RENEWABLE_RESOURCE": (self.renewable_resources, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Boss Progression
        if self.include_boss_progression:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Defeat the Ender Dragon",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Defeat the Wither boss",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Defeat ELDER_GUARDIAN_COUNT Elder Guardians",
                    data={"ELDER_GUARDIAN_COUNT": (self.elder_guardian_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Defeat RAID_COUNT successful raids",
                    data={"RAID_COUNT": (self.raid_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Obtain the Dragon Egg",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete all advancement categories",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Collection Goals
        if self.include_collection_goals:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Collect all COLLECTION_CATEGORY items",
                    data={"COLLECTION_CATEGORY": (self.collection_categories, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Build a museum displaying EXHIBIT_COUNT different items",
                    data={"EXHIBIT_COUNT": (self.exhibit_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Obtain ENCHANTED_BOOK_COUNT different enchanted books",
                    data={"ENCHANTED_BOOK_COUNT": (self.enchanted_book_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Collect all MUSIC_DISC_COUNT music discs",
                    data={"MUSIC_DISC_COUNT": (self.music_disc_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Acquire RARE_ITEM",
                    data={"RARE_ITEM": (self.rare_items, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Challenge Runs
        if self.include_challenge_runs:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete a CHALLENGE_TYPE challenge run",
                    data={"CHALLENGE_TYPE": (self.challenge_types, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Beat the game using only RESTRICTION_TYPE",
                    data={"RESTRICTION_TYPE": (self.game_restrictions, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete a speedrun in under SPEEDRUN_TIME",
                    data={"SPEEDRUN_TIME": (self.speedrun_times, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Survive in a superflat world for SUPERFLAT_DAYS days",
                    data={"SUPERFLAT_DAYS": (self.superflat_survival_days, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_survival_basics(self) -> bool:
        return self.archipelago_options.minecraft_include_survival_basics.value

    @property
    def include_building_projects(self) -> bool:
        return self.archipelago_options.minecraft_include_building_projects.value

    @property
    def include_exploration(self) -> bool:
        return self.archipelago_options.minecraft_include_exploration.value

    @property
    def include_redstone_engineering(self) -> bool:
        return self.archipelago_options.minecraft_include_redstone_engineering.value

    @property
    def include_farming_automation(self) -> bool:
        return self.archipelago_options.minecraft_include_farming_automation.value

    @property
    def include_boss_progression(self) -> bool:
        return self.archipelago_options.minecraft_include_boss_progression.value

    @property
    def include_collection_goals(self) -> bool:
        return self.archipelago_options.minecraft_include_collection_goals.value

    @property
    def include_challenge_runs(self) -> bool:
        return self.archipelago_options.minecraft_include_challenge_runs.value

    @property
    def game_mode_focus(self) -> str:
        return self.archipelago_options.minecraft_game_mode_focus.value

    @property
    def difficulty_preference(self) -> str:
        return self.archipelago_options.minecraft_difficulty_preference.value

    # Data lists
    @staticmethod
    def game_modes() -> List[str]:
        return ["Survival", "Creative", "Adventure", "Hardcore"]

    @staticmethod
    def tool_sets() -> List[str]:
        return [
            "Stone Tools", "Iron Tools", "Diamond Tools", "Netherite Tools",
            "Gold Tools", "Complete Tool Set"
        ]

    @staticmethod
    def tool_types() -> List[str]:
        return ["Wood", "Stone", "Iron", "Diamond", "Netherite", "Gold"]

    @staticmethod
    def mineable_materials() -> List[str]:
        return [
            "Coal", "Iron", "Gold", "Diamond", "Emerald", "Lapis Lazuli",
            "Redstone", "Quartz", "Ancient Debris", "Copper"
        ]

    @staticmethod
    def functional_buildings() -> List[str]:
        return [
            "Automatic Farm", "Storage Warehouse", "Enchanting Room", "Brewing Lab",
            "Nether Portal Hub", "Railway Station", "Harbor", "Lighthouse", "Castle",
            "Village", "Trading Post", "Monster Spawner", "Experience Farm"
        ]

    @staticmethod
    def architectural_styles() -> List[str]:
        return [
            "Medieval", "Modern", "Japanese", "Victorian", "Steampunk", "Fantasy",
            "Brutalist", "Art Deco", "Rustic", "Futuristic", "Egyptian", "Greek"
        ]

    @staticmethod
    def building_themes() -> List[str]:
        return [
            "Underwater City", "Sky Island", "Desert Oasis", "Jungle Temple",
            "Ice Palace", "Volcanic Fortress", "Mushroom Village", "End City Replica",
            "Pirate Cove", "Wizard Tower", "Industrial Complex", "Zen Garden"
        ]

    @staticmethod
    def massive_structures() -> List[str]:
        return [
            "Pyramid", "Cathedral", "Skyscraper", "Mountain Carving", "City",
            "Mega Base", "Stadium", "Cruise Ship", "Space Station"
        ]

    @staticmethod
    def replica_subjects() -> List[str]:
        return [
            "Real World Building", "Movie Location", "Video Game Location",
            "Historical Monument", "Natural Wonder", "Famous Landmark"
        ]

    @staticmethod
    def lootable_structures() -> List[str]:
        return [
            "Villages", "Temples", "Strongholds", "End Cities", "Woodland Mansions",
            "Ocean Monuments", "Pillager Outposts", "Ruined Portals", "Shipwrecks",
            "Buried Treasures", "Dungeons", "Mineshafts"
        ]

    @staticmethod
    def dimensions() -> List[str]:
        return ["Overworld", "Nether", "End"]

    @staticmethod
    def tameable_animals() -> List[str]:
        return ["Wolves", "Cats", "Horses", "Llamas", "Parrots", "Axolotls", "Foxes"]

    @staticmethod
    def breedable_animals() -> List[str]:
        return [
            "Cows", "Pigs", "Chickens", "Sheep", "Horses", "Llamas", "Rabbits",
            "Bees", "Villagers", "Turtles", "Pandas", "Foxes"
        ]

    @staticmethod
    def redstone_contraptions() -> List[str]:
        return [
            "Automatic Door", "Piston Elevator", "Item Sorter", "Clock", "Calculator",
            "Combination Lock", "Redstone Computer", "Flying Machine", "Bridge Builder",
            "Automatic Smelter", "Note Block Song", "Redstone Lamp Display"
        ]

    @staticmethod
    def automation_systems() -> List[str]:
        return [
            "Item Transportation", "Crop Harvesting", "Animal Breeding", "Mob Farming",
            "Ore Processing", "Food Production", "Potion Brewing", "Enchanting Setup"
        ]

    @staticmethod
    def redstone_computations() -> List[str]:
        return [
            "Addition", "Binary Counter", "Memory Storage", "Logic Gates",
            "Random Number Generator", "Display Screen"
        ]

    @staticmethod
    def farmable_crops() -> List[str]:
        return [
            "Wheat", "Carrots", "Potatoes", "Beetroot", "Pumpkins", "Melons",
            "Sugar Cane", "Cocoa Beans", "Nether Wart", "Kelp", "Sweet Berries"
        ]

    @staticmethod
    def farmable_mobs() -> List[str]:
        return [
            "Zombie", "Skeleton", "Spider", "Creeper", "Enderman", "Blaze",
            "Witch", "Guardian", "Iron Golem", "Villager"
        ]

    @staticmethod
    def renewable_resources() -> List[str]:
        return [
            "Cobblestone", "Wood", "Water", "Lava", "Ice", "Snow", "Sand",
            "Gravel", "Clay", "Obsidian"
        ]

    @staticmethod
    def collection_categories() -> List[str]:
        return [
            "All Ores", "All Woods", "All Flowers", "All Foods", "All Potions",
            "All Enchantments", "All Banners", "All Dyes", "All Blocks"
        ]

    @staticmethod
    def rare_items() -> List[str]:
        return [
            "Dragon Egg", "Elytra", "Totem of Undying", "Nether Star",
            "Heart of the Sea", "Trident", "Mending Book", "Notch Apple"
        ]

    @staticmethod
    def challenge_types() -> List[str]:
        return [
            "Skyblock", "One Block", "Superflat", "Hardcore", "No Crafting Table",
            "Pacifist", "Vegetarian", "Nomad", "Underground Only"
        ]

    @staticmethod
    def game_restrictions() -> List[str]:
        return [
            "Wood Tools Only", "No Mining", "No Trading", "No Enchanting",
            "No Nether", "No Villages", "Surface Only", "One Chunk"
        ]

    @staticmethod
    def restriction_materials() -> List[str]:
        return ["Iron", "Diamond", "Redstone", "Enchantments", "Potions", "Elytra"]

    @staticmethod
    def biome_restrictions() -> List[str]:
        return [
            "Desert", "Forest", "Plains", "Mountains", "Ocean", "Jungle",
            "Swamp", "Taiga", "Tundra", "Mushroom", "Nether", "End"
        ]

    @staticmethod
    def speedrun_times() -> List[str]:
        return ["30 minutes", "1 hour", "2 hours", "5 hours", "10 hours"]

    # Ranges
    @staticmethod
    def room_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def food_amounts() -> range:
        return range(100, 500, 100)

    @staticmethod
    def ore_amounts() -> range:
        return range(50, 300, 50)

    @staticmethod
    def massive_block_counts() -> range:
        return range(10000, 100000, 10000)

    @staticmethod
    def level_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def biome_counts() -> range:
        return range(10, 30, 5)

    @staticmethod
    def structure_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def travel_distances() -> range:
        return range(5000, 25000, 5000)

    @staticmethod
    def landmark_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def animal_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def circuit_sizes() -> range:
        return range(5, 20, 5)

    @staticmethod
    def production_rates() -> range:
        return range(100, 1000, 100)

    @staticmethod
    def breeding_counts() -> range:
        return range(10, 50, 10)

    @staticmethod
    def sorting_categories() -> range:
        return range(10, 50, 10)

    @staticmethod
    def elder_guardian_counts() -> range:
        return range(3, 9, 3)

    @staticmethod
    def raid_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def exhibit_counts() -> range:
        return range(50, 200, 50)

    @staticmethod
    def enchanted_book_counts() -> range:
        return range(20, 50, 10)

    @staticmethod
    def music_disc_counts() -> range:
        return range(10, 13)

    @staticmethod
    def superflat_survival_days() -> range:
        return range(10, 50, 10)

    @staticmethod
    def night_survival_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def hostile_mob_counts() -> range:
        return range(50, 200, 50)

    @staticmethod
    def day_limits() -> range:
        return range(10, 100, 10)


# Archipelago Options
class MinecraftIncludeSurvivalBasics(Toggle):
    """Include basic survival objectives (tools, shelter, mining)."""
    display_name = "Include Survival Basics"

class MinecraftIncludeBuildingProjects(Toggle):
    """Include building and construction objectives."""
    display_name = "Include Building Projects"

class MinecraftIncludeExploration(Toggle):
    """Include exploration and discovery objectives."""
    display_name = "Include Exploration"

class MinecraftIncludeRedstoneEngineering(Toggle):
    """Include redstone contraption and automation objectives."""
    display_name = "Include Redstone Engineering"

class MinecraftIncludeFarmingAutomation(Toggle):
    """Include farming, breeding, and automation objectives."""
    display_name = "Include Farming & Automation"

class MinecraftIncludeBossProgression(Toggle):
    """Include boss fights and major progression objectives."""
    display_name = "Include Boss Progression"

class MinecraftIncludeCollectionGoals(Toggle):
    """Include item collection and museum objectives."""
    display_name = "Include Collection Goals"

class MinecraftIncludeChallengeRuns(Toggle):
    """Include challenge runs and restriction objectives."""
    display_name = "Include Challenge Runs"

class MinecraftGameModeFocus(Choice):
    """Focus objectives on specific game modes."""
    display_name = "Game Mode Focus"
    option_all = "All"
    option_survival = "Survival"
    option_creative = "Creative"
    default = option_all

class MinecraftDifficultyPreference(Choice):
    """Prefer certain difficulty levels for objectives."""
    display_name = "Difficulty Preference"
    option_all = "All"
    option_easy = "Easy"
    option_hard = "Hard"
    default = option_all
