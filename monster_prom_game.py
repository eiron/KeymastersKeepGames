from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MonsterPromArchipelagoOptions:
    monster_prom_include_second_term: MonsterPromIncludeSecondTerm
    monster_prom_include_long_game: MonsterPromIncludeLongGame
    monster_prom_include_secret_endings: MonsterPromIncludeSecretEndings
    monster_prom_include_stat_challenges: MonsterPromIncludeStatChallenges
    monster_prom_include_multiplayer: MonsterPromIncludeMultiplayer


class MonsterPromGame(Game):
    name = "Monster Prom"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = MonsterPromArchipelagoOptions

    # Properties
    @property
    def include_second_term(self) -> bool:
        return bool(self.archipelago_options.monster_prom_include_second_term.value)

    @property
    def include_long_game(self) -> bool:
        return bool(self.archipelago_options.monster_prom_include_long_game.value)

    @property
    def include_secret_endings(self) -> bool:
        return bool(self.archipelago_options.monster_prom_include_secret_endings.value)

    @property
    def include_stat_challenges(self) -> bool:
        return bool(self.archipelago_options.monster_prom_include_stat_challenges.value)

    @property
    def include_multiplayer(self) -> bool:
        return bool(self.archipelago_options.monster_prom_include_multiplayer.value)

    # Helpers
    def romance_options(self) -> List[str]:
        characters: List[str] = list(self.base_romance_options())

        if self.include_second_term:
            characters += self.second_term_romance_options()

        return characters

    # Optional constraints
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Get a secret ending",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Buy 'The Gift That Keeps On Giving'",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Never enter LOCATION",
                data={
                    "LOCATION": (self.restricted_locations, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Only ever visit LOCATION on stat turns",
                data={
                    "LOCATION": (self.locations, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Go to the same location 3 times in a row",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Don't buy any stat-boosting items",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Enter and leave the shop without buying anything at least once",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Never sit with an NPC at the Cafeteria (always sit with your crush)",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Always sit with an NPC at the Cafeteria (never build HEARTS at lunch)",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Pursue only STAT_NAME as your primary stat for the whole game",
                data={
                    "STAT_NAME": (self.stats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Make every event choice at random",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Never visit the School Shop",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Play the whole game as PLAYABLE",
                data={
                    "PLAYABLE": (self.playable_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
        ]

        return constraints

    # Objectives
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            # Original objectives (preserved)
            GameObjectiveTemplate(
                label="Successfully go to prom with CHARACTER in a Short Game",
                data={
                    "CHARACTER": (self.base_romance_options, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Successfully go to prom with CHARACTER in a Short Game (Requires the Second Term DLC)",
                data={
                    "CHARACTER": (self.second_term_romance_options, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get a secret ending in a Short Game",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            # Added objectives
            GameObjectiveTemplate(
                label="Successfully go to prom with CHARACTER playing as PLAYABLE in a Short Game",
                data={
                    "CHARACTER": (self.romance_options, 1),
                    "PLAYABLE": (self.playable_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Successfully go to prom with CHARACTER without ever visiting LOCATION",
                data={
                    "CHARACTER": (self.romance_options, 1),
                    "LOCATION": (self.locations, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Go to prom with CHARACTER_COUNT different love interests across separate Short Games",
                data={
                    "CHARACTER_COUNT": (self.romance_streak_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Go to prom alone on purpose: end a Short Game with no successful date",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

        if self.include_long_game:
            templates.extend([
                GameObjectiveTemplate(
                    label="Successfully go to prom with CHARACTER in a Long Game (6 turns)",
                    data={
                        "CHARACTER": (self.romance_options, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Successfully go to prom with CHARACTER in a Long Game without buying any items",
                    data={
                        "CHARACTER": (self.romance_options, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            ])

        if self.include_stat_challenges:
            templates.extend([
                GameObjectiveTemplate(
                    label="Finish a Short Game with STAT_NAME at STAT_VALUE or higher",
                    data={
                        "STAT_NAME": (self.stats, 1),
                        "STAT_VALUE": (self.stat_targets_short, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Finish a game with both STAT_A and STAT_B at STAT_VALUE or higher",
                    data={
                        "STAT_A": (self.stats, 1),
                        "STAT_B": (self.stats, 1),
                        "STAT_VALUE": (self.stat_targets_short, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Visit LOCATION on every turn of a Short Game (earn its achievement)",
                    data={
                        "LOCATION": (self.locations, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Earn the ACHIEVEMENT achievement",
                    data={
                        "ACHIEVEMENT": (self.location_achievements, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Win a stat check at LOCATION while STAT_NAME is your lowest stat",
                    data={
                        "LOCATION": (self.locations, 1),
                        "STAT_NAME": (self.stats, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        if self.include_secret_endings:
            templates.extend([
                GameObjectiveTemplate(
                    label="Trigger the SECRET_ENDING secret ending",
                    data={
                        "SECRET_ENDING": (self.secret_endings, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Buy ITEM from the School Shop and follow its event chain to completion",
                    data={
                        "ITEM": (self.shop_items, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Get SECRET_COUNT different secret endings across separate runs",
                    data={
                        "SECRET_COUNT": (self.secret_ending_counts, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        if self.include_multiplayer:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win a multiplayer game by taking CHARACTER to prom",
                    data={
                        "CHARACTER": (self.romance_options, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Win a Hotseat (local) game against PLAYER_COUNT total players",
                    data={
                        "PLAYER_COUNT": (self.multiplayer_player_counts, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Steal a love interest another player was actively pursuing and win",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        return templates

    # Data lists
    @staticmethod
    def base_romance_options() -> List[str]:
        return [
            "Damien",
            "Liam",
            "Miranda",
            "Polly",
            "Scott",
            "Vera",
        ]

    @staticmethod
    def second_term_romance_options() -> List[str]:
        return [
            "Calculester",
            "Zoe",
        ]

    @staticmethod
    def playable_characters() -> List[str]:
        return [
            "Oz",
            "Amira",
            "Brian",
            "Vicky",
        ]

    @staticmethod
    def locations() -> List[str]:
        return [
            "Bathrooms",
            "Auditorium",
            "Classroom",
            "Library",
            "Outdoors",
            "Gym",
        ]

    @staticmethod
    def restricted_locations() -> List[str]:
        return [
            "Bathrooms",
            "Auditorium",
            "Classroom",
            "Library",
            "Outdoors",
            "Gym",
        ]

    @staticmethod
    def location_achievements() -> List[str]:
        return [
            "Nerd!",
            "Small Bladder",
            "Monster Prom: The Musical",
            "Dodgeball God",
            "Bookworm",
            "Party 24/7",
        ]

    @staticmethod
    def stats() -> List[str]:
        return [
            "Smarts",
            "Boldness",
            "Creativity",
            "Charm",
            "Money",
            "Fun",
        ]

    @staticmethod
    def stat_targets_short() -> List[str]:
        return ["8", "10", "12"]

    @staticmethod
    def romance_streak_counts() -> List[str]:
        return ["2", "3", "4"]

    @staticmethod
    def secret_endings() -> List[str]:
        return [
            "Floppy Disk",
            "Deity",
            "Prank Masterz",
            "Party",
            "Sun",
        ]

    @staticmethod
    def secret_ending_counts() -> List[str]:
        return ["2", "3", "5"]

    @staticmethod
    def shop_items() -> List[str]:
        return [
            "The Gift That Keeps On Giving",
            "Floppy Disk",
            "Power Totem of Z'Gord",
        ]

    @staticmethod
    def multiplayer_player_counts() -> List[str]:
        return ["2", "3", "4"]


# Archipelago Options
class MonsterPromIncludeSecondTerm(DefaultOnToggle):
    """Include the Second Term DLC romanceable characters (Calculester and Zoe) in objectives."""
    display_name = "Monster Prom Include Second Term DLC"


class MonsterPromIncludeLongGame(DefaultOnToggle):
    """Include Long Game (6-turn) objectives in addition to Short Game objectives."""
    display_name = "Monster Prom Include Long Game Objectives"


class MonsterPromIncludeSecretEndings(DefaultOnToggle):
    """Include secret-ending and shop event-chain objectives."""
    display_name = "Monster Prom Include Secret Ending Objectives"


class MonsterPromIncludeStatChallenges(DefaultOnToggle):
    """Include stat-focused objectives such as hitting stat thresholds and location achievements."""
    display_name = "Monster Prom Include Stat Challenge Objectives"


class MonsterPromIncludeMultiplayer(Toggle):
    """Include competitive multiplayer and Hotseat objectives. Requires two or more players."""
    display_name = "Monster Prom Include Multiplayer Objectives"
