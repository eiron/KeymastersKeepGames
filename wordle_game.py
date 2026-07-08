from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import DefaultOnToggle, OptionSet, Range

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class WordleArchipelagoOptions:
    wordle_include_wordle: WordleIncludeWordle
    wordle_variants: WordleVariants
    wordle_themed_variants: WordleThemedVariants
    wordle_non_word_variants: WordleNonWordVariants
    wordle_multi_grid_variants: WordleMultiGridVariants
    wordle_include_variants: WordleIncludeVariants
    wordle_include_multi_grid: WordleIncludeMultiGrid
    wordle_include_challenge_runs: WordleIncludeChallengeRuns
    wordle_daily_puzzles: WordleDailyPuzzles
    wordle_minimum_daily_puzzle_count: WordleMinimumDailyPuzzleCount
    wordle_maximum_daily_puzzle_count: WordleMaximumDailyPuzzleCount


class WordleGame(Game):
    name = "Wordle"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = WordleArchipelagoOptions

    # Properties
    @property
    def include_wordle(self) -> bool:
        return bool(self.archipelago_options.wordle_include_wordle.value)

    @property
    def include_variants(self) -> bool:
        return bool(self.archipelago_options.wordle_include_variants.value)

    @property
    def include_multi_grid(self) -> bool:
        return bool(self.archipelago_options.wordle_include_multi_grid.value)

    @property
    def include_challenge_runs(self) -> bool:
        return bool(self.archipelago_options.wordle_include_challenge_runs.value)

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = []

        constraints += [
            GameObjectiveTemplate(
                label="Solve a puzzle without using hints or helper tools",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Play with Hard Mode enabled where the puzzle supports it",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Never reuse a letter you already know is not in the word (Ultra Hard Mode), where applicable",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Solve the puzzle in under TIME_LIMIT",
                data={
                    "TIME_LIMIT": (self.time_limits, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
        ]

        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = []

        if self.include_wordle:
            templates.extend([
                GameObjectiveTemplate(
                    label="Solve today's Wordle",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Solve Wordle in GUESS_LIMIT guesses or less",
                    data={
                        "GUESS_LIMIT": (self.guess_limits, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Solve STREAK_COUNT Wordle puzzle(s) in a row",
                    data={
                        "STREAK_COUNT": (self.streak_counts, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Solve a Wordle puzzle in Hard Mode",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Solve Wordle in Hard Mode in GUESS_LIMIT guesses or less",
                    data={
                        "GUESS_LIMIT": (self.guess_limits, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
            ])

        if self.include_variants and self.wordle_variants():
            templates.extend([
                GameObjectiveTemplate(
                    label="Solve a puzzle in VARIANT",
                    data={
                        "VARIANT": (self.wordle_variants, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Solve a puzzle in VARIANT within GUESS_LIMIT guesses",
                    data={
                        "VARIANT": (self.wordle_variants, 1),
                        "GUESS_LIMIT": (self.guess_limits, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Solve WORDLE_COUNT puzzle(s) today across Wordle-style variants",
                    data={
                        "WORDLE_COUNT": (self.wordle_counts, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            ])

        if self.include_variants and self.themed_variants():
            templates.append(
                GameObjectiveTemplate(
                    label="Solve the THEMED_VARIANT themed puzzle",
                    data={
                        "THEMED_VARIANT": (self.themed_variants, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            )

        if self.include_variants and self.non_word_variants():
            templates.append(
                GameObjectiveTemplate(
                    label="Solve the NON_WORD_VARIANT puzzle (a non-word Wordle-style game)",
                    data={
                        "NON_WORD_VARIANT": (self.non_word_variants, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            )

        if self.include_multi_grid and self.multi_grid_variants():
            templates.extend([
                GameObjectiveTemplate(
                    label="Solve a game of MULTI_GRID_VARIANT (multiple boards at once)",
                    data={
                        "MULTI_GRID_VARIANT": (self.multi_grid_variants, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Solve MULTI_GRID_VARIANT without filling the final guess row",
                    data={
                        "MULTI_GRID_VARIANT": (self.multi_grid_variants, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        if self.include_challenge_runs:
            templates.extend([
                GameObjectiveTemplate(
                    label="Open with the word OPENER",
                    data={
                        "OPENER": (self.opening_words, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Open with a word containing no vowels (e.g. CRYPT, GLYPH, NYMPH)",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Solve a puzzle in under TIME_LIMIT",
                    data={
                        "TIME_LIMIT": (self.time_limits, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Maintain a winning streak of STREAK_COUNT puzzles in Hard Mode",
                    data={
                        "STREAK_COUNT": (self.streak_counts, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        if self.daily_puzzles():
            templates.extend([
                GameObjectiveTemplate(
                    label="Solve the daily DAILY_PUZZLE puzzle",
                    data={
                        "DAILY_PUZZLE": (self.daily_puzzles, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Solve the daily DAILY_PUZZLE puzzle STREAK_COUNT days in a row",
                    data={
                        "DAILY_PUZZLE": (self.daily_puzzles, 1),
                        "STREAK_COUNT": (self.streak_counts, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        min_puzzles: int = self.archipelago_options.wordle_minimum_daily_puzzle_count.value
        max_puzzles: int = self.archipelago_options.wordle_maximum_daily_puzzle_count.value

        for puzzle_count in range(min_puzzles, max_puzzles + 1):
            if puzzle_count > len(self.eligible_daily_puzzles()):
                break

            templates.append(
                GameObjectiveTemplate(
                    label="Solve each of the following daily puzzles in the same day: PUZZLES",
                    data={
                        "PUZZLES": (self.eligible_daily_puzzles, puzzle_count),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            )

        return templates

    def wordle_variants(self) -> List[str]:
        return sorted(self.archipelago_options.wordle_variants.value)

    @staticmethod
    def default_wordle_variants() -> List[str]:
        return [
            "Flagle",
            "Worgle",
            "Weirdle",
            "Worldle",
            "Quordle",
            "Absurdle",
            "Squardle",
            "Colorfle",
            "Dordle",
            "Octordle",
            "Nerdle",
            "Crosswordle",
            "Semantle",
            "Waffle",
            "Antiwordle",
            "Phrazle",
            "Diffle",
            "Squareword",
            "Xordle",
        ]

    def multi_grid_variants(self) -> List[str]:
        return sorted(self.archipelago_options.wordle_multi_grid_variants.value)

    @staticmethod
    def default_multi_grid_variants() -> List[str]:
        return [
            "Dordle",
            "Quordle",
            "Octordle",
            "Sedecordle",
            "Duotrigordle",
        ]

    def themed_variants(self) -> List[str]:
        return sorted(self.archipelago_options.wordle_themed_variants.value)

    @staticmethod
    def default_themed_variants() -> List[str]:
        return [
            "Lewdle",
            "Sweardle",
            "Byrdle",
            "Foodle",
            "Weddle",
        ]

    def non_word_variants(self) -> List[str]:
        return sorted(self.archipelago_options.wordle_non_word_variants.value)

    @staticmethod
    def default_non_word_variants() -> List[str]:
        return [
            "Nerdle",
            "Worldle",
            "Globle",
            "Framed",
            "Semantle",
            "Redactle",
            "Tradle",
            "Poeltl",
            "Contexto",
            "Moviedle",
            "Actorle",
            "Bandle",
            "Chessle",
            "Spotle",
            "Countryle",
        ]

    def daily_puzzles(self) -> List[str]:
        return sorted(self.archipelago_options.wordle_daily_puzzles.value)

    def eligible_daily_puzzles(self) -> List[str]:
        puzzles: List[str] = list(self.daily_puzzles())

        if self.include_wordle:
            puzzles.append("Wordle")

        if self.include_variants:
            puzzles += self.wordle_variants()
            puzzles += self.themed_variants()
            puzzles += self.non_word_variants()

        if self.include_multi_grid:
            puzzles += self.multi_grid_variants()

        return sorted(set(puzzles))

    @staticmethod
    def default_daily_puzzles() -> List[str]:
        return [
            "Connections",
            "Strands",
            "Spelling Bee",
            "The Mini Crossword",
            "Letter Boxed",
            "Murdle",
            "TimeGuessr",
        ]

    @staticmethod
    def opening_words() -> List[str]:
        return [
            "ADIEU",
            "AUDIO",
            "STARE",
            "RAISE",
            "ARISE",
            "SLATE",
            "CRANE",
            "TRACE",
        ]

    @staticmethod
    def time_limits() -> List[str]:
        return ["5 minutes", "4 minutes", "3 minutes"]

    @staticmethod
    def guess_limits() -> List[str]:
        return ["4", "3"]

    @staticmethod
    def streak_counts() -> List[str]:
        return ["2", "3", "4"]

    @staticmethod
    def wordle_counts() -> List[str]:
        return ["3", "5", "7"]


# Archipelago Options
class WordleIncludeWordle(DefaultOnToggle):
    """Include objectives for the original daily Wordle itself."""
    display_name = "Wordle Include Wordle Objectives"


class WordleVariants(OptionSet):
    """Which Wordle-style variants can be targeted by variant objectives and constraints.

    Freely add any other variants you want to play; remove any you do not.
    Emptying the list disables these objectives entirely.
    """
    display_name = "Wordle Variants"
    default = WordleGame.default_wordle_variants()


class WordleThemedVariants(OptionSet):
    """Which themed Wordle variants can be targeted by themed variant objectives.

    Freely add any other themed variants you want to play; remove any you do not.
    Emptying the list disables these objectives entirely.
    """
    display_name = "Wordle Themed Variants"
    default = WordleGame.default_themed_variants()


class WordleNonWordVariants(OptionSet):
    """Which non-word Wordle-style games can be targeted by non-word variant objectives.

    Freely add any other non-word games you want to play; remove any you do not.
    Emptying the list disables these objectives entirely.
    """
    display_name = "Wordle Non-Word Variants"
    default = WordleGame.default_non_word_variants()


class WordleMultiGridVariants(OptionSet):
    """Which multi-grid Wordle variants can be targeted by multi-grid objectives.

    Freely add any other multi-grid variants you want to play; remove any you do not.
    Emptying the list disables these objectives entirely.
    """
    display_name = "Wordle Multi-Grid Variants"
    default = WordleGame.default_multi_grid_variants()


class WordleIncludeVariants(DefaultOnToggle):
    """Include objectives for Wordle-style spinoffs and variants (themed, geography, music, etc.)."""
    display_name = "Wordle Include Variant Objectives"


class WordleIncludeMultiGrid(DefaultOnToggle):
    """Include objectives for multi-grid variants such as Dordle, Quordle and Octordle."""
    display_name = "Wordle Include Multi-Grid Objectives"


class WordleIncludeChallengeRuns(DefaultOnToggle):
    """Include self-imposed challenge objectives such as fixed openers and timed solves."""
    display_name = "Wordle Include Challenge Run Objectives"


class WordleDailyPuzzles(OptionSet):
    """Which non-Wordle daily puzzles can be targeted by daily puzzle objectives.

    Freely add any other daily puzzles you want to play; remove any you do not.
    Emptying the list disables these objectives entirely.
    """
    display_name = "Wordle Daily Puzzles"
    default = WordleGame.default_daily_puzzles()


class WordleMinimumDailyPuzzleCount(Range):
    """The minimum number of puzzles to include in same-day multi-puzzle objectives.

    These draw from all enabled puzzles: Wordle, Wordle-likes and other daily puzzles.
    """
    display_name = "Wordle Minimum Daily Puzzle Count"
    default = 2
    range_start = 2
    range_end = 5


class WordleMaximumDailyPuzzleCount(Range):
    """The maximum number of puzzles to include in same-day multi-puzzle objectives.

    These draw from all enabled puzzles: Wordle, Wordle-likes and other daily puzzles.
    """
    display_name = "Wordle Maximum Daily Puzzle Count"
    default = 3
    range_start = 2
    range_end = 5



