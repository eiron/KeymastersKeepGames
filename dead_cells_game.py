from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, Toggle, Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DeadCellsArchipelagoOptions:
    dead_cells_include_progression_runs: DeadCellsIncludeProgressionRuns
    dead_cells_include_weapon_mastery: DeadCellsIncludeWeaponMastery
    dead_cells_include_boss_challenges: DeadCellsIncludeBossChallenges
    dead_cells_include_biome_exploration: DeadCellsIncludeBiomeExploration
    dead_cells_include_blueprint_collection: DeadCellsIncludeBlueprintCollection
    dead_cells_include_mutation_goals: DeadCellsIncludeMutationGoals
    dead_cells_include_difficulty_scaling: DeadCellsIncludeDifficultyScaling
    dead_cells_include_speed_challenges: DeadCellsIncludeSpeedChallenges
    dead_cells_playstyle_focus: DeadCellsPlaystyleFocus


class DeadCellsGame(Game):
    name = "Dead Cells"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
    ]

    is_adult_only_or_unrated = False

    options_cls = DeadCellsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective without using any healing items",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective using only WEAPON_TYPE weapons",
                data={"WEAPON_TYPE": (self.weapon_types, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without taking more than DAMAGE_COUNT hits",
                data={"DAMAGE_COUNT": (self.damage_limits, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective in under TIME_LIMIT minutes",
                data={"TIME_LIMIT": (self.time_limits, 1)},
            ),
        ])
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Progression Runs
        if self.include_progression_runs:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete a full run to BOSS",
                    data={"BOSS": (self.final_bosses, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Reach BIOME without dying",
                    data={"BIOME": (self.biomes, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete RUN_COUNT successful runs",
                    data={"RUN_COUNT": (self.run_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Collect CELL_COUNT cells in a single run",
                    data={"CELL_COUNT": (self.cell_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Weapon Mastery
        if self.include_weapon_mastery:
            mastery_templates = []
            
            if self.playstyle_focus in ["All", "Brutality"]:
                mastery_templates.extend([
                    GameObjectiveTemplate(
                        label="Complete a run using BRUTALITY_WEAPON",
                        data={"BRUTALITY_WEAPON": (self.brutality_weapons, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Unlock and upgrade BRUTALITY_WEAPON to ++ level",
                        data={"BRUTALITY_WEAPON": (self.brutality_weapons, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                ])
            
            if self.playstyle_focus in ["All", "Tactics"]:
                mastery_templates.extend([
                    GameObjectiveTemplate(
                        label="Complete a run using TACTICS_WEAPON",
                        data={"TACTICS_WEAPON": (self.tactics_weapons, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Unlock and upgrade TACTICS_WEAPON to ++ level",
                        data={"TACTICS_WEAPON": (self.tactics_weapons, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                ])
            
            if self.playstyle_focus in ["All", "Survival"]:
                mastery_templates.extend([
                    GameObjectiveTemplate(
                        label="Complete a run using SURVIVAL_WEAPON",
                        data={"SURVIVAL_WEAPON": (self.survival_weapons, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Unlock and upgrade SURVIVAL_WEAPON to ++ level",
                        data={"SURVIVAL_WEAPON": (self.survival_weapons, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                ])
            
            mastery_templates.extend([
                GameObjectiveTemplate(
                    label="Kill ENEMY_COUNT enemies with SKILL",
                    data={
                        "ENEMY_COUNT": (self.kill_counts, 1),
                        "SKILL": (self.skills, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])
            
            game_objective_templates.extend(mastery_templates)

        # Boss Challenges
        if self.include_boss_challenges:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Defeat BOSS without taking damage",
                    data={"BOSS": (self.bosses, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Defeat BOSS using only WEAPON_TYPE weapons",
                    data={
                        "BOSS": (self.bosses, 1),
                        "WEAPON_TYPE": (self.weapon_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Defeat all bosses in BIOME",
                    data={"BIOME": (self.boss_biomes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Biome Exploration
        if self.include_biome_exploration:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Fully explore BIOME (find all secrets)",
                    data={"BIOME": (self.biomes, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete all challenge rooms in BIOME",
                    data={"BIOME": (self.biomes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Find SECRET_COUNT secret areas",
                    data={"SECRET_COUNT": (self.secret_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Blueprint Collection
        if self.include_blueprint_collection:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Collect BLUEPRINT for EQUIPMENT",
                    data={
                        "BLUEPRINT": (self.blueprint_types, 1),
                        "EQUIPMENT": (self.equipment, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Unlock BLUEPRINT_COUNT blueprints",
                    data={"BLUEPRINT_COUNT": (self.blueprint_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Collect all blueprints from ENEMY_TYPE enemies",
                    data={"ENEMY_TYPE": (self.enemy_types, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Mutation Goals
        if self.include_mutation_goals:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete a run using MUTATION build",
                    data={"MUTATION": (self.mutation_builds, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Unlock and test MUTATION",
                    data={"MUTATION": (self.mutations, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create a synergy build using MUTATION_COMBO",
                    data={"MUTATION_COMBO": (self.mutation_combos, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Difficulty Scaling
        if self.include_difficulty_scaling:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete a run on BC_LEVEL Boss Cell difficulty",
                    data={"BC_LEVEL": (self.boss_cell_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Unlock BC_LEVEL Boss Cell",
                    data={"BC_LEVEL": (self.boss_cell_unlocks, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Survive MALAISE_LEVEL malaise infection",
                    data={"MALAISE_LEVEL": (self.malaise_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Speed Challenges
        if self.include_speed_challenges:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete a run to BOSS in under TIME_GOAL minutes",
                    data={
                        "BOSS": (self.final_bosses, 1),
                        "TIME_GOAL": (self.speed_goals, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete BIOME in under BIOME_TIME minutes",
                    data={
                        "BIOME_TYPE": (self.biomes, 1),
                        "BIOME_TIME": (self.biome_time_goals, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_progression_runs(self) -> bool:
        return self.archipelago_options.dead_cells_include_progression_runs.value

    @property
    def include_weapon_mastery(self) -> bool:
        return self.archipelago_options.dead_cells_include_weapon_mastery.value

    @property
    def include_boss_challenges(self) -> bool:
        return self.archipelago_options.dead_cells_include_boss_challenges.value

    @property
    def include_biome_exploration(self) -> bool:
        return self.archipelago_options.dead_cells_include_biome_exploration.value

    @property
    def include_blueprint_collection(self) -> bool:
        return self.archipelago_options.dead_cells_include_blueprint_collection.value

    @property
    def include_mutation_goals(self) -> bool:
        return self.archipelago_options.dead_cells_include_mutation_goals.value

    @property
    def include_difficulty_scaling(self) -> bool:
        return self.archipelago_options.dead_cells_include_difficulty_scaling.value

    @property
    def include_speed_challenges(self) -> bool:
        return self.archipelago_options.dead_cells_include_speed_challenges.value

    @property
    def playstyle_focus(self) -> str:
        return self.archipelago_options.dead_cells_playstyle_focus.value

    # Data lists
    @staticmethod
    def biomes() -> List[str]:
        return [
            "Prisoners' Quarters", "Promenade of the Condemned", "Toxic Sewers", "Depths",
            "Ossuary", "Ancient Sewers", "Ramparts", "Prison Depths", "Corrupted Prison",
            "Graveyard", "Cavern", "Forgotten Sepulcher", "Slumbering Sanctuary",
            "Stilt Village", "Clock Tower", "Time Keeper's Room", "Clock Room",
            "High Peak Castle", "Throne Room", "Observatory", "Undying Shores",
            "Mausoleum", "Fractured Shrines", "Distillery", "Morass of the Banished"
        ]

    @staticmethod
    def final_bosses() -> List[str]:
        return ["The Hand of the King", "The Giant", "The Collector", "Mama Tick", "The Queen"]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "The Concierge", "Conjunctivius", "Time Keeper", "The Hand of the King",
            "The Giant", "The Collector", "Mama Tick", "The Queen", "The Scarecrow"
        ]

    @staticmethod
    def boss_biomes() -> List[str]:
        return ["Prisoners' Quarters", "Ancient Sewers", "Clock Tower", "High Peak Castle"]

    @staticmethod
    def brutality_weapons() -> List[str]:
        return [
            "Rusty Sword", "Balanced Blade", "Blood Sword", "Twin Daggers", "Sadist's Stiletto",
            "Cursed Sword", "Broadsword", "Assassin's Dagger", "Frantic Sword", "Vorpan",
            "Hayabusa Gauntlets", "Meat Skewer", "Nutcracker", "Rapier", "Seismic Strike"
        ]

    @staticmethod
    def tactics_weapons() -> List[str]:
        return [
            "Bow and Endless Quiver", "Magic Missiles", "Ice Blast", "Throwing Knife",
            "Electric Whip", "Frost Blast", "Fire Blast", "Lightning Bolt", "Sonic Carbine",
            "Pyrotechnics", "Quick Bow", "Repeater Crossbow", "Hokuto's Bow", "Boomerang",
            "Giant Killer", "Alchemic Carbine", "War Javelin"
        ]

    @staticmethod
    def survival_weapons() -> List[str]:
        return [
            "Broadsword", "Lance", "War Spear", "Heavy Crossbow", "Rampart", "Flamethrower Turret",
            "Corrupted Power", "Explosive Crossbow", "Demolisher", "Shovel", "Scythe Claw",
            "Spite Sword", "Iron Staff", "Tombstone", "Toothpick", "Rhythm n' Bouzouki"
        ]

    @staticmethod
    def weapon_types() -> List[str]:
        return ["Brutality", "Tactics", "Survival", "Melee", "Ranged", "Shields"]

    @staticmethod
    def skills() -> List[str]:
        return [
            "Grenades", "Double Crossb-o-matic", "Heavy Turret", "Knife Dance", "Phaser",
            "Tornado", "Wolf Trap", "Death Orb", "Chakram", "Fire Grenade", "Ice Grenade",
            "Magnetic Grenade", "Vampirism", "Lacerating Aura", "Toxic Cloud", "Smoke Bomb"
        ]

    @staticmethod
    def equipment() -> List[str]:
        return [
            "Rusty Sword", "Bow", "Shield", "Grenade", "Heavy Turret", "Wolf Trap",
            "Amulet", "Power", "Tonic", "Outfit", "Mutation"
        ]

    @staticmethod
    def mutations() -> List[str]:
        return [
            "Combo", "Vengeance", "Extended Healing", "Alienation", "Adrenaline", "Velocity",
            "Tranquility", "Initiative", "Dead Inside", "Soldier Resistance", "Frenzy",
            "Berserker", "Brutality", "Emergency Triage", "What Doesn't Kill Me", "Necromancy",
            "Masochist", "Scheme", "Gastronomy", "Acceptance", "Blind Faith", "Open Wounds"
        ]

    @staticmethod
    def mutation_builds() -> List[str]:
        return [
            "Pure Brutality", "Pure Tactics", "Pure Survival", "Hybrid Brutality-Tactics",
            "Hybrid Brutality-Survival", "Hybrid Tactics-Survival", "Balanced Build"
        ]

    @staticmethod
    def mutation_combos() -> List[str]:
        return [
            "Necromancy + What Doesn't Kill Me", "Combo + Frenzy", "Vengeance + Dead Inside",
            "Scheme + Initiative", "Gastronomy + Extended Healing", "Open Wounds + Sadist's Stiletto"
        ]

    @staticmethod
    def blueprint_types() -> List[str]:
        return ["weapon", "skill", "mutation", "upgrade", "outfit"]

    @staticmethod
    def enemy_types() -> List[str]:
        return [
            "Zombies", "Bats", "Archers", "Shieldbearers", "Runners", "Bombers",
            "Slashers", "Rampagers", "Defenders", "Cannibals", "Golems"
        ]

    @staticmethod
    def boss_cell_levels() -> List[str]:
        return ["1BC", "2BC", "3BC", "4BC", "5BC"]

    @staticmethod
    def boss_cell_unlocks() -> List[str]:
        return ["1st Boss Cell", "2nd Boss Cell", "3rd Boss Cell", "4th Boss Cell", "5th Boss Cell"]

    @staticmethod
    def malaise_levels() -> List[str]:
        return ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 10"]

    # Ranges
    @staticmethod
    def run_counts() -> range:
        return range(1, 10, 2)

    @staticmethod
    def cell_counts() -> range:
        return range(50, 300, 50)

    @staticmethod
    def kill_counts() -> range:
        return range(10, 100, 10)

    @staticmethod
    def secret_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def blueprint_counts() -> range:
        return range(5, 30, 5)

    @staticmethod
    def speed_goals() -> range:
        return range(20, 60, 10)

    @staticmethod
    def biome_time_goals() -> range:
        return range(3, 15, 3)

    @staticmethod
    def damage_limits() -> range:
        return range(0, 10, 2)

    @staticmethod
    def time_limits() -> range:
        return range(5, 30, 5)


# Archipelago Options
class DeadCellsIncludeProgressionRuns(DefaultOnToggle):
    """Include progression run objectives (completing runs, reaching biomes)."""
    display_name = "Include Progression Runs"

class DeadCellsIncludeWeaponMastery(DefaultOnToggle):
    """Include weapon mastery objectives (unlocks, upgrades, kills)."""
    display_name = "Include Weapon Mastery"

class DeadCellsIncludeBossChallenges(DefaultOnToggle):
    """Include boss challenge objectives (no damage, specific weapons)."""
    display_name = "Include Boss Challenges"

class DeadCellsIncludeBiomeExploration(DefaultOnToggle):
    """Include biome exploration objectives (secrets, challenge rooms)."""
    display_name = "Include Biome Exploration"

class DeadCellsIncludeBlueprintCollection(DefaultOnToggle):
    """Include blueprint collection objectives."""
    display_name = "Include Blueprint Collection"

class DeadCellsIncludeMutationGoals(Toggle):
    """Include mutation and build objectives."""
    display_name = "Include Mutation Goals"

class DeadCellsIncludeDifficultyScaling(Toggle):  # Keep as False by default - difficulty scaling is specialized/harder
    """Include Boss Cell difficulty progression."""
    display_name = "Include Difficulty Scaling"
    default = False

class DeadCellsIncludeSpeedChallenges(Toggle):  # Keep as False by default - speed challenges are specialized/harder
    """Include speedrun and time challenge objectives."""
    display_name = "Include Speed Challenges"

class DeadCellsPlaystyleFocus(Choice):
    """Focus weapon objectives on specific stat builds."""
    display_name = "Playstyle Focus"
    option_all = "All"
    option_brutality = "Brutality"
    option_tactics = "Tactics"
    option_survival = "Survival"
    default = option_all
