from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, Toggle, TextChoice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class IntoTheBreachArchipelagoOptions:
    itb_include_squad_objectives: IntoTheBreachIncludeSquadObjectives
    itb_include_pilot_objectives: IntoTheBreachIncludePilotObjectives
    itb_include_island_objectives: IntoTheBreachIncludeIslandObjectives
    itb_include_achievement_objectives: IntoTheBreachIncludeAchievementObjectives
    itb_include_difficulty_objectives: IntoTheBreachIncludeDifficultyObjectives
    itb_include_advanced_edition_objectives: IntoTheBreachIncludeAdvancedEditionObjectives
    itb_difficulty_preference: IntoTheBreachDifficultyPreference


class IntoTheBreachGame(Game):
    name = "Into the Breach"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = IntoTheBreachArchipelagoOptions

    # Properties
    @property
    def include_squad_objectives(self) -> bool:
        return self.archipelago_options.itb_include_squad_objectives.value

    @property
    def include_pilot_objectives(self) -> bool:
        return self.archipelago_options.itb_include_pilot_objectives.value

    @property
    def include_island_objectives(self) -> bool:
        return self.archipelago_options.itb_include_island_objectives.value

    @property
    def include_achievement_objectives(self) -> bool:
        return self.archipelago_options.itb_include_achievement_objectives.value

    @property
    def include_difficulty_objectives(self) -> bool:
        return self.archipelago_options.itb_include_difficulty_objectives.value

    @property
    def include_advanced_edition_objectives(self) -> bool:
        return self.archipelago_options.itb_include_advanced_edition_objectives.value

    @property
    def difficulty_preference(self) -> str:
        return self.archipelago_options.itb_difficulty_preference.current_key

    # Optional constraints
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = [
            GameObjectiveTemplate(label="Do not reset/restart any missions", data={}),
            GameObjectiveTemplate(label="Do not repair mechs between missions", data={}),
            GameObjectiveTemplate(label="Do not use any Grid Defense upgrades", data={}),
            GameObjectiveTemplate(label="Do not collect Time Pods", data={}),
            GameObjectiveTemplate(label="Destroy every Time Pod", data={}),
            GameObjectiveTemplate(label="Never allow a building to be set on fire", data={}),
            GameObjectiveTemplate(label="Do not block Vek spawns using mechs", data={}),
            GameObjectiveTemplate(label="Complete each mission without using the Repair action", data={}),
            GameObjectiveTemplate(label="Do not use pilots with bonus abilities (use default pilots only)", data={}),
            GameObjectiveTemplate(
                label="On a successful run, finish exactly CORPORATE_COUNT corporate islands",
                data={"CORPORATE_COUNT": (self.corporate_island_counts, 1)},
            ),
        ]

        if self.difficulty_preference in ["hard", "unfair"]:
            constraints.extend([
                GameObjectiveTemplate(label="Complete this objective with no Grid damage taken", data={}),
                GameObjectiveTemplate(label="Complete this objective without losing any mech", data={}),
                GameObjectiveTemplate(label="Complete this objective without using any reactor cores", data={}),
            ])

        return constraints

    # Objectives
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Complete a mission with all mechs intact",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a mission with GRID_POWER grid power or more remaining",
                data={"GRID_POWER": (self.grid_power_thresholds, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Destroy VEK_COUNT Vek in a single mission",
                data={"VEK_COUNT": (self.vek_kill_counts, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Block exactly SPAWN_COUNT Vek spawns in a single mission",
                data={"SPAWN_COUNT": (self.spawn_block_counts, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete MISSION_COUNT consecutive missions without losing a mech",
                data={"MISSION_COUNT": (self.mission_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Block 10 Vek spawns across a full island",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish an island without taking mech damage (repairs allowed)",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Fully power at least 1 mech",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat an island without failing an objective",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="On a successful run, take exactly 2 mech damage in the first mission",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

        if self.include_squad_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win a run with SQUAD",
                    data={"SQUAD": (self.squads, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Complete ISLAND with SQUAD",
                    data={
                        "ISLAND": (self.islands, 1),
                        "SQUAD": (self.squads, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete two islands with SQUAD in different runs",
                    data={"SQUAD": (self.squads, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat the Boss Island with the Rift Walkers",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat the Boss Island with the Rusting Hulks",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat the Boss Island with the Zenith Guard",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat the Boss Island with the Blitzkrieg",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat the Boss Island with the Steel Judoka",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat the Boss Island with the Flame Behemoths",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat the Boss Island with the Frozen Titans",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat the Boss Island with the Random Squad (3 Chaotic Rolls)",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Defeat the Boss Island with the Random Squad (3 Balanced Rolls)",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        if self.include_pilot_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win a run with PILOT in your squad",
                    data={"PILOT": (self.pilots, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Reach PILOT_LEVEL with PILOT in a single run",
                    data={
                        "PILOT_LEVEL": (self.pilot_levels, 1),
                        "PILOT": (self.pilots, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        if self.include_island_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Liberate ISLAND",
                    data={"ISLAND": (self.islands, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Achieve a perfect island on ISLAND (no Grid damage)",
                    data={"ISLAND": (self.islands, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        if self.include_achievement_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win a mission without moving any mech (if possible)",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Kill two Vek with a single attack",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Finish a mission with no Grid damage and all mechs intact",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete a mission without using any weapons (push/repair only)",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        if self.include_difficulty_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win a run on DIFFICULTY",
                    data={"DIFFICULTY": (self.difficulty_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a run on DIFFICULTY with SQUAD",
                    data={
                        "DIFFICULTY": (self.difficulty_levels, 1),
                        "SQUAD": (self.squads, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
            ])

        if self.include_advanced_edition_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete a mission with a tank/turret ally alive",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Win a run while using any Advanced Edition squad",
                    data={"SQUAD": (self.advanced_edition_squads, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
            ])

        return templates

    # Data lists
    @staticmethod
    def squads() -> List[str]:
        return [
            "Rift Walkers",
            "Rusting Hulks",
            "Zenith Guard",
            "Blitzkrieg",
            "Steel Judoka",
            "Flame Behemoths",
            "Frozen Titans",
            "Hazardous Mechs",
            "Bombermechs",
            "Arachnophiles",
            "Mist Eaters",
            "Cataclysm",
            "Heat Sinkers",
            "Custom Squad",
            "Secret Squad",
        ]

    @staticmethod
    def advanced_edition_squads() -> List[str]:
        return [
            "Bombermechs",
            "Arachnophiles",
            "Mist Eaters",
            "Cataclysm",
            "Heat Sinkers",
        ]

    @staticmethod
    def pilots() -> List[str]:
        return [
            "Archimedes",
            "Bethany Jones",
            "Camila Vera",
            "Chen Rong",
            "Gana",
            "Harold Schmidt",
            "Kai Miller",
            "KazaaakplethKilik",
            "Lily Reed",
            "Maia",
            "Morgan Lejeune",
            "Ralph Karlsson",
            "Silica",
        ]

    @staticmethod
    def islands() -> List[str]:
        return [
            "Archive Inc.",
            "Detritus Corporation",
            "Pinnacle Robotics",
            "R.S.T. Corporation",
        ]

    @staticmethod
    def difficulty_levels() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
            "Unfair",
        ]

    @staticmethod
    def grid_power_thresholds() -> List[str]:
        return ["4", "5", "6", "7"]

    @staticmethod
    def vek_kill_counts() -> List[str]:
        return ["4", "5", "6", "7"]

    @staticmethod
    def spawn_block_counts() -> List[str]:
        return ["2", "3", "4"]

    @staticmethod
    def mission_counts() -> List[str]:
        return ["2", "3"]

    @staticmethod
    def pilot_levels() -> List[str]:
        return ["2", "3"]

    @staticmethod
    def corporate_island_counts() -> List[str]:
        return ["2", "4"]


# Archipelago Options
class IntoTheBreachIncludeSquadObjectives(DefaultOnToggle):
    """Include squad-based objectives (wins, island clears)."""
    display_name = "Into the Breach Include Squad Objectives"


class IntoTheBreachIncludePilotObjectives(DefaultOnToggle):
    """Include pilot-focused objectives (wins, levels)."""
    display_name = "Into the Breach Include Pilot Objectives"


class IntoTheBreachIncludeIslandObjectives(DefaultOnToggle):
    """Include island progression objectives."""
    display_name = "Into the Breach Include Island Objectives"


class IntoTheBreachIncludeAchievementObjectives(DefaultOnToggle):
    """Include achievement-style objectives."""
    display_name = "Into the Breach Include Achievement Objectives"


class IntoTheBreachIncludeDifficultyObjectives(Toggle):
    """Include difficulty-specific objectives (Hard/Unfair)."""
    display_name = "Into the Breach Include Difficulty Objectives"


class IntoTheBreachIncludeAdvancedEditionObjectives(Toggle):
    """Include Advanced Edition objectives and squads."""
    display_name = "Into the Breach Include Advanced Edition Objectives"


class IntoTheBreachDifficultyPreference(TextChoice):
    """Sets difficulty preference for optional constraints."""
    display_name = "Into the Breach Difficulty Preference"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_unfair = 3
    default = 1
