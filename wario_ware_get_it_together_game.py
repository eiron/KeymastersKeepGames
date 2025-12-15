from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class WarioWareArchipelagoOptions:
    warioware_include_story_progress: WarioWareIncludeStoryProgress
    warioware_include_variety_pack: WarioWareIncludeVarietyPack
    warioware_include_wario_cup: WarioWareIncludeWarioCup


class WarioWareGetItTogetherGame(Game):
    name = "WarioWare: Get It Together!"
    platform = KeymastersKeepGamePlatforms.SW

    platforms_other: List[KeymastersKeepGamePlatforms] = []

    is_adult_only_or_unrated = False

    options_cls = WarioWareArchipelagoOptions

    # Properties
    @property
    def include_story_progress(self) -> bool:
        return self.archipelago_options.warioware_include_story_progress.value

    @property
    def include_variety_pack(self) -> bool:
        return self.archipelago_options.warioware_include_variety_pack.value

    @property
    def include_wario_cup(self) -> bool:
        return self.archipelago_options.warioware_include_wario_cup.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(label="Use a random crew member for the entire run", data={}),
            GameObjectiveTemplate(label="No jumping in applicable microgames", data={}),
            GameObjectiveTemplate(label="Controller rumble off for the session", data={}),
            GameObjectiveTemplate(label="Time-attack: finish a stage under 3 minutes", data={}),
            GameObjectiveTemplate(label="Perfect a boss microgame (no fails)", data={}),
            GameObjectiveTemplate(label="Only projectile characters for the session", data={}),
            GameObjectiveTemplate(label="Only mobility-specialist characters for the session", data={}),
            # Additional constraints/challenges
            GameObjectiveTemplate(label="Beat two consecutive microgames without pressing the A button", data={}),
            GameObjectiveTemplate(label="Get 5 points more than your goal", data={}),
            GameObjectiveTemplate(label="Get 10 points more than your goal", data={}),
            GameObjectiveTemplate(label="Get at least 130 coins in a Bonus stage", data={}),
            GameObjectiveTemplate(label="Get at least 150 coins in a Bonus stage", data={}),
            GameObjectiveTemplate(label="Play using only one hand", data={}),
            GameObjectiveTemplate(label="Intentionally fail your first boss microgame", data={}),
            GameObjectiveTemplate(label="Play using a single joycon", data={}),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = []

        if self.include_story_progress:
            templates.extend([
                GameObjectiveTemplate(
                    label="Play STORY_STAGE in Story with CHARACTERS. Earn a score of SCORE_TARGET or higher",
                    data={
                        "STORY_STAGE": (self.story_stages, 1),
                        "CHARACTERS": (self.characters, 3),
                        "SCORE_TARGET": (self.story_score_targets, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Play STORY_STAGE in Story with CHARACTERS. Earn a score of SCORE_TARGET or higher",
                    data={
                        "STORY_STAGE": (self.story_stages, 1),
                        "CHARACTERS": (self.characters, 2),
                        "SCORE_TARGET": (self.story_score_targets, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Play STORY_STAGE in Story with CHARACTER. Earn a score of SCORE_TARGET or higher",
                    data={
                        "STORY_STAGE": (self.story_stages, 1),
                        "CHARACTERS": (self.characters, 1),
                        "SCORE_TARGET": (self.story_score_targets, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Play STORY_STAGE in Story with CHARACTERS. Earn a score of SCORE_TARGET or higher",
                    data={
                        "STORY_STAGE": (self.story_stages, 1),
                        "CHARACTERS": (self.characters, 4),
                        "SCORE_TARGET": (self.story_score_targets, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Clear STORY_STAGE without losing a life",
                    data={"STORY_STAGE": (self.story_stages, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Beat MICROGAME on first try",
                    data={"MICROGAME": (self.microgames, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Finish STORY_STAGE using only CHARACTER",
                    data={
                        "STORY_STAGE": (self.story_stages, 1),
                        "CHARACTER": (self.characters, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=6,
                ),
            ])

        if self.include_variety_pack:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win MICROGAME_STREAK consecutive microgames in VARIETY_MODE",
                    data={
                        "MICROGAME_STREAK": (self.microgame_streak_targets, 1),
                        "VARIETY_MODE": (self.variety_pack_modes, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Co-op: clear VARIETY_MODE with no fails",
                    data={"VARIETY_MODE": (self.variety_pack_modes, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Versus: win a best-of-ROUND_TARGET in VARIETY_MODE",
                    data={
                        "ROUND_TARGET": (self.versus_round_targets, 1),
                        "VARIETY_MODE": (self.variety_pack_modes, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        if self.include_wario_cup:
            templates.extend([
                GameObjectiveTemplate(
                    label="Score SCORE_TARGET or higher in Wario Cup",
                    data={"SCORE_TARGET": (self.wario_cup_score_targets, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Place within RANK_TARGET% on a weekly Wario Cup",
                    data={"RANK_TARGET": (self.wario_cup_rank_targets, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=7,
                ),
            ])

        return templates

    # Data lists
    @staticmethod
    def characters() -> List[str]:
        # Roster with paired characters represented as pairs (single slot with P1/P2 variants)
        return [
            # Main cast
            "Wario",
            "Young Cricket",
            "18-Volt",
            "Mona",
            "Dribble & Spitz",
            "Dr. Crygor",
            "9-Volt",
            "Mike",
            "Kat & Ana",
            "Jimmy T",
            "Ashley",
            "Orbulon",
            # Extra and late-game characters
            "5-Volt",
            "Red",
            "Master Mantis",
            "Lulu",
            "Penny",
            "Pyoro",
        ]

    @staticmethod
    def story_stages() -> List[str]:
        # Official Story stage themes (representative list)
        return [
            "Intro",
            "That's Life",
            "Fantasy",
            "High Tech",
            "Nintendo Classics",
            "Nature",
            "Sports",
            "Food",
            "Culture",
            "Anything Goes",
        ]

    @staticmethod
    def microgames() -> List[str]:
        # Example microgames to target simple first-try clears
        return [
            "Pick the nose",
            "Dodge the spear",
            "Cut the grass",
            "Sort the trash",
            "Plug it in",
            "Keep the balance",
            "Find the alien",
            "Shoot the target",
        ]

    @staticmethod
    def variety_pack_modes() -> List[str]:
        # Full Variety Pack roster (10 modes)
        return [
            # Completionist (solo/turn-based)
            "Gotta Bounce",
            "Daily Grind",
            "Friendless Battle",
            # Party (competitive)
            "High Five",
            "Duelius Maximus",
            "Rising Star",
            "Balloon Bang",
            "Sly Angle",
            "Puck 'er Up",
            "Frenemy Frenzy",
        ]

    @staticmethod
    def microgame_streak_targets() -> List[str]:
        return ["3", "5", "7"]

    @staticmethod
    def versus_round_targets() -> List[str]:
        return ["3", "5"]

    @staticmethod
    def wario_cup_score_targets() -> List[str]:
        return ["30", "40", "50", "60"]

    @staticmethod
    def wario_cup_rank_targets() -> List[str]:
        return ["50", "25", "10"]

    @staticmethod
    def crew_size_targets() -> List[str]:
        # Crew sizes vary by mode; Story supports smaller crews too
        return ["1", "2", "3", "4"]

    @staticmethod
    def story_score_targets() -> List[str]:
        # 46 aligns with provided examples; include 58 and higher for scaling
        return ["46", "52", "58", "70"]


# Archipelago Options
class WarioWareIncludeStoryProgress(DefaultOnToggle):
    """Include objectives for clearing Story stages and boss microgames."""
    display_name = "WarioWare Include Story Progress"


class WarioWareIncludeVarietyPack(DefaultOnToggle):
    """Include objectives for Variety Pack co-op and versus."""
    display_name = "WarioWare Include Variety Pack"


class WarioWareIncludeWarioCup(DefaultOnToggle):
    """Include objectives for Wario Cup score and ranking."""
    display_name = "WarioWare Include Wario Cup"
