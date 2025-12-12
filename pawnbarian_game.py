from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PawnbarianArchipelagoOptions:
    pawnbarian_include_character_runs: PawnbarianIncludeCharacterRuns
    pawnbarian_include_chain_challenges: PawnbarianIncludeChainChallenges


class PawnbarianGame(Game):
    name = "Pawnbarian"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
    ]

    is_adult_only_or_unrated = False

    options_cls = PawnbarianArchipelagoOptions

    # Properties
    @property
    def include_character_runs(self) -> bool:
        return self.archipelago_options.pawnbarian_include_character_runs.value

    @property
    def include_chain_challenges(self) -> bool:
        return self.archipelago_options.pawnbarian_include_chain_challenges.value

    @property
    def include_daily_runs(self) -> bool:
        return False

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="No shop purchases during the run",
                data={},
            ),
            GameObjectiveTemplate(
                label="Do not buy extra hearts",
                data={},
            ),
            GameObjectiveTemplate(
                label="Finish a run without taking damage on a floor",
                data={},
            ),
            GameObjectiveTemplate(
                label="Go down to one health, then heal back to full",
                data={},
            ),
            GameObjectiveTemplate(
                label="Buy exactly one thing in each shop",
                data={},
            ),
            GameObjectiveTemplate(
                label="Survive three floors of the Gauntlet after winning",
                data={},
            ),
            GameObjectiveTemplate(
                label="Beat a floor without activating a cantrip effect",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't lose any health from Blight",
                data={},
            ),
            GameObjectiveTemplate(
                label="Beat a floor after moving to all four corners of the board",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't buy any health from the shop",
                data={},
            ),
            GameObjectiveTemplate(
                label="Intentionally take damage once per floor",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = []

        if self.include_character_runs:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win DUNGEON_NAME with CHARACTER",
                    data={
                        "DUNGEON_NAME": (self.dungeon_names, 1),
                        "CHARACTER": (self.characters, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Reach FLOOR_COUNT floors cleared with CHARACTER",
                    data={
                        "FLOOR_COUNT": (self.floor_counts, 1),
                        "CHARACTER": (self.characters, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
            ])

        if self.include_chain_challenges:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win DUNGEON_NAME with CHARACTER at CHAIN_LEVEL chains",
                    data={
                        "DUNGEON_NAME": (self.dungeon_names, 1),
                        "CHARACTER": (self.characters, 1),
                        "CHAIN_LEVEL": (self.low_chain_levels, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Win with CHARACTER at CHAIN_LEVEL chains without shop purchases",
                    data={
                        "CHARACTER": (self.characters, 1),
                        "CHAIN_LEVEL": (self.low_chain_levels, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Win DUNGEON_NAME with CHARACTER at CHAIN_LEVEL chains",
                    data={
                        "DUNGEON_NAME": (self.dungeon_names, 1),
                        "CHARACTER": (self.characters, 1),
                        "CHAIN_LEVEL": (self.high_chain_levels, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Win with CHARACTER at CHAIN_LEVEL chains without shop purchases",
                    data={
                        "CHARACTER": (self.characters, 1),
                        "CHAIN_LEVEL": (self.high_chain_levels, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Conquer all dungeons with CHARACTER at CHAIN_LEVEL chains",
                    data={
                        "CHARACTER": (self.characters, 1),
                        "CHAIN_LEVEL": (self.high_chain_levels, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=9,
                ),
            ])

        # Gauntlet objectives (endless mode unlocked after main dungeons)
        templates.extend([
            GameObjectiveTemplate(
                label="Reach GAUNTLET_FLOORS floors in Gauntlet with CHARACTER",
                data={
                    "GAUNTLET_FLOORS": (self.gauntlet_floor_targets_high, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Reach GAUNTLET_FLOORS floors in Gauntlet with CHARACTER at CHAIN_LEVEL chains",
                data={
                    "GAUNTLET_FLOORS": (self.gauntlet_floor_targets, 1),
                    "CHARACTER": (self.characters, 1),
                    "CHAIN_LEVEL": (self.high_chain_levels, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
        ])

        return templates

    # Data lists
    @staticmethod
    def characters() -> List[str]:
        return [
            "Pawnbarian",
            "Knight Templar",
            "Shogun",
            "Nomad",
            "Capyzerker",
            "Mystic",
        ]

    @staticmethod
    def dungeon_names() -> List[str]:
        return [
            "Goblin Caves",
            "Golem Fortress",
            "Foul Shrine",
        ]

    @staticmethod
    def chain_levels() -> List[str]:
        return ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

    @staticmethod
    def low_chain_levels() -> List[str]:
        return ["0", "I", "II", "III", "IV"]

    @staticmethod
    def high_chain_levels() -> List[str]:
        return ["V", "VI", "VII", "VIII", "IX", "X"]

    @staticmethod
    def floor_counts() -> List[str]:
        return ["3", "5", "7"]

    @staticmethod
    def gauntlet_floor_targets() -> List[str]:
        return ["8", "10", "12"]

    @staticmethod
    def gauntlet_floor_targets_high() -> List[str]:
        return ["12", "15", "18"]


# Archipelago Options
class PawnbarianIncludeCharacterRuns(DefaultOnToggle):
    """Include objectives for winning runs with each character."""
    display_name = "Pawnbarian Include Character Runs"


class PawnbarianIncludeChainChallenges(DefaultOnToggle):
    """Include chain difficulty objectives."""
    display_name = "Pawnbarian Include Chain Challenges"


class PawnbarianIncludeDailyRuns(DefaultOnToggle):
    """Include daily run objectives."""
    display_name = "Pawnbarian Include Daily Runs"
    # Deprecated: Daily mode not confirmed on wiki; leaving class for backward compatibility.
