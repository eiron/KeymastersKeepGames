from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PokerQuestArchipelagoOptions:
    poker_quest_include_victory_plus_objectives: PokerQuestIncludeVictoryPlusObjectives
    poker_quest_include_challenge_objectives: PokerQuestIncludeChallengeObjectives


class PokerQuestGame(Game):
    name = "Poker Quest"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = PokerQuestArchipelagoOptions

    @property
    def include_victory_plus_objectives(self) -> bool:
        return self.archipelago_options.poker_quest_include_victory_plus_objectives.value

    @property
    def include_challenge_objectives(self) -> bool:
        return self.archipelago_options.poker_quest_include_challenge_objectives.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = []

        constraints += [
            GameObjectiveTemplate(
                label="Skip the first turn of the first combat in each area",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Don't spend any chips in the Castle Hearts Shop",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Don't eat any food to heal",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Successfully clear the Dungeon in both Castle Hearts and Castle Clubs",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Don't enter any Caves, Dungeons, or Catacombs",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Enter both Castle Hearts and Castle Clubs with maximum Energy",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Enhance one card type at the earliest opportunity, then avoid every other Temple and Church",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Don't refill any consumables",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Achieve 3 Perfect Kills (reduce an enemy to exactly 0 HP)",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Achieve Victory+ instead of Victory",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Fight every Elite combat you can (Elites are marked with a Silver Border on the map)",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
        ]

        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Play as HERO, Achieve Victory",
                data={"HERO": (self.heroes, 1)},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Discover ZONE",
                data={"ZONE": (self.zones, 1)},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Achieve a score of over SCORE in a single run",
                data={"SCORE": (self.score_thresholds, 1)},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Achieve N Perfect Kills in a single run",
                data={"N": (self.perfect_kill_counts, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Use a 5-card Straight Flush in combat during a run",
                data={},
                is_time_consuming=True,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Kill a monster by dealing exactly 1 damage",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Reach exactly 1 HP during a run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Accumulate at least 200 chips at any point in a single run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Have over 10 consumables in your inventory at once",
                data={},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Enter CASTLE with maximum Energy",
                data={"CASTLE": (self.castle_zones, 1)},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Complete a Dungeon encounter in a single run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Complete N Catacomb encounters in a single run",
                data={"N": (self.catacomb_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Enhance all four card suits in a single run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Discover The Halls of Probability",
                data={},
                is_time_consuming=True,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Achieve Victory in a Daily Run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Hop at least 20 times in a single run as the Toad",
                data={},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Eat at least 125 food in a single run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
            ),
        ]

        if self.include_victory_plus_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Play as HERO, Achieve Victory+",
                    data={"HERO": (self.heroes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Play as HERO, Achieve Victory++",
                    data={"HERO": (self.heroes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Play as HERO, Achieve Victory+++",
                    data={"HERO": (self.heroes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Achieve Victory+++ without using your Energy ability",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Achieve Victory+++ without purchasing anything from any Shops",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Achieve Victory+++ with every combat ending in a Perfect Kill",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Achieve Victory+++ with N different heroes",
                    data={"N": (self.hero_victory_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Win N Classic Runs in a row",
                    data={"N": (self.classic_streak_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Achieve a score of over 5,000 in a single run",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Deal at least 10,000 damage in a single hit",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
            ])

        if self.include_challenge_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Achieve Victory in the CHALLENGE Challenge Run",
                    data={"CHALLENGE": (self.challenge_runs, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Achieve Victory+++ with the Bard in the Unprepared+ Challenge",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Achieve Victory+++ with the Vampire in the Nearsighted Challenge",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Achieve Victory+++ with the Warlock in the Burnination Challenge",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Achieve Victory+++ in N Daily Runs in a row",
                    data={"N": (self.daily_streak_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Achieve Victory+++ in the Unprepared+ Challenge with N different heroes",
                    data={"N": (self.improvisation_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Achieve Victory+++ in 30 Challenge Runs",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
            ])

        return templates

    @staticmethod
    def heroes() -> List[str]:
        return [
            "the Assassin",
            "the Bard",
            "the Banker",
            "the Druid",
            "the Huntress",
            "the Knight",
            "the Locksmith",
            "the Mage",
            "the Monk",
            "the Ninja",
            "the Paladin",
            "the Priest",
            "the Prince",
            "the Queen",
            "the Rainbow Knight",
            "the Rogue",
            "the Sorceress",
            "the Titan",
            "the Toad",
            "the Tortoise",
            "the Vampire",
            "the Warlock",
        ]

    @staticmethod
    def zones() -> List[str]:
        return [
            "Castle Hearts",
            "The Barren Desert",
            "The Fungal Swamps",
            "The Great Pyramid",
            "Castle Clubs",
            "The Frigid Peaks",
            "Castle Spades",
            "The Deep Blue Sea",
            "Castle Diamonds",
            "The Astral Rift",
        ]

    @staticmethod
    def castle_zones() -> List[str]:
        return [
            "Castle Hearts",
            "Castle Clubs",
            "Castle Spades",
            "Castle Diamonds",
        ]

    @staticmethod
    def score_thresholds() -> List[str]:
        return [
            "1,000",
            "2,000",
        ]

    @staticmethod
    def perfect_kill_counts() -> List[int]:
        return [3, 10, 25]

    @staticmethod
    def catacomb_counts() -> List[int]:
        return [1, 2, 3]

    @staticmethod
    def hero_victory_counts() -> List[int]:
        return [5, 10]

    @staticmethod
    def classic_streak_counts() -> List[int]:
        return [2, 5]

    @staticmethod
    def challenge_runs() -> List[str]:
        return [
            "Unprepared+",
            "Nearsighted",
            "Burnination",
        ]

    @staticmethod
    def daily_streak_counts() -> List[int]:
        return [2, 3]

    @staticmethod
    def improvisation_counts() -> List[int]:
        return [6, 12]


class PokerQuestIncludeVictoryPlusObjectives(DefaultOnToggle):
    """Include objectives requiring Victory+, Victory++, or Victory+++ difficulty."""
    display_name = "Poker Quest Include Victory Plus Objectives"


class PokerQuestIncludeChallengeObjectives(DefaultOnToggle):
    """Include objectives for Challenge Runs and Daily Run streaks."""
    display_name = "Poker Quest Include Challenge Objectives"
