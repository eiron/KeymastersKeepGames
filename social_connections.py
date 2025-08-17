from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SocialConnectionsArchipelagoOptions:
    social_meetup_selection: SocialMeetupSelection
    social_family_selection: SocialFamilySelection
    social_community_selection: SocialCommunitySelection
    social_networking_selection: SocialNetworkingSelection
    social_people_selection: SocialPeopleSelection
    social_meetup_actions: SocialMeetupActions
    social_family_actions: SocialFamilyActions
    social_community_actions: SocialCommunityActions
    social_networking_actions: SocialNetworkingActions


class SocialConnectionsGame(Game):
    name = "Social/Connections Challenges"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = SocialConnectionsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        if self.has_meetups:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION_VERB MEETUP_TYPE with PERSON_NAME",
                    data={"ACTION_VERB": (self.meetup_actions, 1), "MEETUP_TYPE": (self.meetups, 1), "PERSON_NAME": (self.people, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        if self.has_family_activities:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION_VERB FAMILY_ACTIVITY_TYPE with PERSON_NAME",
                    data={"ACTION_VERB": (self.family_actions, 1), "FAMILY_ACTIVITY_TYPE": (self.family_activities, 1), "PERSON_NAME": (self.people, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            )

        if self.has_community_events:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION_VERB COMMUNITY_EVENT",
                    data={"ACTION_VERB": (self.community_actions, 1), "COMMUNITY_EVENT": (self.community_events, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            )

        if self.has_networking:
            game_objective_templates.append(
                GameObjectiveTemplate(
                    label="ACTION_VERB NETWORKING_EVENT",
                    data={"ACTION_VERB": (self.networking_actions, 1), "NETWORKING_EVENT": (self.networking_events, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        return game_objective_templates

    @property
    def has_meetups(self) -> bool:
        meetups = self.meetups()
        return len(meetups) > 0

    @property
    def has_family_activities(self) -> bool:
        family_activities = self.family_activities()
        return len(family_activities) > 0

    @property
    def has_community_events(self) -> bool:
        community_events = self.community_events()
        return len(community_events) > 0

    @property
    def has_networking(self) -> bool:
        networking_events = self.networking_events()
        return len(networking_events) > 0

    @functools.cached_property
    def meetup_actions(self) -> List[str]:
        return sorted(self.archipelago_options.social_meetup_actions.value)

    @functools.cached_property
    def family_actions(self) -> List[str]:
        return sorted(self.archipelago_options.social_family_actions.value)

    @functools.cached_property
    def community_actions(self) -> List[str]:
        return sorted(self.archipelago_options.social_community_actions.value)

    @functools.cached_property
    def networking_actions(self) -> List[str]:
        return sorted(self.archipelago_options.social_networking_actions.value)

    @functools.cached_property
    def meetups(self) -> List[str]:
        return sorted(self.archipelago_options.social_meetup_selection.value)

    @functools.cached_property
    def family_activities(self) -> List[str]:
        return sorted(self.archipelago_options.social_family_selection.value)

    @functools.cached_property
    def community_events(self) -> List[str]:
        return sorted(self.archipelago_options.social_community_selection.value)

    @functools.cached_property
    def networking_events(self) -> List[str]:
        return sorted(self.archipelago_options.social_networking_selection.value)

    @functools.cached_property
    def people(self) -> List[str]:
        return sorted(self.archipelago_options.social_people_selection.value)


# Archipelago Options
class SocialMeetupSelection(OptionSet):
    """
    Defines which friend meetups and social gatherings are in the player's social backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Social Meetup Selection"

    default = ["Coffee Meetup", "Lunch Date", "Game Night", "Movie Night", "Dinner Plans", "..."]


class SocialFamilySelection(OptionSet):
    """
    Defines which family activities and visits are in the player's social backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Social Family Selection"

    default = ["Family Dinner", "Holiday Visit", "Family Game Night", "Outdoor Activity", "Family Reunion", "..."]


class SocialCommunitySelection(OptionSet):
    """
    Defines which community events and local activities are in the player's social backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Social Community Selection"

    default = ["Local Festival", "Community Meeting", "Volunteer Activity", "Neighborhood Event", "Public Workshop", "..."]


class SocialNetworkingSelection(OptionSet):
    """
    Defines which networking events and professional gatherings are in the player's social backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Social Networking Selection"

    default = ["Professional Meetup", "Industry Conference", "Alumni Event", "Business Lunch", "Workshop", "..."]


class SocialPeopleSelection(OptionSet):
    """
    Defines the list of people (friends, family, colleagues, etc.) that you might interact with during social activities.

    Replace the placeholders with actual names or relationship descriptions of your choosing.
    """

    display_name = "Social People Selection"

    default = ["Best Friend", "College Friend", "Work Colleague", "Family Member", "Neighbour", "Old Friend", "..."]


class SocialMeetupActions(OptionSet):
    """
    Defines the possible actions that could be required for friend meetups and social gatherings.

    You can customize this list to your liking.
    """

    display_name = "Social Meetup Actions"

    default = [
        "ARRANGE",
        "MEET UP WITH",
        "HANG OUT WITH",
        "CATCH UP WITH",
        "RECONNECT WITH",
    ]


class SocialFamilyActions(OptionSet):
    """
    Defines the possible actions that could be required for family activities and visits.

    You can customize this list to your liking.
    """

    display_name = "Social Family Actions"

    default = [
        "VISIT",
        "SPEND TIME WITH",
        "RECONNECT WITH",
        "CALL",
        "PLAN WITH",
    ]


class SocialCommunityActions(OptionSet):
    """
    Defines the possible actions that could be required for community events and local activities.

    You can customize this list to your liking.
    """

    display_name = "Social Community Actions"

    default = [
        "ATTEND",
        "PARTICIPATE IN",
        "VOLUNTEER FOR",
        "JOIN",
        "SUPPORT",
    ]


class SocialNetworkingActions(OptionSet):
    """
    Defines the possible actions that could be required for networking events and professional gatherings.

    You can customize this list to your liking.
    """

    display_name = "Social Networking Actions"

    default = [
        "ATTEND",
        "NETWORK AT",
        "PRESENT AT",
        "PARTICIPATE IN",
        "CONNECT AT",
    ]

