from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, OptionSet, TextChoice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DanganronpaArchipelagoOptions:
    danganronpa_owned_games: "DanganronpaOwnedGames"
    danganronpa_enable_story_mode: "DanganronpaEnableStoryMode"
    danganronpa_enable_bonus_modes: "DanganronpaEnableBonusModes"
    danganronpa_include_investigation: "DanganronpaIncludeInvestigation"
    danganronpa_include_class_trial: "DanganronpaIncludeClassTrial"
    danganronpa_include_free_time: "DanganronpaIncludeFreeTime"
    danganronpa_include_report_card: "DanganronpaIncludeReportCard"
    danganronpa_include_skills: "DanganronpaIncludeSkills"
    danganronpa_include_presents: "DanganronpaIncludePresents"
    danganronpa_include_underwear_presents: "DanganronpaIncludeUnderwearPresents"
    danganronpa_include_school_mode: "DanganronpaIncludeSchoolMode"
    danganronpa_include_island_mode: "DanganronpaIncludeIslandMode"
    danganronpa_include_collectibles: "DanganronpaIncludeCollectibles"
    danganronpa_include_summer_camp: "DanganronpaIncludeSummerCamp"
    danganronpa_logic_difficulty: "DanganronpaLogicDifficulty"
    danganronpa_action_difficulty: "DanganronpaActionDifficulty"


