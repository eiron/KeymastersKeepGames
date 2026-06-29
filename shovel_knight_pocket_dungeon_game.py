from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ShovelKnightPocketDungeonArchipelagoOptions:
    shovel_knight_pocket_dungeon_include_character_challenge_objectives: ShovelKnightPocketDungeonIncludeCharacterChallengeObjectives
    shovel_knight_pocket_dungeon_include_dlc_objectives: ShovelKnightPocketDungeonIncludeDLCObjectives


class ShovelKnightPocketDungeonGame(Game):
    name = "Shovel Knight Pocket Dungeon"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = ShovelKnightPocketDungeonArchipelagoOptions

    @property
    def include_character_challenge_objectives(self) -> bool:
        return self.archipelago_options.shovel_knight_pocket_dungeon_include_character_challenge_objectives.value

    @property
    def include_dlc_objectives(self) -> bool:
        return self.archipelago_options.shovel_knight_pocket_dungeon_include_dlc_objectives.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = []

        constraints += [
            GameObjectiveTemplate(
                label="Ignore the first Up in Plains Power",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Destroy at least 7 Chests",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Beat Lich Yard without picking up unchained potions",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Buy a maximum of 1 item per Chester Chest",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Get at least 3 Key Pieces",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Get a chain at least 15 enemies long",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Do not visit Portal areas",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Beat any Stage (Excluding Plains) in less than 1:30",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Beat Pridemoor's Keep without activating a character ability (use a character with an ability)",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Do not open the Chester Chest in Pridemoor's Keep",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Beat Iron Whale without directly killing any Grapps",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
        ]

        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Beat the game as CHARACTER",
                data={"CHARACTER": (self.characters, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Complete the True Ending run as CHARACTER",
                data={"CHARACTER": (self.characters, 1)},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Achieve a chain of N enemies in a single action",
                data={"N": (self.chain_lengths, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Deal at least N damage in a single strike",
                data={"N": (self.strike_damages, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Collect N Gems in a single run",
                data={"N": (self.gem_counts, 1)},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Have N Relics at once in a single run",
                data={"N": (self.relic_counts, 1)},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Beat Puzzle Knight without equipping any Relics",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Score at least 150 points in Mona's minigame",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Clear all 4 Shrine portals in a single run",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Reach DUNGEON in a single run",
                data={"DUNGEON": (self.later_dungeons, 1)},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Reach wave N in Marathon mode",
                data={"N": (self.marathon_wave_counts, 1)},
                is_time_consuming=False,
                is_difficult=True,
            ),
        ]

        if self.include_character_challenge_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Destroy 20 enemies using Shovel Knight's extra chain damage in a single run",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Take 4 HP or fewer in a single stage as Shield Knight",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Defeat a boss with a 5+ damage Shoulder Bash as King Knight",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Finish a stage without collecting any Potion as Specter Knight",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Defeat 20 enemies with poison in a single stage as Plague Knight",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Hoard 50,000 Gems in a single run as Treasure Knight",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Construct your mech 10 times in a single stage as Tinker Knight",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Avoid damage 10 times using Mole Knight's burrow in a single run",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Defeat a boss in fewer than 5 strikes as Propeller Knight",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Slay 50 frozen enemies in a single stage as Polar Knight",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Boost to 8 base attack as Black Knight",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Chain 10 enemies 5 times in a single stage as Scrap Knight",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Finish a stage in fewer than 10 steps as Prism Knight",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
            ])

        if self.include_dlc_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Beat the game as DLC_CHARACTER",
                    data={"DLC_CHARACTER": (self.dlc_characters, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Complete a Quandary run as CHARACTER",
                    data={"CHARACTER": (self.quandary_characters, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Complete all four Quandaries as CHARACTER",
                    data={"CHARACTER": (self.quandary_characters, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Complete a Weekly Run",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Win a VS Mode match",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Win a VS Mode Volleybomb match",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Reach Loop N in Venture Endlessly mode",
                    data={"N": (self.endless_loop_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
                GameObjectiveTemplate(
                    label="Reach wave 100 in Marathon mode",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                ),
            ])

        return templates

    @staticmethod
    def characters() -> List[str]:
        return [
            "Shovel Knight",
            "Shield Knight",
            "King Knight",
            "Specter Knight",
            "Plague Knight",
            "Treasure Knight",
            "Tinker Knight",
            "Mole Knight",
            "Propeller Knight",
            "Polar Knight",
            "Black Knight",
            "Scrap Knight",
            "Prism Knight",
        ]

    @staticmethod
    def dlc_characters() -> List[str]:
        return [
            "Puzzle Knight",
            "Mona",
            "Quandary Sage",
            "Spinwulf",
            "Chester",
            "The Enchantress",
            "Random Knight",
            "Shuffle Knight",
        ]

    @staticmethod
    def quandary_characters() -> List[str]:
        return [
            "Shovel Knight",
            "Shield Knight",
            "King Knight",
            "Specter Knight",
            "Plague Knight",
            "Treasure Knight",
            "Tinker Knight",
            "Mole Knight",
            "Propeller Knight",
            "Polar Knight",
            "Black Knight",
            "Scrap Knight",
            "Prism Knight",
            "Puzzle Knight",
            "Mona",
        ]

    @staticmethod
    def chain_lengths() -> List[int]:
        return [10, 25, 50]

    @staticmethod
    def strike_damages() -> List[int]:
        return [5, 10]

    @staticmethod
    def gem_counts() -> List[str]:
        return [
            "10,000",
            "50,000",
            "100,000",
        ]

    @staticmethod
    def relic_counts() -> List[int]:
        return [5, 8, 10]

    @staticmethod
    def later_dungeons() -> List[str]:
        return [
            "Chromatic Caverns",
            "Clockwork Tower",
            "Stranded Ship",
            "Flying Machine",
            "Scholar's Sanctum",
            "Tower of Fate",
        ]

    @staticmethod
    def marathon_wave_counts() -> List[int]:
        return [10, 30]

    @staticmethod
    def endless_loop_counts() -> List[int]:
        return [2, 5, 10]


class ShovelKnightPocketDungeonIncludeCharacterChallengeObjectives(DefaultOnToggle):
    """Include character-specific Feat challenge objectives for each knight."""
    display_name = "Shovel Knight Pocket Dungeon Include Character Challenge Objectives"


class ShovelKnightPocketDungeonIncludeDLCObjectives(DefaultOnToggle):
    """Include objectives for DLC content (Puzzler's Pack, Paradox Pack, Pals Pack)."""
    display_name = "Shovel Knight Pocket Dungeon Include DLC Objectives"
