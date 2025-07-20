from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class AdventureExperienceArchipelagoOptions:
    adventure_local_exploration_selection: AdventureLocalExplorationSelection
    adventure_cultural_experience_selection: AdventureCulturalExperienceSelection
    adventure_outdoor_activity_selection: AdventureOutdoorActivitySelection
    adventure_culinary_adventure_selection: AdventureCulinaryAdventureSelection
    adventure_local_exploration_actions: AdventureLocalExplorationActions
    adventure_cultural_experience_actions: AdventureCulturalExperienceActions
    adventure_outdoor_activity_actions: AdventureOutdoorActivityActions
    adventure_culinary_adventure_actions: AdventureCulinaryAdventureActions


class AdventureExperienceGame(Game):
    name = "Adventure/Experience Challenges"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = AdventureExperienceArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        if self.has_local_exploration:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION LOCAL",
                    data={"ACTION": (self.local_exploration_actions, 1), "LOCAL": (self.local_exploration, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        if self.has_cultural_experiences:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION CULTURAL",
                    data={"ACTION": (self.cultural_experience_actions, 1), "CULTURAL": (self.cultural_experiences, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            )

        if self.has_outdoor_activities:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION OUTDOOR",
                    data={"ACTION": (self.outdoor_activity_actions, 1), "OUTDOOR": (self.outdoor_activities, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            )

        if self.has_culinary_adventures:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION CULINARY",
                    data={"ACTION": (self.culinary_adventure_actions, 1), "CULINARY": (self.culinary_adventures, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        return game_objective_templates

    @property
    def has_local_exploration(self) -> bool:
        local_exploration = self.local_exploration()
        return len(local_exploration) > 0 and not (len(local_exploration) == 1 and local_exploration[0] in ["...", "Local Place 1"])

    @property
    def has_cultural_experiences(self) -> bool:
        cultural_experiences = self.cultural_experiences()
        return len(cultural_experiences) > 0 and not (len(cultural_experiences) == 1 and cultural_experiences[0] in ["...", "Cultural Experience 1"])

    @property
    def has_outdoor_activities(self) -> bool:
        outdoor_activities = self.outdoor_activities()
        return len(outdoor_activities) > 0 and not (len(outdoor_activities) == 1 and outdoor_activities[0] in ["...", "Outdoor Activity 1"])

    @property
    def has_culinary_adventures(self) -> bool:
        culinary_adventures = self.culinary_adventures()
        return len(culinary_adventures) > 0 and not (len(culinary_adventures) == 1 and culinary_adventures[0] in ["...", "Culinary Adventure 1"])

    def local_exploration_actions(self) -> List[str]:
        return sorted(self.archipelago_options.adventure_local_exploration_actions.value)

    def cultural_experience_actions(self) -> List[str]:
        return sorted(self.archipelago_options.adventure_cultural_experience_actions.value)

    def outdoor_activity_actions(self) -> List[str]:
        return sorted(self.archipelago_options.adventure_outdoor_activity_actions.value)

    def culinary_adventure_actions(self) -> List[str]:
        return sorted(self.archipelago_options.adventure_culinary_adventure_actions.value)

    def local_exploration(self) -> List[str]:
        return sorted(self.archipelago_options.adventure_local_exploration_selection.value)

    def cultural_experiences(self) -> List[str]:
        return sorted(self.archipelago_options.adventure_cultural_experience_selection.value)

    def outdoor_activities(self) -> List[str]:
        return sorted(self.archipelago_options.adventure_outdoor_activity_selection.value)

    def culinary_adventures(self) -> List[str]:
        return sorted(self.archipelago_options.adventure_culinary_adventure_selection.value)


# Archipelago Options
class AdventureLocalExplorationSelection(OptionSet):
    """
    Defines which local places and areas are in the player's exploration backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Adventure Local Exploration Selection"

    default = ["Downtown District", "Local Park", "Historic Neighborhood", "Nearby Trail", "..."]


class AdventureCulturalExperienceSelection(OptionSet):
    """
    Defines which cultural experiences are in the player's adventure backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Adventure Cultural Experience Selection"

    default = ["Art Museum", "Live Theater Show", "Music Festival", "Cultural Workshop", "..."]


class AdventureOutdoorActivitySelection(OptionSet):
    """
    Defines which outdoor activities are in the player's adventure backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Adventure Outdoor Activity Selection"

    default = ["Hiking Trail", "Camping Trip", "Rock Climbing", "Kayaking Adventure", "..."]


class AdventureCulinaryAdventureSelection(OptionSet):
    """
    Defines which culinary adventures are in the player's experience backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Adventure Culinary Adventure Selection"

    default = ["International Restaurant", "Food Festival", "Cooking Class", "Wine Tasting", "..."]


class AdventureLocalExplorationActions(OptionSet):
    """
    Defines the possible actions that could be required for local exploration in the adventure backlog.

    You can customize this list to your liking.
    """

    display_name = "Adventure Local Exploration Actions"

    default = [
        "VISIT",
        "EXPLORE",
        "DISCOVER",
        "REVISIT",
        "PHOTOGRAPH",
    ]


class AdventureCulturalExperienceActions(OptionSet):
    """
    Defines the possible actions that could be required for cultural experiences in the adventure backlog.

    You can customize this list to your liking.
    """

    display_name = "Adventure Cultural Experience Actions"

    default = [
        "ATTEND",
        "EXPERIENCE",
        "PARTICIPATE IN",
        "LEARN ABOUT",
        "IMMERSE IN",
    ]


class AdventureOutdoorActivityActions(OptionSet):
    """
    Defines the possible actions that could be required for outdoor activities in the adventure backlog.

    You can customize this list to your liking.
    """

    display_name = "Adventure Outdoor Activity Actions"

    default = [
        "ATTEMPT",
        "COMPLETE",
        "CONQUER",
        "EXPERIENCE",
        "MASTER",
    ]


class AdventureCulinaryAdventureActions(OptionSet):
    """
    Defines the possible actions that could be required for culinary adventures in the adventure backlog.

    You can customize this list to your liking.
    """

    display_name = "Adventure Culinary Adventure Actions"

    default = [
        "TRY",
        "VISIT",
        "SAMPLE",
        "EXPLORE",
        "DISCOVER",
    ]
