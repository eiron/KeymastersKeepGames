from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle, DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CallOfDutyBlackOps7ArchipelagoOptions:
    call_of_duty_black_ops_7_enable_multiplayer: CallOfDutyBlackOps7EnableMultiplayer
    call_of_duty_black_ops_7_enable_zombies: CallOfDutyBlackOps7EnableZombies
    call_of_duty_black_ops_7_include_post_launch_weapons: CallOfDutyBlackOps7IncludePostLaunchWeapons
    call_of_duty_black_ops_7_include_party_games: CallOfDutyBlackOps7IncludePartyGames


class CallOfDutyBlackOps7Game(Game):
    name = "Call of Duty: Black Ops 7"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = CallOfDutyBlackOps7ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()

        if self.enable_multiplayer:
            objectives += self.multiplayer_objectives()

        if self.enable_zombies:
            objectives += self.zombies_objectives()

        return objectives

    def multiplayer_objectives(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Complete 3 matches of GAMEMODE",
                data={
                    "GAMEMODE": (self.gamemodes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Win a match of GAMEMODE",
                data={
                    "GAMEMODE": (self.gamemodes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Get 10 kills with WEAPON",
                data={
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Get 10 METHOD kills",
                data={
                    "METHOD": (self.methods_multiplayer, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Deploy SCORESTREAK",
                data={
                    "SCORESTREAK": (self.scorestreaks_easy, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Deploy SCORESTREAK",
                data={
                    "SCORESTREAK": (self.scorestreaks_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Use FIELDUPGRADE 3 times",
                data={
                    "FIELDUPGRADE": (self.field_upgrades_multiplayer, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Capture 5 Objectives",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Appear in Top 3",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
            ),
        ]

        if self.include_post_launch_weapons:
            objectives.append(
                GameObjectiveTemplate(
                    label="Get 10 kills with DLCWEAPON",
                    data={
                        "DLCWEAPON": (self.dlc_weapons, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            )

        if self.include_party_games:
            objectives.append(
                GameObjectiveTemplate(
                    label="Complete 3 matches of PARTYGAME",
                    data={
                        "PARTYGAME": (self.party_games, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            )
            objectives.append(
                GameObjectiveTemplate(
                    label="Win a match of PARTYGAME",
                    data={
                        "PARTYGAME": (self.party_games, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            )

        return objectives

    def zombies_objectives(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Exfil on round ROUND on MAP",
                data={
                    "ROUND": (self.rounds, 1),
                    "MAP": (self.maps_zombies, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Exfil on round ROUND on MAP in Cursed Mode",
                data={
                    "ROUND": (self.rounds, 1),
                    "MAP": (self.maps_zombies, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Complete 5 TEDD Tasks on MAP",
                data={
                    "MAP": (self.maps_zombies, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Reach round 20 on MAP while CHALLENGE",
                data={
                    "MAP": (self.maps_zombies, 1),
                    "CHALLENGE": (self.challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Complete Main Quest on MAP in Directed Mode",
                data={
                    "MAP": (self.maps_standard, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Complete Main Quest on MAP in Standard Mode",
                data={
                    "MAP": (self.maps_standard, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Complete any side easter egg on MAP",
                data={
                    "MAP": (self.maps_standard, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Kill 200 zombies with WEAPON",
                data={
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Kill 200 zombies with WONDERWEAPON",
                data={
                    "WONDERWEAPON": (self.wonder_weapons, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Upgrade WEAPON to Legendary rarity",
                data={
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Upgrade WONDERWEAPON to Legendary rarity",
                data={
                    "WONDERWEAPON": (self.wonder_weapons, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Use the Pack-A-Punch to upgrade WEAPON to Tier III",
                data={
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Use the Pack-A-Punch to upgrade WONDERWEAPON to Tier III",
                data={
                    "WONDERWEAPON": (self.wonder_weapons, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Get 100 METHOD kills on zombies",
                data={
                    "METHOD": (self.methods_zombies, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
            GameObjectiveTemplate(
                label="Use FIELDUPGRADE 5 times",
                data={
                    "FIELDUPGRADE": (self.field_upgrades_zombies, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
            ),
        ]

        if self.include_post_launch_weapons:
            objectives.append(
                GameObjectiveTemplate(
                    label="Kill 200 zombies with DLCWEAPON",
                    data={
                        "DLCWEAPON": (self.dlc_weapons, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            )
            objectives.append(
                GameObjectiveTemplate(
                    label="Upgrade DLCWEAPON to Legendary rarity",
                    data={
                        "DLCWEAPON": (self.dlc_weapons, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            )
            objectives.append(
                GameObjectiveTemplate(
                    label="Use the Pack-A-Punch to upgrade DLCWEAPON to Tier III",
                    data={
                        "DLCWEAPON": (self.dlc_weapons, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                ),
            )

        return objectives

    @property
    def enable_multiplayer(self) -> bool:
        return bool(self.archipelago_options.call_of_duty_black_ops_7_enable_multiplayer.value)

    @property
    def enable_zombies(self) -> bool:
        return bool(self.archipelago_options.call_of_duty_black_ops_7_enable_zombies.value)

    @property
    def include_post_launch_weapons(self) -> bool:
        return bool(self.archipelago_options.call_of_duty_black_ops_7_include_post_launch_weapons.value)

    @property
    def include_party_games(self) -> bool:
        return bool(self.archipelago_options.call_of_duty_black_ops_7_include_party_games.value)

    @staticmethod
    def gamemodes() -> List[str]:
        return [
            "Team Deathmatch",
            "Domination",
            "Hardpoint",
            "Kill Confirmed",
            "Overload",
            "Search and Destroy",
            "Free-for-all",
            "Safeguard",
            "Demolition",
            "Overdrive",
        ]

    @staticmethod
    def party_games() -> List[str]:
        return [
            "Prop Hunt",
            "Infected",
            "Gun Game",
            "Sticks and Stones",
            "One in the Chamber",
            "Gunfight",
        ]

    @staticmethod
    def weapons() -> List[str]:
        return [
            "M15 Mod 0",
            "AK-27",
            "MXR-17",
            "X9 Maverick",
            "DS20 Mirage",
            "Peacekeeper MK1",
            "Ryden 45K",
            "RK-9",
            "Razor 9MM",
            "Dravec 45",
            "Carbon 57",
            "MPC-25",
            "M10 Breacher",
            "Echo 12",
            "Akita",
            "MK.78",
            "XM325",
            "M8A1",
            "Warden 308",
            "M34 Novaline",
            "VS Recon",
            "Shadow SK",
            "XR-3 Ion",
            "Jäger 45",
            "Velox 5.7",
            "Coda 9",
            "Arrow 109",
            "A.R.C. M1",
            "Knife",
            "Flatline MK.II",
        ]

    @staticmethod
    def dlc_weapons() -> List[str]:
        return [
            "Maddox RFB",
            "EGRT-17",
            "Voyak KT-3",
            "MK35 ISR",
            "Kogot-7",
            "Sturmwolf 45",
            "Rev-46",
            "VST",
            "SG-12",
            "Sokol 545",
            "Swordfish A1",
            "Hawker HX",
            "Strider 300",
            "1911",
            "NX Ravager",
            "GDL Havoc",
            "Siren",
            "Ballistic Knife",
            "H311-SAW",
            "Katana",
        ]

    @staticmethod
    def methods_multiplayer() -> List[str]:
        return [
            "critical",
            "melee",
            "equipment",
            "explosive",
            "objective",
            "Scorestreak",
        ]

    @staticmethod
    def methods_zombies() -> List[str]:
        return [
            "critical",
            "melee",
            "equipment",
            "explosive",
            "Scorestreak",
            "trap",
        ]

    @staticmethod
    def scorestreaks_easy() -> List[str]:
        return [
            "Scout Pulse",
            "RC-XD",
            "Combat Bow",
            "SAM Turret",
            "UAV",
            "Skewer",
            "Care Package",
            "Deadeye Drone",
            "Counter UAV",
            "Archangel Launcher",
            "Lockshot",
            "Napalm Strike",
            "LDBR",
            "Sentry Turret",
            "Death Machine",
            "Hand Cannon",
            "Hellstorm",
            "Strategic Bomber",
            "Grim Reaper",
            "Watchdog Helo",
        ]

    @staticmethod
    def scorestreaks_hard() -> List[str]:
        return [
            "Gravemaker",
            "Interceptors",
            "D.A.W.G",
            "War Machine",
            "Ion Core",
            "HKDS",
            "Rhino",
            "EMP Systems",
            "VTOL Warship",
            "Harp",
            "Legion",
            "Dreadnought",
        ]

    @staticmethod
    def field_upgrades_multiplayer() -> List[str]:
        return [
            "Assault Pack",
            "Drone Pod",
            "Trophy System",
            "Active Camo",
            "Echo Unit",
            "Squad Link",
            "Scrambler",
            "Fear Trap",
            "Black Hat",
            "Mute Field",
            "Morphine Injector",
            "Tactical Insertion",
        ]

    @staticmethod
    def field_upgrades_zombies() -> List[str]:
        return [
            "Dark Flare",
            "Energy Mine",
            "Frenzied Guard",
            "Toxic Growth",
            "Healing Aura",
            "Aether Shroud",
            "Mister Peeks",
            "Tesla Storm",
            "Frost Blast",
            "Wild Fire",
        ]

    @staticmethod
    def rounds() -> List[str]:
        return [
            "11",
            "16",
            "21",
            "26",
            "31",
            "36",
            "41",
        ]

    @staticmethod
    def maps_zombies() -> List[str]:
        return [
            "Ashes of the Damned",
            "Astra Malorum",
            "Paradox Junction",
            "Totenreich",
            "Vandorn Farm",
            "Exit 115",
            "Zarya Cosmodrome",
            "Mars",
            "Ashwood",
        ]

    @staticmethod
    def maps_standard() -> List[str]:
        return [
            "Ashes of the Damned",
            "Astra Malorum",
            "Paradox Junction",
            "Totenreich",
        ]

    @staticmethod
    def challenges() -> List[str]:
        return [
            "using no GobbleGums",
            "not upgrading any weapons",
            "not buying any perks",
            "not downing",
            "using only melee",
            "not using the Pack-A-Punch",
            "not upgrading your armor",
            "having a Cursed Relic enabled",
        ]

    @staticmethod
    def wonder_weapons() -> List[str]:
        return [
            "Ray Gun",
            "Ray Gun Mark II",
            "Necrofluid Gauntlet",
            "LGM-1",
            "Blundergat",
            "Jotunn Star",
        ]


# Archipelago Options
class CallOfDutyBlackOps7EnableMultiplayer(DefaultOnToggle):
    """
    If true, enables Multiplayer objectives.
    """
    display_name = "Call of Duty: Black Ops 7 - Enable Multiplayer"


class CallOfDutyBlackOps7EnableZombies(DefaultOnToggle):
    """
    If true, enables Zombies objectives.
    """
    display_name = "Call of Duty: Black Ops 7 - Enable Zombies"


class CallOfDutyBlackOps7IncludePostLaunchWeapons(Toggle):
    """
    If true, enables objectives involving post-launch DLC weapons.
    """
    display_name = "Call of Duty: Black Ops 7 - Include Post-Launch Weapons"


class CallOfDutyBlackOps7IncludePartyGames(DefaultOnToggle):
    """
    If true, enables objectives involving Party Game modes.
    """
    display_name = "Call of Duty: Black Ops 7 - Include Party Games"
