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
    beyond_the_long_night_include_hat_objectives: BeyondTheLongNightIncludeHatObjectives


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
                label="Play with increased Storm speed (enable any fast-storm modifier)",
                data={},
            ),
            GameObjectiveTemplate(
                label="Never heal at Campfires",
                data={},
            ),
            GameObjectiveTemplate(
                label="Do not purchase map revealing upgrades",
                data={},
            ),
            GameObjectiveTemplate(
                label="Rescue villagers before entering any Storm layer",
                data={},
            ),
            GameObjectiveTemplate(
                label="No companion pets",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't give Bobbins a single torch (he doesn't deserve it)",
                data={},
            ),
            GameObjectiveTemplate(
                label="Be in the starting room of the storm when the storm starts",
                data={},
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
        if self.include_hat_objectives:
            objectives += self.hat_objectives()

        return objectives

    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run (Reach the surface)",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Reach Layer 3 of the Storm",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat a miniboss",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Collect 5 different artifacts in one run",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Carry 3 active powers simultaneously",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    def npc_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Rescue 3 villagers",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Complete a villager quest chain",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Unlock the Airship upgrade",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
        ]

    def upgrade_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Unlock 3 permanent meta upgrades",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Fully upgrade a single power",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Unlock the Storm Scanner",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    def challenge_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run without taking damage from Storm hazards",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Win a run without using Campfire healing",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Win a run while the Storm speed modifier is active",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Reach Layer 3 in under 15 minutes",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Use the bird somewhere in Sanctuary",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Give a toot in Tetchy & Dopey's starting room",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Expose Tetchy & Dopey to the storm",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Grab Sara's leftmost item",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Do a toot in an oddly shaped stone room encased in the storm",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Defeat at least two Birds",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Visit every room on the map",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Visit the Annoying Child in the Strange Dimension",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Lose at least one health from the storm during the run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    def hat_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run while wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Rescue 3 villagers while wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Reach Storm Layer 3 while continuously wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Collect 5 different artifacts while wearing the HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a run without changing from the starting HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
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

    @property
    def include_hat_objectives(self) -> bool:
        return self.archipelago_options.beyond_the_long_night_include_hat_objectives.value

    @staticmethod
    def hats() -> List[str]:
        return [
            "Explorer Hat",
            "Party Hat",
            "Mushroom Hat",
            "Iron Hat",
        ]


# Archipelago Options
class BeyondTheLongNightIncludeNPCObjectives(DefaultOnToggle):
    """Indicates whether to include objectives involving rescuing NPC villagers and their quests."""
    display_name = "Beyond the Long Night: Include NPC Objectives"

class BeyondTheLongNightIncludeChallengeObjectives(Toggle):
    """Indicates whether to include difficult challenge run objectives."""
    display_name = "Beyond the Long Night: Include Challenge Objectives"

class BeyondTheLongNightIncludeUpgradeObjectives(DefaultOnToggle):
    """Indicates whether to include objectives related to unlocking or upgrading powers/meta progression."""
    display_name = "Beyond the Long Night: Include Upgrade Objectives"

class BeyondTheLongNightIncludeHatObjectives(DefaultOnToggle):
    """Indicates whether to include objectives that require wearing specific hats."""
    display_name = "Beyond the Long Night: Include Hat Objectives"
