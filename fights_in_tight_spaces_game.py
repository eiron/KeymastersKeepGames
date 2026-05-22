from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle, DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class FightsInTightSpacesArchipelagoOptions:
    fits_include_deck_objectives: FightsInTightSpacesIncludeDeckObjectives
    fits_include_chapter_objectives: FightsInTightSpacesIncludeChapterObjectives
    fits_include_combat_feat_objectives: FightsInTightSpacesIncludeCombatFeatObjectives
    fits_include_environmental_objectives: FightsInTightSpacesIncludeEnvironmentalObjectives
    fits_include_endless_mode_objectives: FightsInTightSpacesIncludeEndlessModeObjectives
    fits_include_dlc_weapon_of_choice: FightsInTightSpacesIncludeDlcWeaponOfChoice
    fits_include_dlc_k9_division: FightsInTightSpacesIncludeDlcK9Division


class FightsInTightSpacesGame(Game):
    name = "Fights in Tight Spaces"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = FightsInTightSpacesArchipelagoOptions

    # Properties
    @property
    def include_deck_objectives(self) -> bool:
        return self.archipelago_options.fits_include_deck_objectives.value

    @property
    def include_chapter_objectives(self) -> bool:
        return self.archipelago_options.fits_include_chapter_objectives.value

    @property
    def include_combat_feat_objectives(self) -> bool:
        return self.archipelago_options.fits_include_combat_feat_objectives.value

    @property
    def include_environmental_objectives(self) -> bool:
        return self.archipelago_options.fits_include_environmental_objectives.value

    @property
    def include_endless_mode_objectives(self) -> bool:
        return self.archipelago_options.fits_include_endless_mode_objectives.value

    @property
    def include_dlc_weapon_of_choice(self) -> bool:
        return self.archipelago_options.fits_include_dlc_weapon_of_choice.value

    @property
    def include_dlc_k9_division(self) -> bool:
        return self.archipelago_options.fits_include_dlc_k9_division.value

    # Constraints
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Do not use any Counter cards",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Do not use any Block/Defense cards",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Do not push enemies off ledges or through windows",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Do not upgrade any cards during the run",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Do not remove any cards from your deck during the run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Do not visit any shops",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Do not use any Movement cards (attack-embedded repositioning is allowed)",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Never let your Combo meter drop below COMBO_FLOOR after the first turn",
                data={"COMBO_FLOOR": (self.combo_thresholds, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Do not skip adding a card after any fight",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Never use more than CARD_LIMIT cards per turn",
                data={"CARD_LIMIT": (self.card_per_turn_limits, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Do not heal at any point during the run",
                data={},
                is_time_consuming=True,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Start from Chapter 1 with no checkpoint skips",
                data={},
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Only play cards that cost ENERGY_COST or less energy",
                data={"ENERGY_COST": (self.energy_cost_limits, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Do not visit more than one medical station during the run",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Always take the topmost (leftmost) path whenever possible",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Use your emergency move in the first EMERGENCY_FIGHTS fights after receiving it",
                data={"EMERGENCY_FIGHTS": (self.emergency_move_counts, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Use the Deck Draft instead of a fixed starter deck",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
        ]

    # Objectives
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        objectives += self.base_objectives()

        if self.include_deck_objectives:
            objectives += self.deck_objectives()

        if self.include_chapter_objectives:
            objectives += self.chapter_objectives()

        if self.include_combat_feat_objectives:
            objectives += self.combat_feat_objectives()

        if self.include_environmental_objectives:
            objectives += self.environmental_objectives()

        if self.include_endless_mode_objectives:
            objectives += self.endless_mode_objectives()

        return objectives

    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a full run (all 5 missions)",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Complete a run without ever falling below HEALTH_THRESHOLD HP",
                data={"HEALTH_THRESHOLD": (self.health_thresholds, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a run with a deck of DECK_SIZE or fewer cards",
                data={"DECK_SIZE": (self.small_deck_sizes, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a run with a deck of DECK_SIZE or more cards",
                data={"DECK_SIZE": (self.large_deck_sizes, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete all optional objectives in a single chapter",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a Daily Challenge",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
        ]

    def deck_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a run using the DECK starter deck",
                data={"DECK": (self.starter_decks, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Complete a run using a Custom Deck built around ARCHETYPE cards",
                data={"ARCHETYPE": (self.card_archetypes, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete a run using only ARCHETYPE and Movement cards",
                data={"ARCHETYPE": (self.card_archetypes, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a run without adding any ARCHETYPE cards to your deck",
                data={"ARCHETYPE": (self.card_archetypes, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a run where every card in your final deck is upgraded",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
        ]

    def chapter_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Clear CHAPTER using the DECK deck on MODE",
                data={
                    "CHAPTER": (self.chapters, 1),
                    "DECK": (self.starter_decks, 1),
                    "MODE": (self.difficulty_modes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Clear CHAPTER without taking any damage",
                data={"CHAPTER": (self.chapters, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Clear CHAPTER in TURN_COUNT or fewer total turns",
                data={
                    "CHAPTER": (self.chapters, 1),
                    "TURN_COUNT": (self.chapter_turn_limits, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat the boss of CHAPTER",
                data={"CHAPTER": (self.chapters, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Defeat the boss of CHAPTER without taking damage during the boss fight",
                data={"CHAPTER": (self.chapters, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete every fight in CHAPTER with at least one optional objective cleared",
                data={"CHAPTER": (self.chapters, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
        ]

    def combat_feat_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Reach a Combo of COMBO_COUNT or higher in a single fight",
                data={"COMBO_COUNT": (self.high_combo_counts, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Defeat ENEMY_COUNT enemies in a single turn",
                data={"ENEMY_COUNT": (self.enemies_per_turn, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a fight in TURN_COUNT or fewer turns",
                data={"TURN_COUNT": (self.fight_turn_limits, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a fight without playing any cards on one turn (bait and dodge only)",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a fight using only Counter cards for damage",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Block BLOCK_COUNT or more damage in a single fight",
                data={"BLOCK_COUNT": (self.block_thresholds, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat an enemy by knocking them into another enemy",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Cause enemies to damage each other FRIENDLY_FIRE_COUNT times in a single run",
                data={"FRIENDLY_FIRE_COUNT": (self.friendly_fire_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a fight taking exactly 0 damage",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Spend all your Momentum in a single turn",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete all optional objectives in at least OBJECTIVE_COUNT fights in a single run",
                data={"OBJECTIVE_COUNT": (self.objective_completion_counts, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Force an enemy with a gun to shoot another enemy at least FRIENDLY_FIRE_COUNT times in a single run",
                data={"FRIENDLY_FIRE_COUNT": (self.gun_friendly_fire_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Push at least LEDGE_KILL_COUNT enemies out of levels in a single run",
                data={"LEDGE_KILL_COUNT": (self.push_out_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Upgrade your maximum health at least HEALTH_UPGRADE_COUNT times in a single run",
                data={"HEALTH_UPGRADE_COUNT": (self.health_upgrade_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Visit at least EVENT_COUNT mystery events in a single run",
                data={"EVENT_COUNT": (self.event_visit_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Deal 50 or more damage in a single hit",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Deal 100 or more damage in a single attack",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a fight without playing any Attack cards",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a fight by throwing all enemies into the void",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Have £1,000 or more at any point during a run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a run without losing any Informants or Ambassadors",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a full run in under an hour",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
        ]

    def environmental_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Push LEDGE_KILL_COUNT enemies off ledges or through windows in a single run",
                data={"LEDGE_KILL_COUNT": (self.ledge_kill_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Slam WALL_SLAM_COUNT enemies into walls in a single fight",
                data={"WALL_SLAM_COUNT": (self.wall_slam_counts, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Push an enemy into another enemy's gunfire lane",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Block a reinforcement spawn point for BLOCK_TURNS consecutive turns",
                data={"BLOCK_TURNS": (self.spawn_block_turns, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a run with LEDGE_KILL_COUNT or more environmental kills total",
                data={"LEDGE_KILL_COUNT": (self.total_env_kills, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a fight without using any environmental kills",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
        ]

    def endless_mode_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Survive ENDLESS_WAVES waves in Endless Mode",
                data={"ENDLESS_WAVES": (self.endless_wave_counts, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Survive ENDLESS_WAVES waves in Endless Mode using the DECK starter deck",
                data={
                    "ENDLESS_WAVES": (self.endless_wave_counts, 1),
                    "DECK": (self.starter_decks, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach a Combo of COMBO_COUNT in Endless Mode",
                data={"COMBO_COUNT": (self.high_combo_counts, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
        ]

    # Data lists
    def starter_decks(self) -> List[str]:
        decks = [
            "Balanced",
            "Counter Striker",
            "Aggressive",
            "Slasher",
            "Grappler",
            "Trickster",
        ]
        if self.include_dlc_weapon_of_choice:
            decks.append("Gunslinger")
        if self.include_dlc_k9_division:
            decks.extend([
                "K-9 Handler",
                "K-9 Support",
            ])
        return decks

    @staticmethod
    def card_archetypes() -> List[str]:
        return [
            "Attack",
            "Counter",
            "Block",
            "Movement",
            "Combo",
            "Momentum",
        ]

    @staticmethod
    def chapters() -> List[str]:
        return [
            "Death's Head Biker Gang",
            "The Insiders",
            "Jade Staff",
            "iCompleti",
            "Renegade Agents",
        ]

    @staticmethod
    def health_thresholds() -> List[str]:
        return ["50", "60", "70", "80"]

    @staticmethod
    def small_deck_sizes() -> List[str]:
        return ["12", "15", "16"]

    @staticmethod
    def large_deck_sizes() -> List[str]:
        return ["25", "30", "40", "50"]

    @staticmethod
    def combo_thresholds() -> List[str]:
        return ["2", "3", "4"]

    @staticmethod
    def card_per_turn_limits() -> List[str]:
        return ["3", "4"]

    @staticmethod
    def energy_cost_limits() -> List[str]:
        return ["1", "2"]

    @staticmethod
    def high_combo_counts() -> List[str]:
        return ["8", "10", "12", "15", "20"]

    @staticmethod
    def enemies_per_turn() -> List[str]:
        return ["2", "3", "4"]

    @staticmethod
    def fight_turn_limits() -> List[str]:
        return ["2", "3", "4"]

    @staticmethod
    def block_thresholds() -> List[str]:
        return ["15", "20", "30"]

    @staticmethod
    def friendly_fire_counts() -> List[str]:
        return ["5", "8", "10"]

    @staticmethod
    def ledge_kill_counts() -> List[str]:
        return ["3", "5", "8"]

    @staticmethod
    def wall_slam_counts() -> List[str]:
        return ["2", "3", "4"]

    @staticmethod
    def spawn_block_turns() -> List[str]:
        return ["2", "3"]

    @staticmethod
    def total_env_kills() -> List[str]:
        return ["10", "15", "20"]

    @staticmethod
    def endless_wave_counts() -> List[str]:
        return ["10", "15", "20", "25"]

    @staticmethod
    def chapter_turn_limits() -> List[str]:
        return ["25", "30", "40"]

    @staticmethod
    def difficulty_modes() -> List[str]:
        return [
            "Suave",
            "Classic",
            "Secret Agent",
            "Purist",
        ]

    @staticmethod
    def emergency_move_counts() -> List[str]:
        return ["2", "3"]

    @staticmethod
    def objective_completion_counts() -> List[str]:
        return ["4", "6", "8"]

    @staticmethod
    def gun_friendly_fire_counts() -> List[str]:
        return ["3", "4", "6"]

    @staticmethod
    def push_out_counts() -> List[str]:
        return ["3", "5", "7"]

    @staticmethod
    def health_upgrade_counts() -> List[str]:
        return ["2", "3"]

    @staticmethod
    def event_visit_counts() -> List[str]:
        return ["2", "3", "4"]


# Archipelago Options
class FightsInTightSpacesIncludeDeckObjectives(DefaultOnToggle):
    """Include objectives that require completing runs with specific starter decks or card archetypes."""
    display_name = "Fights in Tight Spaces: Include Deck Objectives"


class FightsInTightSpacesIncludeChapterObjectives(DefaultOnToggle):
    """Include objectives focused on clearing specific chapters with conditions."""
    display_name = "Fights in Tight Spaces: Include Chapter Objectives"


class FightsInTightSpacesIncludeCombatFeatObjectives(DefaultOnToggle):
    """Include objectives for achieving specific combat feats (combos, kills per turn, etc.)."""
    display_name = "Fights in Tight Spaces: Include Combat Feat Objectives"


class FightsInTightSpacesIncludeEnvironmentalObjectives(DefaultOnToggle):
    """Include objectives involving environmental kills and positioning mechanics."""
    display_name = "Fights in Tight Spaces: Include Environmental Objectives"


class FightsInTightSpacesIncludeEndlessModeObjectives(Toggle):
    """Include objectives for Endless Mode survival challenges."""
    display_name = "Fights in Tight Spaces: Include Endless Mode Objectives"


class FightsInTightSpacesIncludeDlcWeaponOfChoice(Toggle):
    """Include the Gunslinger starter deck from the Weapon of Choice DLC."""
    display_name = "Fights in Tight Spaces: Include DLC - Weapon of Choice"


class FightsInTightSpacesIncludeDlcK9Division(Toggle):
    """Include the K-9 Handler and K-9 Support starter decks from the K-9 Division DLC."""
    display_name = "Fights in Tight Spaces: Include DLC - K-9 Division"
