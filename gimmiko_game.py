from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GimmikoArchipelagoOptions:
    gimmiko_include_boss_objectives: GimmikoIncludeBossObjectives
    gimmiko_include_solitaire_objectives: GimmikoIncludeSolitaireObjectives


class GimmikoGame(Game):
    name = "Gimmiko"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = GimmikoArchipelagoOptions

    @property
    def include_boss_objectives(self) -> bool:
        return self.archipelago_options.gimmiko_include_boss_objectives.value

    @property
    def include_solitaire_objectives(self) -> bool:
        return self.archipelago_options.gimmiko_include_solitaire_objectives.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = []

        constraints += [
            GameObjectiveTemplate(
                label="Don't visit the crows",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Before you leave Salty Caramel, always freeze the stock",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Visit the second secret shop and buy as many things as possible",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Always tip Ika at the 1-8-1 whenever you visit",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Never visit Sterling Customs",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Accept Hasshaku-Sama's deal if she appears",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Follow Konomi's shop suggestions whenever she appears",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Give Retsu to Jinmenken whenever he appears",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Let Kokkuri-San change the upcoming boss if he appears",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
        ]

        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Complete one run in Gimmiko",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Complete one run in Gimmiko as CHARACTER",
                data={"CHARACTER": (self.playable_characters, 1)},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Reach Wave 13 in a run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Discover a hidden shop during a run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Acquire a Legendary gimmick and equip it to your die during a run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Visit the Rotten Playroom during a run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Visit Tail's End during a run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Visit the Hot Springs during a run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Complete a Catacombs challenge",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Successfully complete Hanako-San's fly-hunting challenge",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Survive Gozu's barrage and claim your Onigiri reward from Rawhide Kobayashi",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Give Retsu to Jinmenken and receive his return reward",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Accept a boost from Akamanto during a run",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Keep an Auric Hog alive long enough to collect its bonus",
                data={},
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Let Konomi lead you to a shop and follow her choice",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Have Mr. Scary ectoplasmify Retsu during a wave",
                data={},
                is_time_consuming=False,
                is_difficult=False,
            ),
        ]

        if self.include_boss_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Defeat BOSS on Wave 13",
                    data={"BOSS": (self.wave_13_bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSS in the Catacombs",
                    data={"BOSS": (self.catacombs_bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
            ])

        if self.include_solitaire_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win a round of Jabberwock Solitaire",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                ),
                GameObjectiveTemplate(
                    label="Win a round of Jabberwock Solitaire in Night Mode",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                ),
            ])

        return templates

    @staticmethod
    def playable_characters() -> List[str]:
        return [
            "Merci",
            "Zo",
        ]

    @staticmethod
    def wave_13_bosses() -> List[str]:
        return [
            "Yuki-Onna",
            "Okiku",
        ]

    @staticmethod
    def catacombs_bosses() -> List[str]:
        return [
            "Kusagata",
            "Oiwa",
        ]


class GimmikoIncludeBossObjectives(DefaultOnToggle):
    """Include objectives for defeating specific bosses on Wave 13 and in the Catacombs."""
    display_name = "Gimmiko Include Boss Objectives"


class GimmikoIncludeSolitaireObjectives(DefaultOnToggle):
    """Include objectives for Jabberwock Solitaire, including Night Mode."""
    display_name = "Gimmiko Include Solitaire Objectives"
