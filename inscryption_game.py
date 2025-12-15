from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class InscryptionArchipelagoOptions:
    inscryption_include_campaign: InscryptionIncludeCampaign
    inscryption_include_card_objectives: InscryptionIncludeCardObjectives
    inscryption_include_kaycee_mod: InscryptionIncludeKayceesMod


class InscryptionGame(Game):
    name = "Inscryption"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = InscryptionArchipelagoOptions

    # Properties
    @property
    def include_campaign(self) -> bool:
        return self.archipelago_options.inscryption_include_campaign.value

    @property
    def include_card_objectives(self) -> bool:
        return self.archipelago_options.inscryption_include_card_objectives.value

    @property
    def include_kaycee_mod(self) -> bool:
        return self.archipelago_options.inscryption_include_kaycee_mod.value

    # Optional constraints
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(label="Use only a single tribe throughout the run", data={"TRIBE": (self.card_tribes, 1)}),
            GameObjectiveTemplate(label="Never use items during battles", data={}),
            GameObjectiveTemplate(label="Win all battles without losing a life", data={}),
            GameObjectiveTemplate(label="Never merge or upgrade cards", data={}),
            GameObjectiveTemplate(label="Never restart a battle", data={}),
            GameObjectiveTemplate(label="Defeat the final boss with only 1 card in deck", data={}),
            GameObjectiveTemplate(label="Build a deck using only cards with the Unkillable sigil", data={}),
            GameObjectiveTemplate(label="Never sacrifice creatures (blood cost only allowed)", data={}),
            GameObjectiveTemplate(label="Complete the run using cards from only one Scrybe", data={"SCRYBE": (self.scrybes, 1)}),
            GameObjectiveTemplate(label="Buy the Trapper's skinning knife", data={}),
            GameObjectiveTemplate(label="Take at least three copies of the same card", data={}),
            GameObjectiveTemplate(label="Buy a golden pelt", data={}),
            GameObjectiveTemplate(label="Fail the Cave Trial at least 3 times", data={}),
            GameObjectiveTemplate(label="Never finish creating a totem", data={}),
            GameObjectiveTemplate(label="Avoid all regular card draft spots", data={}),
            GameObjectiveTemplate(label="Finish the run with a card that has no added sigils", data={}),
            GameObjectiveTemplate(label="Visit every Mycologist available", data={}),
            GameObjectiveTemplate(label="Paint a card with no added sigils", data={}),
        ]

    # Objectives
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = []

        if self.include_campaign:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete Act I: Defeat Leshy in his cabin",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Complete Act II: Defeat all four Scrybes in the overworld",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Complete Act III: Defeat P03 and all Uberbots in the factory",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Beat BOSS_NAME without losing a single life",
                    data={"BOSS_NAME": (self.major_bosses, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Defeat the final boss with a deck composed entirely of TRIBE creatures",
                    data={"TRIBE": (self.card_tribes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                ),
            ])

        if self.include_card_objectives:
            templates.extend([
                GameObjectiveTemplate(
                    label="Collect all TRIBE creatures in a single run",
                    data={"TRIBE": (self.card_tribes, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Collect RARE_CARD during a run and reach the final boss",
                    data={"RARE_CARD": (self.rare_cards, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Build a deck with POWER_LEVEL or higher average creature power",
                    data={"POWER_LEVEL": (self.power_thresholds, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Create a SIGIL_TYPE-focused deck and defeat a boss with it",
                    data={"SIGIL_TYPE": (self.sigil_types, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Win using cards from only SCRYBE_NAME",
                    data={"SCRYBE_NAME": (self.scrybes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                ),
            ])

        if self.include_kaycee_mod:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete Kaycee's Mod with STARTER_DECK starter deck",
                    data={"STARTER_DECK": (self.starter_decks, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Reach Ascension Level ASCENSION_LEVEL in Kaycee's Mod",
                    data={"ASCENSION_LEVEL": (self.ascension_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Complete a run with CHALLENGE_MODIFIER active",
                    data={"CHALLENGE_MODIFIER": (self.challenge_modifiers, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Win Skull Storm: Complete Kaycee's Mod with all challenges enabled",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Defeat all Grizzly Bear encounter waves in Kaycee's Mod",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Complete a run with the modifiers CHALLENGE_MODIFIERS active",
                    data={
                        "CHALLENGE_MODIFIERS": (self.challenge_modifiers, 2),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Complete a run with the modifiers CHALLENGE_MODIFIERS active",
                    data={
                        "CHALLENGE_MODIFIERS": (self.challenge_modifiers, 3),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=10,
                ),
            ])

        return templates

    # Data lists
    @staticmethod
    def major_bosses() -> List[str]:
        return [
            "Leshy (Act I)",
            "Prospector (Act I Boss)",
            "Angler (Act I Boss)",
            "Trapper/Trader (Act I Boss)",
            "Leshy (Scrybe - Act II)",
            "Grimora (Scrybe - Act II)",
            "P03 (Scrybe - Act II)",
            "Magnificus (Scrybe - Act II)",
        ]

    @staticmethod
    def card_tribes() -> List[str]:
        return [
            "Avian",
            "Canine",
            "Hooved",
            "Insect",
            "Reptile",
        ]

    @staticmethod
    def rare_cards() -> List[str]:
        return [
            "Ouroboros",
            "Mantis God",
            "Cockroach",
            "Rat King",
            "Beehive",
            "Urayuli",
        ]

    @staticmethod
    def power_thresholds() -> List[str]:
        return ["2.0", "2.5", "3.0"]

    @staticmethod
    def sigil_types() -> List[str]:
        return [
            "Airborne",
            "Waterborne",
            "Unkillable",
            "Mighty Leap",
            "Bifurcated Strike",
            "Trifurcated Strike",
            "Fecundity",
            "Burrower",
            "Touch of Death",
            "Guardian",
        ]

    @staticmethod
    def scrybes() -> List[str]:
        return [
            "Leshy (Beasts)",
            "Grimora (Undead)",
            "P03 (Technology)",
            "Magnificus (Magicks)",
        ]

    @staticmethod
    def starter_decks() -> List[str]:
        return [
            "Vanilla",
            "Moose Blood",
            "Ants",
            "Mantis God",
            "Submersibles",
            "Bones",
            "Free Reptiles",
            "Eggs",
        ]

    @staticmethod
    def ascension_levels() -> List[str]:
        return [
            "5",
            "10",
            "15",
            "20",
            "25",
        ]

    @staticmethod
    def challenge_modifiers() -> List[str]:
        return [
            "No Hook",
            "Smaller Backpack",
            "Cloverless",
            "Expensive Pelts",
            "Annoying Starters",
            "Totem Bosses",
            "No Boss Rares",
            "Boss Totems",
            "Tipped Scales",
            "All Totem Battles",
            "Squirrel Fish",
            "Final Boss",
            "Single Candle",
            "Grizzly Bosses",
        ]


# Archipelago Options
class InscryptionIncludeCampaign(DefaultOnToggle):
    """Include objectives for beating acts, bosses, and campaign progression."""
    display_name = "Inscryption Include Campaign"


class InscryptionIncludeCardObjectives(DefaultOnToggle):
    """Include objectives for collecting cards, building synergies, and deck composition."""
    display_name = "Inscryption Include Card Objectives"


class InscryptionIncludeKayceesMod(DefaultOnToggle):
    """Include objectives for Kaycee's Mod endless challenges and ascension progression."""
    display_name = "Inscryption Include Kaycee's Mod"
