from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BoardGameCollectionArchipelagoOptions:
    board_game_collection_selection: BoardGameCollectionSelection
    board_game_solo_selection: BoardGameSoloSelection
    board_game_coop_selection: BoardGameCoopSelection
    board_game_competitive_selection: BoardGameCompetitiveSelection
    board_game_party_selection: BoardGamePartySelection
    board_game_collection_actions: BoardGameCollectionActions
    board_game_solo_actions: BoardGameSoloActions
    board_game_coop_actions: BoardGameCoopActions
    board_game_competitive_actions: BoardGameCompetitiveActions
    board_game_party_actions: BoardGamePartyActions


class BoardGameCollectionGame(Game):
    name = "Board Game Collection"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = BoardGameCollectionArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # General collection objectives
        if self.has_collection_games:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION GAME",
                    data={"ACTION": (self.collection_actions, 1), "GAME": (self.collection_games, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            )

        # Solo game objectives
        if self.has_solo_games:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION SOLO_GAME",
                    data={"ACTION": (self.solo_actions, 1), "SOLO_GAME": (self.solo_games, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            )

        # Cooperative game objectives
        if self.has_coop_games:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION COOP_GAME cooperatively",
                    data={"ACTION": (self.coop_actions, 1), "COOP_GAME": (self.coop_games, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            )

        # Competitive game objectives
        if self.has_competitive_games:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION COMPETITIVE_GAME competitively",
                    data={"ACTION": (self.competitive_actions, 1), "COMPETITIVE_GAME": (self.competitive_games, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            )

        # Party game objectives
        if self.has_party_games:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION PARTY_GAME with a group",
                    data={"ACTION": (self.party_actions, 1), "PARTY_GAME": (self.party_games, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        return game_objective_templates

    @property
    def has_collection_games(self) -> bool:
        collection_games = self.collection_games()
        return len(collection_games) > 0

    @property
    def has_solo_games(self) -> bool:
        solo_games = self.solo_games()
        return len(solo_games) > 0

    @property
    def has_coop_games(self) -> bool:
        coop_games = self.coop_games()
        return len(coop_games) > 0

    @property
    def has_competitive_games(self) -> bool:
        competitive_games = self.competitive_games()
        return len(competitive_games) > 0

    @property
    def has_party_games(self) -> bool:
        party_games = self.party_games()
        return len(party_games) > 0

    def collection_actions(self) -> List[str]:
        return sorted(self.archipelago_options.board_game_collection_actions.value)

    def solo_actions(self) -> List[str]:
        return sorted(self.archipelago_options.board_game_solo_actions.value)

    def coop_actions(self) -> List[str]:
        return sorted(self.archipelago_options.board_game_coop_actions.value)

    def competitive_actions(self) -> List[str]:
        return sorted(self.archipelago_options.board_game_competitive_actions.value)

    def party_actions(self) -> List[str]:
        return sorted(self.archipelago_options.board_game_party_actions.value)

    def collection_games(self) -> List[str]:
        return sorted(self.archipelago_options.board_game_collection_selection.value)

    def solo_games(self) -> List[str]:
        return sorted(self.archipelago_options.board_game_solo_selection.value)

    def coop_games(self) -> List[str]:
        return sorted(self.archipelago_options.board_game_coop_selection.value)

    def competitive_games(self) -> List[str]:
        return sorted(self.archipelago_options.board_game_competitive_selection.value)

    def party_games(self) -> List[str]:
        return sorted(self.archipelago_options.board_game_party_selection.value)


# Archipelago Options
class BoardGameCollectionSelection(OptionSet):
    """
    Defines which board games are in the player's general collection backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Board Game Collection Selection"

    default = [
        "Wingspan", "Azul", "Ticket to Ride", "Splendor", "King of Tokyo",
        "Catan", "7 Wonders", "Pandemic", "Gloomhaven", "Scythe", "..."
    ]


class BoardGameSoloSelection(OptionSet):
    """
    Defines which solo board games are in the player's backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Board Game Solo Selection"

    default = [
        "Spirit Island", "Mage Knight", "Robinson Crusoe", "Arkham Horror LCG",
        "Terraforming Mars", "Everdell", "Wingspan", "..."
    ]


class BoardGameCoopSelection(OptionSet):
    """
    Defines which cooperative board games are in the player's backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Board Game Cooperative Selection"

    default = [
        "Pandemic", "Spirit Island", "Gloomhaven", "Forbidden Island",
        "Arkham Horror", "Flash Point", "Mysterium", "..."
    ]


class BoardGameCompetitiveSelection(OptionSet):
    """
    Defines which competitive board games are in the player's backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Board Game Competitive Selection"

    default = [
        "Scythe", "Terraforming Mars", "Through the Ages", "Race for the Galaxy",
        "Puerto Rico", "Power Grid", "Agricola", "..."
    ]


class BoardGamePartySelection(OptionSet):
    """
    Defines which party board games are in the player's backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Board Game Party Selection"

    default = [
        "Codenames", "Just One", "Wavelength", "Telestrations",
        "The Resistance", "One Night Ultimate Werewolf", "Dixit", "..."
    ]


class BoardGameCollectionActions(OptionSet):
    """
    Defines the possible actions that could be required for general board game collection objectives.

    You can customize this list to your liking.
    """

    display_name = "Board Game Collection Actions"

    default = [
        "PLAY",
        "LEARN",
        "MASTER",
        "EXPLORE",
        "COMPLETE",
        "EXPERIENCE",
        "REVISIT",
    ]


class BoardGameSoloActions(OptionSet):
    """
    Defines the possible actions that could be required for solo board game objectives.

    You can customize this list to your liking.
    """

    display_name = "Board Game Solo Actions"

    default = [
        "SOLO PLAY",
        "MASTER",
        "COMPLETE",
        "CHALLENGE YOURSELF WITH",
        "ACHIEVE HIGH SCORE IN",
        "PRACTICE",
    ]


class BoardGameCoopActions(OptionSet):
    """
    Defines the possible actions that could be required for cooperative board game objectives.

    You can customize this list to your liking.
    """

    display_name = "Board Game Cooperative Actions"

    default = [
        "WIN",
        "COMPLETE",
        "WORK TOGETHER IN",
        "SUCCEED AT",
        "CONQUER",
        "TEAM UP FOR",
    ]


class BoardGameCompetitiveActions(OptionSet):
    """
    Defines the possible actions that could be required for competitive board game objectives.

    You can customize this list to your liking.
    """

    display_name = "Board Game Competitive Actions"

    default = [
        "WIN",
        "COMPETE IN",
        "DOMINATE",
        "TRIUMPH IN",
        "OUTPLAY OPPONENTS IN",
        "CLAIM VICTORY IN",
    ]


class BoardGamePartyActions(OptionSet):
    """
    Defines the possible actions that could be required for party board game objectives.

    You can customize this list to your liking.
    """

    display_name = "Board Game Party Actions"

    default = [
        "HOST",
        "ENJOY",
        "LAUGH WITH",
        "ENTERTAIN FRIENDS WITH",
        "HAVE FUN WITH",
        "GATHER FOR",
    ]
