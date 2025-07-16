from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class WatchlistArchipelagoOptions:
    watchlist_film_selection: WatchlistFilmSelection
    watchlist_tv_selection: WatchlistTVSelection
    watchlist_film_actions: WatchlistFilmActions
    watchlist_tv_actions: WatchlistTVActions


class WatchlistGame(Game):
    name = "Watchlist"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = WatchlistArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        if self.has_films:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION FILM",
                    data={"ACTION": (self.film_actions, 1), "FILM": (self.films, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        if self.has_tv_shows:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION TV",
                    data={"ACTION": (self.tv_actions, 1), "TV": (self.tv_shows, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        return game_objective_templates

    @property
    def has_films(self) -> bool:
        films = self.films()
        return len(films) > 0 and not (len(films) == 1 and films[0] in ["...", "Film 1"])

    @property
    def has_tv_shows(self) -> bool:
        tv_shows = self.tv_shows()
        return len(tv_shows) > 0 and not (len(tv_shows) == 1 and tv_shows[0] in ["...", "TV Show 1"])

    def film_actions(self) -> List[str]:
        return sorted(self.archipelago_options.watchlist_film_actions.value)

    def tv_actions(self) -> List[str]:
        return sorted(self.archipelago_options.watchlist_tv_actions.value)

    def films(self) -> List[str]:
        return sorted(self.archipelago_options.watchlist_film_selection.value)

    def tv_shows(self) -> List[str]:
        return sorted(self.archipelago_options.watchlist_tv_selection.value)


# Archipelago Options
class WatchlistFilmSelection(OptionSet):
    """
    Defines which films are in the player's watchlist.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Watchlist Film Selection"

    default = ["Film 1", "Film 2", "Documentary 1", "..."]


class WatchlistTVSelection(OptionSet):
    """
    Defines which TV shows/series are in the player's watchlist.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Watchlist TV Selection"

    default = ["TV Show 1", "TV Series 1", "Miniseries 1", "..."]


class WatchlistFilmActions(OptionSet):
    """
    Defines the possible actions that could be required for films in the watchlist.

    You can customize this list to your liking.
    """

    display_name = "Watchlist Film Actions"

    default = [
        "WATCH",
        "FINISH",
    ]


class WatchlistTVActions(OptionSet):
    """
    Defines the possible actions that could be required for TV shows in the watchlist.

    You can customize this list to your liking.
    """

    display_name = "Watchlist TV Actions"

    default = [
        "WATCH",
        "FINISH",
        "BINGE",
        "CATCH UP",
        "WATCH SEASON",
    ]
