from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ChristmasHolidayChallengesArchipelagoOptions:
    christmas_decoration_selection: ChristmasDecorationSelection
    christmas_gift_selection: ChristmasGiftSelection
    christmas_baking_selection: ChristmasBakingSelection
    christmas_tradition_selection: ChristmasTraditionSelection
    christmas_decoration_actions: ChristmasDecorationActions
    christmas_gift_actions: ChristmasGiftActions
    christmas_baking_actions: ChristmasBakingActions
    christmas_tradition_actions: ChristmasTraditionActions


class ChristmasHolidayChallengesGame(Game):
    name = "Christmas Holiday Challenges"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = ChristmasHolidayChallengesArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        if self.has_decorations:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION DECORATION",
                    data={"ACTION": (self.decoration_actions, 1), "DECORATION": (self.decorations, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        if self.has_gifts:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION GIFT",
                    data={"ACTION": (self.gift_actions, 1), "GIFT": (self.gifts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            )

        if self.has_baking:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION BAKING",
                    data={"ACTION": (self.baking_actions, 1), "BAKING": (self.baking, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        if self.has_traditions:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION TRADITION",
                    data={"ACTION": (self.tradition_actions, 1), "TRADITION": (self.traditions, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        return game_objective_templates

    @property
    def has_decorations(self) -> bool:
        decorations = self.decorations()
        return len(decorations) > 0 and not (len(decorations) == 1 and decorations[0] in ["...", "Decoration 1"])

    @property
    def has_gifts(self) -> bool:
        gifts = self.gifts()
        return len(gifts) > 0 and not (len(gifts) == 1 and gifts[0] in ["...", "Gift 1"])

    @property
    def has_baking(self) -> bool:
        baking = self.baking()
        return len(baking) > 0 and not (len(baking) == 1 and baking[0] in ["...", "Recipe 1"])

    @property
    def has_traditions(self) -> bool:
        traditions = self.traditions()
        return len(traditions) > 0 and not (len(traditions) == 1 and traditions[0] in ["...", "Tradition 1"])

    def decoration_actions(self) -> List[str]:
        return sorted(self.archipelago_options.christmas_decoration_actions.value)

    def gift_actions(self) -> List[str]:
        return sorted(self.archipelago_options.christmas_gift_actions.value)

    def baking_actions(self) -> List[str]:
        return sorted(self.archipelago_options.christmas_baking_actions.value)

    def tradition_actions(self) -> List[str]:
        return sorted(self.archipelago_options.christmas_tradition_actions.value)

    def decorations(self) -> List[str]:
        return sorted(self.archipelago_options.christmas_decoration_selection.value)

    def gifts(self) -> List[str]:
        return sorted(self.archipelago_options.christmas_gift_selection.value)

    def baking(self) -> List[str]:
        return sorted(self.archipelago_options.christmas_baking_selection.value)

    def traditions(self) -> List[str]:
        return sorted(self.archipelago_options.christmas_tradition_selection.value)


# Archipelago Options
class ChristmasDecorationSelection(OptionSet):
    """
    Defines which Christmas decorations are in the player's holiday preparation backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Christmas Decoration Selection"

    default = ["Christmas Tree", "Outdoor Lights", "Mantel Decorations", "Holiday Wreath", "Window Display", "..."]


class ChristmasGiftSelection(OptionSet):
    """
    Defines which Christmas gifts and gift preparations are in the player's holiday backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Christmas Gift Selection"

    default = ["Handmade Gift", "Gift Wrapping", "Christmas Cards", "Care Package", "Secret Santa Gift", "..."]


class ChristmasBakingSelection(OptionSet):
    """
    Defines which Christmas baking and cooking projects are in the player's holiday backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Christmas Baking Selection"

    default = ["Christmas Cookies", "Gingerbread House", "Holiday Bread", "Festive Cake", "Hot Chocolate Bar", "..."]


class ChristmasTraditionSelection(OptionSet):
    """
    Defines which Christmas traditions and activities are in the player's holiday backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Christmas Tradition Selection"

    default = ["Christmas Movie Marathon", "Holiday Music Playlist", "Advent Calendar", "Christmas Market Visit", "Carol Singing", "..."]


class ChristmasDecorationActions(OptionSet):
    """
    Defines the possible actions that could be required for Christmas decorations in the holiday backlog.

    You can customize this list to your liking.
    """

    display_name = "Christmas Decoration Actions"

    default = [
        "SET UP",
        "CREATE",
        "ARRANGE",
        "COMPLETE",
        "PREPARE",
    ]


class ChristmasGiftActions(OptionSet):
    """
    Defines the possible actions that could be required for Christmas gifts in the holiday backlog.

    You can customize this list to your liking.
    """

    display_name = "Christmas Gift Actions"

    default = [
        "MAKE",
        "PREPARE",
        "WRAP",
        "CREATE",
        "FINISH",
    ]


class ChristmasBakingActions(OptionSet):
    """
    Defines the possible actions that could be required for Christmas baking in the holiday backlog.

    You can customize this list to your liking.
    """

    display_name = "Christmas Baking Actions"

    default = [
        "MAKE",
        "PREPARE",
        "COMPLETE",
        "CREATE",
        "ATTEMPT",
    ]


class ChristmasTraditionActions(OptionSet):
    """
    Defines the possible actions that could be required for Christmas traditions in the holiday backlog.

    You can customize this list to your liking.
    """

    display_name = "Christmas Tradition Actions"

    default = [
        "ENJOY",
        "PARTICIPATE IN",
        "ORGANIZE",
        "ATTEND",
        "EXPERIENCE",
    ]
