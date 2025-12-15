from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DespotsGameArchipelagoOptions:
    despots_include_campaign: DespotsIncludeCampaign
    despots_include_endless: DespotsIncludeEndless
    despots_include_king_of_the_hill: DespotsIncludeKingOfTheHill
    despots_include_challenge_modifiers: DespotsIncludeChallengeModifiers


class DespotsGame(Game):
    name = "Despot's Game"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = DespotsGameArchipelagoOptions

    # Property checks
    @property
    def include_campaign(self) -> bool:
        return self.archipelago_options.despots_include_campaign.value

    @property
    def include_endless(self) -> bool:
        return self.archipelago_options.despots_include_endless.value

    @property
    def include_king_of_the_hill(self) -> bool:
        return self.archipelago_options.despots_include_king_of_the_hill.value

    @property
    def include_challenge_modifiers(self) -> bool:
        return self.archipelago_options.despots_include_challenge_modifiers.value

    # Constraints
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(label="No shop rerolls", data={}),
            GameObjectiveTemplate(label="No food purchases", data={}),
            GameObjectiveTemplate(label="Use only melee classes", data={}),
            GameObjectiveTemplate(label="Use only ranged classes", data={}),
            GameObjectiveTemplate(label="No mutations purchased", data={}),
            GameObjectiveTemplate(label="Limit team to TEAM_SIZE humans", data={"TEAM_SIZE": (self.team_size_caps, 1)}),
            GameObjectiveTemplate(label="Keep food above FOOD_MIN for the whole run", data={"FOOD_MIN": (self.food_minimums, 1)}),
            GameObjectiveTemplate(label="No healers in the run", data={}),
            GameObjectiveTemplate(label="Sacrifice at least 20 humans", data={}),
            GameObjectiveTemplate(label="Have at least 20 humans active at once", data={}),
            GameObjectiveTemplate(label="Take the first Tank you find and always keep a Tank alive", data={}),
            GameObjectiveTemplate(label="Maintain at least 3 different complete alliance bonuses", data={}),
            GameObjectiveTemplate(label="Save 150 gold at once", data={}),
            GameObjectiveTemplate(label="After winning, beat 5 King of the Hill opponents", data={}),
            GameObjectiveTemplate(label="Sacrifice one of your starting units to the pit", data={}),
        ]

    # Objectives
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = []

        if self.include_campaign:
            templates.extend([
                GameObjectiveTemplate(
                    label="Beat the campaign with BUILD_THEME focus",
                    data={"BUILD_THEME": (self.build_themes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Beat the campaign with PRESET preset active",
                    data={"PRESET": (self.campaign_presets, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Reach floor FLOOR_TARGET in the campaign",
                    data={"FLOOR_TARGET": (self.campaign_floor_targets, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Defeat the final boss with at most TEAM_SIZE humans alive",
                    data={"TEAM_SIZE": (self.team_size_caps, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Beat the campaign while fielding only CLASS_FAMILY classes",
                    data={"CLASS_FAMILY": (self.class_families, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                ),
            ])

        if self.include_endless:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win an Endless run with PRESET preset active",
                    data={"PRESET": (self.endless_presets, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Survive to wave WAVE_TARGET in Endless mode",
                    data={"WAVE_TARGET": (self.endless_wave_targets, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSSES_REQUIRED bosses in Endless mode",
                    data={"BOSSES_REQUIRED": (self.endless_boss_targets, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                ),
            ])

        if self.include_king_of_the_hill:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win KING_WINS consecutive King of the Hill battles with PRESET preset",
                    data={
                        "KING_WINS": (self.king_win_streaks, 1),
                        "PRESET": (self.king_presets, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Win KING_WINS consecutive King of the Hill battles",
                    data={"KING_WINS": (self.king_win_streaks, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Reach rating RATING_TARGET in King of the Hill",
                    data={"RATING_TARGET": (self.king_rating_targets, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
            ])

        if self.include_challenge_modifiers:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete a run with MUTATOR active",
                    data={"MUTATOR": (self.challenge_modifiers, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Win a run with MUTATION_SET mutation set as your core",
                    data={"MUTATION_SET": (self.mutation_sets, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
            ])

        return templates

    # Data lists
    @staticmethod
    def build_themes() -> List[str]:
        return [
            "Fencers and Tricksters",
            "Shooters and Throwers",
            "Mages and Cultists",
            "Tanks and Healers",
            "Eggheads and Mimes",
            "Mixed synergy (3+ families)"
        ]

    @staticmethod
    def class_families() -> List[str]:
        return [
            "Fencer",
            "Trickster",
            "Shooter",
            "Thrower",
            "Mage",
            "Cultist",
            "Tank",
            "Healer",
            "Egghead",
            "Joker/Mime"
        ]

    @staticmethod
    def campaign_floor_targets() -> List[str]:
        return ["4", "6", "8", "10"]

    @staticmethod
    def campaign_presets() -> List[str]:
        return [
            "Classic",
            "Cannon Fodder",
            "Sportspeople",
            "Medieval",
            "Cosplay",
            "Special Mages",
            "Cooking Show",
            "Ultra Violence"
        ]

    @staticmethod
    def team_size_caps() -> List[str]:
        return ["8", "10", "12", "14"]

    @staticmethod
    def food_minimums() -> List[str]:
        return ["10", "20", "30"]

    @staticmethod
    def endless_wave_targets() -> List[str]:
        return ["20", "30", "40", "50"]

    @staticmethod
    def endless_presets() -> List[str]:
        return [
            "Classic",
            "Cannon Fodder",
            "Sportspeople",
            "Medieval",
            "Cosplay",
            "Special Mages",
            "Cooking Show",
            "Ultra Violence"
        ]

    @staticmethod
    def endless_boss_targets() -> List[str]:
        return ["3", "5", "7"]

    @staticmethod
    def king_win_streaks() -> List[str]:
        return ["3", "5", "7"]

    @staticmethod
    def king_presets() -> List[str]:
        return [
            "Classic",
            "Cannon Fodder",
            "Sportspeople",
            "Medieval",
            "Cosplay",
            "Special Mages",
            "Cooking Show",
            "Ultra Violence"
        ]

    @staticmethod
    def king_rating_targets() -> List[str]:
        return ["1200", "1400", "1600"]

    @staticmethod
    def challenge_modifiers() -> List[str]:
        return [
            "No food shops",
            "Fog of war rooms",
            "Double room sizes",
            "Exploding corpses",
            "Random teleports"
        ]

    @staticmethod
    def mutation_sets() -> List[str]:
        return [
            "Summoner synergy",
            "Dodge and evasion",
            "Armor stacking",
            "Attack speed focus",
            "Magic damage scaling"
        ]


# Archipelago Options
class DespotsIncludeCampaign(DefaultOnToggle):
    """Include campaign mode objectives."""
    display_name = "Despot's Game Include Campaign"


class DespotsIncludeEndless(DefaultOnToggle):
    """Include Endless mode objectives."""
    display_name = "Despot's Game Include Endless"


class DespotsIncludeKingOfTheHill(DefaultOnToggle):
    """Include King of the Hill mode objectives."""
    display_name = "Despot's Game Include King of the Hill"


class DespotsIncludeChallengeModifiers(DefaultOnToggle):
    """Include runs with specific mutators/modifiers enabled."""
    display_name = "Despot's Game Include Challenge Modifiers"
