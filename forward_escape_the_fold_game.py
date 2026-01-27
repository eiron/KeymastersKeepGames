from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle, DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ForwardEscapeTheFoldArchipelagoOptions:
    forward_include_resource_challenges: ForwardIncludeResourceChallenges
    forward_include_challenge_modes: ForwardIncludeChallengeModes
    forward_include_playstyle_constraints: ForwardIncludePlaystyleConstraints
    forward_include_achievement_objectives: ForwardIncludeAchievementObjectives


class ForwardEscapeTheFoldGame(Game):
    name = "Forward: Escape the Fold"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = ForwardEscapeTheFoldArchipelagoOptions

    @property
    def include_resource_challenges(self) -> bool:
        return self.archipelago_options.forward_include_resource_challenges.value

    @property
    def include_challenge_modes(self) -> bool:
        return self.archipelago_options.forward_include_challenge_modes.value

    @property
    def include_playstyle_constraints(self) -> bool:
        return self.archipelago_options.forward_include_playstyle_constraints.value

    @property
    def include_achievement_objectives(self) -> bool:
        return self.archipelago_options.forward_include_achievement_objectives.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a run without using your Power",
                data={},
            ),
            GameObjectiveTemplate(
                label="Always buy something from every shop encountered",
                data={},
            ),
            GameObjectiveTemplate(
                label="Reach the end with exactly 1 HP remaining",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = []
        objectives += self.base_objectives()

        if self.include_resource_challenges:
            objectives += self.resource_challenge_objectives()

        if self.include_challenge_modes:
            objectives += self.challenge_mode_objectives()

        if self.include_playstyle_constraints:
            objectives += self.playstyle_constraint_objectives()

        if self.include_achievement_objectives:
            objectives += self.achievement_objectives()

        return objectives

    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a full run in Classic mode as CHARACTER",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Complete a full run in Expert mode as CHARACTER",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Complete a Journey mode run at difficulty DIFFICULTY as CHARACTER",
                data={
                    "DIFFICULTY": (self.journey_difficulties, 1),
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=7,
            ),
        ]

    def resource_challenge_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="As CHARACTER, accumulate 45 Skulls at any point during a run",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, accumulate 120 Gold coins at any point during a run",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, carry 20 items in your inventory during a run",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, equip 4 or more Legendary items during a run",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=7,
            ),
        ]

    def challenge_mode_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a full run in the CHALLENGE challenge",
                data={
                    "CHALLENGE": (self.challenges, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
        ]

    def playstyle_constraint_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="As CHARACTER, complete 2 consecutive dungeon levels without using your Power",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, when presented with choices, choose the leftmost option COUNT times",
                data={
                    "COUNT": (self.choice_counts, 1),
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, have 3 or more status effects active at the same time",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(

                label="As CHARACTER, complete a run wearing STATUS effect for at least 5 levels",
                data={
                    "STATUS": (self.status_effects, 1),
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, never remove more than 2 items from your inventory during a run",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, visit all level types (Dungeon, Blood altar, Chest, Store, Jewelry, Blacksmith, Alchemist, Potion, Town, Random item, Healing, Treasure)",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, complete a run while maintaining 50 or more Protection for at least 3 levels",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, purchase only Rare items from shops (no Common or Legendary)",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, defeat at least BOSS_COUNT bosses during a run",
                data={
                    "BOSS_COUNT": (self.boss_counts, 1),
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
        ]

    def achievement_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="As CHARACTER, survive an attack with only 1 hit point remaining",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, survive a boss attack with 22 or more hit points",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, receive 90 damage or more during a single level",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, attack 6 or more enemies during a single level",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, attack the last boss and survive",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, survive an attack by 3 enemies at the same time",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, wear Greed status for a total of 15 instances",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, wear Stealth x9 or more at the same time",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, wear Protection x18 or more at the same time",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, wear 55 points of Armor at the same time",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, play with a very small field of vision (equip 2 Gorgon Eyes)",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, get 4 different statuses at the same time",
                data={
                    "CHARACTER": (self.playable_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
        ]

    @staticmethod
    def playable_characters() -> List[str]:
        return [
            "Edward",
            "Medusa",
            "Black Knight",
            "Phade",
            "Silence",
            "Azerty",
            "Anubis",
            "Raven",
            "Hector",
        ]

    @staticmethod
    def challenges() -> List[str]:
        return [
            "Immunity",
            "Darkness",
            "Thank you",
            "Corruption",
            "Instability",
            "Stealth attacks",
            "Electricity",
            "Blindness",
            "Invisibility",
            "Healing poison",
            "Golden chests",
            "Low health",
            "Eggs party",
            "Grukk??",
            "Halloween",
        ]

    @staticmethod
    def choice_counts() -> List[str]:
        return [
            "3",
            "5",
            "8",
            "12",
        ]

    @staticmethod
    def journey_difficulties() -> List[str]:
        return [
            "20",
            "30",
            "37",
            "50",
            "75",
        ]

    @staticmethod
    def status_effects() -> List[str]:
        return [
            "Poison",
            "Blindness",
            "Stealth",
            "Greed",
            "Protection",
            "Immunity",
        ]

    @staticmethod
    def boss_counts() -> List[str]:
        return [
            "3",
            "4",
            "5",
        ]


class ForwardIncludeResourceChallenges(DefaultOnToggle):
    """Include objectives focused on accumulating resources (Skulls, Gold, items, Legendary items)"""
    display_name = "Include Resource Challenges"


class ForwardIncludeChallengeModes(DefaultOnToggle):
    """Include objectives for completing Challenge modes"""
    display_name = "Include Challenge Modes"


class ForwardIncludePlaystyleConstraints(DefaultOnToggle):
    """Include objectives that impose specific playstyle constraints during runs"""
    display_name = "Include Playstyle Constraints"


class ForwardIncludeAchievementObjectives(DefaultOnToggle):
    """Include objectives based on game achievements (status effects, damage thresholds, etc)"""
    display_name = "Include Achievement Objectives"
