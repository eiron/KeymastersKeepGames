from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MusicListeningArchipelagoOptions:
    music_album_selection: MusicAlbumSelection
    music_artist_selection: MusicArtistSelection
    music_playlist_selection: MusicPlaylistSelection
    music_album_actions: MusicAlbumActions
    music_artist_actions: MusicArtistActions
    music_playlist_actions: MusicPlaylistActions


class MusicListeningGame(Game):
    name = "Music Listening"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = MusicListeningArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        if self.has_albums:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION ALBUM",
                    data={"ACTION": (self.album_actions, 1), "ALBUM": (self.albums, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        if self.has_artists:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION ARTIST",
                    data={"ACTION": (self.artist_actions, 1), "ARTIST": (self.artists, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        if self.has_playlists:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION PLAYLIST",
                    data={"ACTION": (self.playlist_actions, 1), "PLAYLIST": (self.playlists, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        return game_objective_templates

    @property
    def has_albums(self) -> bool:
        albums = self.albums()
        return len(albums) > 0 and not (len(albums) == 1 and albums[0] in ["...", "Album 1"])

    @property
    def has_artists(self) -> bool:
        artists = self.artists()
        return len(artists) > 0 and not (len(artists) == 1 and artists[0] in ["...", "Artist 1"])

    @property
    def has_playlists(self) -> bool:
        playlists = self.playlists()
        return len(playlists) > 0 and not (len(playlists) == 1 and playlists[0] in ["...", "Playlist 1"])

    def album_actions(self) -> List[str]:
        return sorted(self.archipelago_options.music_album_actions.value)

    def artist_actions(self) -> List[str]:
        return sorted(self.archipelago_options.music_artist_actions.value)

    def playlist_actions(self) -> List[str]:
        return sorted(self.archipelago_options.music_playlist_actions.value)

    def albums(self) -> List[str]:
        return sorted(self.archipelago_options.music_album_selection.value)

    def artists(self) -> List[str]:
        return sorted(self.archipelago_options.music_artist_selection.value)

    def playlists(self) -> List[str]:
        return sorted(self.archipelago_options.music_playlist_selection.value)


# Archipelago Options
class MusicAlbumSelection(OptionSet):
    """
    Defines which albums are in the player's music listening backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Music Album Selection"

    default = ["Album 1", "Album 2", "Soundtrack 1", "..."]


class MusicArtistSelection(OptionSet):
    """
    Defines which artists are in the player's music listening backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Music Artist Selection"

    default = ["Artist 1", "Band 1", "Composer 1", "..."]


class MusicPlaylistSelection(OptionSet):
    """
    Defines which playlists are in the player's music listening backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Music Playlist Selection"

    default = ["Playlist 1", "Mix 1", "Curated List 1", "..."]


class MusicAlbumActions(OptionSet):
    """
    Defines the possible actions that could be required for albums in the music backlog.

    You can customize this list to your liking.
    """

    display_name = "Music Album Actions"

    default = [
        "LISTEN TO",
        "COMPLETE",
        "REVISIT",
        "ANALYZE",
    ]


class MusicArtistActions(OptionSet):
    """
    Defines the possible actions that could be required for artists in the music backlog.

    You can customize this list to your liking.
    """

    display_name = "Music Artist Actions"

    default = [
        "EXPLORE",
        "DEEP DIVE",
        "DISCOVER",
        "STUDY DISCOGRAPHY",
    ]


class MusicPlaylistActions(OptionSet):
    """
    Defines the possible actions that could be required for playlists in the music backlog.

    You can customize this list to your liking.
    """

    display_name = "Music Playlist Actions"

    default = [
        "LISTEN TO",
        "COMPLETE",
        "SHUFFLE THROUGH",
        "CURATE FROM",
    ]
