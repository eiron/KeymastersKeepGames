from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ApexLegendsArchipelagoOptions:
    apex_legends_include_legend_objectives: ApexLegendsIncludeLegendObjectives
    apex_legends_include_challenge_objectives: ApexLegendsIncludeChallengeObjectives


class ApexLegendsGame(Game):
    name = "Apex Legends"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = ApexLegendsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play as LEGEND",
                data={
                    "LEGEND": (self.legends, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Play as a CLASS Legend",
                data={
                    "CLASS": (self.classes, 1),
                },
            ),
            GameObjectiveTemplate(
                label="No Energy Weapons",
                data={},
            ),
            GameObjectiveTemplate(
                label="No Heavy Weapons",
                data={},
            ),
            GameObjectiveTemplate(
                label="No Light Weapons",
                data={},
            ),
             GameObjectiveTemplate(
                label="Must carry a Mozambique",
                data={},
            ),
            GameObjectiveTemplate(
                label="Only use pistols",
                data={},
            ),
            GameObjectiveTemplate(
                label="Once you have over 120 total ammo in your inventory, never let your total ammo count drop below 120",
                data={},
            ),
            GameObjectiveTemplate(
                label="Use your ultimate as soon as it gets fully charged, every time it gets charged",
                data={},
            ),
            GameObjectiveTemplate(
                label="Don't pick up any armour, helmet, or backpack unless your teammate(s) have one of equal or better quality",
                data={},
            ),
            GameObjectiveTemplate(
                label="Keep the first weapon you pick up for the rest of the game (or, in an Arena, the first weapon you bought in every other round)",
                data={},
            ),
            GameObjectiveTemplate(
                label="Only kill downed enemies with a finisher",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        objectives += self.base_objectives()
        
        if self.include_legend_objectives:
            objectives += self.legend_objectives()
            
        if self.include_challenge_objectives:
            objectives += self.challenge_objectives()
        
        return objectives
    
    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a Battle Royale match",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Win a Mixtape match",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Place Top 5 in Battle Royale",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Finish in the Top 5 of a trios game",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Finish in the Top 10 of a duos game",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
             GameObjectiveTemplate(
                label="Get 3 Kills in a single match",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
             GameObjectiveTemplate(
                label="Deal 1000 Damage in a single match",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get a knockdown with a marksman weapon",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Have two weapons with purple (or better) magazines at the same time",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Knockdown or kill an enemy with a grenade",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Have two weapons with hop-ups at the same time",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get a kill with the Mozambique shotgun",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]
    
    def legend_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a match as LEGEND",
                data={
                    "LEGEND": (self.legends, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
             GameObjectiveTemplate(
                label="Get 5 Kills as LEGEND",
                data={
                    "LEGEND": (self.legends, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
        ]
    
    def challenge_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Become the Kill Leader",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Perform a Finisher",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Respawn a teammate",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get 10 Kills in a single match",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Deal 2000 Damage in a single match (2k Badge)",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
             GameObjectiveTemplate(
                label="Win a match with no armor equipped (drop it before winning)",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
        ]
    
    @property
    def include_legend_objectives(self) -> bool:
        return self.archipelago_options.apex_legends_include_legend_objectives.value
    
    @property
    def include_challenge_objectives(self) -> bool:
        return self.archipelago_options.apex_legends_include_challenge_objectives.value
    
    @staticmethod
    def legends() -> List[str]:
        return [
            "Bangalore", "Fuse", "Ash", "Mad Maggie", "Ballistic",
            "Pathfinder", "Wraith", "Octane", "Horizon", "Valkyrie", "Revenant", "Alter",
            "Bloodhound", "Crypto", "Seer", "Vantage",
            "Gibraltar", "Lifeline", "Mirage", "Loba", "Newcastle", "Conduit",
            "Caustic", "Wattson", "Rampart", "Catalyst"
        ]

    @staticmethod
    def classes() -> List[str]:
        return [
            "Assault",
            "Skirmisher",
            "Recon",
            "Support",
            "Controller",
        ]


# Archipelago Options
class ApexLegendsIncludeLegendObjectives(Toggle):
    """
    Indicates whether to include objectives that require playing as specific Legends.
    """
    display_name = "Apex Legends: Include Legend Objectives"


class ApexLegendsIncludeChallengeObjectives(Toggle):
    """
    Indicates whether to include difficult challenge objectives.
    """
    display_name = "Apex Legends: Include Challenge Objectives"
