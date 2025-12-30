from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DeadEstateArchipelagoOptions:
    dead_estate_allowed_characters: DeadEstateAllowedCharacters
    dead_estate_include_challenge_objectives: DeadEstateIncludeChallengeObjectives


class DeadEstateGame(Game):
    name = "Dead Estate"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = DeadEstateArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a run without using any healing items",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a run using only melee weapons",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a run without firing a gun more than 10 times",
                data={},
            ),
            GameObjectiveTemplate(
                label="Reach floor 5 without picking up any ammo",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete a run without opening any chests",
                data={},
            ),
            GameObjectiveTemplate(
                label="Leave behind every golden pot you find",
                data={},
            ),
            GameObjectiveTemplate(
                label="Do not buy anything on the first floor",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        objectives += self.base_objectives()

        if self.include_challenge_objectives:
            objectives += self.challenge_objectives()
        
        return objectives
    
    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete the normal ending (Exit Realm) as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Obtain the true ending (defeat Diavola) as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=12,
            ),
            GameObjectiveTemplate(
                label="Obtain the awakening ending (defeat the Leviathan) as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=12,
            ),
            GameObjectiveTemplate(
                label="Loop once (jump from the Balcony and continue the run) as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Reach the Attic Sanctum (Floor 3) as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach the Balcony (Floor 5) as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Reach the Dead Estate (Floor 6) as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Find a secret room as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect 5 different weapons in a single run as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
        ]
    
    def challenge_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Assemble the Silver Key and open the Coffin as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Loop twice in a single run as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Finish a run in under 20 minutes as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Complete a run without taking any damage as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Find all 5 secret rooms in a run as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Flawless at least 3 bosses in one run as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Buy Ambrosia while at full HP as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Destroy two weapons without using either even once and win the run as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Upgrade your health at the Doctor 4 times and win the run as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Finish a floor before Chunks shows up as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Get down to 1 HP then return to full without using Ambrosia as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Buy out an entire shop as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]
    
    @property
    def include_challenge_objectives(self) -> bool:
        return self.archipelago_options.dead_estate_include_challenge_objectives.value

    def available_characters(self) -> List[str]:
        allowed = getattr(self.archipelago_options.dead_estate_allowed_characters, "value", [])
        return allowed if allowed else DeadEstateAllowedCharacters.valid_keys

# Archipelago Options
class DeadEstateAllowedCharacters(OptionSet):
    """
    Limit which Dead Estate characters can be selected for objectives.
    Leave empty to allow all characters.
    """
    display_name = "Dead Estate: Allowed Characters"
    valid_keys = [
        "Jeff",
        "Jules",
        "Axel",
        "BOSS",
        "Cordelia",
        "Digby",
        "Fuji",
        "Luis",
        "Lydia",
        "Mumba",
    ]
    default = valid_keys


class DeadEstateIncludeChallengeObjectives(DefaultOnToggle):
    """
    Indicates whether to include difficult challenge objectives.
    """
    display_name = "Dead Estate: Include Challenge Objectives"
