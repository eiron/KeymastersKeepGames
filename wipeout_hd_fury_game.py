from __future__ import annotations

from dataclasses import dataclass
from typing import List

from Options import OptionSet, Range, DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class WipeoutHDFuryArchipelagoOptions:
    wipeout_hd_fury_team_selection: WipeoutHDFuryTeamSelection
    wipeout_hd_fury_include_speed_class_progression: WipeoutHDFuryIncludeSpeedClassProgression
    wipeout_hd_fury_include_zone_challenges: WipeoutHDFuryIncludeZoneChallenges
    wipeout_hd_fury_include_eliminator_mode: WipeoutHDFuryIncludeEliminatorMode
    wipeout_hd_fury_include_weapon_challenges: WipeoutHDFuryIncludeWeaponChallenges
    wipeout_hd_fury_race_count: WipeoutHDFuryRaceCount


class WipeoutHDFuryGame(Game):
    name = "Wipeout HD Fury"
    platform = KeymastersKeepGamePlatforms.PS3
    
    platforms_other = [KeymastersKeepGamePlatforms.PS4]  # Via Omega Collection
    
    is_adult_only_or_unrated = False
    
    options_cls = WipeoutHDFuryArchipelagoOptions
    
    @property
    def selected_teams(self) -> List[str]:
        return self.archipelago_options.wipeout_hd_fury_team_selection.value
    
    @property
    def include_speed_class_progression(self) -> bool:
        return self.archipelago_options.wipeout_hd_fury_include_speed_class_progression.value
    
    @property
    def include_zone_challenges(self) -> bool:
        return self.archipelago_options.wipeout_hd_fury_include_zone_challenges.value
    
    @property
    def include_eliminator_mode(self) -> bool:
        return self.archipelago_options.wipeout_hd_fury_include_eliminator_mode.value
    
    @property
    def include_weapon_challenges(self) -> bool:
        return self.archipelago_options.wipeout_hd_fury_include_weapon_challenges.value
    
    def race_count_range(self) -> range:
        return range(
            self.archipelago_options.wipeout_hd_fury_race_count.value,
            self.archipelago_options.wipeout_hd_fury_race_count.value * 2 + 1,
            self.archipelago_options.wipeout_hd_fury_race_count.value
        )
    
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        # Speed class restrictions
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective in Venom class only",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective in Flash class or higher",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective in Rapier class",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective in Phantom class",
                data={},
            ),
        ])
        
        # Team restrictions
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective using only TEAM ships",
                data={"TEAM": (self.selected_teams, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without using TEAM ships",
                data={"TEAM": (self.selected_teams, 1)},
            ),
        ])
        
        # Gameplay restrictions
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective without using Shield power-ups",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without using Turbo power-ups",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without using Autopilot",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without absorbing any weapons",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective with Pilot Assist disabled",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective while maintaining a perfect lap (no wall collisions)",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without using any weapons",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without doing any barrel rolls",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without failing a single barrel roll",
                data={},
            ),
        ])
        
        return constraints
    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives = []
        
        # Single Race objectives
        objectives.extend([
            GameObjectiveTemplate(
                label="Win COUNT Single Races on TRACK",
                data={
                    "COUNT": (self.race_count_range, 1),
                    "TRACK": (self.all_tracks, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Win COUNT Single Races using TEAM ships",
                data={
                    "COUNT": (self.race_count_range, 1),
                    "TEAM": (self.selected_teams, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Win COUNT Single Races on CPU_LEVEL difficulty",
                data={
                    "COUNT": (self.race_count_range, 1),
                    "CPU_LEVEL": (self.cpu_levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Finish in the top 3 in COUNT races on TRACK",
                data={
                    "COUNT": (self.race_count_range, 1),
                    "TRACK": (self.all_tracks, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=12,
            ),
            GameObjectiveTemplate(
                label="Win COUNT races on TRACK with CPU set to CPU_LEVEL",
                data={
                    "COUNT": (self.race_count_range, 1),
                    "TRACK": (self.all_tracks, 1),
                    "CPU_LEVEL": (self.cpu_levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Complete a perfect lap (no wall collisions) on TRACK in SPEED_CLASS class",
                data={
                    "TRACK": (self.all_tracks, 1),
                    "SPEED_CLASS": (self.speed_classes, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
        ])
        
        # Tournament objectives
        objectives.extend([
            GameObjectiveTemplate(
                label="Win COUNT Tournaments in SPEED_CLASS class",
                data={
                    "COUNT": (self.tournament_counts, 1),
                    "SPEED_CLASS": (self.speed_classes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Win a Tournament using only TEAM ships",
                data={
                    "TEAM": (self.selected_teams, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Finish in the top 3 of COUNT Tournaments",
                data={
                    "COUNT": (self.tournament_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Win a TRACK_NUMBER track Tournament in TEAM craft on SPEED_CLASS Speed Class with the CPU set to CPU_LEVEL",
                data={
                    "TRACK_NUMBER": (self.tournament_track_numbers, 1),
                    "TEAM": (self.selected_teams, 1),
                    "SPEED_CLASS": (self.speed_classes, 1),
                    "CPU_LEVEL": (self.cpu_levels, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win COUNT Tournaments on CPU_LEVEL difficulty",
                data={
                    "COUNT": (self.tournament_counts, 1),
                    "CPU_LEVEL": (self.cpu_levels, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
        ])
        
        # Time Trial objectives
        objectives.extend([
            GameObjectiveTemplate(
                label="Achieve a Gold medal in Time Trial on TRACK",
                data={
                    "TRACK": (self.all_tracks, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Complete COUNT Time Trials with Gold medals",
                data={
                    "COUNT": (self.time_trial_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Beat your personal best on TRACK by COUNT seconds",
                data={
                    "TRACK": (self.all_tracks, 1),
                    "COUNT": (self.time_improvements, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
        ])
        
        # Speed Lap objectives
        objectives.extend([
            GameObjectiveTemplate(
                label="Achieve a Speed Lap time under GOAL_TIME on TRACK",
                data={
                    "GOAL_TIME": (self.speed_lap_times, 1),
                    "TRACK": (self.all_tracks, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Set COUNT Speed Lap records in SPEED_CLASS class",
                data={
                    "COUNT": (self.speed_lap_counts, 1),
                    "SPEED_CLASS": (self.speed_classes, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
        ])
        
        # Speed Class Progression
        if self.include_speed_class_progression:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Win COUNT races in Venom class",
                    data={
                        "COUNT": (self.race_count_range, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Win COUNT races in Flash class",
                    data={
                        "COUNT": (self.race_count_range, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Win COUNT races in Rapier class",
                    data={
                        "COUNT": (self.race_count_range, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Win COUNT races in Phantom class",
                    data={
                        "COUNT": (self.race_count_range, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Complete a race in each speed class (Venom, Flash, Rapier, Phantom)",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
            ])
        
        # Zone mode objectives
        if self.include_zone_challenges:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Reach Zone ZONE_NUMBER on TRACK",
                    data={
                        "ZONE_NUMBER": (self.zone_levels, 1),
                        "TRACK": (self.all_tracks, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Reach Zone ZONE_NUMBER on any Zone track",
                    data={
                        "ZONE_NUMBER": (self.zone_levels_hard, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Complete COUNT Zone events reaching at least Zone ZONE_NUMBER",
                    data={
                        "COUNT": (self.zone_event_counts, 1),
                        "ZONE_NUMBER": (self.zone_levels, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Reach Zone 50 on ZONE_TRACK",
                    data={
                        "ZONE_TRACK": (self.zone_tracks, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Reach Zone 75 on any track",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
            ])
        
        # Zone Battle objectives (Fury DLC)
        if self.include_zone_challenges:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Win COUNT Zone Battle events",
                    data={
                        "COUNT": (self.zone_battle_counts, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Win a Zone Battle event on ZONE_TRACK",
                    data={
                        "ZONE_TRACK": (self.zone_tracks, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Win a Zone Battle event without taking damage",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
            ])
        
        # Detonator objectives (Fury DLC)
        objectives.extend([
            GameObjectiveTemplate(
                label="Score POINTS points in a single Detonator event",
                data={
                    "POINTS": (self.detonator_scores, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Complete COUNT Detonator events with Bronze medal or better",
                data={
                    "COUNT": (self.detonator_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Destroy COUNT bombs in a single Detonator event",
                data={
                    "COUNT": (self.bomb_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
        ])
        
        # Eliminator mode objectives
        if self.include_eliminator_mode:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Win COUNT Eliminator events",
                    data={
                        "COUNT": (self.eliminator_counts, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=7,
                ),
                GameObjectiveTemplate(
                    label="Achieve COUNT eliminations in a single Eliminator event",
                    data={
                        "COUNT": (self.elimination_targets, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Win an Eliminator event on TRACK",
                    data={
                        "TRACK": (self.all_tracks, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Win COUNT Eliminator events using TEAM ships",
                    data={
                        "COUNT": (self.eliminator_counts, 1),
                        "TEAM": (self.selected_teams, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Win COUNT Eliminator events on CPU_LEVEL difficulty",
                    data={
                        "COUNT": (self.eliminator_counts, 1),
                        "CPU_LEVEL": (self.cpu_levels, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Finish an Eliminator event without being eliminated",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
            ])
        
        # Weapon-based objectives
        if self.include_weapon_challenges:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Score COUNT eliminations using WEAPON in Eliminator mode",
                    data={
                        "COUNT": (self.weapon_elimination_counts, 1),
                        "WEAPON": (self.offensive_weapons, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Win a race using only WEAPON_TYPE weapons",
                    data={
                        "WEAPON_TYPE": (self.weapon_types, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Absorb COUNT weapons for shield energy in a single race",
                    data={
                        "COUNT": (self.absorption_counts, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Complete a race without firing any offensive weapons",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
            ])
        
        # Track mastery objectives
        objectives.extend([
            GameObjectiveTemplate(
                label="Complete COUNT perfect laps on TRACK (no wall collisions)",
                data={
                    "COUNT": (self.perfect_lap_counts, 1),
                    "TRACK": (self.all_tracks, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win races on COUNT different HD tracks",
                data={
                    "COUNT": (self.track_variety_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win races on COUNT different Fury tracks",
                data={
                    "COUNT": (self.fury_track_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
        ])
        
        # Advanced race challenge objectives
        objectives.extend([
            GameObjectiveTemplate(
                label="Lap at least 2 other contenders in a single race and win it",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a single race without using a Shield",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Without failing a single barrel roll in 2 races, win both of them",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a single race without doing any barrel rolls",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a single race without firing any weapons",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a single race without absorbing any weapons",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a single race without using a Turbo",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Eliminate at least one other contender in 2 races and win both",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Have at least 2 perfect laps in 2 races and win both",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Hit every contender at least once in a single race and win it",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
        ])
        
        # Campaign objectives
        objectives.extend([
            GameObjectiveTemplate(
                label="Complete COUNT events in the HD Campaign",
                data={
                    "COUNT": (self.campaign_event_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete COUNT events in the Fury Campaign",
                data={
                    "COUNT": (self.fury_campaign_counts, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Unlock all ships in the game",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
        ])
        
        return objectives
    
    # Data lists
    @staticmethod
    def all_teams() -> List[str]:
        """All 12 teams available in Wipeout HD"""
        return [
            "FEISAR", "Qirex", "Piranha", "AG Systems", "Triakis", "Goteki 45",
            "EG-X", "Assegai", "Mirage", "Harimau", "Auricom", "Icaras"
        ]
    
    @staticmethod
    def hd_tracks() -> List[str]:
        """Original HD tracks"""
        return [
            "Vineta K", "Anulpha Pass", "Moa Therma", "Chenghou Project",
            "Metropia", "Sebenco Climb", "Ubermall", "Sol 2"
        ]
    
    @staticmethod
    def fury_tracks() -> List[str]:
        """Fury expansion tracks"""
        return [
            "Talon's Junction", "The Amphiseum", "Modesto Heights", "Tech De Ra"
        ]
    
    @staticmethod
    def zone_tracks() -> List[str]:
        """Zone-only tracks from Fury"""
        return [
            "Pro Tozo", "Mallavol", "Corridon 12", "Syncopia"
        ]
    
    def all_tracks(self) -> List[str]:
        """All tracks combined"""
        return self.hd_tracks() + self.fury_tracks()
    
    @staticmethod
    def speed_classes() -> List[str]:
        """Speed classes from slowest to fastest"""
        return ["Venom", "Flash", "Rapier", "Phantom"]
    
    @staticmethod
    def game_modes() -> List[str]:
        """Available game modes"""
        return [
            "Single Race", "Tournament", "Speed Lap", "Time Trial", "Zone",
            "Eliminator", "Zone Battle", "Detonator"
        ]
    
    @staticmethod
    def offensive_weapons() -> List[str]:
        """Offensive weapons available"""
        return [
            "Missile", "Rockets", "Cannon", "Plasma", "Quake", "Leech Beam"
        ]
    
    @staticmethod
    def defensive_weapons() -> List[str]:
        """Defensive weapons available"""
        return ["Mines", "Bomb", "Shield"]
    
    @staticmethod
    def assistive_weapons() -> List[str]:
        """Assistive power-ups"""
        return ["Turbo", "Autopilot"]
    
    @staticmethod
    def weapon_types() -> List[str]:
        """Weapon categories"""
        return ["Offensive", "Defensive", "Assistive"]
    
    @staticmethod
    def cpu_levels() -> List[str]:
        """CPU difficulty levels"""
        return ["Novice", "Skilled", "Pro", "Elite"]
    
    @staticmethod
    def tournament_track_numbers() -> List[int]:
        """Tournament track counts (3, 4, or 8 tracks)"""
        return [3, 4, 8]
    
    @staticmethod
    def tournament_counts() -> List[int]:
        return [1, 2, 3, 5]
    
    @staticmethod
    def time_trial_counts() -> List[int]:
        return [3, 5, 8, 10]
    
    @staticmethod
    def speed_lap_counts() -> List[int]:
        return [3, 5, 8]
    
    @staticmethod
    def time_improvements() -> List[int]:
        """Seconds to improve by"""
        return [2, 5, 10]
    
    @staticmethod
    def speed_lap_times() -> List[str]:
        return ["1:30", "1:00", "0:45", "0:30"]
    
    @staticmethod
    def zone_levels() -> List[int]:
        """Zone milestones"""
        return [20, 30, 40, 50]
    
    @staticmethod
    def zone_levels_hard() -> List[int]:
        """Difficult zone milestones"""
        return [60, 70, 75]
    
    @staticmethod
    def zone_event_counts() -> List[int]:
        return [3, 5, 10]
    
    @staticmethod
    def zone_battle_counts() -> List[int]:
        return [3, 5, 8, 10]
    
    @staticmethod
    def detonator_scores() -> List[int]:
        """Target scores in Detonator mode"""
        return [50000, 100000, 150000, 200000]
    
    @staticmethod
    def detonator_counts() -> List[int]:
        return [3, 5, 8]
    
    @staticmethod
    def bomb_counts() -> List[int]:
        """Large bombs to destroy in Detonator"""
        return [5, 10, 14]
    
    @staticmethod
    def eliminator_counts() -> List[int]:
        return [3, 5, 8, 10]
    
    @staticmethod
    def elimination_targets() -> List[int]:
        """Eliminations to achieve in single event"""
        return [3, 5, 8, 10]
    
    @staticmethod
    def weapon_elimination_counts() -> List[int]:
        """Eliminations with specific weapon"""
        return [3, 5, 8]
    
    @staticmethod
    def absorption_counts() -> List[int]:
        """Weapons to absorb for energy"""
        return [3, 5, 8, 10]
    
    @staticmethod
    def perfect_lap_counts() -> List[int]:
        return [1, 3, 5]
    
    @staticmethod
    def track_variety_counts() -> List[int]:
        """Number of different tracks"""
        return [4, 6, 8]
    
    @staticmethod
    def fury_track_counts() -> List[int]:
        """Number of Fury tracks"""
        return [2, 3, 4]
    
    @staticmethod
    def campaign_event_counts() -> List[int]:
        """HD Campaign events (87 total)"""
        return [20, 40, 60, 87]
    
    @staticmethod
    def fury_campaign_counts() -> List[int]:
        """Fury Campaign events (80 total)"""
        return [20, 40, 60, 80]


# Archipelago Options
class WipeoutHDFuryTeamSelection(OptionSet):
    """
    Defines which racing teams can be selected for challenges.
    """
    display_name = "Wipeout HD Fury Team Selection"
    
    default = [
        "FEISAR", "Qirex", "Piranha", "AG Systems", "Triakis", "Goteki 45",
        "EG-X", "Assegai", "Mirage", "Harimau", "Auricom", "Icaras"
    ]


class WipeoutHDFuryIncludeSpeedClassProgression(DefaultOnToggle):
    """
    Include objectives that require progressing through different speed classes (Venom → Phantom).
    """
    display_name = "Include Speed Class Progression"


class WipeoutHDFuryIncludeZoneChallenges(DefaultOnToggle):
    """
    Include Zone mode challenges that test high-speed endurance and reflexes.
    """
    display_name = "Include Zone Challenges"


class WipeoutHDFuryIncludeEliminatorMode(DefaultOnToggle):
    """
    Include Eliminator mode objectives focused on combat and weapon usage.
    """
    display_name = "Include Eliminator Mode"


class WipeoutHDFuryIncludeWeaponChallenges(DefaultOnToggle):
    """
    Include objectives requiring specific weapon usage and mastery.
    """
    display_name = "Include Weapon Challenges"


class WipeoutHDFuryRaceCount(Range):
    """
    Number of races to complete in objectives.
    """
    display_name = "Race Count"
    range_start = 3
    range_end = 20
    default = 10
