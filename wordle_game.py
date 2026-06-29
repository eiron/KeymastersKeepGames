from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import DefaultOnToggle, OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class WordleArchipelagoOptions:
    wordle_variants: WordleVariants
    wordle_include_variants: WordleIncludeVariants
    wordle_include_multi_grid: WordleIncludeMultiGrid
    wordle_include_challenge_runs: WordleIncludeChallengeRuns


class WordleGame(Game):
    name = "Wordle"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = WordleArchipelagoOptions

    # Properties
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
                label="Solve a puzzle in VARIANT",
                data={
                    "VARIANT": (self.wordle_variants, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Solve VARIANT within ATTEMPT_LIMIT attempts",
                data={
                    "VARIANT": (self.wordle_variants, 1),
                    "ATTEMPT_LIMIT": (self.attempt_limits, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Solve a puzzle without using hints or helper tools",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Solve a puzzle with Hard Mode enabled",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Open with the word OPENER",
                data={
                    "OPENER": (self.opening_words, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Open with a word containing no vowels (e.g. CRYPT, GLYPH, NYMPH)",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Solve without ever reusing a letter you already know is not in the word (Ultra Hard Mode)",
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
                is_difficult=True,
            ),
        ]

        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            # Original objectives (preserved)
            GameObjectiveTemplate(
                label="Solve Wordle in GUESS_LIMIT guesses or less",
                data={
                    "GUESS_LIMIT": (self.guess_limits, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Solve STREAK_COUNT Wordle puzzle(s) in a row",
                data={
                    "STREAK_COUNT": (self.streak_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=4,
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
            GameObjectiveTemplate(
                label="Solve a puzzle in VARIANT within GUESS_LIMIT guesses",
                data={
                    "VARIANT": (self.wordle_variants, 1),
                    "GUESS_LIMIT": (self.guess_limits, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            # Added objectives
            GameObjectiveTemplate(
                label="Solve today's Wordle and share the emoji grid",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Solve Wordle in Hard Mode in GUESS_LIMIT guesses or less",
                data={
                    "GUESS_LIMIT": (self.guess_limits, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
        ]

        if self.include_variants:
            templates.extend([
                GameObjectiveTemplate(
                    label="Solve a puzzle in VARIANT",
                    data={
                        "VARIANT": (self.wordle_variants, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Solve a puzzle in each of VARIANT and OTHER_VARIANT in the same day",
                    data={
                        "VARIANT": (self.wordle_variants, 1),
                        "OTHER_VARIANT": (self.wordle_variants, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Solve the THEMED_VARIANT themed puzzle",
                    data={
                        "THEMED_VARIANT": (self.themed_variants, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Solve the NON_WORD_VARIANT puzzle (a non-word Wordle-style game)",
                    data={
                        "NON_WORD_VARIANT": (self.non_word_variants, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ])

        if self.include_multi_grid:
            templates.extend([
                GameObjectiveTemplate(
                    label="Solve a game of MULTI_GRID_VARIANT (multiple boards at once)",
                    data={
                        "MULTI_GRID_VARIANT": (self.multi_grid_variants, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Solve MULTI_GRID_VARIANT without filling the final guess row",
                    data={
                        "MULTI_GRID_VARIANT": (self.multi_grid_variants, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        if self.include_challenge_runs:
            templates.extend([
                GameObjectiveTemplate(
                    label="Solve a puzzle always opening with the word OPENER",
                    data={
                        "OPENER": (self.opening_words, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Solve a puzzle using a no-vowel opening word",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Solve a puzzle blind: enter all guesses without reading color feedback",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Solve a puzzle in under TIME_LIMIT",
                    data={
                        "TIME_LIMIT": (self.time_limits, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Maintain a winning streak of STREAK_COUNT puzzles in Hard Mode",
                    data={
                        "STREAK_COUNT": (self.streak_counts, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        return templates

    def wordle_variants(self) -> List[str]:
        selected: List[str] = sorted(self.archipelago_options.wordle_variants.value)

        if not selected:
            return self.default_wordle_variants()

        return selected

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
        ]

    @staticmethod
    def multi_grid_variants() -> List[str]:
        return [
            "Dordle",
            "Quordle",
            "Octordle",
            "Sedecordle",
            "Duotrigordle",
        ]

    @staticmethod
    def themed_variants() -> List[str]:
        return [
            "Lewdle",
            "Sweardle",
            "Byrdle",
            "Foodle",
            "Weddle",
        ]

    @staticmethod
    def non_word_variants() -> List[str]:
        return [
            "Nerdle",
            "Worldle",
            "Globle",
            "Heardle",
            "Framed",
            "Semantle",
            "Redactle",
            "Tradle",
            "Poeltl",
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
        return ["3 minutes", "2 minutes", "1 minute"]

    @staticmethod
    def guess_limits() -> List[str]:
        return ["6", "5", "4", "3"]

    @staticmethod
    def attempt_limits() -> List[str]:
        return ["10", "8", "6"]

    @staticmethod
    def streak_counts() -> List[str]:
        return ["2", "3", "4"]

    @staticmethod
    def wordle_counts() -> List[str]:
        return ["3", "5", "7"]


# Archipelago Options
class WordleVariants(OptionSet):
    """Which Wordle-style variants can be targeted by variant objectives and constraints.

    Defaults to the full built-in list; players may edit this to remove variants or add their own.
    """
    display_name = "Wordle Variants"
    default = WordleGame.default_wordle_variants()


class WordleIncludeVariants(DefaultOnToggle):
    """Include objectives for Wordle-style spinoffs and variants (themed, geography, music, etc.)."""
    display_name = "Wordle Include Variant Objectives"


class WordleIncludeMultiGrid(DefaultOnToggle):
    """Include objectives for multi-grid variants such as Dordle, Quordle and Octordle."""
    display_name = "Wordle Include Multi-Grid Objectives"


class WordleIncludeChallengeRuns(DefaultOnToggle):
    """Include self-imposed challenge objectives such as fixed openers, blind solves and timed solves."""
    display_name = "Wordle Include Challenge Run Objectives"



