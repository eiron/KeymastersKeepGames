from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CreativeChallengesArchipelagoOptions:
    creative_art_project_selection: CreativeArtProjectSelection
    creative_writing_selection: CreativeWritingSelection
    creative_photography_selection: CreativePhotographySelection
    creative_craft_selection: CreativeCraftSelection
    creative_art_project_actions: CreativeArtProjectActions
    creative_writing_actions: CreativeWritingActions
    creative_photography_actions: CreativePhotographyActions
    creative_craft_actions: CreativeCraftActions


class CreativeChallengesGame(Game):
    name = "Creative Challenges"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = CreativeChallengesArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        if self.has_art_projects:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION ART",
                    data={"ACTION": (self.art_project_actions, 1), "ART": (self.art_projects, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            )

        if self.has_writing:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION WRITING",
                    data={"ACTION": (self.writing_actions, 1), "WRITING": (self.writing, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            )

        if self.has_photography:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION PHOTOGRAPHY",
                    data={"ACTION": (self.photography_actions, 1), "PHOTOGRAPHY": (self.photography, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        if self.has_crafts:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION CRAFT",
                    data={"ACTION": (self.craft_actions, 1), "CRAFT": (self.crafts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        return game_objective_templates

    @property
    def has_art_projects(self) -> bool:
        art_projects = self.art_projects()
        return len(art_projects) > 0

    @property
    def has_writing(self) -> bool:
        writing = self.writing()
        return len(writing) > 0

    @property
    def has_photography(self) -> bool:
        photography = self.photography()
        return len(photography) > 0

    @property
    def has_crafts(self) -> bool:
        crafts = self.crafts()
        return len(crafts) > 0

    def art_project_actions(self) -> List[str]:
        return sorted(self.archipelago_options.creative_art_project_actions.value)

    def writing_actions(self) -> List[str]:
        return sorted(self.archipelago_options.creative_writing_actions.value)

    def photography_actions(self) -> List[str]:
        return sorted(self.archipelago_options.creative_photography_actions.value)

    def craft_actions(self) -> List[str]:
        return sorted(self.archipelago_options.creative_craft_actions.value)

    def art_projects(self) -> List[str]:
        return sorted(self.archipelago_options.creative_art_project_selection.value)

    def writing(self) -> List[str]:
        return sorted(self.archipelago_options.creative_writing_selection.value)

    def photography(self) -> List[str]:
        return sorted(self.archipelago_options.creative_photography_selection.value)

    def crafts(self) -> List[str]:
        return sorted(self.archipelago_options.creative_craft_selection.value)


# Archipelago Options
class CreativeArtProjectSelection(OptionSet):
    """
    Defines which art projects are in the player's creative backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Creative Art Project Selection"

    default = ["Watercolor Painting", "Digital Illustration", "Sketch Series", "Mixed Media Piece", "..."]


class CreativeWritingSelection(OptionSet):
    """
    Defines which writing projects are in the player's creative backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Creative Writing Selection"

    default = ["Short Story", "Poetry Collection", "Creative Prompt", "Character Study", "..."]


class CreativePhotographySelection(OptionSet):
    """
    Defines which photography challenges are in the player's creative backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Creative Photography Selection"

    default = ["Portrait Session", "Nature Photography", "Street Photography", "Macro Challenge", "..."]


class CreativeCraftSelection(OptionSet):
    """
    Defines which craft projects are in the player's creative backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Creative Craft Selection"

    default = ["Knitting Project", "Woodworking", "Jewelry Making", "Origami Challenge", "..."]


class CreativeArtProjectActions(OptionSet):
    """
    Defines the possible actions that could be required for art projects in the creative backlog.

    You can customize this list to your liking.
    """

    display_name = "Creative Art Project Actions"

    default = [
        "CREATE",
        "COMPLETE",
        "EXPERIMENT WITH",
        "PRACTICE",
        "REFINE",
    ]


class CreativeWritingActions(OptionSet):
    """
    Defines the possible actions that could be required for writing projects in the creative backlog.

    You can customize this list to your liking.
    """

    display_name = "Creative Writing Actions"

    default = [
        "WRITE",
        "COMPLETE",
        "DRAFT",
        "REVISE",
        "EXPLORE",
    ]


class CreativePhotographyActions(OptionSet):
    """
    Defines the possible actions that could be required for photography challenges in the creative backlog.

    You can customize this list to your liking.
    """

    display_name = "Creative Photography Actions"

    default = [
        "CAPTURE",
        "COMPLETE",
        "EXPERIMENT WITH",
        "PRACTICE",
        "MASTER",
    ]


class CreativeCraftActions(OptionSet):
    """
    Defines the possible actions that could be required for craft projects in the creative backlog.

    You can customize this list to your liking.
    """

    display_name = "Creative Craft Actions"

    default = [
        "MAKE",
        "COMPLETE",
        "ATTEMPT",
        "PRACTICE",
        "MASTER",
    ]