class DanganronpaGame(Game):
    name = "Danganronpa Decadence"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = DanganronpaArchipelagoOptions

    # ===== Optional constraints =====
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = []

        if self.logic_difficulty in ("mean", "cruel"):
            constraints.extend([
                GameObjectiveTemplate(
                    label="Complete this objective within DAYS in-game days",
                    data={"DAYS": (self.all_day_counts, 1)},
                ),
                GameObjectiveTemplate(
                    label="Complete this objective without any incorrect statements",
                    data={},
                ),
            ])

        if self.action_difficulty in ("mean", "cruel"):
            constraints.extend([
                GameObjectiveTemplate(
                    label="Complete this objective with at least HEALTH percent Influence remaining",
                    data={"HEALTH": (self.all_health_thresholds, 1)},
                ),
                GameObjectiveTemplate(
                    label="Complete this objective without using Focus Gauge",
                    data={},
                ),
            ])

        if self.logic_difficulty == "cruel" or self.action_difficulty == "cruel":
            constraints.extend([
                GameObjectiveTemplate(label="Complete this objective without retrying", data={}),
                GameObjectiveTemplate(label="Complete this objective without equipping skills", data={}),
            ])

        return constraints

    # ===== Objective templates =====
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = []

        has_dr1 = "Danganronpa: Trigger Happy Havoc" in self.games_owned
        has_dr2 = "Danganronpa 2: Goodbye Despair" in self.games_owned
        has_v3 = "Danganronpa V3: Killing Harmony" in self.games_owned
        has_drs = "Danganronpa S: Ultimate Summer Camp" in self.games_owned

        # ==================== DR1: Trigger Happy Havoc ====================
        if has_dr1 and self.enable_story_mode:
            if self.include_investigation:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Find all Truth Bullets in Chapter CHAPTER (DR1)",
                        data={"CHAPTER": (self.all_chapters, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=3,
                    ),
                    GameObjectiveTemplate(
                        label="Examine a point of interest in LOCATION during an investigation (DR1)",
                        data={"LOCATION": (self.dr1_investigation_locations, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Earn QUANTITY Monocoins (DR1)",
                        data={"QUANTITY": (self.all_monocoin_quantities, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            if self.include_class_trial:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Achieve RANK rank in the Chapter CHAPTER Class Trial (DR1)",
                        data={
                            "RANK": (self.all_trial_ranks, 1),
                            "CHAPTER": (self.all_chapters, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=4,
                    ),
                    GameObjectiveTemplate(
                        label="Clear QUANTITY MECHANIC encounters without mistakes (DR1)",
                        data={
                            "QUANTITY": (self.all_perfect_segment_counts, 1),
                            "MECHANIC": (self.dr1_trial_mechanics, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=3,
                    ),
                    GameObjectiveTemplate(
                        label="Complete a Closing Argument without any mistakes (DR1)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                ])

            if self.include_free_time:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Max out friendship with STUDENT (DR1)",
                        data={"STUDENT": (self.dr1_students, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Spend QUANTITY Free Time sessions with different students (DR1)",
                        data={"QUANTITY": (self.all_free_time_targets, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Have a Free Time conversation with STUDENT (DR1)",
                        data={"STUDENT": (self.dr1_students, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            if self.include_report_card:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Complete the Report Card for STUDENT (DR1)",
                        data={"STUDENT": (self.dr1_students, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Complete Report Cards for QUANTITY different students (DR1)",
                        data={"QUANTITY": (self.all_report_card_counts, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=3,
                    ),
                ])

            if self.include_skills:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Obtain the SKILL skill (DR1)",
                        data={"SKILL": (self.dr1_skills, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Earn QUANTITY Skill Points (DR1)",
                        data={"QUANTITY": (self.all_skill_point_quantities, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            if self.include_presents:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Obtain PRESENT from the MonoMono Machine (DR1)",
                        data={"PRESENT": (self.dr1_presents, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Collect QUANTITY different presents (DR1)",
                        data={"QUANTITY": (self.all_present_quantities, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Gift a present to STUDENT (DR1)",
                        data={"STUDENT": (self.dr1_students, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Gift a Loved present to STUDENT (DR1)",
                        data={"STUDENT": (self.dr1_students, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                ])

        # DR1 Bonus: School Mode
        if has_dr1 and self.enable_bonus_modes and self.include_school_mode:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete a School Mode backup with DAYS days to spare (DR1)",
                    data={"DAYS": (self.all_school_mode_remaining_days, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Maintain top cleanliness for DAYS consecutive days in School Mode (DR1)",
                    data={"DAYS": (self.all_school_mode_streak_days, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Max out friendship with STUDENT in School Mode (DR1)",
                    data={"STUDENT": (self.dr1_students, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # ==================== DR2: Goodbye Despair ====================
        if has_dr2 and self.enable_story_mode:
            if self.include_investigation:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Find all Truth Bullets in Chapter CHAPTER (DR2)",
                        data={"CHAPTER": (self.all_chapters, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=3,
                    ),
                    GameObjectiveTemplate(
                        label="Examine a point of interest in LOCATION during an investigation (DR2)",
                        data={"LOCATION": (self.dr2_investigation_locations, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Earn QUANTITY Monocoins (DR2)",
                        data={"QUANTITY": (self.all_monocoin_quantities, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            if self.include_class_trial:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Achieve RANK rank in the Chapter CHAPTER Class Trial (DR2)",
                        data={
                            "RANK": (self.all_trial_ranks, 1),
                            "CHAPTER": (self.all_chapters, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=4,
                    ),
                    GameObjectiveTemplate(
                        label="Clear QUANTITY MECHANIC encounters without mistakes (DR2)",
                        data={
                            "QUANTITY": (self.all_perfect_segment_counts, 1),
                            "MECHANIC": (self.dr2_trial_mechanics, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=3,
                    ),
                    GameObjectiveTemplate(
                        label="Complete a Closing Argument without any mistakes (DR2)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                ])

            if self.include_free_time:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Max out friendship with STUDENT (DR2)",
                        data={"STUDENT": (self.dr2_students, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Spend QUANTITY Free Time sessions with different students (DR2)",
                        data={"QUANTITY": (self.all_free_time_targets, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Have a Free Time conversation with STUDENT (DR2)",
                        data={"STUDENT": (self.dr2_students, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            if self.include_report_card:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Complete the Report Card for STUDENT (DR2)",
                        data={"STUDENT": (self.dr2_students, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Complete Report Cards for QUANTITY different students (DR2)",
                        data={"QUANTITY": (self.all_report_card_counts, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=3,
                    ),
                ])

            if self.include_skills:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Obtain the SKILL skill (DR2)",
                        data={"SKILL": (self.dr2_skills, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Earn QUANTITY Hope Fragments (DR2)",
                        data={"QUANTITY": (self.all_hope_fragment_quantities, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            if self.include_presents:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Obtain PRESENT from the MonoMono Machine (DR2)",
                        data={"PRESENT": (self.dr2_presents, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Collect QUANTITY different presents (DR2)",
                        data={"QUANTITY": (self.all_present_quantities, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Gift a present to STUDENT (DR2)",
                        data={"STUDENT": (self.dr2_students, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Gift a Loved present to STUDENT (DR2)",
                        data={"STUDENT": (self.dr2_students, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                ])

            if self.include_collectibles:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Find QUANTITY Hidden Monokumas in Chapter CHAPTER (DR2)",
                        data={
                            "QUANTITY": (self.all_hidden_monokuma_counts, 1),
                            "CHAPTER": (self.all_chapters, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Find a Hidden Monokuma in LOCATION (DR2)",
                        data={"LOCATION": (self.dr2_locations, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

        # DR2 Bonus: Island Mode
        if has_dr2 and self.enable_bonus_modes and self.include_island_mode:
            templates.extend([
                GameObjectiveTemplate(
                    label="Earn all Hope Fragments for STUDENT in Island Mode (DR2)",
                    data={"STUDENT": (self.dr2_students, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Reach day DAY in Island Mode without gathering failures (DR2)",
                    data={"DAY": (self.all_island_mode_days, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Max out friendship with STUDENT in Island Mode (DR2)",
                    data={"STUDENT": (self.dr2_students, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # DR2 Bonus: Magical Girl Monomi
        if has_dr2 and self.enable_bonus_modes:
            templates.extend([
                GameObjectiveTemplate(
                    label="Clear Chapter CHAPTER of Magical Girl Monomi (DR2)",
                    data={"CHAPTER": (self.all_monomi_chapters, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete Magical Girl Monomi Chapter CHAPTER without taking damage (DR2)",
                    data={"CHAPTER": (self.all_monomi_chapters, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
            ])

        # ==================== V3: Killing Harmony ====================
        if has_v3 and self.enable_story_mode:
            if self.include_investigation:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Find all Truth Bullets in Chapter CHAPTER (V3)",
                        data={"CHAPTER": (self.all_chapters, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=3,
                    ),
                    GameObjectiveTemplate(
                        label="Examine a point of interest in LOCATION during an investigation (V3)",
                        data={"LOCATION": (self.v3_investigation_locations, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Earn QUANTITY Monocoins (V3)",
                        data={"QUANTITY": (self.all_monocoin_quantities, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            if self.include_class_trial:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Achieve RANK rank in the Chapter CHAPTER Class Trial (V3)",
                        data={
                            "RANK": (self.all_trial_ranks, 1),
                            "CHAPTER": (self.all_chapters, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=4,
                    ),
                    GameObjectiveTemplate(
                        label="Clear QUANTITY MECHANIC encounters without mistakes (V3)",
                        data={
                            "QUANTITY": (self.all_perfect_segment_counts, 1),
                            "MECHANIC": (self.v3_trial_mechanics, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=3,
                    ),
                    GameObjectiveTemplate(
                        label="Win a Debate Scrum with at least HEALTH percent Influence remaining (V3)",
                        data={"HEALTH": (self.all_health_thresholds, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Complete an Argument Armament without missing a beat (V3)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Complete a Closing Argument without any mistakes (V3)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                ])

            if self.include_free_time:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Max out friendship with STUDENT (V3)",
                        data={"STUDENT": (self.v3_students, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Spend QUANTITY Free Time sessions with different students (V3)",
                        data={"QUANTITY": (self.all_free_time_targets, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Have a Free Time conversation with STUDENT (V3)",
                        data={"STUDENT": (self.v3_students, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            if self.include_report_card:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Complete the Report Card for STUDENT (V3)",
                        data={"STUDENT": (self.v3_students, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Complete Report Cards for QUANTITY different students (V3)",
                        data={"QUANTITY": (self.all_report_card_counts, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=3,
                    ),
                ])

            if self.include_skills:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Obtain the SKILL skill (V3)",
                        data={"SKILL": (self.v3_skills, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Earn QUANTITY Hope Fragments (V3)",
                        data={"QUANTITY": (self.all_hope_fragment_quantities, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            if self.include_presents:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Obtain PRESENT from the MonoMono Machine (V3)",
                        data={"PRESENT": (self.v3_presents, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Collect QUANTITY different presents (V3)",
                        data={"QUANTITY": (self.all_present_quantities, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Gift a present to STUDENT (V3)",
                        data={"STUDENT": (self.v3_students, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Gift a Loved present to STUDENT (V3)",
                        data={"STUDENT": (self.v3_students, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                ])

            if self.include_collectibles:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Find QUANTITY Hidden Monokumas in Chapter CHAPTER (V3)",
                        data={
                            "QUANTITY": (self.all_hidden_monokuma_counts, 1),
                            "CHAPTER": (self.all_chapters, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Find a Hidden Monokuma in LOCATION (V3)",
                        data={"LOCATION": (self.v3_locations, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

        # V3 Bonus Modes
        if has_v3 and self.enable_bonus_modes:
            templates.extend([
                GameObjectiveTemplate(
                    label="Clear Death Road of Despair (V3)",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Complete a Love Across the Universe event with STUDENT (V3)",
                    data={"STUDENT": (self.v3_students, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Win QUANTITY Casino Coins at the Casino (V3)",
                    data={"QUANTITY": (self.all_casino_coin_quantities, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # ==================== DRS: Ultimate Summer Camp ====================
        if has_drs and self.include_summer_camp:
            templates.extend([
                GameObjectiveTemplate(
                    label="Reach turn TURN in Development Mode as CHARACTER (DRS)",
                    data={
                        "TURN": (self.all_development_turn_counts, 1),
                        "CHARACTER": (self.all_summer_camp_characters, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Develop a character to level LEVEL in Development Mode (DRS)",
                    data={"LEVEL": (self.all_development_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Clear floor FLOOR in Tower of Despair (DRS)",
                    data={"FLOOR": (self.all_tower_floors, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Clear floor FLOOR in Tower of Despair with a party that includes CHARACTER (DRS)",
                    data={
                        "FLOOR": (self.all_tower_floors, 1),
                        "CHARACTER": (self.all_summer_camp_characters, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Clear floor FLOOR in Tower of Despair using CHARACTERS (DRS)",
                    data={
                        "FLOOR": (self.all_tower_floors, 1),
                        "CHARACTERS": (self.all_summer_camp_characters, 4),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Unlock a swimsuit outfit for CHARACTER (DRS)",
                    data={"CHARACTER": (self.all_swimsuit_characters, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSS in Development Mode (DRS)",
                    data={"BOSS": (self.all_summer_camp_bosses, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Collect QUANTITY Hope Fragments in Development Mode (DRS)",
                    data={"QUANTITY": (self.all_hope_fragment_quantities, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Acquire a rare card from the MonoMono Machine (DRS)",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Trigger a character event between CHARACTERS during Development Mode (DRS)",
                    data={"CHARACTERS": (self.all_summer_camp_characters, 2)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        return templates

    # ==================== Shared numeric pools ====================

    @staticmethod
    def all_chapters() -> List[int]:
        return [1, 2, 3, 4, 5, 6]

    @staticmethod
    def all_trial_ranks() -> List[str]:
        return ["A", "S"]

    @staticmethod
    def all_perfect_segment_counts() -> List[int]:
        return [1, 2, 3]

    @staticmethod
    def all_health_thresholds() -> List[int]:
        return [25, 50, 75, 100]

    @staticmethod
    def all_free_time_targets() -> List[int]:
        return [3, 5, 8]

    @staticmethod
    def all_hope_fragment_quantities() -> List[int]:
        return [5, 10, 20, 30]

    @staticmethod
    def all_skill_point_quantities() -> List[int]:
        return [5, 10, 20, 30]

    @staticmethod
    def all_report_card_counts() -> List[int]:
        return [3, 5, 10]

    @staticmethod
    def all_present_quantities() -> List[int]:
        return [10, 20, 30, 50]

    @staticmethod
    def all_monocoin_quantities() -> List[int]:
        return [25, 50, 100]

    @staticmethod
    def all_hidden_monokuma_counts() -> List[int]:
        return [1, 3, 5]

    @staticmethod
    def all_day_counts() -> List[int]:
        return [5, 10, 15, 20]

    # ==================== DR1 data pools ====================

    @staticmethod
    def dr1_students() -> List[str]:
        return [
            "Kyoko Kirigiri", "Byakuya Togami", "Toko Fukawa", "Aoi Asahina",
            "Yasuhiro Hagakure", "Kiyotaka Ishimaru", "Mondo Owada", "Chihiro Fujisaki",
            "Leon Kuwata", "Sakura Ogami", "Hifumi Yamada", "Celestia Ludenberg",
            "Sayaka Maizono", "Junko Enoshima",
        ]

    @staticmethod
    def dr1_investigation_locations() -> List[str]:
        return [
            "Classroom", "Dormitory", "Dining Hall", "Gymnasium", "Library",
            "Nurse's Office", "A/V Room", "Pool", "Laundry Room", "Bio Lab",
            "Chemistry Lab", "Music Room", "Bathhouse", "Rec Room", "Garden",
            "Trash Room",
        ]

    @staticmethod
    def dr1_locations() -> List[str]:
        return [
            "Gymnasium", "Cafeteria", "Dormitory", "Library", "Pool", "Bathhouse",
            "Bio Lab", "Chemistry Lab", "Music Room", "Nurse's Office", "School Store",
            "Rec Room", "Headmaster's Office", "Garden", "Laundry Room", "A/V Room",
        ]

    @staticmethod
    def dr1_trial_mechanics() -> List[str]:
        return ["Nonstop Debate", "Hangman's Gambit", "Bullet Time Battle"]

    @staticmethod
    def dr1_skills() -> List[str]:
        return [
            "Algorithm", "Attentive Influence", "Cool and Composed",
            "Envious Influence", "Handiwork", "High Voltage", "Kind Composure",
            "Machine Gun Talk Battle", "Menacing Focus", "Motor Skill",
            "Neural Liberation", "Psychic Focus", "Robot Jock",
            "Speed Loader", "Steady Aim", "Tranquility",
        ]

    DR1_PRESENTS = [
        "Mineral Water", "Cola Cola", "Civet Coffee", "Rose Hip Tea", "Sea Salt",
        "Potato Chips", "Prismatic Hardtack", "Black Croissant", "Sonic Cup-a-Noodle",
        "Royal Curry", "Ration", "Flotation Donut", "Overflowing Lunch Box",
        "Sunflower Seeds", "Birdseed", "Kitten Hairclip", "Everlasting Bracelet",
        "Love Status Ring", "Zoles Diamond", "Hope's Peak Ring", "Blueberry Perfume",
        "Scarab Brooch", "God of War Charm", "Mac's Gloves", "Glasses", "G-Sick",
        "Roller Slippers", "Red Scarf", "Bunny Earmuffs", "Fresh Bindings",
        "Jimmy Decay T-Shirt", "Emperor's Thong", "Hand Bra", "Waterlover",
        "Demon Angel Princess Figure", "Astral Boy Doll", "Shears", "Layering Shears",
        "Quality Chinchilla Cover", "Kirlian Camera", "Adorable Reactions Collection",
        "Tumbleweed", "Unending Dandelion", "Rose in Vitro", "Cherry Blossom Bouquet",
        "Rose Whip", "Zantetsuken", "Muramasa", "Raygun Zurion", "Golden Gun",
        "Berserker Armor", "Self-Destructing Cassette", "Silent Receiver",
        "Pretty Hungry Caterpillar", "Old Timey Radio", "Mr. Fastball", "Antique Doll",
        "Crystal Skull", "Golden Airplane", "Prince Shotoku's Globe", "Moon Rock",
        "Asura's Tears", "Secrets of the Omoplata", "Millennium Prize Problems",
        "The Funplane", "Project Zombie", "Pagan Dancer", "Tips & Tips",
        "Maiden's Handbag", "Kokeshi Dynamo", "The Second Button",
        "Someone's Graduation Album", "Vise", "Sacred Tree Sprig", "Pumice", "Oblaat",
        "Water Flute", "Bojobo Dolls", "Small Light", "Voice-Changing Bowtie",
        "Ancient Tour Tickets", "Novelist's Fountain Pen", "If Fax", "Cat-Dog Magazine",
        "Meteorite Arrowhead", "Chin Drill", "Green Costume", "Red Costume",
        "A Man's Fantasy", "Escape Button",
    ]

    DR1_UNDERWEAR = [
        "Kiyotaka's Undergarments", "Byakuya's Undergarments", "Mondo's Undergarments",
        "Leon's Undergarments", "Hifumi's Undergarments", "Yasuhiro's Undergarments",
        "Sayaka's Undergarments", "Kyoko's Undergarments", "Aoi's Undergarments",
        "Toko's Undergarments", "Sakura's Undergarments", "Celeste's Undergarments",
        "Junko's Undergarments", "Chihiro's Undergarments",
    ]

    def dr1_presents(self) -> List[str]:
        presents = list(self.DR1_PRESENTS)
        if self.include_underwear_presents:
            presents.extend(self.DR1_UNDERWEAR)
        return presents

    # ==================== DR2 data pools ====================

    @staticmethod
    def dr2_students() -> List[str]:
        return [
            "Nagito Komaeda", "Chiaki Nanami", "Sonia Nevermind", "Gundham Tanaka",
            "Kazuichi Soda", "Fuyuhiko Kuzuryu", "Peko Pekoyama", "Akane Owari",
            "Nekomaru Nidai", "Teruteru Hanamura", "Mahiru Koizumi", "Hiyoko Saionji",
            "Ibuki Mioda", "Mikan Tsumiki", "Ultimate Imposter",
        ]

    @staticmethod
    def dr2_investigation_locations() -> List[str]:
        return [
            "Hotel Lobby", "Restaurant", "Beach", "Rocketpunch Market", "Airport",
            "Library", "Beach House", "Music Venue", "Electric Avenue",
            "Movie Theater", "Hospital", "Funhouse", "Nezumi Castle", "Motel",
        ]

    @staticmethod
    def dr2_locations() -> List[str]:
        return [
            "Central Island", "First Island", "Second Island", "Third Island",
            "Fourth Island", "Fifth Island", "Hotel Mirai", "Restaurant", "Beach",
            "Rocketpunch Market", "Airport", "Library", "Beach House", "Music Venue",
            "Electric Avenue", "Movie Theater", "Hospital", "Nezumi Castle",
        ]

    @staticmethod
    def dr2_trial_mechanics() -> List[str]:
        return [
            "Nonstop Debate", "Improved Hangman's Gambit", "Rebuttal Showdown",
            "Logic Dive", "Panic Talk Action",
        ]

    @staticmethod
    def dr2_skills() -> List[str]:
        return [
            "Absorb", "Armor Piercing", "Astute Influence", "Awakening",
            "Cheat Code", "Detection", "Fast Focus", "Flashlight",
            "Fortress Defense", "Hard Blade", "Ideal Bullet",
            "Knowing Focus", "Max Volume", "Optimist", "Silver Tongue",
        ]

    DR2_PRESENTS = [
        "Mineral Water", "Ramune", "Coconut Juice", "Blue Ram", "Civet Coffee",
        "Cinnamon Tea", "Non-Alcoholic Wine", "Prepackaged Orzotto",
        "Chocolate Chip Jerky", "Cod Roe Baguette", "Gugelhupf Cake",
        "Hardtack of Hope", "Sweet Bun Bag", "Potato Chips", "Viva Ice",
        "Jabba's Natural Salt", "Cocoshimi", "Sunflower Seeds", "Coconut",
        "Iroha T-Shirt", "Brightly Colored Jeans", "Apron Dress", "Falkor's Muffler",
        "Fresh Bindings", "Queen's Straitjacket", "Spy Spike", "Secret Boots",
        "Safety Half-Shoes", "Passionate Glasses", "Bvlbari's Gold",
        "Earring of Crushed Evil", "Silver Ring", "Hope's Peak Ring", "Spectre Ring",
        "Cloth Wrap Backpack", "Another Hope", "Jabbaian Jewelry", "Biggest Fantom",
        "Ubiquitous Handbook", "Millennium Prize Problems", "Tips & Tips 2nd Edition",
        "Ogami Clan Codex", "Men's Manma", "Kiss Note", "Black Rabbit Picture Book",
        "2.5D Headphones", "Radiosonde", "Male Cylinder", "Measuring Flask",
        "Razor Ramon HG", "Infrared Thermometer", "Flash Suppressor",
        "Lilienthal's Wings", "Kirlian Photography", "Mr. Stapler",
        "Small Degenerated Reactor", "Many-Sided Dice Set", "The Funbox",
        "The Funplane", "American Clacker", "Power Gauntlet", "Mesopotamia",
        "Nitro Racer", "Slap Bracelet", "Gag Ball", "Kokeshi Dynamo", "Go Stone",
        "Message In a Bottle", "Old Timey Radio", "Antique Doll", "The Second Button",
        "Moon Rock", "Another Battle", "Desperation", "1000 Cherry Blossoms",
        "Paper '10th Act Verse'", "Marine Snow", "Gold Coated Sheath",
        "Mini Wave-Dissipaters", "Stardust", "Japanese Tea Cup", "Two-Sided Ukulele",
        "Collapsible Fishing Rod", "Bojobo Dolls", "Century Potpourri",
        "Absolute Tuning Fork", "Seven Sword", "Sand God's Storm Horn",
        "Memory Notebook", "Mukuro's Knife", "Broken Warhead",
        "Girl with the Bear Hairpin", "Bar", "Dip Pen", "Tissue", "Jabba the Frog",
        "Iguana Daughter", "Dull Kitchen Knife", "Occult Photo Frame",
        "Lust Setsugekka", "Rose In Vitro", "Skullhead Mask", "Compact Costume",
        "Angel's Fruit", "Bandage Wrap", "Secret Wind Sword Book",
        "Hagakure Crystal Ball", "Used Carrot",
        "Toy Camera", "Replica Sword", "An An Aan", "Man's Nut",
        "Summer Festival Tree", "R/C 4WD Battler Taro", "Wooden Stick",
        "Usami Strap", "Danganronpa IF",
    ]

    DR2_UNDERWEAR = [
        "Nagito's Undergarments", "Byakuya's Undergarments", "Gundham's Undergarments",
        "Kazuichi's Undergarments", "Teruteru's Undergarments",
        "Nekomaru's Undergarments", "Fuyuhiko's Undergarments", "Akane's Undergarments",
        "Chiaki's Undergarments", "Sonia's Undergarments", "Hiyoko's Undergarments",
        "Mahiru's Undergarments", "Mikan's Undergarments", "Ibuki's Undergarments",
        "Peko's Undergarments",
    ]

    def dr2_presents(self) -> List[str]:
        presents = list(self.DR2_PRESENTS)
        if self.include_underwear_presents:
            presents.extend(self.DR2_UNDERWEAR)
        return presents

    # ==================== V3 data pools ====================

    @staticmethod
    def v3_students() -> List[str]:
        return [
            "Shuichi Saihara", "Kaede Akamatsu", "Kaito Momota", "Maki Harukawa",
            "Rantaro Amami", "Ryoma Hoshi", "Kirumi Tojo", "Angie Yonaga",
            "Tenko Chabashira", "Himiko Yumeno", "Korekiyo Shinguji", "Miu Iruma",
            "Gonta Gokuhara", "Kokichi Oma", "K1-B0", "Tsumugi Shirogane",
        ]

    @staticmethod
    def v3_investigation_locations() -> List[str]:
        return [
            "Classroom", "Dormitory", "Dining Hall", "Library", "Gymnasium",
            "Casino", "Game Room", "Courtyard", "Warehouse", "Pool",
            "Shrine of Judgment", "Ultimate Lab", "Exisal Hangar", "Virtual World",
        ]

    @staticmethod
    def v3_locations() -> List[str]:
        return [
            "Ultimate Academy", "Dormitory", "Dining Hall", "Library", "Gymnasium",
            "Casino", "Game Room", "Courtyard", "Shrine of Judgment", "Love Suite",
            "Exisal Hangar", "Pool", "Death Road Entrance", "Virtual World",
        ]

    @staticmethod
    def v3_trial_mechanics() -> List[str]:
        return [
            "Nonstop Debate", "Mass Panic Debate", "Debate Scrum",
            "Hangman's Gambit V3", "Psyche Taxi", "Mind Mine",
            "Argument Armament", "Rebuttal Showdown",
        ]

    @staticmethod
    def v3_skills() -> List[str]:
        return [
            "Adrenaline Boost", "Attentiveness", "Calming Concentrate",
            "Clockwork Precision", "Cool Down", "Cram Session", "Diamond Armor",
            "Extreme Focus", "First Strike", "Head Start", "Iron Clad",
            "Mechanical Focus", "Pep Talk", "Reversal", "Sniper Scope",
            "Tactical Move",
        ]

    V3_PRESENTS = [
        "Oolong Tea", "Boba Tea", "Ginger Tea", "Cleopatra's Pearl Cocktail",
        "Non-Alcoholic Drink of Immortality", "Ketchup", "Sugar", "Olive Oil",
        "Astro Cake", "Bubble Gum Bomb", "Maple Fudge", "Greek Yogurt",
        "Bunny Apples", "Rock Hard Ice Cream", "Sukiyaki Caramel", "Candy Cigarette",
        "Gyoza In the Shape of a Face", "Silver Earring", "Crystal Bangle",
        "Striped Necktie", "Bondage Boots", "Ultimate Academy Bracelet",
        "Workout Clothes", "Mono-Jinbei", "Autumn-Colored Scarf", "Hand-Knit Sweater",
        "Cheer Coat Uniform", "Nail Brush", "Wearable Blanket", "Beret",
        "Ladybug Brooch", "Cufflinks", "Dog Tag", "White Robot Mustache",
        "Book of the Blackened", "Feelings of Ham", "Travel Journal",
        "Dreams Come True Spell Book", "Story of Tokono", "Spla-Teen Vogue",
        "Fun Book of Animals", "Latest Machine Parts Catalogue", "Stainless Tray",
        "Tennis Ball Set", "High-End Headphones", "Teddy Bear", "Milk Puzzle",
        "Illusion Rod", "Hand Mirror", "Prop Carrying Case", "Japanese Doll Wig",
        "Photoshop Software", "Sewing Kit", "Flame Thunder", "Tattered Music Score",
        "Indigo Hakama", "Fashionable Glasses", "Gold Origami",
        "Plastic Moon Buggy Model", "I'm a Picture Book Artist!", "Hand Grips",
        "Commemorative Medal Set", "Metronome", "Sketchbook", "Art Manikin",
        "Bird Food", "Proxilingual Device", "Gourd Insect Trap", "Potted Banyan Tree",
        "Pocket Tissue", "Dancing Haniwa", "Work Chair Of Doom", "3-Hit KO Sandbag",
        "Sports Towel", "Steel Glasses Case", "Robot Oil",
        "Clock-Shaped Gaming Console", "Everywhere Parasol", "Three-Layered Lunch Box",
        "Aluminum Water Bottle", "Jelly Balls", "Upbeat Humidifier", "Earnest Compass",
        "Semazen Doll", "Weathercock of Barcelous", "Pillow of Admiration",
        "46 Moves of the Killing Game", "Monkey's Paw", "Art Piece of Spring",
        "Electric Tempest", "Space Egg", "Super Lucky Button", "Sparkly Sheet",
        "Hammock", "Cleansing Air Freshener", "Flower for Floromancy",
        "Variety Cushion", "Key of Love", "To Each Their Own Roulette", "Monomune",
        "Gun of Man's Passion", "Pure-White Practice Sword", "Dark Belt",
    ]

    V3_UNDERWEAR = [
        "Kaito's Undergarments", "Ryoma's Undergarments", "Rantaro's Undergarments",
        "Gonta's Undergarments", "Kokichi's Undergarments", "Korekiyo's Undergarments",
        "K1-B0's Built-In Parts", "Kirumi's Undergarments", "Himiko's Undergarments",
        "Maki's Undergarments", "Tenko's Undergarments", "Tsumugi's Undergarments",
        "Angie's Undergarments", "Miu's Undergarments", "Kaede's Undergarments",
    ]

    def v3_presents(self) -> List[str]:
        presents = list(self.V3_PRESENTS)
        if self.include_underwear_presents:
            presents.extend(self.V3_UNDERWEAR)
        return presents

    # ==================== Bonus mode pools ====================

    @staticmethod
    def all_school_mode_remaining_days() -> List[int]:
        return [1, 3, 5, 10]

    @staticmethod
    def all_school_mode_streak_days() -> List[int]:
        return [3, 5, 10]

    @staticmethod
    def all_island_mode_days() -> List[int]:
        return [10, 20, 30]

    @staticmethod
    def all_monomi_chapters() -> List[int]:
        return [1, 2, 3, 4, 5]

    @staticmethod
    def all_casino_coin_quantities() -> List[int]:
        return [100, 500, 1000]

    # ==================== DRS data pools ====================

    @staticmethod
    def all_development_turn_counts() -> List[int]:
        return [5, 10, 20, 30, 50]

    @staticmethod
    def all_development_levels() -> List[int]:
        return [20, 50, 99]

    @staticmethod
    def all_tower_floors() -> List[int]:
        return [10, 30, 50, 100, 150, 200]

    @staticmethod
    def all_summer_camp_characters() -> List[str]:
        return [
            # DR1
            "Makoto Naegi", "Kyoko Kirigiri", "Byakuya Togami", "Toko Fukawa",
            "Aoi Asahina", "Yasuhiro Hagakure", "Kiyotaka Ishimaru", "Mondo Owada",
            "Chihiro Fujisaki", "Leon Kuwata", "Sakura Ogami", "Hifumi Yamada",
            "Celestia Ludenberg", "Sayaka Maizono", "Junko Enoshima", "Mukuro Ikusaba",
            # DR2
            "Hajime Hinata", "Nagito Komaeda", "Chiaki Nanami", "Sonia Nevermind",
            "Gundham Tanaka", "Kazuichi Soda", "Fuyuhiko Kuzuryu", "Peko Pekoyama",
            "Akane Owari", "Nekomaru Nidai", "Teruteru Hanamura", "Mahiru Koizumi",
            "Hiyoko Saionji", "Ibuki Mioda", "Mikan Tsumiki", "Ultimate Imposter",
            # V3
            "Shuichi Saihara", "Kaede Akamatsu", "Kaito Momota", "Maki Harukawa",
            "Rantaro Amami", "Ryoma Hoshi", "Kirumi Tojo", "Angie Yonaga",
            "Tenko Chabashira", "Himiko Yumeno", "Korekiyo Shinguji", "Miu Iruma",
            "Gonta Gokuhara", "Kokichi Oma", "K1-B0", "Tsumugi Shirogane",
            # Mascots
            "Monokuma", "Usami",
        ]

    @staticmethod
    def all_swimsuit_characters() -> List[str]:
        return [
            # DR1
            "Makoto Naegi", "Kyoko Kirigiri", "Byakuya Togami", "Toko Fukawa",
            "Aoi Asahina", "Sayaka Maizono", "Celestia Ludenberg", "Junko Enoshima",
            "Mukuro Ikusaba",
            # DR2
            "Hajime Hinata", "Nagito Komaeda", "Chiaki Nanami", "Sonia Nevermind",
            "Ibuki Mioda", "Hiyoko Saionji", "Mahiru Koizumi", "Akane Owari",
            "Mikan Tsumiki", "Peko Pekoyama",
            # V3
            "Kaede Akamatsu", "Shuichi Saihara", "Maki Harukawa", "Kaito Momota",
            "Kokichi Oma", "Miu Iruma", "Angie Yonaga", "Tenko Chabashira",
            "Himiko Yumeno", "Tsumugi Shirogane",
        ]

    @staticmethod
    def all_summer_camp_bosses() -> List[str]:
        return [
            "Monobeast (First Island)", "Monobeast (Second Island)",
            "Monobeast (Third Island)", "Monobeast (Fourth Island)",
            "Monobeast (Fifth Island)",
        ]

    # ==================== Property accessors ====================

    @property
    def games_owned(self) -> List[str]:
        return sorted(list(self.archipelago_options.danganronpa_owned_games.value))

    @property
    def enable_story_mode(self) -> bool:
        return self.archipelago_options.danganronpa_enable_story_mode.value

    @property
    def enable_bonus_modes(self) -> bool:
        return self.archipelago_options.danganronpa_enable_bonus_modes.value

    @property
    def include_investigation(self) -> bool:
        return self.archipelago_options.danganronpa_include_investigation.value

    @property
    def include_class_trial(self) -> bool:
        return self.archipelago_options.danganronpa_include_class_trial.value

    @property
    def include_free_time(self) -> bool:
        return self.archipelago_options.danganronpa_include_free_time.value

    @property
    def include_report_card(self) -> bool:
        return self.archipelago_options.danganronpa_include_report_card.value

    @property
    def include_skills(self) -> bool:
        return self.archipelago_options.danganronpa_include_skills.value

    @property
    def include_presents(self) -> bool:
        return self.archipelago_options.danganronpa_include_presents.value

    @property
    def include_underwear_presents(self) -> bool:
        return self.archipelago_options.danganronpa_include_underwear_presents.value

    @property
    def include_school_mode(self) -> bool:
        return self.archipelago_options.danganronpa_include_school_mode.value

    @property
    def include_island_mode(self) -> bool:
        return self.archipelago_options.danganronpa_include_island_mode.value

    @property
    def include_collectibles(self) -> bool:
        return self.archipelago_options.danganronpa_include_collectibles.value

    @property
    def include_summer_camp(self) -> bool:
        return self.archipelago_options.danganronpa_include_summer_camp.value

    @property
    def logic_difficulty(self) -> str:
        return self.archipelago_options.danganronpa_logic_difficulty.value

    @property
    def action_difficulty(self) -> str:
        return self.archipelago_options.danganronpa_action_difficulty.value


# ==================== Option Classes ====================

class DanganronpaOwnedGames(OptionSet):
    """Select which Danganronpa games you own."""
    display_name = "Danganronpa Owned Games"
    valid_keys = [
        "Danganronpa: Trigger Happy Havoc",
        "Danganronpa 2: Goodbye Despair",
        "Danganronpa V3: Killing Harmony",
        "Danganronpa S: Ultimate Summer Camp",
    ]
    default = valid_keys


class DanganronpaEnableStoryMode(DefaultOnToggle):
    """Enable main story mode objectives."""
    display_name = "Danganronpa Enable Story Mode Objectives"


class DanganronpaEnableBonusModes(DefaultOnToggle):
    """Enable bonus mode objectives (School Mode, Island Mode, etc.)."""
    display_name = "Danganronpa Enable Bonus Mode Objectives"


class DanganronpaIncludeInvestigation(DefaultOnToggle):
    """Include investigation objectives."""
    display_name = "Danganronpa Include Investigation Objectives"


class DanganronpaIncludeClassTrial(DefaultOnToggle):
    """Include class trial objectives."""
    display_name = "Danganronpa Include Class Trial Objectives"


class DanganronpaIncludeFreeTime(DefaultOnToggle):
    """Include free time objectives."""
    display_name = "Danganronpa Include Free Time Objectives"


class DanganronpaIncludeReportCard(DefaultOnToggle):
    """Include report card objectives."""
    display_name = "Danganronpa Include Report Card Objectives"


class DanganronpaIncludeSkills(DefaultOnToggle):
    """Include skill objectives."""
    display_name = "Danganronpa Include Skill Objectives"


class DanganronpaIncludePresents(DefaultOnToggle):
    """Include present objectives."""
    display_name = "Danganronpa Include Present Objectives"


class DanganronpaIncludeUnderwearPresents(DefaultOnToggle):
    """Include underwear presents in the present pool."""
    display_name = "Danganronpa Include Underwear Presents"


class DanganronpaIncludeSchoolMode(DefaultOnToggle):
    """Include School Mode objectives (DR1)."""
    display_name = "Danganronpa Include School Mode Objectives"


class DanganronpaIncludeIslandMode(DefaultOnToggle):
    """Include Island Mode objectives (DR2)."""
    display_name = "Danganronpa Include Island Mode Objectives"


class DanganronpaIncludeCollectibles(DefaultOnToggle):
    """Include collectible objectives."""
    display_name = "Danganronpa Include Collectibles Objectives"


class DanganronpaIncludeSummerCamp(DefaultOnToggle):
    """Include Danganronpa S: Ultimate Summer Camp objectives (Development Mode, Tower of Despair)."""
    display_name = "Danganronpa Include Summer Camp Objectives"


class DanganronpaLogicDifficulty(TextChoice):
    """Difficulty level for logic-based objectives."""
    display_name = "Danganronpa Logic Difficulty"
    option_gentle = 0
    option_kind = 1
    option_mean = 2
    option_cruel = 3
    default = 1


class DanganronpaActionDifficulty(TextChoice):
    """Difficulty level for action-based objectives."""
    display_name = "Danganronpa Action Difficulty"
    option_gentle = 0
    option_kind = 1
    option_mean = 2
    option_cruel = 3
    default = 1
