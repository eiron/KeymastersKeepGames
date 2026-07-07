from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BaldursGate3ArchipelagoOptions:
    bg3_include_character_builds: BG3IncludeCharacterBuilds
    bg3_include_story_progression: BG3IncludeStoryProgression
    bg3_include_companion_quests: BG3IncludeCompanionQuests
    bg3_include_exploration: BG3IncludeExploration
    bg3_include_combat_challenges: BG3IncludeCombatChallenges
    bg3_include_social_encounters: BG3IncludeSocialEncounters
    bg3_include_collectibles: BG3IncludeCollectibles
    bg3_include_achievement_hunting: BG3IncludeAchievementHunting


class BaldursGate3Game(Game):
    name = "Baldur's Gate 3"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = BaldursGate3ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play as a RACE CLASS_SUBCLASS",
                data={
                    "RACE": (self.character_races, 1),
                    "CLASS_SUBCLASS": (self.class_subclasses, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Play as the Origin character ORIGIN",
                data={"ORIGIN": (self.origin_characters, 1)},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Play a custom character with the BACKGROUND background",
                data={"BACKGROUND": (self.character_backgrounds, 1)},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Do not multiclass your main character, and never ask Withers to change your class",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Do not use any Illithid powers",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Do not use consumable items in combat (potions, scrolls, coatings or grenades)",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Do not cast Guidance",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Your main character may only fight with WEAPON_STYLE",
                data={"WEAPON_STYLE": (self.weapon_styles, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Play on Tactician difficulty or higher",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Character Builds
        if self.include_character_builds:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach level LEVEL_THRESHOLD with a pure CLASS character",
                    data={
                        "CLASS": (self.character_classes, 1),
                        "LEVEL_THRESHOLD": (self.level_thresholds, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Create a multiclass combining CLASSES and reach level LEVEL_THRESHOLD",
                    data={
                        "CLASSES": (self.character_classes, 2),
                        "LEVEL_THRESHOLD": (self.level_thresholds, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Multiclass into MULTICLASS_COUNT different classes on one character without asking Withers to change your class",
                    data={"MULTICLASS_COUNT": (self.multiclass_progression_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Build a character focused on ABILITY_SCORE_FOCUS and raise that ability score to HIGH_STAT or higher",
                    data={
                        "ABILITY_SCORE_FOCUS": (self.ability_score_focuses, 1),
                        "HIGH_STAT": (self.high_stat_targets, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Perform ACTION_COUNT attacks in one turn with a single character",
                    data={"ACTION_COUNT": (self.action_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Complete BACKGROUND_GOAL_COUNT Background Goals in one playthrough",
                    data={"BACKGROUND_GOAL_COUNT": (self.background_goal_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Win a boss fight with a party consisting only of CLASS characters (hirelings allowed)",
                    data={"CLASS": (self.character_classes, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        # Story Progression
        if self.include_story_progression:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the game, reaching GAME_ENDING",
                    data={"GAME_ENDING": (self.game_endings, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Complete the game making primarily ALIGNMENT_CHOICE choices",
                    data={"ALIGNMENT_CHOICE": (self.alignment_choices, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="GROVE_DECISION the Emerald Grove in Act 1",
                    data={"GROVE_DECISION": (self.grove_decisions, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Save every tiefling refugee you can across all three acts of a single playthrough",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Consume PARASITE_COUNT parasite specimens in one playthrough",
                    data={"PARASITE_COUNT": (self.parasite_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Complete SIDE_QUEST",
                    data={"SIDE_QUEST": (self.challenging_side_quests, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
            ])

        # Companion Quests and Relationships
        if self.include_companion_quests:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="See COMPANION_QUEST through to its conclusion",
                    data={"COMPANION_QUEST": (self.companion_quests, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Romance ROMANCE_COMPANION",
                    data={"ROMANCE_COMPANION": (self.romance_companions, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Reach the end of the game still in a committed relationship with ROMANCE_COMPANION",
                    data={"ROMANCE_COMPANION": (self.romance_companions, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Raise COMPANION's approval of you to its maximum level",
                    data={"COMPANION": (self.approval_companions, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Make choices that drive COMPANION to leave your party for good",
                    data={"COMPANION": (self.approval_companions, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Begin a romance, then make choices that cause your partner to end it",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defuse the confrontation between Lae'zel and Shadowheart without losing either companion",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Recruit every recruitable companion in a single playthrough",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        # Exploration
        if self.include_exploration:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Fully explore LOCATION_NAME and complete its associated quests",
                    data={"LOCATION_NAME": (self.major_locations, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Find your way into SECRET_AREA",
                    data={"SECRET_AREA": (self.secret_areas, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Solve PUZZLE",
                    data={"PUZZLE": (self.puzzles, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Dig up BURIED_CHEST_COUNT buried chests",
                    data={"BURIED_CHEST_COUNT": (self.buried_chest_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Question CORPSE_COUNT different corpses using Speak with Dead",
                    data={"CORPSE_COUNT": (self.speak_with_dead_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Hold conversations with ANIMAL_COUNT different creatures using Speak with Animals",
                    data={"ANIMAL_COUNT": (self.speak_with_animals_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Successfully use Detect Thoughts on DETECT_THOUGHTS_COUNT NPCs",
                    data={"DETECT_THOUGHTS_COUNT": (self.detect_thoughts_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="CURIOSITY",
                    data={"CURIOSITY": (self.curiosities, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
            ])

        # Combat Challenges
        if self.include_combat_challenges:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Defeat OPTIONAL_BOSS",
                    data={"OPTIONAL_BOSS": (self.optional_bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="TACTICAL_FEAT",
                    data={"TACTICAL_FEAT": (self.tactical_feats, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Defeat CREATURE_COUNT creatures of the TYPE type",
                    data={
                        "CREATURE_COUNT": (self.creature_counts, 1),
                        "TYPE": (self.creature_types, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Defeat RARE_CREATURE_COUNT creatures of the RARE_TYPE type",
                    data={
                        "RARE_CREATURE_COUNT": (self.rare_creature_counts, 1),
                        "RARE_TYPE": (self.rare_creature_types, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Kill a creature with KILL_METHOD",
                    data={"KILL_METHOD": (self.kill_methods, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Use one enemy as an improvised weapon against another",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat DRUNK_OPPONENT_COUNT opponents while a party member is drunk",
                    data={"DRUNK_OPPONENT_COUNT": (self.drunk_opponent_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Win a battle without any party member taking damage",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Defeat an entire enemy group using only summoned creatures and familiars",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Defeat an entire enemy group using only thrown weapons and objects",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Win a battle in which you exploit SURFACE_COMBO",
                    data={"SURFACE_COMBO": (self.surface_combos, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
            ])

        # Social Encounters
        if self.include_social_encounters:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Succeed on a skill check of DC CHECK_DC or higher",
                    data={"CHECK_DC": (self.skill_check_dcs, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="SOCIAL_FEAT",
                    data={"SOCIAL_FEAT": (self.social_feats, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Break out of prison after being arrested",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Earn BUSKING_GOLD gold from performing music",
                    data={"BUSKING_GOLD": (self.busking_gold_amounts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Steal an item worth STOLEN_VALUE gold or more from a vendor without being caught",
                    data={"STOLEN_VALUE": (self.stolen_item_values, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Complete an entire quest while under the effect of Disguise Self, without your true face being seen",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Rescue every prisoner from the depths of Moonrise Towers (Act 2)",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Rescue Sazza the goblin from all three of her predicaments in one playthrough",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        # Collectibles and Loot
        if self.include_collectibles:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Obtain NOTABLE_ITEM",
                    data={"NOTABLE_ITEM": (self.notable_treasures, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Craft CRAFT_COUNT items at the Adamantine Forge in one playthrough",
                    data={"CRAFT_COUNT": (self.craft_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Brew ALCHEMY_POTION_COUNT different alchemical concoctions in one playthrough",
                    data={"ALCHEMY_POTION_COUNT": (self.alchemy_potion_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Brew and drink SPECIAL_ELIXIR",
                    data={"SPECIAL_ELIXIR": (self.special_elixirs, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="ANIMAL_INTERACTION ANIMAL_COMPANION",
                    data={
                        "ANIMAL_INTERACTION": (self.animal_interactions, 1),
                        "ANIMAL_COMPANION": (self.animal_companions, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Pet Scratch and the owlbear cub at the same time",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Challenge Runs
        if self.include_achievement_hunting:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the game in DIFFICULTY_MODE",
                    data={"DIFFICULTY_MODE": (self.difficulty_modes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Complete ACT_NAME without any party member dying",
                    data={"ACT_NAME": (self.act_names, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Finish the game PLAYTHROUGH_RESTRICTION",
                    data={"PLAYTHROUGH_RESTRICTION": (self.playthrough_restrictions, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Multiclass one character into all twelve classes in a single playthrough without asking Withers to change your class",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_character_builds(self) -> bool:
        return self.archipelago_options.bg3_include_character_builds.value

    @property
    def include_story_progression(self) -> bool:
        return self.archipelago_options.bg3_include_story_progression.value

    @property
    def include_companion_quests(self) -> bool:
        return self.archipelago_options.bg3_include_companion_quests.value

    @property
    def include_exploration(self) -> bool:
        return self.archipelago_options.bg3_include_exploration.value

    @property
    def include_combat_challenges(self) -> bool:
        return self.archipelago_options.bg3_include_combat_challenges.value

    @property
    def include_social_encounters(self) -> bool:
        return self.archipelago_options.bg3_include_social_encounters.value

    @property
    def include_collectibles(self) -> bool:
        return self.archipelago_options.bg3_include_collectibles.value

    @property
    def include_achievement_hunting(self) -> bool:
        return self.archipelago_options.bg3_include_achievement_hunting.value

    # Data lists — Characters and Builds
    @staticmethod
    def character_classes() -> List[str]:
        return [
            "Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk",
            "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard",
        ]

    @staticmethod
    def class_subclasses() -> List[str]:
        return [
            "Barbarian (Berserker)",
            "Barbarian (Wildheart)",
            "Barbarian (Wild Magic)",
            "Bard (College of Lore)",
            "Bard (College of Valour)",
            "Bard (College of Swords)",
            "Cleric (Light Domain)",
            "Cleric (Trickery Domain)",
            "Cleric (Tempest Domain)",
            "Cleric (War Domain)",
            "Druid (Circle of the Moon)",
            "Druid (Circle of the Land)",
            "Druid (Circle of the Spores)",
            "Fighter (Battle Master)",
            "Fighter (Eldritch Knight)",
            "Fighter (Champion)",
            "Monk (Way of the Open Hand)",
            "Monk (Way of Shadow)",
            "Monk (Way of the Four Elements)",
            "Paladin (Oath of Devotion)",
            "Paladin (Oath of the Ancients)",
            "Paladin (Oath of Vengeance)",
            "Ranger (Beast Master)",
            "Ranger (Hunter)",
            "Ranger (Gloom Stalker)",
            "Rogue (Thief)",
            "Rogue (Assassin)",
            "Rogue (Arcane Trickster)",
            "Sorcerer (Draconic Bloodline)",
            "Sorcerer (Wild Magic)",
            "Sorcerer (Storm Sorcery)",
            "Warlock (The Fiend)",
            "Warlock (The Great Old One)",
            "Warlock (Archfey)",
            "Wizard (Evocation School)",
            "Wizard (Abjuration School)",
            "Wizard (Necromancy School)",
            "Wizard (Divination School)",
        ]

    @staticmethod
    def character_races() -> List[str]:
        return [
            "Human", "Elf", "Drow", "Half-Elf", "Half-Orc", "Halfling",
            "Gnome", "Dwarf", "Duergar", "Tiefling", "Githyanki", "Dragonborn",
        ]

    @staticmethod
    def character_backgrounds() -> List[str]:
        return [
            "Acolyte", "Charlatan", "Criminal", "Entertainer", "Folk Hero",
            "Guild Artisan", "Noble", "Outlander", "Sage", "Soldier", "Urchin",
        ]

    @staticmethod
    def origin_characters() -> List[str]:
        return [
            "Astarion",
            "Gale",
            "Karlach",
            "Lae'zel",
            "Shadowheart",
            "Wyll",
            "The Dark Urge",
        ]

    @staticmethod
    def weapon_styles() -> List[str]:
        return [
            "two-handed melee weapons",
            "one-handed weapons and no shield",
            "ranged weapons",
            "thrown weapons and improvised objects",
            "unarmed strikes",
        ]

    @staticmethod
    def ability_score_focuses() -> List[str]:
        return [
            "Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma",
        ]

    @staticmethod
    def high_stat_targets() -> List[str]:
        return ["18", "20", "22"]

    @staticmethod
    def level_thresholds() -> List[str]:
        return ["5", "8", "10", "12"]

    # Data lists — Story
    @staticmethod
    def game_endings() -> List[str]:
        return [
            "an ending in which the Absolute is destroyed for good",
            "an ending in which you claim the Absolute's power for yourself",
            "an ending that demands the ultimate sacrifice",
        ]

    @staticmethod
    def alignment_choices() -> List[str]:
        return [
            "good and heroic",
            "evil and ruthless",
            "pragmatic and self-serving",
            "chaotic and unpredictable",
        ]

    @staticmethod
    def grove_decisions() -> List[str]:
        return [
            "Save",
            "Forsake",
            "Side with the goblins against",
        ]

    @staticmethod
    def challenging_side_quests() -> List[str]:
        return [
            "the rescue of everyone trapped aboard the Iron Throne, leaving no one behind (Act 3)",
            "the rescue of Counsellor Florrick before her execution at Wyrm's Rock (Act 3)",
            "the effort to bring Minsc back to his senses without harming him permanently (Act 3)",
            "the rescue of Vanra in Baldur's Gate (Act 3)",
            "all three trials of the Gauntlet of Shar (Act 2)",
            "all four trials of the Wyrmway (Act 3)",
            "the heist to claim the Orphic Hammer from the House of Hope without signing the resident's contract (Act 3)",
            "the destruction of the Steel Watch while saving every Gondian (Act 3)",
            "Halsin's effort to lift the shadow curse (Act 2)",
            "the quest to break Wyll's pact with Mizora (Act 3)",
            "the liberation of the Grand Design and the Ironhand gnomes (Acts 2-3)",
        ]

    # Data lists — Companions
    @staticmethod
    def companion_quests() -> List[str]:
        return [
            "Shadowheart's crisis of faith",
            "Astarion's reckoning with his master",
            "Gale's search for a cure to his condition",
            "Lae'zel's crisis of loyalty",
            "Wyll's entanglement with Mizora",
            "Karlach's search for engine repairs",
            "Halsin's battle against the shadow curse",
            "Jaheira and Minsc's unfinished Harper business",
        ]

    @staticmethod
    def romance_companions() -> List[str]:
        return [
            "Shadowheart",
            "Astarion",
            "Karlach",
            "Gale",
            "Lae'zel",
            "Wyll",
            "Halsin",
            "Minthara",
            "your Dream Guardian",
        ]

    @staticmethod
    def approval_companions() -> List[str]:
        return [
            "Shadowheart",
            "Astarion",
            "Karlach",
            "Gale",
            "Lae'zel",
            "Wyll",
        ]

    # Data lists — Exploration
    @staticmethod
    def major_locations() -> List[str]:
        return [
            "the Underdark (Act 1)",
            "Grymforge (Act 1)",
            "the Githyanki Creche at Rosymorn Monastery (Act 1)",
            "the Shadow-Cursed Lands (Act 2)",
            "Moonrise Towers (Act 2)",
            "the Gauntlet of Shar (Act 2)",
            "Rivington and Wyrm's Crossing (Act 3)",
            "Baldur's Gate Lower City (Act 3)",
            "the Undercity and Lower City sewers (Act 3)",
        ]

    @staticmethod
    def secret_areas() -> List[str]:
        return [
            "the Arcane Tower in the Underdark, with its power restored (Act 1)",
            "the hidden cellar beneath the Blighted Village apothecary (Act 1)",
            "the Zhentarim Hideout (Act 1)",
            "the Whispering Depths beneath the Blighted Village (Act 1)",
            "the Silent Library (Act 2)",
            "the House of Hope (Act 3)",
            "the Iron Throne (Act 3)",
            "the hidden vault of Sorcerous Sundries (Act 3)",
            "the upper floors of Ramazith's Tower (Act 3)",
            "the deepest vault of the Counting House (Act 3)",
            "the Wyrmway (Act 3)",
            "the cloister hidden beneath the House of Grief (Act 3)",
            "the temple hidden behind Candulhallow's Tombstones (Act 3)",
            "the jungle beyond the Djinni's wheel at the Circus of the Last Days (Act 3)",
        ]

    @staticmethod
    def puzzles() -> List[str]:
        return [
            "the moon-phase puzzle of the Defiled Temple (Act 1)",
            "the ceremonial weapons puzzle of Rosymorn Monastery (Act 1)",
            "the mystery of the Arcane Tower's power source (Act 1)",
            "the gallery puzzle of the Thorm Mausoleum (Act 2)",
            "the riddle guarding the Silent Library's inner vault (Act 2)",
            "the Soft-Step Trial of the Gauntlet of Shar (Act 2)",
            "the Faith-Leap Trial of the Gauntlet of Shar (Act 2)",
            "the door puzzles guarding the Sorcerous Sundries vault (Act 3)",
            "the chess challenge of the Wyrmway (Act 3)",
        ]

    @staticmethod
    def curiosities() -> List[str]:
        return [
            "Rescue Us, an unlikely ally, aboard the Nautiloid (Prologue)",
            "Befriend the owlbear cub and see it safely to your camp (Act 1)",
            "Win Mattis's shell game in the Emerald Grove (Act 1)",
            "Perform a duet with Alfira and her lute (Act 1)",
            "Attend the celebration at your camp after saving the Emerald Grove (Act 1)",
            "Strike a bargain with a hag and come away with a strand of her hair (Act 1)",
            "Free the pixie trapped inside a moonlantern (Act 2)",
            "Convince Astarion to grant Araj Oblodra's unusual request at Moonrise Towers (Act 2)",
            "Gaze into the Mirror of Loss and come away stronger for what you gave up (Act 3)",
            "Reunite Dribbles the Clown, piece by piece (Act 3)",
            "Track down the secret that keeps Mystic Carrion standing, hidden across the Lower City (Act 3)",
            "Read the Necromancy of Thay from cover to cover, whatever it takes (Acts 1-3)",
        ]

    # Data lists — Combat
    @staticmethod
    def optional_bosses() -> List[str]:
        return [
            "Commander Zhalk aboard the Nautiloid (Prologue)",
            "the Phase Spider Matriarch in the Whispering Depths (Act 1)",
            "the bulette prowling the Underdark (Act 1)",
            "Auntie Ethel in her lair beneath the Riverside Teahouse (Act 1)",
            "the Githyanki Inquisitor at Creche Y'llek (Act 1)",
            "Grym, guardian of the Adamantine Forge (Act 1)",
            "Yurgir the Orthon in the Gauntlet of Shar (Act 2)",
            "Gerringothe Thorm at the Reithwin Tollhouse (Act 2)",
            "Malus Thorm at the House of Healing (Act 2)",
            "Thisobald Thorm at the Waning Moon (Act 2)",
            "Raphael in the House of Hope (Act 3)",
            "Ansur, who slumbers beyond the Wyrmway (Act 3)",
            "Mystic Carrion of Philgrave's Mansion (Act 3)",
            "the mistress of the House of Grief and her congregation (Act 3)",
            "Lorroakan at Ramazith's Tower (Act 3)",
            "the Steel Watcher Titan in the Steel Watch Foundry (Act 3)",
            "Cazador Szarr in his palace (Act 3)",
        ]

    @staticmethod
    def tactical_feats() -> List[str]:
        return [
            "Defeat Grym without using the Forge Hammer (Act 1)",
            "Kill the Phase Spider Matriarch before any of her eggs hatch (Act 1)",
            "Eliminate all three leaders of the Goblin Camp without raising the alarm (Act 1)",
            "Defeat Gerringothe Thorm without letting her absorb any gold (Act 2)",
            "Defeat the Apostle of Myrkul before it consumes a single necromite (Act 2)",
            "Defeat Yurgir and his entire retinue in open combat (Act 2)",
            "Defeat Gortash without triggering any of the traps in his audience chamber (Act 3)",
            "Kill Orin while her followers' ritual chant is still under way (Act 3)",
            "Kill the Surgeon before he can operate on a member of your party (Act 3)",
            "Knock the dragon of the Wyrmway's Trial of Courage out of the sky mid-flight (Act 3)",
            "Defeat Raphael without destroying the Pillars of Souls that empower him (Act 3)",
            "Defeat Cazador without any of his named vampire spawn perishing (Act 3)",
            "Kill the red dragon during the final assault on the Upper City (Act 3)",
        ]

    @staticmethod
    def creature_types() -> List[str]:
        return [
            "Undead",
            "Fiend",
            "Aberration",
            "Beast",
            "Construct",
            "Monstrosity",
        ]

    @staticmethod
    def rare_creature_types() -> List[str]:
        return [
            "Elemental",
            "Fey",
        ]

    @staticmethod
    def kill_methods() -> List[str]:
        return [
            "falling damage",
            "an unarmed strike",
            "an improvised weapon",
            "an exploding barrel",
            "lightning damage while they are Wet",
            "fire damage while they stand in grease or oil",
            "a thrown weapon",
            "an attack made by a summoned creature",
        ]

    @staticmethod
    def surface_combos() -> List[str]:
        return [
            "a grease or oil surface ignited into flame",
            "water or rain combined with lightning damage",
            "water or rain combined with cold damage to freeze enemies",
            "a cloud of daggers or blade barrier placed on a chokepoint",
            "darkness or fog used to blind enemy archers and casters",
        ]

    # Data lists — Social
    @staticmethod
    def social_feats() -> List[str]:
        return [
            "Talk Yurgir the Orthon out of existence without ever drawing a blade (Act 2)",
            "Out-drink Thisobald Thorm and walk away with everything he knows (Act 2)",
            "Convince Gerringothe Thorm to part with her gold without a fight (Act 2)",
            "Persuade the nurses of the House of Healing to give their teacher one final lesson (Act 2)",
            "Befriend Bernard of the Arcane Tower using the words hidden in his tower's books (Act 1)",
            "Infiltrate the Goblin Camp and speak with all three of its leaders without shedding blood (Act 1)",
            "Expose the rigged wheel at the Circus of the Last Days and claim the true jackpot (Act 3)",
            "Get your party's name into the pages of the Baldur's Mouth Gazette (Act 3)",
        ]

    # Data lists — Loot
    @staticmethod
    def notable_treasures() -> List[str]:
        return [
            "the Blood of Lathander (Act 1)",
            "a weapon or armour forged from adamantine (Act 1)",
            "the Club of Hill Giant Strength from the Arcane Tower (Act 1)",
            "the Sussur Greatsword, Sickle or Dagger (Act 1)",
            "Phalar Aluve, sung free from the stone in the Underdark (Act 1)",
            "Mourning Frost, assembled from three pieces scattered across the Underdark (Act 1)",
            "the Vision of the Absolute, restored from its broken halves (Act 1)",
            "the Silver Sword of the Astral Plane (Act 3)",
            "the Orphic Hammer (Act 3)",
            "Balduran's Giantslayer (Act 3)",
            "the Helm of Balduran (Act 3)",
            "Gontr Mael (Act 3)",
            "Nyrulna (Act 3)",
            "Markoheshkir (Act 3)",
            "the Robe of the Weave (Act 3)",
            "Viconia's Walking Fortress (Act 3)",
            "the Duellist's Prerogative (Act 3)",
            "a full set of Helldusk armour (Act 3)",
            "the Bhaalist Armour (Act 3)",
            "the Gauntlets of Hill Giant Strength (Act 3)",
        ]

    @staticmethod
    def special_elixirs() -> List[str]:
        return [
            "an Elixir of Battlemage's Power",
            "an Elixir of Cloud Giant Strength",
            "an Elixir of Viciousness",
            "an Elixir of Bloodlust",
            "a Potion of Speed",
        ]

    @staticmethod
    def animal_interactions() -> List[str]:
        return [
            "Pet",
            "Play fetch with",
        ]

    @staticmethod
    def animal_companions() -> List[str]:
        return [
            "Scratch",
            "the owlbear cub",
            "Shovel",
        ]

    # Data lists — Challenge Runs
    @staticmethod
    def difficulty_modes() -> List[str]:
        return [
            "Tactician mode",
            "Honour mode",
        ]

    @staticmethod
    def act_names() -> List[str]:
        return ["Act 1", "Act 2", "Act 3"]

    @staticmethod
    def playthrough_restrictions() -> List[str]:
        return [
            "playing solo, with no companions in your active party",
            "without ever using Illithid powers",
            "without ever buying from or selling to a vendor",
            "as the Dark Urge, resisting your darkest impulses",
            "as the Dark Urge, embracing your nature",
            "making only good and heroic choices",
            "without any party member ever being knocked out or killed",
        ]

    # Ranges
    @staticmethod
    def multiclass_progression_counts() -> List[str]:
        return ["3", "5", "8", "12"]

    @staticmethod
    def action_counts() -> List[str]:
        return ["5", "6", "7"]

    @staticmethod
    def background_goal_counts() -> List[str]:
        return ["10", "15", "20"]

    @staticmethod
    def parasite_counts() -> List[str]:
        return ["5", "10", "15"]

    @staticmethod
    def buried_chest_counts() -> List[str]:
        return ["5", "10", "15"]

    @staticmethod
    def speak_with_dead_counts() -> List[str]:
        return ["5", "10", "15"]

    @staticmethod
    def speak_with_animals_counts() -> List[str]:
        return ["5", "10", "15"]

    @staticmethod
    def detect_thoughts_counts() -> List[str]:
        return ["3", "5", "10"]

    @staticmethod
    def drunk_opponent_counts() -> List[str]:
        return ["10", "20", "30"]

    @staticmethod
    def busking_gold_amounts() -> List[str]:
        return ["100", "200", "300"]

    @staticmethod
    def stolen_item_values() -> List[str]:
        return ["500", "1000", "2000"]

    @staticmethod
    def skill_check_dcs() -> List[str]:
        return ["20", "25", "30"]

    @staticmethod
    def craft_counts() -> List[str]:
        return ["1", "2"]

    @staticmethod
    def alchemy_potion_counts() -> List[str]:
        return ["5", "10", "15"]

    @staticmethod
    def creature_counts() -> List[str]:
        return ["10", "15", "20"]

    @staticmethod
    def rare_creature_counts() -> List[str]:
        return ["3", "5"]


# Archipelago Options
class BG3IncludeCharacterBuilds(DefaultOnToggle):
    """Include character build experimentation and multiclassing objectives."""
    display_name = "Baldurs Gate 3 Include Character Builds"

class BG3IncludeStoryProgression(DefaultOnToggle):
    """Include main story, ending, and demanding side-quest objectives."""
    display_name = "Baldurs Gate 3 Include Story Progression"

class BG3IncludeCompanionQuests(DefaultOnToggle):
    """Include companion relationship, romance, and falling-out objectives."""
    display_name = "Baldurs Gate 3 Include Companion Quests"

class BG3IncludeExploration(DefaultOnToggle):
    """Include world exploration, secret area, and puzzle objectives."""
    display_name = "Baldurs Gate 3 Include Exploration"

class BG3IncludeCombatChallenges(DefaultOnToggle):
    """Include optional boss, tactical feat, and monster hunting objectives."""
    display_name = "Baldurs Gate 3 Include Combat Challenges"

class BG3IncludeSocialEncounters(DefaultOnToggle):
    """Include dialogue, persuasion, larceny, and social interaction objectives."""
    display_name = "Baldurs Gate 3 Include Social Encounters"

class BG3IncludeCollectibles(DefaultOnToggle):
    """Include rare loot, crafting, and treasure hunting objectives."""
    display_name = "Baldurs Gate 3 Include Collectibles"

class BG3IncludeAchievementHunting(DefaultOnToggle):
    """Include difficulty-mode completion and challenge-run objectives."""
    display_name = "Baldurs Gate 3 Include Challenge Objectives"
