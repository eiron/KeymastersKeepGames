from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class OneStepFromEdenArchipelagoOptions:
    osfe_allowed_characters: OneStepFromEdenAllowedCharacters
    osfe_include_boss_objectives: OneStepFromEdenIncludeBossObjectives
    osfe_include_pacifist_objectives: OneStepFromEdenIncludePacifistObjectives
    osfe_include_flawless_objectives: OneStepFromEdenIncludeFlawlessObjectives


class OneStepFromEdenGame(Game):
    name = "One Step From Eden"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [KeymastersKeepGamePlatforms.SW]

    is_adult_only_or_unrated = False

    options_cls = OneStepFromEdenArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(label="Win a run without equipping any artifacts", data={}),
            GameObjectiveTemplate(label="Win a run without removing any spells", data={}),
            GameObjectiveTemplate(label="Win a run without taking any mana upgrades", data={}),
            GameObjectiveTemplate(label="Win a run while keeping your starter loadout", data={}),
            GameObjectiveTemplate(label="Win a run without visiting shops", data={}),
            GameObjectiveTemplate(label="Win a run without buying any upgrades from shops", data={}),
            GameObjectiveTemplate(label="Win a run without buying spell removes from shops", data={}),
            GameObjectiveTemplate(label="Win a run while skipping all treasure room artifacts", data={}),
            GameObjectiveTemplate(label="Win a run while picking every self-damaging spell offered", data={}),
            GameObjectiveTemplate(label="Win a run using only spells of 2 cost or less", data={}),
            GameObjectiveTemplate(label="Win a run with 5 or fewer spells in your deck", data={}),
            GameObjectiveTemplate(label="Win a run after rescuing every NPC you find", data={}),
            GameObjectiveTemplate(label="Win a run after removing every starter spell", data={}),
            GameObjectiveTemplate(label="Win a run without picking up any Legendary or Calamity spells", data={}),
            GameObjectiveTemplate(label="Win a run after upgrading a single spell at least 4 times", data={}),
            GameObjectiveTemplate(label="Win a run without upgrading any spell more than once", data={}),
            GameObjectiveTemplate(label="Win a run after defeating every boss you encounter", data={}),
            GameObjectiveTemplate(label="Route through every miniboss you see and win", data={}),
            GameObjectiveTemplate(label="Enter every Hazard room you see and win", data={}),
            GameObjectiveTemplate(label="Kill 5 bunnies (visit at least 5 campfires) and win the run", data={}),
            GameObjectiveTemplate(label="On floor 1, pick the path with the most combat rooms", data={}),
            GameObjectiveTemplate(label="Pacifist every world except bosses and still win", data={}),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = []
        objectives += self.base_objectives()

        if self.include_boss_objectives:
            objectives += self.boss_objectives()

        if self.include_pacifist_objectives:
            objectives += self.pacifist_objectives()

        if self.include_flawless_objectives:
            objectives += self.flawless_objectives()

        return objectives

    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Reach Eden on ROUTE with CHARACTER",
                data={
                    "ROUTE": (self.routes, 1),
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Win a run on ROUTE using DECK as CHARACTER",
                data={
                    "ROUTE": (self.routes, 1),
                    "DECK": (self.decks, 1),
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Win a run after saving NPC_COUNT NPCs as CHARACTER",
                data={
                    "NPC_COUNT": (self.npc_targets, 1),
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Complete a no-upgrade run on ROUTE as CHARACTER",
                data={
                    "ROUTE": (self.routes, 1),
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=9,
            ),
            GameObjectiveTemplate(
                label="Win with 4 or more Flow stacks active as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win with at least 2 Trinity spells in deck as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a run without casting any Jam spells as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
        ]

    def boss_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Defeat BOSS_NAME on EDEN_RANK as CHARACTER",
                data={
                    "BOSS_NAME": (self.boss_names, 1),
                    "EDEN_RANK": (self.eden_ranks, 1),
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=9,
            ),
            GameObjectiveTemplate(
                label="Defeat Seraph on EDEN_RANK without removing spells as CHARACTER",
                data={
                    "EDEN_RANK": (self.eden_ranks, 1),
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Defeat Shopkeeper as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS_NAME using only CHARACTER's basic attack",
                data={
                    "BOSS_NAME": (self.boss_names, 1),
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=6,
            ),
        ]

    def pacifist_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Reach Eden on Pacifist as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Reach Eden on Pacifist without breaking any crystals as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Finish a Pacifist run with 9 or more Mercy as CHARACTER",
                data={
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
        ]

    def flawless_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Flawless BOSS_NAME on EDEN_RANK as CHARACTER",
                data={
                    "BOSS_NAME": (self.flawless_boss_names, 1),
                    "EDEN_RANK": (self.eden_ranks, 1),
                    "CHARACTER": (self.available_characters, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
        ]

    @property
    def include_boss_objectives(self) -> bool:
        return self.archipelago_options.osfe_include_boss_objectives.value

    @property
    def include_pacifist_objectives(self) -> bool:
        return self.archipelago_options.osfe_include_pacifist_objectives.value

    @property
    def include_flawless_objectives(self) -> bool:
        return self.archipelago_options.osfe_include_flawless_objectives.value

    def available_characters(self) -> List[str]:
        allowed = getattr(self.archipelago_options.osfe_allowed_characters, "value", [])
        return allowed if allowed else OneStepFromEdenAllowedCharacters.valid_keys

    @staticmethod
    def routes() -> List[str]:
        # Routes per wiki (including subroutes)
        return [
            "Neutral",
            "Pacifist",
            "True Pacifist",
            "False Pacifist",
            "Genocide",
        ]

    @staticmethod
    def decks() -> List[str]:
        # Wiki-recognized archetype decks
        return [
            "Kunai",
            "Jam",
            "Poison",
            "Flame",
            "Flow",
            "Trinity",
            "Frost",
            "Viruspell",
            "Spell Power",
            "Switchbait",
            "Big Shield",
            "Money",
            "Building Spam",
            "Kinesys Combo",
        ]

    @staticmethod
    def boss_names() -> List[str]:
        # Includes Eden bosses and regional bosses per wiki list
        return [
            "Seraph",      # Neutral final
            "Serif",       # Eden boss
            "Gate",        # Neutral boss
            "Terrable",    # Pacifist boss
            "Saffron",
            "Reva",
            "Selicy",
            "Gunner",
            "Terra",
            "Hazel",
            "Violette",
            "Shiso",
            "Shopkeeper",
        ]

    @staticmethod
    def flawless_boss_names() -> List[str]:
        # Full boss list usable for flawless objectives
        return OneStepFromEdenGame.boss_names()

    @staticmethod
    def eden_ranks() -> List[str]:
        return [str(rank) for rank in range(0, 16)]

    @staticmethod
    def npc_targets() -> List[str]:
        return [
            "3",
            "4",
            "5",
            "6",
        ]


# Archipelago Options
class OneStepFromEdenAllowedCharacters(OptionSet):
    """
    Limit which One Step From Eden characters can be selected for objectives.
    Leave empty to allow all characters.
    """

    display_name = "One Step From Eden: Allowed Characters"
    valid_keys = [
        "Saffron",
        "Reva",
        "Gunner",
        "Terra",
        "Selicy",
        "Hazel",
        "Violette",
        "Shiso",
        "Shopkeeper",
        "Chrono",
        "Orbo",
    ]
    default = valid_keys


class OneStepFromEdenIncludeBossObjectives(DefaultOnToggle):
    """
    Indicates whether to include boss-focused objectives such as Gate, Seraph, or shopkeeper clears.
    """

    display_name = "One Step From Eden: Include Boss Objectives"


class OneStepFromEdenIncludePacifistObjectives(DefaultOnToggle):
    """
    Indicates whether to include pacifist-route objectives.
    """

    display_name = "One Step From Eden: Include Pacifist Objectives"


class OneStepFromEdenIncludeFlawlessObjectives(DefaultOnToggle):
    """
    Indicates whether to include flawless (no damage) objectives.
    """

    display_name = "One Step From Eden: Include Flawless Objectives"
