from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CavesOfQudArchipelagoOptions:
    pass


class CavesOfQudGame(Game):
    name = "Caves of Qud"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = CavesOfQudArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="No using the wish system",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use ranged weapons",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="No mutations allowed (True Kin only)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot wear any armor",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must remain neutral reputation with all factions",
                data=dict(),
            ),
            # Persistent run-modifying constraints (no one-off events)
            GameObjectiveTemplate(
                label="Keep a difference of at least six between your highest and lowest stat at all times",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Take the Night Vision cybernetic and keep it turned on at all times",
                data=dict(),
            ),
            # Additional mutation / cybernetics themed constraints
            GameObjectiveTemplate(
                label="Must choose Unstable Genome morphotype if Mutant",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must not take a starting cybernetic (gain +1 Toughness instead)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must never use the Precognition mutation",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must install only arcology-specific cybernetics (No general implants)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Accept the first offered mutation every time (simulate Irritable Genome)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="May not unequip installed cybernetics (no uninstalling)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Dismember and eat one of your own limbs before leaving the starting area",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Reach LOCATION",
                data={
                    "LOCATION": (self.locations, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat ENEMY",
                data={
                    "ENEMY": (self.enemies, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a run as CASTE",
                data={
                    "CASTE": (self.castes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a run as CALLING",
                data={
                    "CALLING": (self.callings, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach level LEVEL",
                data={
                    "LEVEL": (self.levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Achieve REPUTATION reputation with FACTION",
                data={
                    "REPUTATION": (self.reputation_levels, 1),
                    "FACTION": (self.factions, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Acquire ARTIFACT",
                data={
                    "ARTIFACT": (self.artifacts, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete QUEST",
                data={
                    "QUEST": (self.quests, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Survive DEPTH without dying",
                data={
                    "DEPTH": (self.depths, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            # Event / milestone style objectives drawn from game mechanics
            GameObjectiveTemplate(
                label="Perform water rituals with COUNT different NPCs",
                data={
                    "COUNT": (self.water_ritual_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Trade one secret for another during a water ritual",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Donate a book at Six Day Stilt library",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Create and name a recipe",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Install CYBERNETIC at a becoming nook",
                data={
                    "CYBERNETIC": (self.cybernetics, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Infect yourself with glowcrust fungi",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Break through a solid wall",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Kill and eat a bear",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Discover a dromad caravan",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Discover and visit a sultan shrine other than the one in Joppa",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Carry four different liquids at once",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Take the Evil Twin defect during character creation and kill them",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Take the Nerve Poppy defect during character creation",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Take the Space-Time Vortex mutation and enter it before leaving your starting village",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Learn Trash Divining and gain a secret from rifling through trash",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="While in your starting village, use the wish console to infect yourself with glowcrust",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach the Six Day Stilt and donate a book to the library",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach mutation level LEVEL on MUTATION",
                data={
                    "LEVEL": (self.mutation_target_levels, 1),
                    "MUTATION": (self.all_tracked_mutations, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            # Mutation & defect oriented objectives
            GameObjectiveTemplate(
                label="Reach mutation level LEVEL on MUTATION",
                data={
                    "LEVEL": (self.mutation_target_levels, 1),
                    "MUTATION": (self.all_tracked_mutations, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Manifest morphotype MORPHOTYPE at character creation",
                data={
                    "MORPHOTYPE": (self.morphotypes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Start with DEFECT and survive to level SURVIVOR_LEVEL",
                data={
                    "DEFECT": (self.defects, 1),
                    "SURVIVOR_LEVEL": (self.mutation_survival_levels, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Rapidly advance a physical mutation",
                data={
                    "MUTATION": (self.physical_mutations, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Use Precognition to revert time",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beguile a powerful enemy",
                data={
                    "ENEMY": (self.beguile_targets, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Achieve GLIMMER glimmer score",
                data={
                    "GLIMMER": (self.glimmer_levels, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach cybernetic license tier LICENSE_TIER",
                data={
                    "LICENSE_TIER": (self.license_tiers, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Acquire COUNT cybernetic credit wedges",
                data={
                    "COUNT": (self.credit_wedge_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Cook a meal with a nectar-based effect",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Trigger rapid advancement at level ADV_LEVEL",
                data={
                    "ADV_LEVEL": (self.rapid_advancement_levels, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Identify an artifact via Psychometry",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def castes() -> List[str]:
        """True Kin character types"""
        return [
            # The Toxic Arboreta of Ekuemekiyye
            "Horticulturist",
            "Priest of All Suns",
            "Priest of All Moons",
            "Syzygyrior",
            # The Ice-Sheathed Arcology of Ibul
            "Artifex",
            "Consul",
            "Praetorian",
            "Eunuch",
            # The Crustal Mortars of Yawningmoon
            "Child of the Hearth",
            "Child of the Wheel",
            "Child of the Deep",
            "Fuming God-Child",
        ]

    @staticmethod
    def callings() -> List[str]:
        """Mutated Human character types"""
        return [
            "Apostle",
            "Arconaut",
            "Greybeard",
            "Gunslinger",
            "Marauder",
            "Pilgrim",
            "Nomad",
            "Scholar",
            "Tinker",
            "Warden",
            "Water Merchant",
            "Watervine Farmer",
        ]

    @staticmethod
    def locations() -> List[str]:
        return [
            "Joppa",
            "Kyakukya",
            "The Six Day Stilt",
            "Grit Gate",
            "Bethesda Susa",
            "Golgotha",
            "The Tomb of the Eaters",
            "The Spindle",
            "Banana Grove",
            "Omonporch",
            "The Yd Freehold",
        ]

    @staticmethod
    def enemies() -> List[str]:
        return [
            "Chrome Pyramid",
            "Jilted Lover",
            "Legendary Snapjaw",
            "Putus Templar",
            "Sawhander",
            "Star Kraken",
            "Tyrant",
            "Slog of the Cloaca",
            "Rodanis Y",
        ]

    @staticmethod
    def factions() -> List[str]:
        return [
            "Barathrumites",
            "Consortium of Phyta",
            "Denizens of the Yd Freehold",
            "Disciples of the Sightless Way",
            "Farmers' Guild",
            "Mechanimists",
            "Putus Templar",
            "Seekers of the Sightless Way",
            "Sultanate",
            "Trolls",
        ]

    @staticmethod
    def artifacts() -> List[str]:
        return [
            "Stopsvalinn",
            "Ruin of House Isner",
            "Kindrish",
            "Wraith-Knight Templar",
            "Dreadroot",
            "Schemasoft Overclocking Chip",
            "Quantum Mote",
            "Stasis Pod",
        ]

    @staticmethod
    def quests() -> List[str]:
        return [
            "Find Eskhind",
            "The Earl of Omonporch",
            "Kith and Kin",
            "Pax Klanq",
            "Tomb Robbers",
            "Fraying Favorites",
            "The Golem",
            "Raising Indrix",
        ]

    @staticmethod
    def reputation_levels() -> List[str]:
        return [
            "Loved",
            "Cherished",
        ]

    @staticmethod
    def depths() -> List[str]:
        return [
            "depth 10",
            "depth 15",
            "depth 20",
            "depth 25",
        ]

    @staticmethod
    def levels() -> range:
        return range(10, 26, 5)

    @staticmethod
    def cybernetics() -> List[str]:
        """Subset of notable starting / arcology cybernetics for objectives"""
        return [
            "Optical Bioscanner",
            "Night Vision Implant",
            "Parabolic Muscular Subroutine",
            "Hyper-elastic Ankle Tendons",
            "Rapid Release Finger Flexors",
            "Stabilizer Arm Locks",
            "Translucent Skin",
            "Air Current Microsensor",
            "Cherubic Visage",
            "Nocturnal Apex",
        ]

    @staticmethod
    def water_ritual_counts() -> List[int]:
        return [4, 5, 6]

    # Mutation-related helper lists
    @staticmethod
    def physical_mutations() -> List[str]:
        return [
            "Burrowing Claws",
            "Multiple Arms",
            "Regeneration",
            "Carapace",
            "Wings",
            "Photosynthetic Skin",
            "Quills",
            "Night Vision",
        ]

    @staticmethod
    def mental_mutations() -> List[str]:
        return [
            "Temporal Fugue",
            "Precognition",
            "Teleportation",
            "Psychometry",
            "Beguiling",
            "Disintegration",
            "Sunder Mind",
            "Space-Time Vortex",
        ]

    @staticmethod
    def all_tracked_mutations() -> List[str]:
        return CavesOfQudGame.physical_mutations() + CavesOfQudGame.mental_mutations()

    @staticmethod
    def mutation_target_levels() -> List[int]:
        return [3, 5, 7, 10]

    @staticmethod
    def morphotypes() -> List[str]:
        return ["Chimera", "Esper", "Unstable Genome"]

    @staticmethod
    def defects() -> List[str]:
        return [
            "Evil Twin",
            "Nerve Poppy",
            "Irritable Genome",
            "Quantum Jitters",
            "Albino",
            "Myopic",
        ]

    @staticmethod
    def mutation_survival_levels() -> List[int]:
        return [10, 15, 20]

    @staticmethod
    def beguile_targets() -> List[str]:
        # subset of enemies suitable for a 'powerful beguile' objective
        return [
            "Chrome Pyramid",
            "Putus Templar",
            "Tyrant",
        ]

    @staticmethod
    def glimmer_levels() -> List[int]:
        return [10, 20, 30]

    @staticmethod
    def license_tiers() -> List[int]:
        return [4, 8, 12]

    @staticmethod
    def credit_wedge_counts() -> List[int]:
        return [3, 6, 9]

    @staticmethod
    def rapid_advancement_levels() -> List[int]:
        # Level 5 and every 10 thereafter are canonical triggers; offer early milestones
        return [5, 15, 25]


# Archipelago Options
# ...
