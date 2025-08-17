from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PhysicalHealthChallengesArchipelagoOptions:
    physical_health_exercise_selection: PhysicalHealthExerciseSelection
    physical_health_wellness_selection: PhysicalHealthWellnessSelection
    physical_health_nutrition_selection: PhysicalHealthNutritionSelection
    physical_health_movement_selection: PhysicalHealthMovementSelection
    physical_health_exercise_actions: PhysicalHealthExerciseActions
    physical_health_wellness_actions: PhysicalHealthWellnessActions
    physical_health_nutrition_actions: PhysicalHealthNutritionActions
    physical_health_movement_actions: PhysicalHealthMovementActions


class PhysicalHealthChallengesGame(Game):
    name = "Physical/Health Challenges"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = PhysicalHealthChallengesArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        if self.has_exercises:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION_VERB_VERB EXERCISE_OBJECTIVE",
                    data={"ACTION_VERB_VERB": (self.exercise_actions, 1), "EXERCISE_OBJECTIVE": (self.exercises, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            )

        if self.has_wellness:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION_VERB_VERB WELLNESS_OBJECTIVE",
                    data={"ACTION_VERB_VERB": (self.wellness_actions, 1), "WELLNESS_OBJECTIVE": (self.wellness, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        if self.has_nutrition:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION_VERB_VERB NUTRITION_OBJECTIVE",
                    data={"ACTION_VERB_VERB": (self.nutrition_actions, 1), "NUTRITION_OBJECTIVE": (self.nutrition, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        if self.has_movement:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION_VERB_VERB MOVEMENT_OBJECTIVE",
                    data={"ACTION_VERB_VERB": (self.movement_actions, 1), "MOVEMENT_OBJECTIVE": (self.movement, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        return game_objective_templates

    @property
    def has_exercises(self) -> bool:
        exercises = self.exercises()
        return len(exercises) > 0

    @property
    def has_wellness(self) -> bool:
        wellness = self.wellness()
        return len(wellness) > 0

    @property
    def has_nutrition(self) -> bool:
        nutrition = self.nutrition()
        return len(nutrition) > 0

    @property
    def has_movement(self) -> bool:
        movement = self.movement()
        return len(movement) > 0

    @functools.cached_property
    def exercise_actions(self) -> List[str]:
        return sorted(self.archipelago_options.physical_health_exercise_actions.value)

    @functools.cached_property
    def wellness_actions(self) -> List[str]:
        return sorted(self.archipelago_options.physical_health_wellness_actions.value)

    @functools.cached_property
    def nutrition_actions(self) -> List[str]:
        return sorted(self.archipelago_options.physical_health_nutrition_actions.value)

    @functools.cached_property
    def movement_actions(self) -> List[str]:
        return sorted(self.archipelago_options.physical_health_movement_actions.value)

    @functools.cached_property
    def exercises(self) -> List[str]:
        return sorted(self.archipelago_options.physical_health_exercise_selection.value)

    @functools.cached_property
    def wellness(self) -> List[str]:
        return sorted(self.archipelago_options.physical_health_wellness_selection.value)

    @functools.cached_property
    def nutrition(self) -> List[str]:
        return sorted(self.archipelago_options.physical_health_nutrition_selection.value)

    @functools.cached_property
    def movement(self) -> List[str]:
        return sorted(self.archipelago_options.physical_health_movement_selection.value)


# Archipelago Options
class PhysicalHealthExerciseSelection(OptionSet):
    """
    Defines which exercises are in the player's physical health challenge backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Physical Health Exercise Selection"

    default = ["Push-up Challenge", "Plank Hold", "Burpee Set", "Strength Circuit", "..."]


class PhysicalHealthWellnessSelection(OptionSet):
    """
    Defines which wellness activities are in the player's physical health challenge backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Physical Health Wellness Selection"

    default = ["Meditation Session", "Sleep Schedule", "Morning Routine", "Stress Management", "..."]


class PhysicalHealthNutritionSelection(OptionSet):
    """
    Defines which nutrition goals are in the player's physical health challenge backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Physical Health Nutrition Selection"

    default = ["Healthy Recipe", "Meal Prep", "Water Intake", "Vegetable Goal", "..."]


class PhysicalHealthMovementSelection(OptionSet):
    """
    Defines which movement activities are in the player's physical health challenge backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Physical Health Movement Selection"

    default = ["10,000 Steps", "Morning Stretch", "Dance Session", "Walking Break", "..."]


class PhysicalHealthExerciseActions(OptionSet):
    """
    Defines the possible actions that could be required for exercises in the physical health backlog.

    You can customize this list to your liking.
    """

    display_name = "Physical Health Exercise Actions"

    default = [
        "COMPLETE",
        "ATTEMPT",
        "PRACTICE",
        "REPEAT",
        "MASTER",
    ]


class PhysicalHealthWellnessActions(OptionSet):
    """
    Defines the possible actions that could be required for wellness activities in the physical health backlog.

    You can customize this list to your liking.
    """

    display_name = "Physical Health Wellness Actions"

    default = [
        "PRACTICE",
        "MAINTAIN",
        "ESTABLISH",
        "IMPROVE",
        "FOLLOW",
    ]


class PhysicalHealthNutritionActions(OptionSet):
    """
    Defines the possible actions that could be required for nutrition goals in the physical health backlog.

    You can customize this list to your liking.
    """

    display_name = "Physical Health Nutrition Actions"

    default = [
        "TRY",
        "PREPARE",
        "TRACK",
        "INCREASE",
        "IMPROVE",
    ]


class PhysicalHealthMovementActions(OptionSet):
    """
    Defines the possible actions that could be required for movement activities in the physical health backlog.

    You can customize this list to your liking.
    """

    display_name = "Physical Health Movement Actions"

    default = [
        "COMPLETE",
        "ATTEMPT",
        "PRACTICE",
        "REPEAT",
        "EXTEND",
    ]

