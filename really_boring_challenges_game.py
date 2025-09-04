from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ReallyBoringChallengesArchipelagoOptions:
    really_boring_challenges_include_repetitive_counting: RBCIncludeRepetitiveCounting
    really_boring_challenges_include_mindless_clicking: RBCIncludeMindlessClicking
    really_boring_challenges_include_patience_tests: RBCIncludeTediousWaiting
    really_boring_challenges_include_tedious_sorting: RBCIncludePointlessOrganizing
    really_boring_challenges_include_mind_numbing_memorization: RBCIncludeMindNumbingTasks
    really_boring_challenges_include_soul_crushing_repetition: RBCIncludeSoulCrushingGrinds
    really_boring_challenges_task_count: RBCTaskCount
    really_boring_challenges_completion_goal: RBCCompletionGoal


class ReallyBoringChallengesGame(Game):
    name = "Really Boring Challenges"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = ReallyBoringChallengesArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective without any distractions (no music, videos, etc.)",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective while maintaining FOCUS_LEVEL concentration",
                data={"FOCUS_LEVEL": (self.focus_levels, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective in ENVIRONMENT_TYPE environment",
                data={"ENVIRONMENT_TYPE": (self.boring_environments, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective using only INTERACTION_VERB_METHOD",
                data={"INTERACTION_VERB_METHOD": (self.tedious_methods, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective while documenting every DOCUMENTATION_INTERVAL",
                data={"DOCUMENTATION_INTERVAL": (self.documentation_frequencies, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective at SPEED_LEVEL speed",
                data={"SPEED_LEVEL": (self.painfully_slow_speeds, 1)},
            ),
        ])
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Repetitive Counting
        if self.include_repetitive_counting:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Count from 1 to COUNT_TARGET out loud without losing track",
                    data={"COUNT_TARGET": (self.massive_count_targets, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Count every COUNTABLE_THING in COUNTING_LOCATION",
                    data={
                        "COUNTABLE_THING": (self.boring_countables, 1),
                        "COUNTING_LOCATION": (self.vast_areas, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Perform COUNT_REPETITIONS repetitions of BORING_ACTION_VERB",
                    data={
                        "COUNT_REPETITIONS": (self.soul_crushing_repetitions, 1),
                        "BORING_ACTION_VERB": (self.mind_numbing_actions, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Count backwards from COUNTDOWN_START to 0 without making errors",
                    data={"COUNTDOWN_START": (self.large_countdown_numbers, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Count in increments of INCREMENT_VALUE up to FINAL_COUNT",
                    data={
                        "INCREMENT_VALUE": (self.tedious_increments, 1),
                        "FINAL_COUNT": (self.exhausting_totals, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Mindless Clicking
        if self.include_mindless_clicking:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Click CLICK_TARGET exactly CLICK_COUNT times",
                    data={
                        "CLICK_TARGET": (self.clickable_things, 1),
                        "CLICK_COUNT": (self.astronomical_click_counts, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Press BUTTON_SEQUENCE SEQUENCE_REPETITIONS times in exact order",
                    data={
                        "BUTTON_SEQUENCE": (self.button_sequences, 1),
                        "SEQUENCE_REPETITIONS": (self.sequence_counts, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Click at exactly CLICK_INTERVAL second intervals for DURATION minutes",
                    data={
                        "CLICK_INTERVAL": (self.precise_intervals, 1),
                        "DURATION": (self.endless_durations, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Alternate between BUTTON_A and BUTTON_B for ALTERNATION_COUNT times",
                    data={
                        "BUTTON_A": (self.buttons, 1),
                        "BUTTON_B": (self.buttons, 1),
                        "ALTERNATION_COUNT": (self.alternation_counts, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Tedious Waiting
        if self.include_tedious_waiting:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Wait exactly WAIT_DURATION without doing anything else",
                    data={"WAIT_DURATION": (self.excruciating_wait_times, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Watch WATCHING_TARGET for OBSERVATION_DURATION without looking away",
                    data={
                        "WATCHING_TARGET": (self.boring_watch_targets, 1),
                        "OBSERVATION_DURATION": (self.mind_melting_durations, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Sit completely still for STILLNESS_DURATION",
                    data={"STILLNESS_DURATION": (self.torture_durations, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Wait for RANDOM_EVENT to occur naturally (no interference)",
                    data={"RANDOM_EVENT": (self.rare_random_events, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Stare at STARING_TARGET for STARE_DURATION without blinking excessively",
                    data={
                        "STARING_TARGET": (self.staring_targets, 1),
                        "STARE_DURATION": (self.eye_strain_durations, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Pointless Organizing
        if self.include_pointless_organizing:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Organize ITEM_COUNT ITEMS by ORGANIZATION_CRITERIA",
                    data={
                        "ITEM_COUNT": (self.overwhelming_item_counts, 1),
                        "ITEMS": (self.mundane_items, 1),
                        "ORGANIZATION_CRITERIA": (self.absurd_criteria, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Arrange ARRANGEMENT_ITEMS in perfect ARRANGEMENT_PATTERN",
                    data={
                        "ARRANGEMENT_ITEMS": (self.arrangeable_objects, 1),
                        "ARRANGEMENT_PATTERN": (self.complex_patterns, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Categorize CATEGORIZATION_COUNT items into CATEGORY_COUNT categories",
                    data={
                        "CATEGORIZATION_COUNT": (self.massive_categorization_counts, 1),
                        "CATEGORY_COUNT": (self.category_counts, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Create a detailed inventory of INVENTORY_SUBJECT",
                    data={"INVENTORY_SUBJECT": (self.inventory_subjects, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Soul Crushing Grinds
        if self.include_soul_crushing_grinds:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Perform GRIND_ACTION_VERB GRIND_COUNT times consecutively",
                    data={
                        "GRIND_ACTION_VERB": (self.soul_destroying_actions, 1),
                        "GRIND_COUNT": (self.spirit_breaking_counts, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete GRIND_TASK for GRIND_DURATION without breaks",
                    data={
                        "GRIND_TASK": (self.monotonous_tasks, 1),
                        "GRIND_DURATION": (self.soul_crushing_durations, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Achieve ACHIEVEMENT_TARGET through pure repetition",
                    data={"ACHIEVEMENT_TARGET": (self.pointless_achievements, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Mind Numbing Tasks
        if self.include_mind_numbing_tasks:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete MIND_NUMBING_TASK with perfect precision",
                    data={"MIND_NUMBING_TASK": (self.precision_tasks, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Repeat REPETITIVE_PHRASE PHRASE_COUNT times out loud",
                    data={
                        "REPETITIVE_PHRASE": (self.mind_numbing_phrases, 1),
                        "PHRASE_COUNT": (self.phrase_repetition_counts, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Perform MEDITATION_TASK for MEDITATION_DURATION",
                    data={
                        "MEDITATION_TASK": (self.boring_meditation_tasks, 1),
                        "MEDITATION_DURATION": (self.meditation_durations, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_repetitive_counting(self) -> bool:
        return self.archipelago_options.really_boring_challenges_include_repetitive_counting.value

    @property
    def include_mindless_clicking(self) -> bool:
        return self.archipelago_options.really_boring_challenges_include_mindless_clicking.value

    @property
    def include_tedious_waiting(self) -> bool:
        return self.archipelago_options.really_boring_challenges_include_patience_tests.value

    @property
    def include_pointless_organizing(self) -> bool:
        return self.archipelago_options.really_boring_challenges_include_tedious_sorting.value

    @property
    def include_soul_crushing_grinds(self) -> bool:
        return self.archipelago_options.really_boring_challenges_include_soul_crushing_repetition.value

    @property
    def include_mind_numbing_tasks(self) -> bool:
        return self.archipelago_options.really_boring_challenges_include_mind_numbing_memorization.value

    # Data lists for maximum boredom
    @staticmethod
    def boring_countables() -> List[str]:
        return [
            "grains of sand", "blades of grass", "ceiling tiles", "floor tiles", "bricks",
            "leaves on trees", "stars in the sky", "clouds", "raindrops", "dust particles",
            "pixels on screen", "words in books", "letters in sentences", "cracks in walls"
        ]

    @staticmethod
    def vast_areas() -> List[str]:
        return [
            "entire city", "large park", "shopping mall", "university campus", "airport",
            "convention center", "forest", "beach", "mountain range", "desert"
        ]

    @staticmethod
    def mind_numbing_actions() -> List[str]:
        return [
            "tapping finger", "blinking", "breathing deeply", "nodding head", "shrugging",
            "clapping hands", "snapping fingers", "clearing throat", "saying 'yes'", "saying 'no'"
        ]

    @staticmethod
    def clickable_things() -> List[str]:
        return [
            "empty space", "desktop", "menu button", "refresh button", "same link",
            "calculator numbers", "keyboard keys", "mouse buttons", "touchpad", "screen"
        ]

    @staticmethod
    def button_sequences() -> List[str]:
        return [
            "A-B-A-B", "1-2-3-4-5", "Up-Down-Left-Right", "Space-Enter-Space-Enter",
            "Tab-Tab-Enter", "Ctrl-C-Ctrl-V", "Alt-Tab-Alt-Tab", "F5-F5-F5"
        ]

    @staticmethod
    def buttons() -> List[str]:
        return [
            "Space", "Enter", "A", "B", "1", "2", "Left Click", "Right Click", "Tab", "Shift"
        ]

    @staticmethod
    def boring_watch_targets() -> List[str]:
        return [
            "loading screen", "progress bar", "clock", "blank wall", "unchanging desktop",
            "static image", "paused video", "screensaver", "cursor blinking", "empty document"
        ]

    @staticmethod
    def rare_random_events() -> List[str]:
        return [
            "specific cloud formation", "bird landing nearby", "car honking", "phone ringing",
            "notification sound", "someone walking by", "wind blowing", "door closing"
        ]

    @staticmethod
    def staring_targets() -> List[str]:
        return [
            "single dot", "blank wall", "white screen", "black screen", "cursor",
            "corner of room", "ceiling fan", "light bulb", "window", "mirror"
        ]

    @staticmethod
    def mundane_items() -> List[str]:
        return [
            "paperclips", "rubber bands", "pens", "pencils", "staples", "coins", "buttons",
            "screws", "nails", "paper clips", "thumbtacks", "erasers", "marbles"
        ]

    @staticmethod
    def absurd_criteria() -> List[str]:
        return [
            "color intensity", "weight estimation", "alphabetical order", "size perception",
            "age guessing", "material type", "origin country", "purchase date", "usage frequency"
        ]

    @staticmethod
    def arrangeable_objects() -> List[str]:
        return [
            "books", "CDs", "files", "photos", "cards", "coins", "stones", "shells",
            "leaves", "papers", "tools", "utensils", "toys", "bottles"
        ]

    @staticmethod
    def complex_patterns() -> List[str]:
        return [
            "perfect spiral", "rainbow gradient", "size progression", "geometric shape",
            "mandala pattern", "symmetrical design", "color wheel", "mathematical sequence"
        ]

    @staticmethod
    def inventory_subjects() -> List[str]:
        return [
            "entire room contents", "computer files", "clothing items", "kitchen utensils",
            "bathroom supplies", "office supplies", "book collection", "music collection"
        ]

    @staticmethod
    def monotonous_patterns() -> List[str]:
        return [
            "perfect circle", "figure eight", "straight line", "zigzag", "square",
            "triangle", "spiral", "back and forth", "random walk", "maze pattern"
        ]

    @staticmethod
    def walking_areas() -> List[str]:
        return [
            "room", "hallway", "parking lot", "field", "track", "sidewalk",
            "mall corridor", "office floor", "backyard", "driveway"
        ]

    @staticmethod
    def boring_collectibles() -> List[str]:
        return [
            "bottle caps", "candy wrappers", "receipts", "business cards", "napkins",
            "plastic bags", "rubber bands", "twist ties", "paper clips", "staples"
        ]

    @staticmethod
    def tedious_gathering_targets() -> List[str]:
        return [
            "fallen leaves", "small stones", "pieces of paper", "lost items", "trash",
            "twigs", "acorns", "shells", "bottle caps", "coins"
        ]

    @staticmethod
    def exhaustive_areas() -> List[str]:
        return [
            "entire neighborhood", "large parking lot", "public park", "beach shoreline",
            "forest floor", "field", "campus grounds", "shopping district"
        ]

    @staticmethod
    def sortable_items() -> List[str]:
        return [
            "socks", "books", "papers", "photos", "files", "emails", "contacts",
            "music", "videos", "documents", "tools", "supplies"
        ]

    @staticmethod
    def tedious_sorting_methods() -> List[str]:
        return [
            "alphabetical order", "chronological order", "size order", "color gradient",
            "frequency of use", "personal preference", "random assignment", "category type"
        ]

    @staticmethod
    def soul_destroying_actions() -> List[str]:
        return [
            "opening and closing doors", "turning lights on and off", "refreshing browser",
            "typing and deleting text", "drawing circles", "counting to 100", "saying alphabet"
        ]

    @staticmethod
    def monotonous_tasks() -> List[str]:
        return [
            "data entry", "copy-pasting", "file organizing", "email sorting", "list making",
            "inventory checking", "repetitive calculations", "format adjusting"
        ]

    @staticmethod
    def pointless_achievements() -> List[str]:
        return [
            "world record sitting", "most clicks per hour", "longest staring contest",
            "perfect organization", "complete inventory", "maximum boredom level"
        ]

    @staticmethod
    def precision_tasks() -> List[str]:
        return [
            "drawing perfect circles", "typing without errors", "timing to exact seconds",
            "measuring precisely", "aligning perfectly", "spacing evenly", "balancing objects"
        ]

    @staticmethod
    def mind_numbing_phrases() -> List[str]:
        return [
            "the quick brown fox", "hello world", "this is boring", "counting numbers",
            "alphabet recitation", "color names", "day of week", "month names"
        ]

    @staticmethod
    def boring_meditation_tasks() -> List[str]:
        return [
            "counting breaths", "focusing on single point", "emptying mind completely",
            "observing thoughts without judgment", "body scan meditation", "mantra repetition"
        ]

    @staticmethod
    def focus_levels() -> List[str]:
        return [
            "laser focus", "intense concentration", "moderate attention", "minimal awareness"
        ]

    @staticmethod
    def boring_environments() -> List[str]:
        return [
            "completely silent room", "white-walled space", "empty office", "library corner",
            "basement", "waiting room", "sterile environment", "beige cubicle"
        ]

    @staticmethod
    def tedious_methods() -> List[str]:
        return [
            "single finger typing", "one-handed operation", "eyes closed", "standing on one foot",
            "left hand only", "right hand only", "voice commands only", "minimal movement"
        ]

    @staticmethod
    def documentation_frequencies() -> List[str]:
        return [
            "every minute", "every 5 minutes", "every 10 minutes", "every action",
            "every thought", "every blink", "every breath", "every movement"
        ]

    @staticmethod
    def painfully_slow_speeds() -> List[str]:
        return [
            "glacial pace", "snail speed", "turtle speed", "sloth speed", "extremely slow",
            "barely moving", "micro-movements", "freeze-frame speed"
        ]

    # Ranges for manageable tedium (10 minutes to 2 hours mostly)
    @staticmethod
    def massive_count_targets() -> range:
        return range(500, 5000, 500)  # 10-60 minutes

    @staticmethod
    def soul_crushing_repetitions() -> range:
        return range(100, 2000, 200)  # 5-30 minutes

    @staticmethod
    def large_countdown_numbers() -> range:
        return range(1000, 10000, 1000)  # 10-60 minutes

    @staticmethod
    def tedious_increments() -> range:
        return range(7, 13, 1)  # Prime numbers for extra tedium

    @staticmethod
    def exhausting_totals() -> range:
        return range(5000, 50000, 5000)  # 30 minutes to 2+ hours

    @staticmethod
    def astronomical_click_counts() -> range:
        return range(500, 10000, 1000)  # 15-90 minutes

    @staticmethod
    def sequence_counts() -> range:
        return range(50, 1000, 100)  # 10-60 minutes

    @staticmethod
    def precise_intervals() -> range:
        return range(1, 10, 1)

    @staticmethod
    def endless_durations() -> range:
        return range(10, 120, 15)  # 10 minutes to 2 hours

    @staticmethod
    def alternation_counts() -> range:
        return range(200, 5000, 500)  # 10-60 minutes

    @staticmethod
    def excruciating_wait_times() -> range:
        return range(5, 120, 10)  # 5 minutes to 2 hours

    @staticmethod
    def mind_melting_durations() -> range:
        return range(10, 90, 15)  # 10-90 minutes

    @staticmethod
    def torture_durations() -> range:
        return range(10, 60, 10)  # 10-60 minutes

    @staticmethod
    def eye_strain_durations() -> range:
        return range(3, 30, 3)  # 3-30 minutes

    @staticmethod
    def overwhelming_item_counts() -> range:
        return range(100, 2000, 200)  # 15-60 minutes

    @staticmethod
    def massive_categorization_counts() -> range:
        return range(200, 3000, 300)  # 20-90 minutes

    @staticmethod
    def category_counts() -> range:
        return range(5, 25, 5)  # More manageable categories

    @staticmethod
    def marathon_distances() -> range:
        return range(1, 10, 1)  # 1-10 miles (20 minutes to 3 hours)

    @staticmethod
    def leg_numbing_durations() -> range:
        return range(20, 120, 20)  # 20 minutes to 2 hours

    @staticmethod
    def precise_step_counts() -> range:
        return range(2000, 20000, 2000)  # 20-60 minutes

    @staticmethod
    def dizzying_lap_counts() -> range:
        return range(10, 200, 20)  # 10-45 minutes

    @staticmethod
    def enormous_collection_counts() -> range:
        return range(100, 5000, 500)  # 15-90 minutes

    @staticmethod
    def overwhelming_sorting_counts() -> range:
        return range(100, 3000, 300)  # 15-75 minutes

    @staticmethod
    def spirit_breaking_counts() -> range:
        return range(200, 5000, 500)  # 15-90 minutes

    @staticmethod
    def soul_crushing_durations() -> range:
        return range(30, 180, 30)  # 30 minutes to 3 hours (rare extremes)

    @staticmethod
    def phrase_repetition_counts() -> range:
        return range(100, 2000, 200)  # 10-45 minutes

    @staticmethod
    def meditation_durations() -> range:
        return range(15, 120, 15)  # 15 minutes to 2 hours


# Archipelago Options
class RBCIncludeRepetitiveCounting(DefaultOnToggle):
    """Include repetitive counting objectives that test patience."""
    display_name = "Include Repetitive Counting"

class RBCIncludeMindlessClicking(DefaultOnToggle):
    """Include mindless clicking and button pressing objectives."""
    display_name = "Include Mindless Clicking"

class RBCIncludeTediousWaiting(DefaultOnToggle):
    """Include waiting and observation objectives."""
    display_name = "Include Tedious Waiting"

class RBCIncludePointlessOrganizing(DefaultOnToggle):
    """Include organizing and sorting objectives."""
    display_name = "Include Pointless Organizing"

class RBCIncludeEndlessWalking(DefaultOnToggle):
    """Include walking and movement pattern objectives."""
    display_name = "Include Endless Walking"

class RBCIncludeMonotonousCollection(DefaultOnToggle):
    """Include collection and gathering objectives."""
    display_name = "Include Monotonous Collection"

class RBCIncludeSoulCrushingGrinds(DefaultOnToggle):
    """Include repetitive grinding and achievement objectives."""
    display_name = "Include Soul Crushing Grinds"

class RBCIncludeMindNumbingTasks(DefaultOnToggle):
    """Include precision and meditation objectives."""
    display_name = "Include Mind Numbing Tasks"

class RBCBoredomIntensity(Choice):
    """How boring should the challenges be?"""
    display_name = "Boredom Intensity"
    option_mildly_tedious = "Mildly Tedious"
    option_quite_boring = "Quite Boring"
    option_extremely_dull = "Extremely Dull"
    option_soul_crushing = "Soul Crushing"
    option_mind_numbing = "Mind Numbing"
    default = "quite_boring"

class RBCTaskCount(Choice):
    """How many boring challenges should be included?"""
    display_name = "Task Count"
    option_all_fifty = "All Fifty"
    option_thirty_five = "Thirty Five"
    default = option_twenty_five = "Twenty Five"
    option_fifteen = "Fifteen"
    option_ten = "Ten"
    option_five = "Five"

class RBCCompletionGoal(Choice):
    """What percentage of tasks should you aim to complete?"""
    display_name = "Completion Goal"
    option_complete_everything = "Complete Everything"
    option_most_tasks = "Most Tasks"
    default = option_half_tasks = "Half Tasks"
    option_minimal_engagement = "Minimal Engagement"
    option_survival_mode = "Survival Mode"
