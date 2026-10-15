from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, TextChoice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class HadesArchipelagoOptions:
    hades_include_escape_attempts: HadesIncludeEscapeAttempts
    hades_include_run_challenges: HadesIncludeRunChallenges
    hades_difficulty_level: HadesDifficultyLevel


class HadesGame(Game):
    name = "Hades"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = HadesArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        if self.difficulty_level in ["hard", "extreme"]:
            constraints.extend([
                GameObjectiveTemplate(
                    label="Complete this objective using only ASPECT weapon aspect",
                    data={"ASPECT": (self.weapon_aspects, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Complete this objective without using BOON_TYPE boons",
                    data={"BOON_TYPE": (self.boon_types, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
            ])
        
        if self.difficulty_level == "extreme":
            constraints.extend([
                GameObjectiveTemplate(
                    label="Complete this objective with at least HEAT heat",
                    data={"HEAT": (self.high_heat_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Complete this objective without dying more than DEATH_COUNT times",
                    data={"DEATH_COUNT": (self.low_death_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
            ])
        
        constraints.extend([
            GameObjectiveTemplate(label="Don't change Keepsakes midrun", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Purge at least 1 Boon each region", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Do not pick up Poms unless forced to", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Start the run with at least 5 levels of Heat", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Do not buy anything from at least one shop", data={}, is_time_consuming=False, is_difficult=False),
            GameObjectiveTemplate(label="Completely invert your current mirror (left to right)", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Have at least 1000 Obols at any point", data={}, is_time_consuming=False, is_difficult=False),
            GameObjectiveTemplate(label="Have at least 300 Max HP at any point", data={}, is_time_consuming=False, is_difficult=False),
            GameObjectiveTemplate(label="Go through exactly two Chaos gates, if possible", data={}, is_time_consuming=False, is_difficult=False),
            GameObjectiveTemplate(label="End with all Death Defiances", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Finish the run in less than 25 minutes (according to the in game timer)", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Start the run with the Cosmic Egg", data={}, is_time_consuming=False, is_difficult=False),
            GameObjectiveTemplate(label="Complete without taking any Legendary or Duo boons", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Never use Fated Persuasion to reroll a Boon", data={}, is_time_consuming=False, is_difficult=False),
            GameObjectiveTemplate(label="Complete with boons from at least GOD_COUNT different gods", data={"GOD_COUNT": (self.god_counts, 1)}, is_time_consuming=False, is_difficult=False),
            GameObjectiveTemplate(label="Don't use Call or Greater Call during boss fights", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Complete with only Common and Rare boons (no Epic or Heroic)", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Purge at least 3 boons at Pools of Purging", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Have at least one boon at level 5 or higher", data={}, is_time_consuming=False, is_difficult=False),
            GameObjectiveTemplate(label="Complete without using any Daedalus Hammers", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Don't take damage in any mini-boss rooms", data={}, is_time_consuming=False, is_difficult=True),
            GameObjectiveTemplate(label="Complete with at least 10 different boons", data={}, is_time_consuming=False, is_difficult=False),
            GameObjectiveTemplate(label="Never enter a Erebus gate", data={}, is_time_consuming=False, is_difficult=False),
            GameObjectiveTemplate(label="Finish with at least 500 gold", data={}, is_time_consuming=False, is_difficult=False),
            GameObjectiveTemplate(label="Take damage from traps at least 5 times", data={}, is_time_consuming=False, is_difficult=True),
        ])
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Escape Attempts
        if self.include_escape_attempts:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete a successful escape using WEAPON",
                    data={"WEAPON": (self.weapons, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete a successful escape using ASPECT",
                    data={"ASPECT": (self.weapon_aspects, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Reach LOCATION in a single run",
                    data={"LOCATION": (self.locations, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete an escape with HEAT heat or higher",
                    data={"HEAT": (self.heat_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ])

            if self.difficulty_level in ["hard", "extreme"]:
                game_objective_templates.append(
                    GameObjectiveTemplate(
                        label="Defeat BOSS without taking damage",
                        data={"BOSS": (self.bosses, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    )
                )

        # Repeatable run challenges
        if self.include_run_challenges:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Purchase every item offered at Charon's shop in the Temple of Styx in a single visit",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Purchase every item offered at Charon's shop in a single visit",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Purchase every item offered at a Well of Charon in a single visit",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Reach the Temple of Styx with at least BOON_COUNT boons",
                    data={"BOON_COUNT": (self.midrun_boon_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Have boons from at least GOD_COUNT different Olympians in a single run",
                    data={"GOD_COUNT": (self.god_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Purge a Boon at a Pool of Purging",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_escape_attempts(self) -> bool:
        return self.archipelago_options.hades_include_escape_attempts.value

    @property
    def include_run_challenges(self) -> bool:
        return self.archipelago_options.hades_include_run_challenges.value

    @property
    def difficulty_level(self) -> str:
        option = self.archipelago_options.hades_difficulty_level
        return str(option.current_key).lower()

    # Data lists
    @staticmethod
    def weapons() -> List[str]:
        return [
            "Stygius", "Varatha", "Aegis", 
            "Coronacht", "Malphon", "Exagryph"
        ]

    @staticmethod
    def weapon_aspects() -> List[str]:
        return [
            "Aspect of Zagreus (Stygian Blade)", "Aspect of Nemesis (Stygian Blade)",
            "Aspect of Poseidon (Stygian Blade)",
            "Aspect of Zagreus (Heart-Seeking Bow)", "Aspect of Chiron (Heart-Seeking Bow)",
            "Aspect of Hera (Heart-Seeking Bow)",
            "Aspect of Zagreus (Shield of Chaos)", "Aspect of Chaos (Shield of Chaos)",
            "Aspect of Zeus (Shield of Chaos)",
            "Aspect of Zagreus (Eternal Spear)", "Aspect of Achilles (Eternal Spear)",
            "Aspect of Hades (Eternal Spear)",
            "Aspect of Zagreus (Twin Fists)", "Aspect of Talos (Twin Fists)",
            "Aspect of Demeter (Twin Fists)",
            "Aspect of Zagreus (Adamant Rail)", "Aspect of Eris (Adamant Rail)",
            "Aspect of Hestia (Adamant Rail)",
            "Aspect of Arthur (Stygian Blade)", "Aspect of Rama (Heart-Seeking Bow)",
            "Aspect of Beowulf (Shield of Chaos)", "Aspect of Guan Yu (Eternal Spear)",
            "Aspect of Gilgamesh (Twin Fists)", "Aspect of Lucifer (Adamant Rail)",
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Megaera", "Alecto", "Tisiphone", "Lernaean Bone Hydra", 
            "Theseus and Asterius (together)"
        ]

    @staticmethod
    def locations() -> List[str]:
        return ["Tartarus", "Asphodel", "Elysium", "Temple of Styx", "Greece"]

    @staticmethod
    def god_counts() -> range:
        return range(5, 9)

    @staticmethod
    def boon_types() -> List[str]:
        return [
            "Zeus", "Poseidon", "Athena", "Aphrodite", "Artemis", "Ares",
            "Dionysus", "Hermes", "Demeter", "Chaos"
        ]

    # Ranges
    @staticmethod
    def heat_levels() -> range:
        return range(2, 17, 2)

    @staticmethod
    def high_heat_levels() -> range:
        return range(10, 32, 5)

    @staticmethod
    def low_death_counts() -> range:
        return range(0, 5)

    @staticmethod
    def midrun_boon_counts() -> range:
        return range(8, 17, 4)


# Archipelago Options
class HadesIncludeEscapeAttempts(DefaultOnToggle):
    """Include escape attempt objectives (runs, bosses, heat)."""
    display_name = "Hades Include Escape Attempts"

class HadesIncludeRunChallenges(DefaultOnToggle):
    """Include repeatable in-run challenges."""
    display_name = "Hades Include Run Challenges"

class HadesDifficultyLevel(TextChoice):
    """Sets the difficulty level for objectives and constraints."""
    display_name = "Hades Difficulty Level"
    option_normal = 0
    option_hard = 1
    option_extreme = 2
    default = 0
