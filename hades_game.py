from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class HadesArchipelagoOptions:
    hades_include_escape_attempts: HadesIncludeEscapeAttempts
    hades_include_weapon_mastery: HadesIncludeWeaponMastery
    hades_include_relationship_building: HadesIncludeRelationshipBuilding
    hades_include_story_progression: HadesIncludeStoryProgression
    hades_include_mirror_upgrades: HadesIncludeMirrorUpgrades
    hades_include_prophecies: HadesIncludeProphecies
    hades_include_contractor_upgrades: HadesIncludeContractorUpgrades
    hades_include_collection_goals: HadesIncludeCollectionGoals
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
        
        if self.difficulty_level in ["Hard", "Extreme"]:
            constraints.extend([
                GameObjectiveTemplate(
                    label="Complete this objective using only ASPECT weapon aspect",
                    data={"ASPECT": (self.weapon_aspects, 1)},
                ),
                GameObjectiveTemplate(
                    label="Complete this objective without using BOON_TYPE boons",
                    data={"BOON_TYPE": (self.boon_types, 1)},
                ),
            ])
        
        if self.difficulty_level == "Extreme":
            constraints.extend([
                GameObjectiveTemplate(
                    label="Complete this objective with at least HEAT heat",
                    data={"HEAT": (self.high_heat_levels, 1)},
                ),
                GameObjectiveTemplate(
                    label="Complete this objective without dying more than DEATH_COUNT times",
                    data={"DEATH_COUNT": (self.low_death_counts, 1)},
                ),
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
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSS without taking damage",
                    data={"BOSS": (self.bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Reach LOCATION in a single run",
                    data={"LOCATION": (self.locations, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete RUN_COUNT successful escapes",
                    data={"RUN_COUNT": (self.escape_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete an escape with HEAT heat or higher",
                    data={"HEAT": (self.heat_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Weapon Mastery
        if self.include_weapon_mastery:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Unlock the ASPECT aspect for WEAPON",
                    data={
                        "ASPECT": (self.weapon_aspects, 1),
                        "WEAPON": (self.weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Fully upgrade WEAPON with Titan Blood",
                    data={"WEAPON": (self.weapons, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete COUNT runs using WEAPON",
                    data={
                        "COUNT": (self.weapon_run_counts, 1),
                        "WEAPON": (self.weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Achieve a personal best time with WEAPON",
                    data={"WEAPON": (self.weapons, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Relationship Building
        if self.include_relationship_building:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Max out your relationship with CHARACTER",
                    data={"CHARACTER": (self.characters, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Give GIFT_COUNT GIFT to CHARACTER",
                    data={
                        "GIFT_COUNT": (self.gift_counts, 1),
                        "GIFT": (self.gifts, 1),
                        "CHARACTER": (self.characters, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Unlock KEEPSAKE from CHARACTER",
                    data={
                        "KEEPSAKE": (self.keepsakes, 1),
                        "CHARACTER": (self.characters, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Reach max rank with KEEPSAKE",
                    data={"KEEPSAKE": (self.keepsakes, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Story Progression
        if self.include_story_progression:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete STORYLINE storyline",
                    data={"STORYLINE": (self.storylines, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Unlock CODEX_COUNT codex entries",
                    data={"CODEX_COUNT": (self.codex_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete the main story ending",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Mirror Upgrades
        if self.include_mirror_upgrades:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Fully upgrade MIRROR_TALENT in the Mirror of Night",
                    data={"MIRROR_TALENT": (self.mirror_talents, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Unlock all alternate Mirror of Night talents",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Spend DARKNESS_AMOUNT Darkness on Mirror upgrades",
                    data={"DARKNESS_AMOUNT": (self.darkness_amounts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Prophecies
        if self.include_prophecies:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete PROPHECY_COUNT prophecies from the Fated List",
                    data={"PROPHECY_COUNT": (self.prophecy_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete all prophecies in the PROPHECY_CATEGORY category",
                    data={"PROPHECY_CATEGORY": (self.prophecy_categories, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Contractor Upgrades
        if self.include_contractor_upgrades:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Purchase UPGRADE_COUNT upgrades from the House Contractor",
                    data={"UPGRADE_COUNT": (self.contractor_upgrade_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Fully renovate the HOUSE_AREA area",
                    data={"HOUSE_AREA": (self.house_areas, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Collection Goals
        if self.include_collection_goals:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Collect RESOURCE_COUNT RESOURCE",
                    data={
                        "RESOURCE_COUNT": (self.resource_counts, 1),
                        "RESOURCE": (self.resources, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Purchase all items from MERCHANT",
                    data={"MERCHANT": (self.merchants, 1)},
                    is_time_consuming=True,
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
    def include_weapon_mastery(self) -> bool:
        return self.archipelago_options.hades_include_weapon_mastery.value

    @property
    def include_relationship_building(self) -> bool:
        return self.archipelago_options.hades_include_relationship_building.value

    @property
    def include_story_progression(self) -> bool:
        return self.archipelago_options.hades_include_story_progression.value

    @property
    def include_mirror_upgrades(self) -> bool:
        return self.archipelago_options.hades_include_mirror_upgrades.value

    @property
    def include_prophecies(self) -> bool:
        return self.archipelago_options.hades_include_prophecies.value

    @property
    def include_contractor_upgrades(self) -> bool:
        return self.archipelago_options.hades_include_contractor_upgrades.value

    @property
    def include_collection_goals(self) -> bool:
        return self.archipelago_options.hades_include_collection_goals.value

    @property
    def difficulty_level(self) -> str:
        return self.archipelago_options.hades_difficulty_level.value

    # Data lists
    @staticmethod
    def weapons() -> List[str]:
        return [
            "Stygian Blade", "Eternal Spear", "Shield of Chaos", 
            "Heart-Seeking Bow", "Twin Fists", "Adamant Rail"
        ]

    @staticmethod
    def weapon_aspects() -> List[str]:
        return [
            "Zagreus", "Nemesis", "Poseidon", "Arthur", "Guan Yu", "Beowulf",
            "Hestia", "Eris", "Zeus", "Chiron", "Hera", "Rama", "Demeter",
            "Talos", "Gilgamesh", "Lucifer", "Hades", "Eris"
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Megaera", "Alecto", "Tisiphone", "Lernaean Bone Hydra", 
            "Theseus", "Asterius", "Hades"
        ]

    @staticmethod
    def locations() -> List[str]:
        return ["Tartarus", "Asphodel", "Elysium", "Temple of Styx", "Greece"]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Achilles", "Nyx", "Cerberus", "Orpheus", "Eurydice", "Sisyphus",
            "Patroclus", "Thanatos", "Megaera", "Dusa", "Skelly", "Hypnos",
            "Charon", "Chaos", "Zeus", "Poseidon", "Athena", "Aphrodite",
            "Artemis", "Ares", "Dionysus", "Hermes", "Demeter", "Persephone"
        ]

    @staticmethod
    def keepsakes() -> List[str]:
        return [
            "Old Spiked Collar", "Black Shawl", "Chthonic Coin Purse", "Distant Memory",
            "Evergreen Acorn", "Pierced Butterfly", "Bone Hourglass", "Overflowing Cup",
            "Lucky Tooth", "Thunder Signet", "Conch Shell", "Owl Pendant", "Eternal Rose",
            "Blood-Filled Vial", "Skull Earring", "Overflowing Cup", "Lambent Plume",
            "Frostbitten Horn", "Pom Blossom", "Cosmic Egg"
        ]

    @staticmethod
    def gifts() -> List[str]:
        return ["Nectar", "Ambrosia"]

    @staticmethod
    def storylines() -> List[str]:
        return [
            "Zagreus's Escape", "Persephone's Return", "Orpheus and Eurydice",
            "Achilles and Patroclus", "Sisyphus's Freedom", "Thanatos Relationship",
            "Megaera Relationship", "Dusa Relationship", "Family Reunion"
        ]

    @staticmethod
    def mirror_talents() -> List[str]:
        return [
            "Shadow Presence", "Chthonic Vitality", "Death Defiance", "Greater Reflex",
            "Boiling Blood", "Infernal Soul", "Deep Pockets", "Thick Skin",
            "Privileged Status", "Family Trade", "God's Pride", "Fated Authority",
            "Fiery Presence", "Abyssal Blood", "Stubborn Defiance", "Ruthless Reflex",
            "Stygian Soul", "Golden Touch", "Hard Labor", "Olympian Favor"
        ]

    @staticmethod
    def prophecy_categories() -> List[str]:
        return [
            "Chthonic Colleagues", "Olympian Gods", "The Exiled", "Sworn Enemies",
            "Heart-Seekers", "Distant Relatives", "Minor Prophesies"
        ]

    @staticmethod
    def house_areas() -> List[str]:
        return [
            "Zagreus's Room", "Lounge", "Main Hall", "Nyx's Alcove", "Achilles' Arena",
            "Orpheus's Court", "Administrative Chamber", "West Hall", "East Hall"
        ]

    @staticmethod
    def resources() -> List[str]:
        return [
            "Darkness", "Chthonic Key", "Gemstone", "Diamond", "Titan Blood",
            "Ambrosia", "Nectar", "Coin"
        ]

    @staticmethod
    def merchants() -> List[str]:
        return ["Charon", "Well of Charon", "House Contractor", "Wretched Broker"]

    @staticmethod
    def boon_types() -> List[str]:
        return [
            "Zeus", "Poseidon", "Athena", "Aphrodite", "Artemis", "Ares",
            "Dionysus", "Hermes", "Demeter", "Chaos"
        ]

    # Ranges
    @staticmethod
    def escape_counts() -> range:
        return range(1, 10, 2)

    @staticmethod
    def heat_levels() -> range:
        return range(1, 20, 2)

    @staticmethod
    def high_heat_levels() -> range:
        return range(10, 32, 5)

    @staticmethod
    def low_death_counts() -> range:
        return range(0, 5)

    @staticmethod
    def weapon_run_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def gift_counts() -> range:
        return range(1, 10, 2)

    @staticmethod
    def codex_counts() -> range:
        return range(10, 50, 10)

    @staticmethod
    def darkness_amounts() -> range:
        return range(1000, 10000, 1000)

    @staticmethod
    def prophecy_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def contractor_upgrade_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def resource_counts() -> range:
        return range(10, 100, 10)


# Archipelago Options
class HadesIncludeEscapeAttempts(DefaultOnToggle):
    """Include escape attempt objectives (runs, bosses, heat)."""
    display_name = "Include Escape Attempts"

class HadesIncludeWeaponMastery(DefaultOnToggle):
    """Include weapon mastery objectives (aspects, upgrades, runs)."""
    display_name = "Include Weapon Mastery"

class HadesIncludeRelationshipBuilding(DefaultOnToggle):
    """Include relationship objectives (characters, gifts, keepsakes)."""
    display_name = "Include Relationship Building"

class HadesIncludeStoryProgression(DefaultOnToggle):
    """Include story progression objectives (storylines, codex, endings)."""
    display_name = "Include Story Progression"

class HadesIncludeMirrorUpgrades(DefaultOnToggle):
    """Include Mirror of Night upgrade objectives."""
    display_name = "Include Mirror Upgrades"

class HadesIncludeProphecies(DefaultOnToggle):
    """Include Fated List prophecy objectives."""
    display_name = "Include Prophecies"

class HadesIncludeContractorUpgrades(DefaultOnToggle):
    """Include House Contractor upgrade objectives."""
    display_name = "Include Contractor Upgrades"

class HadesIncludeCollectionGoals(DefaultOnToggle):
    """Include resource collection and merchant objectives."""
    display_name = "Include Collection Goals"

class HadesDifficultyLevel(Choice):
    """Sets the difficulty level for objectives and constraints."""
    display_name = "Difficulty Level"
    option_normal = "Normal"
    option_hard = "Hard"
    option_extreme = "Extreme"
    default = option_normal
