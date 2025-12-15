from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MonsterRoadtripArchipelagoOptions:
    mrt_include_endings: MonsterRoadtripIncludeEndings
    mrt_include_resource_goals: MonsterRoadtripIncludeResourceGoals
    mrt_include_challenge_runs: MonsterRoadtripIncludeChallengeRuns


class MonsterRoadtripGame(Game):
    name = "Monster Roadtrip"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = MonsterRoadtripArchipelagoOptions

    # Properties
    @property
    def include_endings(self) -> bool:
        return self.archipelago_options.mrt_include_endings.value

    @property
    def include_resource_goals(self) -> bool:
        return self.archipelago_options.mrt_include_resource_goals.value

    @property
    def include_challenge_runs(self) -> bool:
        return self.archipelago_options.mrt_include_challenge_runs.value

    # Optional constraints
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(label="Do not visit the same location twice", data={}),
            GameObjectiveTemplate(label="No roadside attractions (skip bonus visits)", data={}),
            GameObjectiveTemplate(label="Always pick the chaos option when available", data={}),
            GameObjectiveTemplate(label="Never reroll an event choice", data={}),
            GameObjectiveTemplate(label="Keep all resources above LOW_BOUND for the whole run", data={"LOW_BOUND": (self.resource_low_bounds, 1)}),
            GameObjectiveTemplate(label="No car upgrades purchased", data={}),
            GameObjectiveTemplate(label="Start with random drivers and keep them alive", data={}),
            GameObjectiveTemplate(label="Never talk with Scott and Polly", data={}),
            GameObjectiveTemplate(label="Never visit the Info Board", data={}),
            GameObjectiveTemplate(label="Never wait at the Bus Stop", data={}),
            GameObjectiveTemplate(label="Never enter the car", data={}),
            GameObjectiveTemplate(label="Never trade with Noodles", data={}),
            GameObjectiveTemplate(label="Play in Prank Master Mode and always choose and fulfil the dare giving the most Prank Dollarz", data={}),
            GameObjectiveTemplate(label="When possible, always select a Quantity-type event", data={}),
            GameObjectiveTemplate(label="Never have a Hitchhiker Stat Boost active", data={}),
        ]

    # Objectives
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = []

        if self.include_endings:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win a run reaching DESTINATION",
                    data={"DESTINATION": (self.destinations, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Win a run on DIFFICULTY reaching DESTINATION",
                    data={
                        "DIFFICULTY": (self.difficulties, 1),
                        "DESTINATION": (self.destinations, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Recruit SECRET_HITCHHIKER and finish the run",
                    data={"SECRET_HITCHHIKER": (self.secret_hitchhikers, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                ),
            ])

        if self.include_resource_goals:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win a run by reaching the RESOURCE_NAME goal",
                    data={"RESOURCE_NAME": (self.resources, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Win with both RES_A and RES_B above PRE_WIN_TARGET before reaching the goal",
                    data={
                        "RES_A": (self.resources, 1),
                        "RES_B": (self.resources, 1),
                        "PRE_WIN_TARGET": (self.pre_win_thresholds, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Complete a run without any resource dropping below LOW_BOUND",
                    data={"LOW_BOUND": (self.resource_low_bounds, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                ),
            ])

        if self.include_challenge_runs:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win a Hard Mode run with PRESET active",
                    data={"PRESET": (self.challenge_presets, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Reach DESTINATION after triggering EVENT_COUNT chaos events",
                    data={
                        "DESTINATION": (self.destinations, 1),
                        "EVENT_COUNT": (self.chaos_event_counts, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
            ])

        return templates

    # Data lists
    @staticmethod
    def destinations() -> List[str]:
        return [
            "The Escape",
            "The Safehouse",
            "Eternal Summer",
            "The Summit",
            "The Festival",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Normal Roadtrip",
            "Hardcore Roadtrip",
            "Meteor Showers",
        ]

    @staticmethod
    def secret_hitchhikers() -> List[str]:
        return [
            "The Goth Hitchhiker",
            "The Slayer Camping Crew",
            "The Vampire Truckers",
            "The Forest Spirit",
            "The Interdimensional Scout",
        ]

    @staticmethod
    def resources() -> List[str]:
        return ["Hype", "Magic", "Mind", "Money", "Soul", "Stamina"]

    @staticmethod
    def pre_win_thresholds() -> List[str]:
        return ["15", "18", "20"]

    @staticmethod
    def resource_low_bounds() -> List[str]:
        return ["5", "8", "10"]

    @staticmethod
    def challenge_presets() -> List[str]:
        return [
            "Classic Caravan",
            "Lean Budget",
            "Chaos Route",
            "No Rest Stops",
            "Max Distance",
        ]

    @staticmethod
    def chaos_event_counts() -> List[str]:
        return ["5", "7", "9"]


# Archipelago Options
class MonsterRoadtripIncludeEndings(DefaultOnToggle):
    """Include objectives for winning runs and unique endings."""
    display_name = "Monster Roadtrip Include Endings"


class MonsterRoadtripIncludeResourceGoals(DefaultOnToggle):
    """Include objectives for resource targets and safe runs."""
    display_name = "Monster Roadtrip Include Resource Goals"


class MonsterRoadtripIncludeChallengeRuns(DefaultOnToggle):
    """Include challenge presets and chaos-focused runs."""
    display_name = "Monster Roadtrip Include Challenge Runs"
