from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import OptionSet, Range


@dataclass
class DeathRoadToCanadaArchipelagoOptions:
    death_road_to_canada_modes: DeathRoadToCanadaModesOption
    death_road_to_canada_character_selection_methods: DeathRoadToCanadaCharacterSelectionMethodsOption
    death_road_to_canada_min_party_size: DeathRoadToCanadaMinPartySizeOption
    death_road_to_canada_max_party_size: DeathRoadToCanadaMaxPartySizeOption


class DeathRoadToCanadaGame(Game):
    name = "Death Road to Canada"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = DeathRoadToCanadaArchipelagoOptions

    @property
    def enabled_modes(self) -> set:
        return self.archipelago_options.death_road_to_canada_modes.value

    @property
    def enabled_character_selection_methods(self) -> set:
        return self.archipelago_options.death_road_to_canada_character_selection_methods.value

    @property
    def min_party_size(self) -> int:
        return self.archipelago_options.death_road_to_canada_min_party_size.value

    @property
    def max_party_size(self) -> int:
        return self.archipelago_options.death_road_to_canada_max_party_size.value

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play with Friendly Fire enabled",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="No using melee weapons",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="No using ranged weapons",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only use items from specific category",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use any healing items",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use vehicles",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must complete run on Hard difficulty",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="No purchasing items from stores",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot switch characters after game starts",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must keep all party members alive until Canada",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use any items with negative effects",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Play with permadeath enabled",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only one character per run, no recruitment",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use any food items",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Start run with minimal resources",
                data=dict(),
            ),
            # New constraints
            GameObjectiveTemplate(
                label="Win with a full team of four",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Win with at least one animal on your team",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Have at least three people in your party die",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Say 'Cool It!' at least three times",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Make it to the Canadian border with a working vehicle",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Kill at least 200 zombies in a single siege",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Kill fewer than 25 zombies in a single siege",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Start without a buddy",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives = []
        
        # Define all modes with their properties
        all_modes = {
            "standard": ("Standard Mode", False, True),  # (name, is_difficult, is_time_consuming)
            "rare_characters": ("Rare Characters Mode", True, True),
            "short_trip_to_heck": ("Short Trip to Heck Mode", True, False),
            "familiar_characters": ("Familiar Characters Mode", False, True),
        }
        
        # Filter to only enabled modes
        enabled_modes = [(name, diff, time) for key, (name, diff, time) in all_modes.items() 
                        if key in self.enabled_modes]
        
        # Character selection methods
        selection_methods = self.enabled_character_selection_methods
        
        # Generate objectives for each enabled mode and selection method
        for mode_name, is_difficult, is_time_consuming in enabled_modes:
            # Player chooses their own character (no placeholder)
            if "player_choice" in selection_methods:
                objectives.append(GameObjectiveTemplate(
                    label=f"Reach Canada in {mode_name} with your choice of character",
                    data=dict(),
                    is_time_consuming=is_time_consuming,
                    is_difficult=is_difficult,
                    weight=3,
                ))
            
            # Random character (no specific character assigned)
            if "random" in selection_methods:
                objectives.append(GameObjectiveTemplate(
                    label=f"Reach Canada in {mode_name} with a random character",
                    data=dict(),
                    is_time_consuming=is_time_consuming,
                    is_difficult=is_difficult,
                    weight=2,
                ))
            
            # KMK picks a specific character for the player
            if "kmk_assigned" in selection_methods:
                objectives.append(GameObjectiveTemplate(
                    label=f"Reach Canada in {mode_name} as CHARACTER",
                    data={"CHARACTER": (self.character_types, 1)},
                    is_time_consuming=is_time_consuming,
                    is_difficult=is_difficult,
                    weight=2,
                ))
        
        # Generate party size objectives within the specified range
        for size in range(self.min_party_size, self.max_party_size + 1):
            if size == 1:
                # Solo objectives for each selection method
                if "player_choice" in selection_methods:
                    objectives.append(GameObjectiveTemplate(
                        label=f"Reach Canada solo with your choice of character",
                        data=dict(),
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=3,
                    ))
                if "random" in selection_methods:
                    objectives.append(GameObjectiveTemplate(
                        label=f"Reach Canada solo with a random character",
                        data=dict(),
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=2,
                    ))
                if "kmk_assigned" in selection_methods:
                    objectives.append(GameObjectiveTemplate(
                        label=f"Reach Canada solo as CHARACTER",
                        data={"CHARACTER": (self.character_types, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=2,
                    ))
            else:
                # Multi-character party objectives
                if "player_choice" in selection_methods:
                    objectives.append(GameObjectiveTemplate(
                        label=f"Reach Canada with exactly {size} characters of your choice",
                        data=dict(),
                        is_time_consuming=True,
                        is_difficult=True if size == 4 else False,
                        weight=max(1, 4 - size),
                    ))
                if "random" in selection_methods:
                    objectives.append(GameObjectiveTemplate(
                        label=f"Reach Canada with exactly {size} random characters",
                        data=dict(),
                        is_time_consuming=True,
                        is_difficult=True if size == 4 else False,
                        weight=max(1, 4 - size),
                    ))
                if "kmk_assigned" in selection_methods:
                    objectives.append(GameObjectiveTemplate(
                        label=f"Reach Canada with exactly {size} characters: CHARACTERS",
                        data={"CHARACTERS": (self.character_types, size)},
                        is_time_consuming=True,
                        is_difficult=True if size == 4 else False,
                        weight=max(1, 4 - size),
                    ))
        
        # Additional objectives that work across modes
        objectives.extend([
            GameObjectiveTemplate(
                label="Reach Canada on DIFFICULTY difficulty",
                data={"DIFFICULTY": (self.difficulties, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Survive DAYS days",
                data={"DAYS": (self.days_survived, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect SURVIVOR_TYPE survivors",
                data={"SURVIVOR_TYPE": (self.survivor_roles, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Successfully navigate LOCATION",
                data={"LOCATION": (self.locations, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Earn AMOUNT money in a run",
                data={"AMOUNT": (self.money_amounts, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Find and use ITEM_TYPE",
                data={"ITEM_TYPE": (self.item_types, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a run with TRAIT_COMBO trait combination",
                data={"TRAIT_COMBO": (self.trait_combinations, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Survive encounter with ENEMY_TYPE",
                data={"ENEMY_TYPE": (self.enemy_types, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ])
        
        return objectives

    @staticmethod
    def character_types() -> List[str]:
        return [
            "The Boss",
            "The Cop",
            "The Athlete",
            "The Hacker",
            "The Nerd",
            "The Farmer",
            "The Waitress",
            "The Biker",
            "The Chef",
            "The Clown",
            "The Bouncer",
            "The Firefighter",
            "The Gamer",
            "The Rock Star",
            "The Mechanic",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
            "Ironman",
        ]

    @staticmethod
    def days_survived() -> range:
        return range(5, 21, 5)

    @staticmethod
    def party_sizes() -> List[int]:
        return [1, 2, 3, 4]

    @staticmethod
    def survivor_roles() -> List[str]:
        return [
            "Tough Guy",
            "Hacker",
            "Leader",
            "Athlete",
            "Chef",
            "Medic",
            "Crazy",
            "Religious",
            "Coward",
            "Idiot",
        ]

    @staticmethod
    def locations() -> List[str]:
        return [
            "Highway",
            "Gas Station",
            "Supermarket",
            "Hospital",
            "Roadside Diner",
            "Motel",
            "Police Station",
            "Military Base",
            "Farm",
            "Factory",
            "School",
            "Cemetery",
            "Bridge",
            "Checkpoint",
            "Border Town",
        ]

    @staticmethod
    def money_amounts() -> range:
        return range(100, 1001, 200)

    @staticmethod
    def item_types() -> List[str]:
        return [
            "Melee Weapon",
            "Ranged Weapon",
            "Healing Item",
            "Armor",
            "Vehicle",
            "Food",
            "Utility Item",
            "Rare Weapon",
            "Ammo",
            "Defense Tool",
        ]

    @staticmethod
    def trait_combinations() -> List[str]:
        return [
            "All Tough Characters",
            "All Hackers",
            "All Religious",
            "All Cowards",
            "Mixed Specialists",
            "All Crazy",
            "All Leaders",
            "All Athletes",
        ]

    @staticmethod
    def enemy_types() -> List[str]:
        return [
            "Zombie",
            "Zombie Horde",
            "Armed Survivor",
            "Mutant",
            "Gang Member",
            "Military Unit",
            "Infected Animal",
            "Crazed Scientist",
            "Rogue AI",
            "Boss Zombie",
        ]


# Archipelago Options
class DeathRoadToCanadaModesOption(OptionSet):
    """Select which game modes can be used for objectives. Multiple can be enabled."""
    display_name = "Enabled Game Modes"
    valid_keys = {"standard", "rare_characters", "short_trip_to_heck", "familiar_characters"}
    default = {"standard", "rare_characters", "short_trip_to_heck", "familiar_characters"}


class DeathRoadToCanadaCharacterSelectionMethodsOption(OptionSet):
    """Select which character selection methods can be used for objectives. Multiple can be enabled."""
    display_name = "Enabled Character Selection Methods"
    valid_keys = {"player_choice", "random", "kmk_assigned"}
    default = {"player_choice", "random", "kmk_assigned"}


class DeathRoadToCanadaMinPartySizeOption(Range):
    """Minimum party size for party size variation objectives."""
    display_name = "Minimum Party Size"
    range_start = 1
    range_end = 4
    default = 1


class DeathRoadToCanadaMaxPartySizeOption(Range):
    """Maximum party size for party size variation objectives."""
    display_name = "Maximum Party Size"
    range_start = 1
    range_end = 4
    default = 4
