from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import DefaultOnToggle


@dataclass
class RanchOfRivershineOptions:
    ranch_of_rivershine_include_horse_training: RanchOfRivershineIncludeHorseTraining
    ranch_of_rivershine_include_horse_care: RanchOfRivershineIncludeHorseCare
    ranch_of_rivershine_include_competitions: RanchOfRivershineIncludeCompetitions
    ranch_of_rivershine_include_breeding: RanchOfRivershineIncludeBreeding
    ranch_of_rivershine_include_exploration: RanchOfRivershineIncludeExploration
    ranch_of_rivershine_include_farming: RanchOfRivershineIncludeFarming
    ranch_of_rivershine_include_wild_horses: RanchOfRivershineIncludeWildHorses
    ranch_of_rivershine_include_social: RanchOfRivershineIncludeSocial
    ranch_of_rivershine_include_crafting: RanchOfRivershineIncludeCrafting
    ranch_of_rivershine_include_riding_arena: RanchOfRivershineIncludeRidingArena
    ranch_of_rivershine_include_ranch_upgrades: RanchOfRivershineIncludeRanchUpgrades


class RanchOfRivershineGame(Game):
    name = "Ranch of Rivershine"
    platform = KeymastersKeepGamePlatforms.PC

    is_adult_only_or_unrated = False

    options_cls = RanchOfRivershineOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return []

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives = []

        # Horse Training Objectives
        if self.archipelago_options.ranch_of_rivershine_include_horse_training:
            training_objectives = [
                # Speed training
                GameObjectiveTemplate(
                    label="Train a horse's Speed skill to 25%",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Train a horse's Speed skill to 50%",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Train a horse's Speed skill to 75%",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=30
                ),
                GameObjectiveTemplate(
                    label="Train a horse's Speed skill to 100%",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=15
                ),
                # Endurance training
                GameObjectiveTemplate(
                    label="Train a horse's Endurance skill to 25%",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Train a horse's Endurance skill to 50%",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Train a horse's Endurance skill to 75%",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=30
                ),
                GameObjectiveTemplate(
                    label="Train a horse's Endurance skill to 100%",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=15
                ),
                # Jump training
                GameObjectiveTemplate(
                    label="Train a horse's Jump skill to Intermediate level (25%)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Train a horse's Jump skill to Advanced level (50%)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Train a horse's Jump skill to Expert level (75%)",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=30
                ),
                GameObjectiveTemplate(
                    label="Train a horse's Jump skill to 100%",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=15
                ),
                # Flexibility training
                GameObjectiveTemplate(
                    label="Train a horse's Flexibility skill to 25%",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Train a horse's Flexibility skill to 50%",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Train a horse's Flexibility skill to 75%",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=30
                ),
                GameObjectiveTemplate(
                    label="Train a horse's Flexibility skill to 100%",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=15
                ),
                # Location-specific training
                GameObjectiveTemplate(
                    label="Train a horse at Lupine Meadow (Speed bonus)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Train a horse at Pine Forest (Endurance bonus)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Train a horse at Crystal Lake (Jump bonus)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Train a horse at Rocky Mountain (Flexibility bonus)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                # Accelerated training with grain
                GameObjectiveTemplate(
                    label="Feed a horse Corn before training Speed",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Feed a horse Barley before training Endurance",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Feed a horse Wheat before training Jump",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Feed a horse Milo before training Flexibility",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                # Multi-skill training
                GameObjectiveTemplate(
                    label="Train two skills simultaneously on a single horse",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Fully train a horse in all four skills to 100%",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=10
                ),
            ]
            objectives.extend(training_objectives)

        # Horse Care Objectives
        if self.archipelago_options.ranch_of_rivershine_include_horse_care:
            care_objectives = [
                GameObjectiveTemplate(
                    label="Groom a horse",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=75
                ),
                GameObjectiveTemplate(
                    label="Feed all your horses",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Keep a horse's affection above 75%",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Maintain perfect care for a horse for 7 in-game days",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=40
                ),
                GameObjectiveTemplate(
                    label="Use medicine to treat a horse",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Equip horse tack on a horse",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Purchase new equipment for your horses",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
            ]
            objectives.extend(care_objectives)

        # Competition Objectives
        if self.archipelago_options.ranch_of_rivershine_include_competitions:
            competition_objectives = [
                GameObjectiveTemplate(
                    label="Enter a horse into a Beginner level competition",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Win a Beginner level competition",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Enter a horse into an Intermediate level competition",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Win an Intermediate level competition",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=45
                ),
                GameObjectiveTemplate(
                    label="Enter a horse into an Advanced level competition",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=40
                ),
                GameObjectiveTemplate(
                    label="Win an Advanced level competition",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=30
                ),
                GameObjectiveTemplate(
                    label="Enter a horse into an Expert level competition",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=25
                ),
                GameObjectiveTemplate(
                    label="Win an Expert level competition",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=15
                ),
                GameObjectiveTemplate(
                    label="Earn a competition ribbon",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Earn 5 competition ribbons",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=40
                ),
                GameObjectiveTemplate(
                    label="Compete in a Trail Racing event",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Win a Trail Racing event",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=40
                ),
            ]
            objectives.extend(competition_objectives)

        # Breeding Objectives
        if self.archipelago_options.ranch_of_rivershine_include_breeding:
            breeding_objectives = [
                GameObjectiveTemplate(
                    label="Breed two horses together",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Raise a foal from birth",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Breed a horse with high skill potential",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=40
                ),
                GameObjectiveTemplate(
                    label="Breed a horse with a specific coat pattern",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=35
                ),
                GameObjectiveTemplate(
                    label="Breed three generations of horses in one bloodline",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=25
                ),
                GameObjectiveTemplate(
                    label="Purchase a horse from the auction house",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Purchase a Common horse from the auction house",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Purchase a Legendary horse from the auction house",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=30
                ),
            ]
            objectives.extend(breeding_objectives)

        # Exploration Objectives
        if self.archipelago_options.ranch_of_rivershine_include_exploration:
            exploration_objectives = [
                GameObjectiveTemplate(
                    label="Visit Rivershine Town",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Explore Lupine Meadow",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Explore Pine Forest",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Explore Crystal Lake",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Explore Rocky Mountain",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Explore Azure Coast",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Visit all exploration locations in one day",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=35
                ),
                GameObjectiveTemplate(
                    label="Find a chest while exploring",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Open 5 chests",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=40
                ),
                GameObjectiveTemplate(
                    label="Use a Horse Statue to boost a skill",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Find all Horse Statues in one location",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=40
                ),
            ]
            objectives.extend(exploration_objectives)

        # Farming Objectives
        if self.archipelago_options.ranch_of_rivershine_include_farming:
            farming_objectives = [
                # Grains for training
                GameObjectiveTemplate(
                    label="Plant Corn seeds",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Plant Barley seeds",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Plant Wheat seeds",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Plant Milo seeds",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                # Hay crops
                GameObjectiveTemplate(
                    label="Plant Timothy Hay seeds",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Plant Oats seeds",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Plant Orchard Grass seeds",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Plant Alfalfa Hay seeds",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                # Vegetables and fruits
                GameObjectiveTemplate(
                    label="Plant Carrot seeds",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Plant Cucumber seeds",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Plant Pumpkin seeds",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Plant Watermelon seeds",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                # General farming
                GameObjectiveTemplate(
                    label="Harvest crops from your farm",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=75
                ),
                GameObjectiveTemplate(
                    label="Grow all four training grain types (Corn, Barley, Wheat, Milo)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=45
                ),
                GameObjectiveTemplate(
                    label="Purchase seeds from Aisha Jamil",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Forage for grain while exploring",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Collect Yellow Flowers while foraging",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Grow crops in all seasons using Shield Fertilizer",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=40
                ),
                GameObjectiveTemplate(
                    label="Harvest a crop boosted with Rich Fertilizer",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=50
                ),
            ]
            objectives.extend(farming_objectives)

        # Wild Horse Objectives
        if self.archipelago_options.ranch_of_rivershine_include_wild_horses:
            wild_horse_objectives = [
                GameObjectiveTemplate(
                    label="Encounter a Wild Horse",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Tame a Wild Horse",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Add a Wild Horse to your ranch",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=45
                ),
                GameObjectiveTemplate(
                    label="Train a Wild Horse to competition level",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=30
                ),
            ]
            objectives.extend(wild_horse_objectives)

        # Social/NPC Objectives
        if self.archipelago_options.ranch_of_rivershine_include_social:
            social_objectives = [
                GameObjectiveTemplate(
                    label="Talk to Aisha Jamil (Seed Shop)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Talk to George Robinson",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Talk to Shin Dae",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Talk to Jai Maji",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Talk to Liam Flinn (Ranch Upgrades)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Talk to Madelaine Beauchamp",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Talk to River (Riding Arena Courses)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Talk to Orion Gallio (Stylist/Dyes)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Talk to Daphne Woolsey",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Talk to Amelia Trotter (Veterinarian)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Meet all NPCs in Rivershine Town",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=40
                ),
            ]
            objectives.extend(social_objectives)

        # Crafting Objectives
        if self.archipelago_options.ranch_of_rivershine_include_crafting:
            crafting_objectives = [
                # Medicine Crafting
                GameObjectiveTemplate(
                    label="Purchase a medicine recipe from Amelia Trotter",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Craft Common Cold Remedy",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Craft Fertility Boost medicine",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Craft Hair Growth medicine",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Craft 5 different medicine types",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=35
                ),
                # Dye Crafting
                GameObjectiveTemplate(
                    label="Purchase a dye recipe from Orion Gallio",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Find a dye recipe in a chest",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Craft a dye",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Dye a horse's coat",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Craft 3 different dye colors",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=40
                ),
                # Fertilizer Crafting
                GameObjectiveTemplate(
                    label="Craft Swift Fertilizer",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Craft Rich Fertilizer",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Craft Shield Fertilizer",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Craft Lucky Fertilizer",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=45
                ),
                GameObjectiveTemplate(
                    label="Use fertilizer on your crops",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                # Animal Feed
                GameObjectiveTemplate(
                    label="Craft Animal Feed",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
            ]
            objectives.extend(crafting_objectives)

        # Riding Arena Objectives
        if self.archipelago_options.ranch_of_rivershine_include_riding_arena:
            riding_arena_objectives = [
                # Purchase courses
                GameObjectiveTemplate(
                    label="Purchase a Riding Arena course from River",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                # Cavaletti Courses
                GameObjectiveTemplate(
                    label="Complete a Beginner Cavaletti Course",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Complete an Intermediate Cavaletti Course",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Complete an Advanced Cavaletti Course",
                    data={},
                    is_difficult=True,
                    is_time_consuming=False,
                    weight=35
                ),
                # Flower Fence Courses
                GameObjectiveTemplate(
                    label="Complete a Beginner Flower Fence Course",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Complete an Intermediate Flower Fence Course",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Complete an Advanced Flower Fence Course",
                    data={},
                    is_difficult=True,
                    is_time_consuming=False,
                    weight=35
                ),
                # Country Barrel Courses
                GameObjectiveTemplate(
                    label="Complete a Beginner Country Barrel Course",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Complete an Intermediate Country Barrel Course",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Complete an Advanced Country Barrel Course",
                    data={},
                    is_difficult=True,
                    is_time_consuming=False,
                    weight=35
                ),
                # General arena objectives
                GameObjectiveTemplate(
                    label="Train jumping skills using a Riding Arena",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Complete all 3 course types at Beginner level",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=40
                ),
            ]
            objectives.extend(riding_arena_objectives)

        # Ranch Upgrades Objectives
        if self.archipelago_options.ranch_of_rivershine_include_ranch_upgrades:
            ranch_upgrade_objectives = [
                GameObjectiveTemplate(
                    label="Purchase additional farm plots from Liam Flinn",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Expand your ranch's capacity",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=45
                ),
                GameObjectiveTemplate(
                    label="Purchase farm animals (chickens, sheep, or goats)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=55
                ),
                GameObjectiveTemplate(
                    label="Collect eggs from chickens",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Collect wool from sheep or goats",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=60
                ),
                GameObjectiveTemplate(
                    label="Feed all farm animals with Animal Feed",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=65
                ),
                GameObjectiveTemplate(
                    label="Obtain chickens of all 4 color varieties",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=35
                ),
                GameObjectiveTemplate(
                    label="Plant a fruit tree (Apple or Pear)",
                    data={},
                    is_difficult=False,
                    is_time_consuming=False,
                    weight=50
                ),
                GameObjectiveTemplate(
                    label="Harvest from a fruit tree",
                    data={},
                    is_difficult=False,
                    is_time_consuming=True,
                    weight=40
                ),
            ]
            objectives.extend(ranch_upgrade_objectives)

        return objectives


class RanchOfRivershineIncludeHorseTraining(DefaultOnToggle):
    """
    Include horse training objectives (Speed, Endurance, Jump, Flexibility skills).
    """
    display_name = "Ranch of Rivershine Include Horse Training Objectives"


class RanchOfRivershineIncludeHorseCare(DefaultOnToggle):
    """
    Include horse care objectives (grooming, feeding, affection, equipment).
    """
    display_name = "Ranch of Rivershine Include Horse Care Objectives"


class RanchOfRivershineIncludeCompetitions(DefaultOnToggle):
    """
    Include competition objectives (entering and winning competitions at various levels).
    """
    display_name = "Ranch of Rivershine Include Competition Objectives"


class RanchOfRivershineIncludeBreeding(DefaultOnToggle):
    """
    Include breeding objectives (breeding horses, raising foals, auction house).
    """
    display_name = "Ranch of Rivershine Include Breeding Objectives"


class RanchOfRivershineIncludeExploration(DefaultOnToggle):
    """
    Include exploration objectives (visiting locations, finding chests, horse statues).
    """
    display_name = "Ranch of Rivershine Include Exploration Objectives"


class RanchOfRivershineIncludeFarming(DefaultOnToggle):
    """
    Include farming objectives (planting and harvesting crops, foraging).
    """
    display_name = "Ranch of Rivershine Include Farming Objectives"


class RanchOfRivershineIncludeWildHorses(DefaultOnToggle):
    """
    Include wild horse objectives (encountering, taming, and training wild horses).
    """
    display_name = "Ranch of Rivershine Include Wild Horse Objectives"


class RanchOfRivershineIncludeSocial(DefaultOnToggle):
    """
    Include social objectives (talking to NPCs in Rivershine Town).
    """
    display_name = "Ranch of Rivershine Include Social/NPC Objectives"


class RanchOfRivershineIncludeCrafting(DefaultOnToggle):
    """
    Include crafting objectives (medicine, dyes, fertilizers, animal feed).
    """
    display_name = "Ranch of Rivershine Include Crafting Objectives"


class RanchOfRivershineIncludeRidingArena(DefaultOnToggle):
    """
    Include Riding Arena objectives (Cavaletti, Flower Fence, Country Barrel courses).
    """
    display_name = "Ranch of Rivershine Include Riding Arena Objectives"


class RanchOfRivershineIncludeRanchUpgrades(DefaultOnToggle):
    """
    Include ranch upgrade objectives (farm plots, farm animals, fruit trees).
    """
    display_name = "Ranch of Rivershine Include Ranch Upgrade Objectives"
