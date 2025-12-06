from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet, Range, DefaultOnToggle

from .game import Game
from .game_objective_template import GameObjectiveTemplate

from .enums import KeymastersKeepGamePlatforms


@dataclass
class SuperDungeonMakerArchipelagoOptions:
    super_dungeon_maker_themes: SuperDungeonMakerThemes
    super_dungeon_maker_bosses: SuperDungeonMakerBosses
    super_dungeon_maker_difficulty_preference: SuperDungeonMakerDifficultyPreference
    super_dungeon_maker_include_community_challenges: SuperDungeonMakerIncludeCommunityCharacteristics


class SuperDungeonMakerGame(Game):
    name = "Super Dungeon Maker"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = SuperDungeonMakerArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Complete the dungeon without taking any damage",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Complete the dungeon without using the shield",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Complete the dungeon using only sword attacks (no environmental puzzles)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Complete the dungeon with all lights turned off (darkness challenge)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Defeat all enemies without collecting any health items",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Complete the dungeon in under 5 minutes",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Find and collect all silver eggs without defeating the boss",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Defeat the boss using only three sword hits",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Navigate a THEME dungeon using only the grappling hook",
                data={
                    "THEME": (self.themes, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Clear a trap-filled room without taking damage",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Solve a multi-stage puzzle without resetting the room",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Defeat a boss after disarming half of its attack patterns",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Complete two different THEME themed dungeons back-to-back",
                data={
                    "THEME": (self.themes, 2),
                },
            ),
            GameObjectiveTemplate(
                label="Kill every enemy you see (that you can reach)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't take any damage from drowning in deep water",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't take any damage from falling down a hole",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't take any damage from fire",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="At at least one point, be at one heart of health",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Have at least as much health when you leave a boss room as you did when you entered the boss room",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't take more than three hearts of damage against a boss",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Collect the egg with full health",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Beat the dungeon in half an hour or less",
                data=dict(),
            ),
        ]

        if self.include_community_challenges:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete a community-created dungeon with over 100 hearts",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Create a dungeon and have it receive at least 10 hearts from the community",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Download and complete 5 trending community dungeons",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 3295781 without dying",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 3301744 without dying",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 2987049 without dying",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 2988500 without dying",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 3002833 without dying",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 3300235 without dying",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 3298348 without dying",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 3065752 without dying",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 2755120 (you are permitted to die and restart once)",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 3242507 without dying",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 2770741 without dying",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 3193806 without dying",
                    data=dict(),
                ),
                GameObjectiveTemplate(
                    label="Beat dungeon 2874857 without dying",
                    data=dict(),
                ),
            ])

        return templates

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            # Basic dungeon completion objectives
            GameObjectiveTemplate(
                label="Collect the golden egg from a THEME themed dungeon",
                data={
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Collect golden eggs from all THEMES",
                data={
                    "THEMES": (self.themes, 4),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS in a THEME dungeon",
                data={
                    "BOSS": (self.bosses, 1),
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat all BOSS types",
                data={
                    "BOSS": (self.bosses, 3),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            # Collectible objectives
            GameObjectiveTemplate(
                label="Find COUNT silver eggs in a single THEME dungeon",
                data={
                    "COUNT": (self.silver_egg_counts, 1),
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect all silver eggs from a THEME dungeon",
                data={
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Discover COUNT secret rooms in THEME dungeons",
                data={
                    "COUNT": (self.secret_room_counts, 1),
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            # Tool-based objectives
            GameObjectiveTemplate(
                label="Use the grappling hook to traverse a THEME puzzle section",
                data={
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Use bombs to defeat COUNT enemies",
                data={
                    "COUNT": (self.enemy_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Solve a THEME dungeon using only the hourglass tool for resets",
                data={
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            # Combat-focused objectives
            GameObjectiveTemplate(
                label="Defeat COUNT enemies without using your shield",
                data={
                    "COUNT": (self.enemy_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a THEME dungeon without taking any damage",
                data={
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS without using your shield",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            # Puzzle-focused objectives
            GameObjectiveTemplate(
                label="Complete a multi-stage puzzle in a THEME dungeon",
                data={
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Unlock COUNT locked doors in a single THEME dungeon",
                data={
                    "COUNT": (self.locked_door_counts, 1),
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            # Difficulty-based objectives
            GameObjectiveTemplate(
                label="Complete a DIFFICULTY difficulty THEME dungeon",
                data={
                    "DIFFICULTY": (self.difficulty_modifiers, 1),
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            # Community/creation objectives
            GameObjectiveTemplate(
                label="Play a dungeon from the sandbox without publishing",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Design a THEME themed dungeon",
                data={
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            # Speed and efficiency objectives
            GameObjectiveTemplate(
                label="Complete a THEME dungeon in under 3 minutes",
                data={
                    "THEME": (self.themes, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS using minimal sword strikes (COUNT or less)",
                data={
                    "BOSS": (self.bosses, 1),
                    "COUNT": (self.strike_limits, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

        return templates

    @property
    def include_community_challenges(self) -> bool:
        return self.archipelago_options.super_dungeon_maker_include_community_challenges.value

    @functools.cached_property
    def themes(self) -> List[str]:
        return sorted(self.archipelago_options.super_dungeon_maker_themes.value)

    @functools.cached_property
    def bosses(self) -> List[str]:
        return sorted(self.archipelago_options.super_dungeon_maker_bosses.value)

    @staticmethod
    def silver_egg_counts() -> range:
        return range(1, 6)

    @staticmethod
    def secret_room_counts() -> range:
        return range(1, 4)

    @staticmethod
    def enemy_counts() -> range:
        return range(3, 16)

    @staticmethod
    def locked_door_counts() -> range:
        return range(2, 7)

    @staticmethod
    def strike_limits() -> range:
        return range(3, 10)

    @staticmethod
    def difficulty_modifiers() -> List[str]:
        return [
            "Hard Mode",
            "Darkness Challenge",
            "No Shield Run",
            "Speed Run (5 minutes)",
        ]


# Archipelago Options
class SuperDungeonMakerThemes(OptionSet):
    """
    Indicates which Super Dungeon Maker environment themes can appear in dungeon objectives.
    """

    display_name = "Super Dungeon Maker Themes"
    valid_keys = [
        "Forest",
        "Desert",
        "Ice",
        "Cyber",
    ]

    default = valid_keys


class SuperDungeonMakerBosses(OptionSet):
    """
    Indicates which Super Dungeon Maker bosses can appear in dungeon objectives.
    """

    display_name = "Super Dungeon Maker Bosses"
    valid_keys = [
        "Wormion",
        "Power Plant",
        "Dungeon Master",
    ]

    default = valid_keys


class SuperDungeonMakerDifficultyPreference(OptionSet):
    """
    Indicates which difficulty modifiers should be preferred in objective generation.
    """

    display_name = "Super Dungeon Maker Difficulty Preference"
    valid_keys = [
        "Easy",
        "Normal",
        "Hard",
        "Extreme",
    ]

    default = ["Normal"]


class SuperDungeonMakerIncludeCommunityCharacteristics(DefaultOnToggle):
    """
    Include objectives related to community-created dungeons and custom dungeon creation.
    """

    display_name = "Super Dungeon Maker Include Community Challenges"
