from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle, DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BeyondTheLongNightArchipelagoOptions:
    beyond_the_long_night_include_npc_objectives: BeyondTheLongNightIncludeNPCObjectives
    beyond_the_long_night_include_challenge_objectives: BeyondTheLongNightIncludeChallengeObjectives
    beyond_the_long_night_include_upgrade_objectives: BeyondTheLongNightIncludeUpgradeObjectives


class BeyondTheLongNightGame(Game):
    name = "Beyond the Long Night"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = BeyondTheLongNightArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Only play in Encore mode (New Game+)",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Do not purchase anything from the Annoying Child's shops",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Never pick up a Buddy",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Don't give Bobbins a single torch (he doesn't deserve it)",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Be in the starting room of the storm when the storm starts",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="You must lose at least one health from the storm during the run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = []
        objectives += self.base_objectives()

        if self.include_npc_objectives:
            objectives += self.npc_objectives()
        if self.include_challenge_objectives:
            objectives += self.challenge_objectives()
        if self.include_upgrade_objectives:
            objectives += self.upgrade_objectives()

        return objectives

    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run (defeat the Guardian of the Overworld to escape) wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Reach the Forbidden Temple wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Reach Hope's Peak wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Reach the Sanctuary wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Collect at least one Upgrade of each of the 5 types (Bullet, Passive, Buddy, Superpower, Superpower Upgrade) in one run wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Have 3 different Superpower Upgrades active at once in a single run wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    def npc_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Talk to 3 different NPCs in a single run wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Find and talk to NPC wearing the HAT",
                data={
                    "NPC": (self.npcs, 1),
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Purchase an item from one of the Annoying Child's shops in a single run wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
        ]

    def upgrade_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Level up the same Superpower Upgrade card to level 3 or higher in a single run wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Collect 5 Upgrades from the same category (Bullet, Passive, Buddy, Superpower, or Superpower Upgrade) in a single run wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
        ]

    def challenge_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run without taking any damage from the Storm wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Win a run without collecting any Upgrades wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Win a run without ever using your Superpower wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Escape the Long Night in under 25 minutes wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Use the bird somewhere in Sanctuary wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Give a toot in Tetchy & Dopey's starting room wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Expose Tetchy & Dopey to the storm wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Grab Sara's leftmost item wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Do a toot in an oddly shaped stone room encased in the storm wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Defeat at least two Birds wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Visit every room in the Forbidden Temple in a single run wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Visit every room in Hope's Peak in a single run wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Visit every room in every area (Forbidden Temple, Hope's Peak, and Sanctuary) in a single run wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Win a run firing your main bullets weapon 100 times or fewer wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Win a run in under 25 minutes without taking any damage wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Engrave a cow statue in a single run wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Visit the Annoying Child in the Strange Dimension wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
        ]

    @property
    def include_npc_objectives(self) -> bool:
        return self.archipelago_options.beyond_the_long_night_include_npc_objectives.value

    @property
    def include_challenge_objectives(self) -> bool:
        return self.archipelago_options.beyond_the_long_night_include_challenge_objectives.value

    @property
    def include_upgrade_objectives(self) -> bool:
        return self.archipelago_options.beyond_the_long_night_include_upgrade_objectives.value

    @staticmethod
    def hats() -> List[str]:
        return [
            "Explorer Hat",
            "Party Hat",
            "Mushroom Hat",
            "Iron Hat",
        ]

    @staticmethod
    def npcs() -> List[str]:
        return [
            "Eebi",
            "the Annoying Child",
            "the Pilgrim",
            "Umpa",
            "Archie",
            "Tetchy and Dopey",
        ]


# Archipelago Options
class BeyondTheLongNightIncludeNPCObjectives(DefaultOnToggle):
    """Indicates whether to include objectives involving talking to NPCs and visiting shops."""
    display_name = "Beyond the Long Night: Include NPC Objectives"

class BeyondTheLongNightIncludeChallengeObjectives(Toggle):
    """Indicates whether to include difficult challenge run objectives."""
    display_name = "Beyond the Long Night: Include Challenge Objectives"

class BeyondTheLongNightIncludeUpgradeObjectives(DefaultOnToggle):
    """Indicates whether to include objectives related to collecting and leveling up Upgrades within a run."""
    display_name = "Beyond the Long Night: Include Upgrade Objectives"
