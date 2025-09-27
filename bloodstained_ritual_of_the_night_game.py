from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, Toggle, Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BloodstainedArchipelagoOptions:
    bloodstained_include_shard_collection: BloodstainedIncludeShardCollection
    bloodstained_include_exploration: BloodstainedIncludeExploration
    bloodstained_include_boss_challenges: BloodstainedIncludeBossChallenges
    bloodstained_include_alchemy_crafting: BloodstainedIncludeAlchemyCrafting
    bloodstained_include_equipment_mastery: BloodstainedIncludeEquipmentMastery
    bloodstained_include_completion_goals: BloodstainedIncludeCompletionGoals
    bloodstained_include_speedrun_challenges: BloodstainedIncludeSpeedrunChallenges
    bloodstained_include_difficulty_challenges: BloodstainedIncludeDifficultyChallenges
    bloodstained_include_game_modes: BloodstainedIncludeGameModes
    bloodstained_include_dominiques_curse: BloodstainedIncludeDominiquesCurse
    bloodstained_focus_style: BloodstainedFocusStyle


class BloodstainedRitualOfTheNightGame(Game):
    name = "Bloodstained: Ritual of the Night"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = BloodstainedArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective without using SHARD_TYPE shards",
                data={"SHARD_TYPE": (self.shard_types, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective using only WEAPON_CATEGORY weapons",
                data={"WEAPON_CATEGORY": (self.weapon_categories, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without taking damage",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective at DIFFICULTY_LEVEL or higher",
                data={"DIFFICULTY_LEVEL": (self.difficulty_levels, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective with MAP_COMPLETION% map completion or less",
                data={"MAP_COMPLETION": (self.map_completion_limits, 1)},
            ),
        ])
        
        # Add Dominique's Curse specific constraints if DLC is enabled
        if self.include_dominiques_curse:
            constraints.extend([
                GameObjectiveTemplate(
                    label="Complete this objective while Crystal Curse is at CURSE_STAGE",
                    data={"CURSE_STAGE": (self.crystal_curse_stages, 1)},
                ),
                GameObjectiveTemplate(
                    label="Complete this objective in Limbo within LIMBO_TIME",
                    data={"LIMBO_TIME": (self.limbo_survival_times, 1)},
                ),
            ])
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Shard Collection
        if self.include_shard_collection:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Collect SHARD_COUNT SHARD_TYPE shards",
                    data={
                        "SHARD_COUNT": (self.shard_counts, 1),
                        "SHARD_TYPE": (self.shard_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Max out SHARD_UPGRADE_COUNT shards to Rank 9",
                    data={"SHARD_UPGRADE_COUNT": (self.shard_upgrade_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Obtain the SPECIFIC_SHARD shard",
                    data={"SPECIFIC_SHARD": (self.notable_shards, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Collect all shards from AREA",
                    data={"AREA": (self.major_areas, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Use SHARD_COMBO_COUNT different shards in combination effectively",
                    data={"SHARD_COMBO_COUNT": (self.shard_combo_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Exploration
        if self.include_exploration:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach MAP_PERCENTAGE% map completion",
                    data={"MAP_PERCENTAGE": (self.map_percentages, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Find and access SECRET_COUNT secret areas",
                    data={"SECRET_COUNT": (self.secret_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Discover all fast travel points in TRAVEL_AREA",
                    data={"TRAVEL_AREA": (self.travel_areas, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Open CHEST_COUNT treasure chests",
                    data={"CHEST_COUNT": (self.chest_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete the AREA area fully",
                    data={"AREA": (self.explorable_areas, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Find BOOK_COUNT books/lore entries",
                    data={"BOOK_COUNT": (self.book_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Visit and interact with NPC_NAME",
                    data={"NPC_NAME": (self.npc_names, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Use Todd's barber services HAIRSTYLE_COUNT times",
                    data={"HAIRSTYLE_COUNT": (self.hairstyle_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Plant and harvest CROP_TYPE with Harry",
                    data={"CROP_TYPE": (self.crop_types, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Purchase ITEM_COUNT different items from Dominique's shop",
                    data={"ITEM_COUNT": (self.shop_item_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Boss Challenges
        if self.include_boss_challenges:
            challenge_templates = []
            
            if self.focus_style in ["All", "Combat"]:
                challenge_templates.extend([
                    GameObjectiveTemplate(
                        label="Defeat BOSS without using healing items",
                        data={"BOSS": (self.major_bosses, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Defeat BOSS in under TIME_LIMIT",
                        data={
                            "BOSS": (self.timed_bosses, 1),
                            "TIME_LIMIT": (self.boss_time_limits, 1)
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    ),
                ])
            
            challenge_templates.extend([
                GameObjectiveTemplate(
                    label="Defeat BOSS",
                    data={"BOSS": (self.all_bosses, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Defeat MINI_BOSS_COUNT mini-bosses",
                    data={"MINI_BOSS_COUNT": (self.mini_boss_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete all boss rush challenges",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])
            
            game_objective_templates.extend(challenge_templates)

        # Alchemy & Crafting
        if self.include_alchemy_crafting:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Craft RECIPE_COUNT different recipes",
                    data={"RECIPE_COUNT": (self.recipe_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create ITEM using alchemy",
                    data={"ITEM": (self.craftable_items, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Synthesize FOOD_COUNT different food items",
                    data={"FOOD_COUNT": (self.food_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Craft all EQUIPMENT_TYPE equipment",
                    data={"EQUIPMENT_TYPE": (self.craftable_equipment_types, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Discover INGREDIENT_COUNT different crafting materials",
                    data={"INGREDIENT_COUNT": (self.ingredient_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Enhance SHARD_COUNT shards with Johannes to rank 9",
                    data={"SHARD_COUNT": (self.shard_enhancement_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Help Todd achieve his goal by using HAIRSTYLE_GOAL hairstyles",
                    data={"HAIRSTYLE_GOAL": (self.todd_milestone_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Equipment Mastery
        if self.include_equipment_mastery:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Master WEAPON_COUNT different weapons",
                    data={"WEAPON_COUNT": (self.weapon_mastery_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Obtain LEGENDARY_WEAPON",
                    data={"LEGENDARY_WEAPON": (self.legendary_weapons, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Collect all ARMOR_SET pieces",
                    data={"ARMOR_SET": (self.armor_sets, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Upgrade a weapon to +UPGRADE_LEVEL",
                    data={"UPGRADE_LEVEL": (self.upgrade_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Equip and test ACCESSORY_COUNT different accessories",
                    data={"ACCESSORY_COUNT": (self.accessory_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Completion Goals
        if self.include_completion_goals:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the main story in under STORY_TIME_LIMIT",
                    data={"STORY_TIME_LIMIT": (self.story_time_limits, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Achieve COMPLETION_RATE% total game completion",
                    data={"COMPLETION_RATE": (self.completion_rates, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete all QUEST_TYPE",
                    data={"QUEST_TYPE": (self.quest_types, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Finish the game with ENDING_CONDITION",
                    data={"ENDING_CONDITION": (self.ending_conditions, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete New Game Plus in under NG_PLUS_TIME",
                    data={"NG_PLUS_TIME": (self.ng_plus_times, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Help NPC_NAME complete their personal goal",
                    data={"NPC_NAME": (self.npcs_with_goals, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Read BOOK_READ_COUNT books with O.D. in the library",
                    data={"BOOK_READ_COUNT": (self.library_book_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Speedrun Challenges
        if self.include_speedrun_challenges:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the game in under SPEEDRUN_TIME",
                    data={"SPEEDRUN_TIME": (self.speedrun_times, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Reach AREA_NAME in under AREA_TIME",
                    data={
                        "AREA_NAME": (self.speedrun_areas, 1),
                        "AREA_TIME": (self.area_times, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete a low% run with PERCENTAGE% completion or less",
                    data={"PERCENTAGE": (self.low_percentages, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Difficulty Challenges
        if self.include_difficulty_challenges:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the game on DIFFICULTY difficulty",
                    data={"DIFFICULTY": (self.difficulty_modes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete CHALLENGE_TYPE challenge run",
                    data={"CHALLENGE_TYPE": (self.challenge_types, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Game Modes
        if self.include_game_modes:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete Randomizer mode with RANDOMIZER_SETTING enabled",
                    data={"RANDOMIZER_SETTING": (self.randomizer_settings, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete Randomizer mode with RANDOMIZER_GOAL objective",
                    data={"RANDOMIZER_GOAL": (self.randomizer_goals, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete Full Chaos Randomizer with KEY_ITEM_SETTING, ITEMS_SETTING, ENEMY_DROP_SETTING, SAVE_WARP_SETTING, CRAFTING_SETTING, SHOP_SETTING, and QUEST_SETTING all enabled",
                    data={
                        "KEY_ITEM_SETTING": (self.key_item_settings, 1),
                        "ITEMS_SETTING": (self.items_settings, 1),
                        "ENEMY_DROP_SETTING": (self.enemy_drop_settings, 1),
                        "SAVE_WARP_SETTING": (self.save_warp_settings, 1),
                        "CRAFTING_SETTING": (self.crafting_settings, 1),
                        "SHOP_SETTING": (self.shop_settings, 1),
                        "QUEST_SETTING": (self.quest_settings, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete Classic Mode on CLASSIC_DIFFICULTY difficulty",
                    data={"CLASSIC_DIFFICULTY": (self.classic_difficulties, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete Boss Rush Mode Course COURSE_NUMBER on BOSS_RUSH_DIFFICULTY",
                    data={
                        "COURSE_NUMBER": (self.boss_rush_courses, 1),
                        "BOSS_RUSH_DIFFICULTY": (self.boss_rush_difficulties, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete Boss Revenge mode and defeat REVENGE_BOSS",
                    data={"REVENGE_BOSS": (self.revenge_bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Survive CHAOS_ROOM_COUNT rooms in Chaos Mode",
                    data={"CHAOS_ROOM_COUNT": (self.chaos_room_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete Chaos Mode with CHAOS_CHALLENGE challenge",
                    data={"CHAOS_CHALLENGE": (self.chaos_challenges, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete Speed Run Mode under SPEEDRUN_TIME",
                    data={"SPEEDRUN_TIME": (self.speedrun_times, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Unlock and complete 1986 Mode",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete Zangetsu Mode",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete Bloodless Mode",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete Aurora Mode",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete PLAYABLE_CHARACTER in Randomizer Mode",
                    data={"PLAYABLE_CHARACTER": (self.playable_characters, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Master all abilities as PLAYABLE_CHARACTER",
                    data={"PLAYABLE_CHARACTER": (self.playable_characters, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win VERSUS_MATCH_COUNT matches in Versus Mode",
                    data={"VERSUS_MATCH_COUNT": (self.versus_match_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete CROSSOVER_GAME crossover content",
                    data={"CROSSOVER_GAME": (self.crossover_games, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete all DLC_CONTENT",
                    data={"DLC_CONTENT": (self.dlc_content, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Help CROP_TYPE with Harry's farming quests",
                    data={"CROP_TYPE": (self.crop_types, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Get HAIRSTYLE_COUNT different hairstyles from Todd",
                    data={"HAIRSTYLE_COUNT": (self.hairstyle_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Purchase SHOP_ITEM_COUNT different items from Dominique's shop",
                    data={"SHOP_ITEM_COUNT": (self.shop_item_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Achievement-inspired objectives
        game_objective_templates.extend([
            GameObjectiveTemplate(
                label="Perform JUMP_KICK_COUNT jump kicks without touching the ground",
                data={"JUMP_KICK_COUNT": (self.jump_kick_counts, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Travel TRAVEL_DISTANCE throughout your adventure",
                data={"TRAVEL_DISTANCE": (self.travel_distances, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Perform BACKSTEP_COUNT backsteps",
                data={"BACKSTEP_COUNT": (self.backstep_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Break CANDLEHOLDER_COUNT candleholders",
                data={"CANDLEHOLDER_COUNT": (self.candleholder_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Amass a fortune of GOLD_AMOUNT",
                data={"GOLD_AMOUNT": (self.gold_amounts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Earn SALES_AMOUNT through item sales",
                data={"SALES_AMOUNT": (self.sales_amounts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach level LEVEL_TARGET",
                data={"LEVEL_TARGET": (self.level_targets, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Take in a large quantity of blood (get Bloodstained status)",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Master a weapon technique completely",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Break down items into materials BREAKDOWN_COUNT times",
                data={"BREAKDOWN_COUNT": (self.breakdown_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
        ])

        # Dominique's Curse DLC Content
        if self.include_dominiques_curse:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete Dominique's Curse DLC story",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Survive in Limbo for LIMBO_TIME",
                    data={"LIMBO_TIME": (self.limbo_survival_times, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Collect LOGAETH_COUNT Logaeth Pages",
                    data={"LOGAETH_COUNT": (self.logaeth_page_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Defeat HUNTER_COUNT Hunters",
                    data={"HUNTER_COUNT": (self.hunter_defeat_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Explore CURSE_AREA in Dominique's Curse",
                    data={"CURSE_AREA": (self.dominiques_curse_areas, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Defeat CURSE_BOSS",
                    data={"CURSE_BOSS": (self.dominiques_curse_bosses, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Overcome Crystal Curse CURSE_STAGE",
                    data={"CURSE_STAGE": (self.crystal_curse_stages, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Achieve CURSE_ENDING",
                    data={"CURSE_ENDING": (self.dominiques_curse_endings, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete Dominique's Curse without using save states",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Find all secret areas in Limbo",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Master Dominique's unique abilities",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                # Achievement-based DLC objectives
                GameObjectiveTemplate(
                    label="Strike a foe immediately after dash attack DASH_COUNT times",
                    data={"DASH_COUNT": (self.dash_attack_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Earn COIN_AMOUNT Coins via Remains Exchange",
                    data={"COIN_AMOUNT": (self.remains_coin_amounts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Lie to demons DEMON_LIE_COUNT times and get caught",
                    data={"DEMON_LIE_COUNT": (self.demon_lie_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_shard_collection(self) -> bool:
        return self.archipelago_options.bloodstained_include_shard_collection.value

    @property
    def include_exploration(self) -> bool:
        return self.archipelago_options.bloodstained_include_exploration.value

    @property
    def include_boss_challenges(self) -> bool:
        return self.archipelago_options.bloodstained_include_boss_challenges.value

    @property
    def include_alchemy_crafting(self) -> bool:
        return self.archipelago_options.bloodstained_include_alchemy_crafting.value

    @property
    def include_equipment_mastery(self) -> bool:
        return self.archipelago_options.bloodstained_include_equipment_mastery.value

    @property
    def include_completion_goals(self) -> bool:
        return self.archipelago_options.bloodstained_include_completion_goals.value

    @property
    def include_speedrun_challenges(self) -> bool:
        return self.archipelago_options.bloodstained_include_speedrun_challenges.value

    @property
    def include_difficulty_challenges(self) -> bool:
        return self.archipelago_options.bloodstained_include_difficulty_challenges.value

    @property
    def include_game_modes(self) -> bool:
        return self.archipelago_options.bloodstained_include_game_modes.value

    @property
    def include_dominiques_curse(self) -> bool:
        return self.archipelago_options.bloodstained_include_dominiques_curse.value

    @property
    def focus_style(self) -> str:
        return self.archipelago_options.bloodstained_focus_style.value

    @property
    def playable_characters(self) -> List[str]:
        return ["Miriam", "Zangetsu", "Bloodless", "Aurora"]

    @property
    def dlc_content(self) -> List[str]:
        return [
            "Zangetsu Character", "Bloodless Character", "Aurora Character",
            "Boss Revenge Mode", "Classic Mode", "Chroma Wheel",
            "Kingdom Two Crowns Crossover", "Journey Crossover",
            "Dominique's Curse", "Chaos Mode", "Versus Mode"
        ]

    @property
    def crossover_games(self) -> List[str]:
        return ["Kingdom Two Crowns", "Journey", "Child of Light"]

    @property
    def crop_types(self) -> List[str]:
        return ["Potatoes", "Corn", "Rice"]

    @property
    def hairstyle_counts(self) -> range:
        return range(5, 30, 5)

    @property
    def shop_item_counts(self) -> range:
        return range(10, 50, 10)

    @property
    def versus_match_counts(self) -> range:
        return range(5, 25, 5)

    # Data lists
    @staticmethod
    def shard_types() -> List[str]:
        return ["Conjure", "Manipulative", "Directional", "Passive", "Familiar", "Skill"]

    @staticmethod
    def notable_shards() -> List[str]:
        return [
            "Dimension Shift", "Reflector Ray", "True Arrow", "Void Ray", "Summon Hellhound",
            "Summon Bat", "Blood Steal", "Augment Gold", "Accelerator", "Optimizer",
            "Craftwork", "Alchemystic", "Skill Regenerator", "HP Regenerator", "MP Regenerator"
        ]

    @staticmethod
    def major_areas() -> List[str]:
        return [
            "Entrance", "Galleon Minerva", "Arvantville", "Dian Cecht Cathedral",
            "Forbidden Underground Waterway", "Garden of Silence", "Den of Behemoths",
            "Hall of Termination", "Oriental Sorcery Lab", "Underground Sorcery Lab",
            "Secret Sorcery Lab", "Livre Ex Machina", "Tower of Twin Dragons", 
            "Inferno Cave", "Glacial Tomb", "Hidden Desert", "Bridge of Evil",
            "8-bit Nightmare"
        ]

    @staticmethod
    def explorable_areas() -> List[str]:
        return [
            "Entrance", "Galleon Minerva", "Arvantville", "Dian Cecht Cathedral",
            "Garden of Silence", "Den of Behemoths", "Hall of Termination",
            "Oriental Sorcery Lab", "Underground Sorcery Lab", "Livre Ex Machina", 
            "Tower of Twin Dragons", "Hidden Desert", "8-bit Nightmare"
        ]

    @staticmethod
    def travel_areas() -> List[str]:
        return ["Entrance", "Arvantville", "Cathedral", "Garden", "Den", "Hall", "Lab", "Library"]

    @staticmethod
    def major_bosses() -> List[str]:
        return [
            "Vepar", "Zangetsu", "Bloodless", "Bathin", "Gebel", "Gremory", "O.D.",
            "Valac", "Valefar", "Bael", "Dominique", "Andrealphus", "Glutton Train",
            "Abyssal Guardian", "Orobas"
        ]

    @staticmethod
    def all_bosses() -> List[str]:
        return [
            "Vepar", "Zangetsu", "Bloodless", "Bathin", "Gebel", "Gremory", "O.D.",
            "Valac", "Valefar", "Bael", "Dominique", "Doppelganger", "Alfred",
            "Craftwork", "Revenant", "Morte Arthada", "Andrealphus", "Glutton Train",
            "Abyssal Guardian", "Orobas"
        ]

    @staticmethod
    def timed_bosses() -> List[str]:
        return ["Vepar", "Bloodless", "Gebel", "Zangetsu", "Bael", "Dominique", "Andrealphus", "Glutton Train"]

    @staticmethod
    def boss_time_limits() -> List[str]:
        return ["2 minutes", "3 minutes", "5 minutes", "90 seconds"]

    @staticmethod
    def craftable_items() -> List[str]:
        return [
            "Rhava Velar", "Durandal", "Carabosse", "Curtana", "Fragarach",
            "Diamond Vest", "Valkyrie Dress", "Traveler's Clothes",
            "Regeneration Potion", "Mana Potion", "Amrita"
        ]

    @staticmethod
    def craftable_equipment_types() -> List[str]:
        return ["Swords", "Whips", "Daggers", "Rapiers", "Katanas", "Clubs", "Greatswords", "Spears", "Firearms", "Shoes", "Armor", "Headgear", "Accessories"]

    @staticmethod
    def legendary_weapons() -> List[str]:
        return [
            "Rhava Velar", "Durandal", "Fragarach", "Curtana", "Carabosse", 
            "Bloodbringer", "Flying Edge", "Oracle Blade", "Rhava Búral",
            "Dáinsleif", "Florenberg", "Almace", "Caladbolg", "Ridill",
            "Blue Rose", "Valkyrie Sword", "Gram", "Lohengrin", "Steel Lightning",
            "Dies Irae", "Ukonvasara", "Eternal Blue", "Dawn Blade", 
            "Claw of Onmoraki", "Blood Grinder", "Silent Calamity"
        ]

    @staticmethod
    def armor_sets() -> List[str]:
        return [
            "Light Armor Collection", "Heavy Armor Collection", "Magical Dress Collection", 
            "Combat Armor Collection", "Stealth Armor Collection", "Elite Armor Collection"
        ]

    @staticmethod
    def craftable_equipment_types() -> List[str]:
        return ["Swords", "Whips", "Daggers", "Rapiers", "Katanas", "Clubs", "Greatswords", "Spears", "Firearms", "Shoes", "Armor", "Headgear", "Accessories"]

    @staticmethod
    def weapon_categories() -> List[str]:
        return ["Swords", "Whips", "Daggers", "Rapiers", "Katanas", "Clubs", "Greatswords", "Spears", "Firearms", "Shoes"]

    @staticmethod
    def quest_types() -> List[str]:
        return ["Lindsay's Quests", "Abigail's Quests", "Susie's Quests", "Benjamin's Quests"]

    @staticmethod
    def npc_names() -> List[str]:
        return [
            "Johannes", "Dominique", "Anne", "Lindsay", "Alfred", "Harry", 
            "Abigail", "Susie", "Benjamin", "Todd", "O.D.", "The Coachman"
        ]

    @staticmethod
    def crop_types() -> List[str]:
        return ["Potatoes", "Corn", "Rice"]

    @staticmethod
    def hairstyle_counts() -> range:
        return range(5, 30, 5)

    @staticmethod
    def shop_item_counts() -> range:
        return range(10, 50, 10)

    @staticmethod
    def npcs_with_goals() -> List[str]:
        return ["Todd (666 hairstyles)", "Harry (rebuild his farm)", "Benjamin (survive his adventures)", "Susie (remember her past)"]

    @staticmethod
    def shard_enhancement_counts() -> range:
        return range(3, 12, 3)

    @staticmethod
    def todd_milestone_counts() -> range:
        return range(50, 250, 50)

    @staticmethod
    def difficulty_modes() -> List[str]:
        return ["Normal", "Hard", "Nightmare"]

    @staticmethod
    def difficulty_levels() -> List[str]:
        return ["Normal", "Hard", "Nightmare"]

    @staticmethod
    def challenge_types() -> List[str]:
        return [
            "Speedrun", "Low% Run", "Weapon Master Run",
            "No Healing Items", "Boss Rush Only"
        ]

    @staticmethod
    def speedrun_areas() -> List[str]:
        return ["Galleon Minerva", "Arvantville", "Cathedral", "Garden of Silence"]

    @staticmethod
    def area_times() -> List[str]:
        return ["10 minutes", "15 minutes", "20 minutes", "30 minutes"]

    @staticmethod
    def speedrun_times() -> List[str]:
        return ["under 3 hours", "under 5 hours", "under 8 hours", "under 12 hours"]

    # Ranges
    @staticmethod
    def shard_counts() -> range:
        return range(10, 50, 10)

    @staticmethod
    def shard_upgrade_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def shard_combo_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def map_percentages() -> range:
        return range(70, 100, 10)

    @staticmethod
    def map_completion_limits() -> range:
        return range(50, 90, 10)

    @staticmethod
    def secret_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def chest_counts() -> range:
        return range(20, 100, 20)

    @staticmethod
    def book_counts() -> range:
        return range(10, 30, 5)

    @staticmethod
    def mini_boss_counts() -> range:
        return range(5, 15, 5)

    @staticmethod
    def recipe_counts() -> range:
        return range(20, 80, 20)

    @staticmethod
    def food_counts() -> range:
        return range(15, 45, 15)

    @staticmethod
    def ingredient_counts() -> range:
        return range(30, 90, 30)

    # New lists for playable characters and game modes
    @staticmethod
    def playable_characters() -> List[str]:
        return ["Miriam", "Zangetsu", "Bloodless", "Aurora"]

    @staticmethod
    def game_modes() -> List[str]:
        return [
            "Story Mode", "Randomizer Mode", "Boss Revenge Mode", 
            "Classic Mode", "Chaos Mode", "Versus Mode"
        ]

    @staticmethod
    def dlc_content() -> List[str]:
        return [
            "Zangetsu Character", "Bloodless Character", "Aurora Character",
            "Boss Revenge Mode", "Classic Mode", "Chroma Wheel",
            "Kingdom Two Crowns Crossover", "Journey Crossover",
            "Dominique's Curse", "Chaos Mode", "Versus Mode"
        ]

    @staticmethod
    def crossover_games() -> List[str]:
        return ["Kingdom Two Crowns", "Journey", "Child of Light"]

    @staticmethod
    def weapon_mastery_counts() -> range:
        return range(10, 30, 10)

    @staticmethod
    def upgrade_levels() -> range:
        return range(3, 9, 3)

    @staticmethod
    def accessory_counts() -> range:
        return range(15, 45, 15)

    @staticmethod
    def completion_rates() -> range:
        return range(90, 100, 5)

    @staticmethod
    def low_percentages() -> range:
        return range(20, 50, 10)

    @staticmethod
    def randomizer_settings() -> List[str]:
        return [
            "Key Items: Shuffled", "Key Items: Anywhere", "Save/Warp Rooms: Unchanged", "Save/Warp Rooms: Mixed",
            "Items: Retain Type", "Items: Retain Method", "Items: Total Random", 
            "Enemy Drops: Unchanged", "Enemy Drops: Mixed Shards", "Enemy Drops: Mixed Items", "Enemy Drops: Chaos",
            "Crafting: Unchanged", "Crafting: Shuffled", "Shop: Unchanged", "Shop: Shuffled", 
            "Quests: Unchanged", "Quests: Shuffled"
        ]

    @staticmethod
    def classic_difficulties() -> List[str]:
        return ["Easy", "Normal", "Hard"]

    @staticmethod
    def boss_rush_courses() -> List[str]:
        return ["Course 1", "Course 2"]

    @staticmethod
    def boss_rush_difficulties() -> List[str]:
        return ["Normal", "Hard", "Nightmare"]

    @staticmethod
    def chaos_challenges() -> List[str]:
        return [
            "Defeat All Enemies", "Don't Use Any Special Ability", "Don't Attack Any Enemy",
            "Reach Exit In Time", "Complete Without Taking Damage"
        ]

    @staticmethod
    def chaos_room_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def revenge_bosses() -> List[str]:
        return [
            "All Boss Revenge Enemies", "Revenge Vepar", "Revenge Zangetsu", 
            "Revenge Bloodless", "Revenge Bathin", "Revenge Gebel"
        ]

    @staticmethod
    def randomizer_goals() -> List[str]:
        return ["Defeat Gebel", "Defeat True Evil", "Defeat All Evil"]

    @staticmethod
    def key_item_settings() -> List[str]:
        return ["Key Items: Shuffled", "Key Items: Anywhere"]

    @staticmethod
    def items_settings() -> List[str]:
        return ["Items: Retain Type", "Items: Retain Method", "Items: Total Random"]

    @staticmethod
    def enemy_drop_settings() -> List[str]:
        return ["Enemy Drops: Unchanged", "Enemy Drops: Mixed Shards", "Enemy Drops: Mixed Items", "Enemy Drops: Chaos"]

    @staticmethod
    def save_warp_settings() -> List[str]:
        return ["Save/Warp Rooms: Unchanged", "Save/Warp Rooms: Mixed"]

    @staticmethod
    def crafting_settings() -> List[str]:
        return ["Crafting: Unchanged", "Crafting: Shuffled"]

    @staticmethod
    def shop_settings() -> List[str]:
        return ["Shop: Unchanged", "Shop: Shuffled"]

    @staticmethod
    def quest_settings() -> List[str]:
        return ["Quests: Unchanged", "Quests: Shuffled"]

    # Dominique's Curse DLC-specific content
    @staticmethod
    def dominiques_curse_areas() -> List[str]:
        return [
            "Limbo Entrance", "Crystal Caves", "Cursed Sanctum", "Demonic Throne Room",
            "Void Corridors", "Shattered Halls", "Bael's Domain"
        ]

    @staticmethod
    def dominiques_curse_bosses() -> List[str]:
        return [
            "Crystal Guardian", "Corrupted Familiar", "Bael (Dominique's Curse)",
            "Limbo Wraith", "Cursed Doppelganger", "The Hunter Alpha"
        ]

    @staticmethod
    def logaeth_page_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def hunter_defeat_counts() -> range:
        return range(3, 12, 3)

    @staticmethod
    def crystal_curse_stages() -> List[str]:
        return ["Stage 1", "Stage 2", "Stage 3", "Final Stage"]

    @staticmethod
    def dominiques_curse_endings() -> List[str]:
        return [
            "Queen of Demons Ending", "Limbo Trap Ending", 
            "Crystal Death Ending", "Amnesia Ending", "True Redemption Ending"
        ]

    @staticmethod
    def limbo_survival_times() -> List[str]:
        return ["10 minutes", "15 minutes", "20 minutes", "30 minutes"]

    # Achievement-based objectives data
    @staticmethod
    def jump_kick_counts() -> range:
        return range(5, 15, 5)

    @staticmethod
    def travel_distances() -> List[str]:
        return ["20 kilometers", "30 kilometers", "42.195 kilometers", "50 kilometers"]

    @staticmethod
    def backstep_counts() -> range:
        return range(100, 500, 100)

    @staticmethod
    def candleholder_counts() -> range:
        return range(500, 1500, 250)

    @staticmethod
    def gold_amounts() -> List[str]:
        return ["100,000G", "250,000G", "500,000G", "1,000,000G"]

    @staticmethod
    def sales_amounts() -> List[str]:
        return ["50,000G", "100,000G", "150,000G", "200,000G"]

    @staticmethod
    def level_targets() -> range:
        return range(30, 60, 10)

    @staticmethod
    def breakdown_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def dash_attack_counts() -> range:
        return range(15, 35, 10)

    @staticmethod
    def remains_coin_amounts() -> range:
        return range(500, 1500, 250)

    @staticmethod
    def story_time_limits() -> List[str]:
        return ["2 hours", "3 hours", "4 hours", "5 hours", "6 hours"]

    @staticmethod
    def ending_conditions() -> List[str]:
        return ["all shards collected", "100% map completion", "no deaths", "under 4 hours", "no save stations used"]

    @staticmethod
    def ng_plus_times() -> List[str]:
        return ["1 hour", "1.5 hours", "2 hours", "3 hours", "4 hours"]

    @staticmethod
    def library_book_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def demon_lie_counts() -> range:
        return range(3, 12, 3)


# Archipelago Options
class BloodstainedIncludeShardCollection(DefaultOnToggle):
    """Include shard collection and upgrade objectives."""
    display_name = "Include Shard Collection"

class BloodstainedIncludeExploration(DefaultOnToggle):
    """Include map exploration and discovery objectives."""
    display_name = "Include Exploration"

class BloodstainedIncludeBossChallenges(DefaultOnToggle):
    """Include boss fight and combat challenge objectives."""
    display_name = "Include Boss Challenges"

class BloodstainedIncludeAlchemyCrafting(DefaultOnToggle):
    """Include alchemy, crafting, and synthesis objectives."""
    display_name = "Include Alchemy & Crafting"

class BloodstainedIncludeEquipmentMastery(DefaultOnToggle):
    """Include weapon mastery and equipment collection objectives."""
    display_name = "Include Equipment Mastery"

class BloodstainedIncludeCompletionGoals(DefaultOnToggle):
    """Include story completion and achievement objectives."""
    display_name = "Include Completion Goals"

class BloodstainedIncludeSpeedrunChallenges(Toggle):
    """Include speedrun and time-based challenge objectives."""
    display_name = "Include Speedrun Challenges"

class BloodstainedIncludeDifficultyChallenges(Toggle):
    """Include difficulty and restriction-based challenge objectives."""
    display_name = "Include Difficulty Challenges"

class BloodstainedIncludeGameModes(Toggle):
    """Include objectives for special game modes like Randomizer, Classic, Bloodless, etc."""
    display_name = "Include Game Mode Challenges"

class BloodstainedIncludeDominiquesCurse(Toggle):
    """Include objectives for the paid Dominique's Curse DLC (Classic II) - requires separate purchase."""
    display_name = "Include Dominique's Curse DLC"

class BloodstainedFocusStyle(Choice):
    """Focus objectives on specific gameplay styles."""
    display_name = "Focus Style"
    option_all = "All"
    option_exploration = "Exploration"
    option_combat = "Combat"
    default = option_all
