from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, TextChoice

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
    bg3_difficulty_preference: BG3DifficultyPreference
    bg3_playstyle_focus: BG3PlaystyleFocus


class BaldursGate3Game(Game):
    name = "Baldur's Gate 3"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = BaldursGate3ArchipelagoOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Character Builds
        if self.include_character_builds:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Multiclass into MULTICLASS_COUNT different classes without respeccing and reach LEVEL_THRESHOLD",
                    data={
                        "MULTICLASS_COUNT": (self.multiclass_progression_counts, 1),
                        "LEVEL_THRESHOLD": (self.level_thresholds, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Reach level 12 with a pure CLASS character",
                    data={"CLASS": (self.character_classes, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Build a character focused on ABILITY_SCORE_FOCUS (reaching HIGH_STAT in that stat) and reach LEVEL_THRESHOLD",
                    data={
                        "ABILITY_SCORE_FOCUS": (self.ability_score_focuses, 1),
                        "HIGH_STAT": (self.high_stat_targets, 1),
                        "LEVEL_THRESHOLD": (self.level_thresholds, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Perform ACTION_COUNT attacks in one turn",
                    data={"ACTION_COUNT": (self.action_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Complete BACKGROUND_GOAL_COUNT background goals in one playthrough",
                    data={"BACKGROUND_GOAL_COUNT": (self.background_goal_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
            ])

        # Story Progression
        if self.include_story_progression:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach GAME_ENDING ending",
                    data={"GAME_ENDING": (self.game_endings, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Complete the game making primarily ALIGNMENT_CHOICE choices",
                    data={"ALIGNMENT_CHOICE": (self.alignment_choices, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Consume PARASITE_COUNT parasites and unlock new powers",
                    data={"PARASITE_COUNT": (self.parasite_counts, 1)},
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
                    label="TIEFLING_OUTCOME the tiefling refugees throughout the game",
                    data={"TIEFLING_OUTCOME": (self.tiefling_outcomes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
            ])

        # Companion Quests
        if self.include_companion_quests:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete COMPANION_QUEST companion quest",
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
                    label="Recruit HIRELING_COUNT hirelings",
                    data={"HIRELING_COUNT": (self.hireling_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Recruit PARTY_MEMBER_COUNT party members by end of Act 1",
                    data={"PARTY_MEMBER_COUNT": (self.party_member_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
            ])

        # Exploration
        if self.include_exploration:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Dig up BURIED_CHEST_COUNT buried chests",
                    data={"BURIED_CHEST_COUNT": (self.buried_chest_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Discover WAYPOINT_COUNT waypoints",
                    data={"WAYPOINT_COUNT": (self.waypoint_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Take LONG_REST_COUNT full long rests",
                    data={"LONG_REST_COUNT": (self.long_rest_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Successfully use Detect Thoughts on DETECT_THOUGHTS_COUNT NPCs",
                    data={"DETECT_THOUGHTS_COUNT": (self.detect_thoughts_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Explore LOCATION_NAME and complete its associated quests",
                    data={"LOCATION_NAME": (self.major_locations, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
            ])

        # Combat Challenges
        if self.include_combat_challenges:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="BOSS_CHALLENGE boss challenge",
                    data={"BOSS_CHALLENGE": (self.boss_challenges, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Use one enemy as improvised weapon against another",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Kill a creature with KILL_METHOD",
                    data={"KILL_METHOD": (self.kill_methods, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Defeat DRUNK_OPPONENT_COUNT opponents while drunk",
                    data={"DRUNK_OPPONENT_COUNT": (self.drunk_opponent_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Complete a long rest using only alcohol",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            ])

        # Social Encounters
        if self.include_social_encounters:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Break out of prison after being arrested",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Earn BUSKING_GOLD gold from playing music",
                    data={"BUSKING_GOLD": (self.busking_gold_amounts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="PRISON_RESCUE prisoners from PRISON_LOCATION",
                    data={
                        "PRISON_RESCUE": (self.prison_rescue_goals, 1),
                        "PRISON_LOCATION": (self.prison_locations, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Rescue Sazza from SAZZA_RESCUE_COUNT different locations",
                    data={"SAZZA_RESCUE_COUNT": (self.sazza_rescue_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
            ])

        # Collectibles
        if self.include_collectibles:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Obtain LEGENDARY_ITEM legendary item",
                    data={"LEGENDARY_ITEM": (self.legendary_items, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Craft CRAFT_COUNT items at the Adamantine Forge",
                    data={"CRAFT_COUNT": (self.craft_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Create ALCHEMY_POTION_COUNT unique alchemical solutions",
                    data={"ALCHEMY_POTION_COUNT": (self.alchemy_potion_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="CREATURE_INTERACTION with CREATURE_NAME",
                    data={
                        "CREATURE_INTERACTION": (self.creature_interactions, 1),
                        "CREATURE_NAME": (self.creature_names, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        # Achievement Hunting
        if self.include_achievement_hunting:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the game in DIFFICULTY_MODE difficulty",
                    data={"DIFFICULTY_MODE": (self.difficulty_modes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Complete ACT_NAME without any party member deaths",
                    data={"ACT_NAME": (self.act_names, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Finish the game with PLAYTHROUGH_RESTRICTION restriction",
                    data={"PLAYTHROUGH_RESTRICTION": (self.playthrough_restrictions, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
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

    @property
    def difficulty_preference(self) -> str:
        return self.archipelago_options.bg3_difficulty_preference.value

    @property
    def playstyle_focus(self) -> str:
        return self.archipelago_options.bg3_playstyle_focus.value

    # Data lists
    @staticmethod
    def character_classes() -> List[str]:
        return [
            "Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk",
            "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"
        ]

    @staticmethod
    def ability_score_focuses() -> List[str]:
        return [
            "Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"
        ]

    @staticmethod
    def high_stat_targets() -> List[str]:
        return ["18", "20", "22"]

    @staticmethod
    def level_thresholds() -> List[str]:
        return ["8", "10", "12"]

    @staticmethod
    def game_endings() -> List[str]:
        return [
            "Destroy the Absolute (Hero ending)",
            "Control the Netherbrain for yourself (Absolute Power)",
            "Control the Netherbrain for Bhaal (Sins of the Father)",
            "Become a mindflayer to defeat the Netherbrain (Ceremorphosis)"
        ]

    @staticmethod
    def alignment_choices() -> List[str]:
        return [
            "Good and heroic",
            "Evil and ruthless",
            "Pragmatic and self-serving",
            "Chaotic and unpredictable"
        ]

    @staticmethod
    def grove_decisions() -> List[str]:
        return [
            "Save",
            "Let fall",
            "Side with the goblins against"
        ]

    @staticmethod
    def tiefling_outcomes() -> List[str]:
        return [
            "Save all",
            "Condemn",
            "Save most of"
        ]

    @staticmethod
    def companion_quests() -> List[str]:
        return [
            "Shadowheart's Sharran crisis",
            "Astarion's confrontation with Cazador",
            "Gale's stabilization (Repairing the Weave)",
            "Lae'zel's alliance with Voss (The Lich-Queen's Wrath)",
            "Wyll's pact with Mizora (Loophole)",
            "Karlach's engine and hot date",
            "Halsin's shadow curse quest",
            "Minthara's recruitment",
            "Minsc and Jaheira's companion quests"
        ]

    @staticmethod
    def romance_companions() -> List[str]:
        return [
            "Shadowheart (To Bloom in Darkest Night)",
            "Astarion (Just a Nibble)",
            "Karlach (Hot Date)",
            "Gale",
            "Lae'zel",
            "Wyll",
            "Halsin",
            "Minthara",
            "The Emperor (Mind Blown)"
        ]

    @staticmethod
    def major_locations() -> List[str]:
        return [
            "The Underdark",
            "Grymforge and the Adamantine Forge",
            "The Githyanki Creche",
            "The Shadow-Cursed Lands",
            "Moonrise Towers",
            "The Gauntlet of Shar",
            "Baldur's Gate Lower City",
            "Baldur's Gate Upper City",
            "The Wyrmway",
            "Rosymorn Monastery"
        ]

    @staticmethod
    def boss_challenges() -> List[str]:
        return [
            "Defeat Commander Zhalk on the Nautiloid",
            "Kill the Spider Matriarch before eggs hatch (Pest Control)",
            "Kill the Adamantine Golem without Forge Hammer (A Grym Fate)",
            "Kill the Surgeon before surgery (Non-invasive Procedure)",
            "Defeat Toll Collector without her using gold (Penny Pincher)",
            "Defeat Apostle of Myrkul before it consumes Necromites (No Free Lunches)",
            "Defeat Gortash without activating traps (Fancy Footwork)",
            "Kill Orin during ritual chant (First Blood)",
            "Kill the Red Dragon in Upper City (Interfectorem Draconis)",
            "Knock dragon from sky in Wyrmway (Crash Landing)"
        ]

    @staticmethod
    def kill_methods() -> List[str]:
        return [
            "falling damage (Shove Off)",
            "an unarmed strike (Fists of Fury)"
        ]

    @staticmethod
    def prison_rescue_goals() -> List[str]:
        return [
            "Rescue all",
            "Rescue some of the",
            "Free at least half the"
        ]

    @staticmethod
    def prison_locations() -> List[str]:
        return [
            "Moonrise Towers (Under Lock and Key)",
            "the Emerald Grove",
            "the Goblin Camp",
            "Baldur's Gate prison"
        ]

    @staticmethod
    def legendary_items() -> List[str]:
        return [
            "the Blood of Lathander (Taking Blood)",
            "a legendary weapon from Adamantine Forge",
            "Netherstones from the Chosen Three",
            "the Silver Sword of the Astral Plane",
            "Balduran's Giantslayer",
            "the Orphic Hammer",
            "Viconia's Walking Fortress"
        ]

    @staticmethod
    def creature_interactions() -> List[str]:
        return [
            "Pet both",
            "Play fetch with",
            "Find and summon",
            "Recruit"
        ]

    @staticmethod
    def creature_names() -> List[str]:
        return [
            "Scratch and Owlbear cub (You Have Two Hands for a Reason)",
            "Scratch (Fetch Quest)",
            "Shovel the quasit (Rude, Crude, and Full of Attitude)",
            "Us the intellect devourer"
        ]

    @staticmethod
    def difficulty_modes() -> List[str]:
        return [
            "Tactician mode (Critical Hit)",
            "Honour mode (Foehammer)"
        ]

    @staticmethod
    def act_names() -> List[str]:
        return ["Act 1", "Act 2", "Act 3"]

    @staticmethod
    def playthrough_restrictions() -> List[str]:
        return [
            "Embrace Dark Urge and become Bhaal's Slayer (Embrace Your Urge)",
            "Become Unholy Assassin of Bhaal (Murder in Baldur's Gate)",
            "Pure Good choices only",
            "Solo (no companions)",
            "Pacifist approach where possible"
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
        return ["1", "3", "5", "10"]

    @staticmethod
    def hireling_counts() -> List[str]:
        return ["1", "2", "3"]

    @staticmethod
    def party_member_counts() -> List[str]:
        return ["5", "7", "all"]

    @staticmethod
    def buried_chest_counts() -> List[str]:
        return ["5", "10", "15"]

    @staticmethod
    def long_rest_counts() -> List[str]:
        return ["4", "8", "12"]

    @staticmethod
    def detect_thoughts_counts() -> List[str]:
        return ["3", "5", "10"]

    @staticmethod
    def drunk_opponent_counts() -> List[str]:
        return ["10", "20", "30"]

    @staticmethod
    def busking_gold_amounts() -> List[str]:
        return ["50", "100", "200"]

    @staticmethod
    def sazza_rescue_counts() -> List[str]:
        return ["2", "3"]

    @staticmethod
    def craft_counts() -> List[str]:
        return ["1", "2"]

    @staticmethod
    def alchemy_potion_counts() -> List[str]:
        return ["3", "5", "10"]

    @staticmethod
    def waypoint_counts() -> List[str]:
        return ["10", "15", "20"]


# Archipelago Options
class BG3IncludeCharacterBuilds(DefaultOnToggle):
    """Include character build experimentation and multiclassing objectives."""
    display_name = "Baldurs Gate 3 Include Character Builds"

class BG3IncludeStoryProgression(DefaultOnToggle):
    """Include main story and narrative choice objectives."""
    display_name = "Baldurs Gate 3 Include Story Progression"

class BG3IncludeCompanionQuests(DefaultOnToggle):
    """Include companion relationship and personal quest objectives."""
    display_name = "Baldurs Gate 3 Include Companion Quests"

class BG3IncludeExploration(DefaultOnToggle):
    """Include world exploration and discovery objectives."""
    display_name = "Baldurs Gate 3 Include Exploration"

class BG3IncludeCombatChallenges(DefaultOnToggle):
    """Include tactical combat and boss fight objectives."""
    display_name = "Baldurs Gate 3 Include Combat Challenges"

class BG3IncludeSocialEncounters(DefaultOnToggle):
    """Include dialogue, persuasion, and social interaction objectives."""
    display_name = "Baldurs Gate 3 Include Social Encounters"

class BG3IncludeCollectibles(DefaultOnToggle):
    """Include item collection and treasure hunting objectives."""
    display_name = "Baldurs Gate 3 Include Collectibles"

class BG3IncludeAchievementHunting(DefaultOnToggle):
    """Include achievement and completion challenge objectives."""
    display_name = "Baldurs Gate 3 Include Achievement Hunting"

class BG3DifficultyPreference(TextChoice):
    """Prefer certain difficulty levels for objectives."""
    display_name = "Baldurs Gate 3 Difficulty Preference"
    option_all = 0
    option_easy = 1
    option_hard = 2
    default = 0

class BG3PlaystyleFocus(TextChoice):
    """Focus objectives on specific playstyles."""
    display_name = "Baldurs Gate 3 Playstyle Focus"
    option_all = 0
    option_combat = 1
    option_story = 2
    option_exploration = 3
    default = 0
