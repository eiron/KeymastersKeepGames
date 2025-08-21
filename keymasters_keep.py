"""
Keymaster's Keep Challenges Module

The ultimate meta module for generating challenges to play Keymaster's Keep itself!
This module creates objectives for playing Keymaster's Keep in its two game modes:
- Keymaster's Challenge: Collect artifacts and face the ultimate challenge
- Magic Key Heist: Gather keys and escape the keep

Features a comprehensive list of games from the Keymaster's Keep game selection pool.
"""

from __future__ import annotations
from typing import List
from dataclasses import dataclass

from Options import Range, OptionList

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


# Option Dataclass
@dataclass
class KeymastersKeepArchipelagoOptions:
    keymasters_keep_game_selection: KeymastersKeepGameSelection
    keymasters_keep_minimum_game_count: KeymastersKeepMinimumGameCount
    keymasters_keep_maximum_game_count: KeymastersKeepMaximumGameCount
    keymasters_keep_challenge_type_selection: KeymastersKeepChallengeTypeSelection


# Main Class
class KeymastersKeepGame(Game):
    name = "Keymaster's Keep"
    platform = KeymastersKeepGamePlatforms.META

    is_adult_only_or_unrated = False

    options_cls = KeymastersKeepArchipelagoOptions

    # Main Objectives
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = []

        if self.game_selection and self.challenge_types:
            min_games = self.archipelago_options.keymasters_keep_minimum_game_count.value
            max_games = self.archipelago_options.keymasters_keep_maximum_game_count.value
            
            # Create an objective for each possible game count
            for game_count in range(min_games, max_games + 1):
                game_objective_templates.append(
                    GameObjectiveTemplate(
                        label="Complete a CHALLENGE_TYPE including the games: GAMES",
                        data={
                            "CHALLENGE_TYPE": (self.challenge_types, 1),
                            "GAMES": (self.game_selection, game_count),
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=50,
                    ),
                )
        
        return game_objective_templates

    def challenge_types(self) -> List[str]:
        """Get available challenge types based on user selection."""
        challenge_types = []
        selection = self.archipelago_options.keymasters_keep_challenge_type_selection.value
        
        if "keymasters_challenge" in selection:
            challenge_types.append("Keymaster's Challenge")
        if "magic_key_heist" in selection:
            challenge_types.append("Magic Key Heist")
            
        return challenge_types

    def game_selection(self) -> List[str]:
        """Get the player's game selection."""
        games: List[str] = list(self.archipelago_options.keymasters_keep_game_selection.value)
        return sorted(games)


# Archipelago Options
class KeymastersKeepGameSelection(OptionList):
    """
    Indicates which games can be selected for Keymaster's Keep challenges.
    The player is free to add or remove any options they like. Multiple appearances will function as weightings for the options provided.
    Defaults to the comprehensive game selection from the Keymaster's Keep YAML configuration.
    """
    display_name = "Keymaster's Keep Game Selection"
    default = [
        "14 Minesweeper Variants",
        "14 Minesweeper Variants 2",
        "A Dance of Fire and Ice",
        "Advance Wars: Days of Ruin",
        "Adventure/Experience Challenges",
        "Aeon's End",
        "Anger Foot",
        "Antonblast",
        "Any Game Bingo",
        "Any Game Tasks",
        "Arcaea",
        "Archipelago Multiworld Randomizer",
        "Archipelagourmet",
        "Artwork",
        "Awaria",
        "Backpack Battles",
        "Balatro",
        "BattleBlock Theater",
        "BizHawk Shuffler",
        "Bloons TD 6",
        "Blue Prince",
        "Bomberman 64",
        "Burger Shop",
        "Cataclysm: Dark Days Ahead",
        "Caveblazers",
        "Celeste",
        "Christmas/Holiday Challenges",
        "Cobalt Core",
        "Command and Conquer: Generals Zero Hour",
        "Cook, Serve, Delicious! 2!!",
        "Core Keeper",
        "Creative Challenges",
        "Creeper World 3: Arc Eternal",
        "Creeper World 4",
        "Crush Crush",
        "Cuphead",
        "Custom",
        "Custom Medley",
        "Cytus II",
        "DJMax Respect V",
        "Dandy's World",
        "Dark Souls: Remastered",
        "Dead By Daylight",
        "Deadlock",
        "Deemo -Reborn-",
        "Deep Rock Galactic",
        "DemonCrawl",
        "Descenders",
        "Destiny 2",
        "Diablo II: Resurrected",
        "Disney Music Parade Encore",
        "Dome Keeper",
        "Dungeon Defenders",
        "ELDEN RING",
        "ELDEN RING NIGHTREIGN",
        "Ensemble Stars!! Music",
        "Enter the Gungeon",
        "FTL: Multiverse",
        "Fall Guys",
        "Final Fantasy XIV",
        "Final Fantasy XVI",
        "Fire Emblem Warriors",
        "Fire Emblem: Three Houses",
        "FlatOut 2",
        "Forsaken",
        "Fortnite",
        "Fortune Street",
        "Forza Horizon 4",
        "Forza Horizon 5",
        "Freedom Planet 2",
        "Frogger (1997)",
        "GTFO",
        "GUILTY GEAR -STRIVE-",
        "Game Backlog",
        "God Eater Resurrection",
        "Gran Turismo",
        "Gran Turismo 2",
        "Gran Turismo 3: A-Spec",
        "Gran Turismo 4",
        "Guild Wars 2",
        "Guitar Hero",
        "Guitar Hero 5",
        "Guitar Hero II",
        "Guitar Hero III: Legends of Rock",
        "Guitar Hero World Tour",
        "Guitar Hero: Warriors of Rock",
        "Halls of Torment",
        "Harry Potter: Quidditch World Cup",
        "Haste: Broken Worlds",
        "Hollow Knight",
        "HoloCure: Save the Fans!",
        "Hotline Miami",
        "Hyperspace Dogfights",
        "Hyrule Warriors: Definitive Edition",
        "I Was A Teenage Exocolonist",
        "Identity V",
        "Insaniquarium Deluxe",
        "Jackbox Party Packs",
        "Just Shapes & Beats",
        "Keymaster's Keep",
        "Kingdom Hearts III",
        "Kingdom Hearts: Melody of Memory",
        "Kirby's Return to Dream Land",
        "Layers of Fear (2023)",
        "League of Legends",
        "Left 4 Dead 2",
        "Legendary - A Marvel Deck Building Game",
        "Lego Rock Band",
        "Lethal Company",
        "Lies of P",
        "Little Inferno",
        "MONSTER HUNTER RISE",
        "Made in Abyss: Binary Star Falling into Darkness",
        "Mages of Mystralia",
        "Magic the Gathering",
        "Mario Kart 8",
        "Mario Kart World",
        "Mario Party",
        "Mario Party 2",
        "Mario Party 3",
        "Marvel Rivals",
        "Mega Man",
        "Mega Man 11",
        "Mega Man 2",
        "Mega Man 3",
        "Mega Man 4",
        "Melatonin",
        "Melvor Idle",
        "Minecraft MCParks Server",
        "Monster Hunter 3 Ultimate",
        "Monster Hunter 4 Ultimate",
        "Monster Hunter Generations Ultimate",
        "Monster Hunter Wilds",
        "Monster Hunter World",
        "Monster Rancher 2 DX",
        "Muse Dash",
        "Music Listening",
        "Mythos: Sudoku",
        "NiGHTS into Dreams...",
        "Neon White",
        "Nickelodeon All-Star Brawl 2",
        "Nine Sols",
        "Nubby's Number Factory",
        "OldTV",
        "Octodad: Dadliest Catch",
        "One Deck Dungeon",
        "OpenRCT2",
        "Ori and the Will of the Wisps",
        "Overwatch 2",
        "PEAK",
        "Paperball",
        "Peggle Deluxe",
        "Persona 4 Arena Ultimax",
        "Physical/Health Challenges",
        "Pikmin 4",
        "Pinball FX3",
        "Pizza Tower",
        "Placid Plastic Duck Simulator",
        "Plants vs. Zombies",
        "Plants vs. Zombies 2: It's About Time",
        "Plants vs. Zombies: Heroes",
        "PlatinumQuest",
        "Pokemon Go",
        "Pokémon Diamond, Pearl, and Platinum Versions",
        "Pokémon Platinum Map Randomizer",
        "Pokémon Ruby, Sapphire, and Emerald Versions",
        "PowerWash Simulator",
        "Project Sekai: Colorful Stage",
        "Quake 3 Arena",
        "Rabbit & Steel",
        "Re-Volt",
        "Reading Backlog",
        "Realm of the Mad God",
        "RetroAchievements",
        "Rhythm Doctor",
        "Rhythm Heaven Fever",
        "Rift Wizard 2",
        "Rimworld",
        "Risk of Rain 2",
        "Rock Band",
        "Rock Band 2",
        "Rock Band 3",
        "Rock Band 4",
        "Rock of Ages 2: Bigger & Boulder",
        "SONIC THE HEDGEHOG (2006)",
        "Salt and Sacrifice",
        "Sea of Thieves",
        "Shadow The Hedgehog",
        "Shiny Pokemon Hunt Scarlet/Violet",
        "Shiny Pokémon Hunt",
        "Shovel Knight Dig",
        "Sid Meier's Pirates",
        "Sins of a Solar Empire II",
        "Slay the Spire",
        "Smite 2",
        "Sonic Frontiers",
        "Sonic Mania",
        "Sonic Origins",
        "Sonic R",
        "Sonic Riders",
        "Sonic Riders: Zero Gravity",
        "Splatoon 3",
        "Spore",
        "Spyro Reignited Trilogy",
        "Star Wars: Battlefront II (Classic)",
        "Steam Library",
        "Stellaris",
        "Street Fighter 6",
        "Super Hexagon",
        "Super Mario Galaxy",
        "Super Mario Galaxy 2",
        "Super Mario Sunshine",
        "Super Smash Bros. Melee",
        "Super Smash Bros. Ultimate",
        "Synthetik: Legion Rising",
        "Terraria",
        "Tetris Effect: Connected",
        "The Bazaar",
        "The Binding of Isaac: Rebirth",
        "The Elder Scrolls V: Skyrim - Special Edition",
        "The Finals",
        "The Void Rains Upon Her Heart",
        "Theatrhythm: Final Bar Line",
        "Tony Hawk's Pro Skater 1+2",
        "Touhou Chireiden ~ Subterranean Animism",
        "Touhou Kanjuden: Legacy of Lunatic Kingdom",
        "Touhou Youyoumu~ Perfect Cherry Blossom",
        "Tower Tactics: Liberation",
        "Tower Unite",
        "TrackMania Turbo",
        "TrackMania United Forever",
        "TrackMania²",
        "Trackmania",
        "Trombone Champ",
        "ULTRAKILL",
        "Ultimate Custom Night",
        "Unidentified Falling Objects",
        "Universal Studios Experience (Minecraft Bedrock)",
        "Unreal Tournament: Game of the Year Edition",
        "WEBFISHING",
        "Vampire Survivors",
        "Voez",
        "Warframe",
        "Watchlist",
        "Wayfinder",
        "Wingspan",
        "Worms Armageddon",
        "Ys VIII: Lacrimosa of Dana",
        "Zuma Deluxe",
    ]


class KeymastersKeepChallengeTypeSelection(OptionList):
    """
    Indicates which challenge types (game modes) can be selected for Keymaster's Keep challenges.
    """
    display_name = "Keymaster's Keep Challenge Type Selection"
    default = [
        "keymasters_challenge",
        "magic_key_heist",
    ]


class KeymastersKeepMinimumGameCount(Range):
    """
    The minimum number of games to include when generating Keymaster's Keep challenges (1-10).
    """
    display_name = "Keymaster's Keep Minimum Game Count"
    default = 2
    range_start = 1
    range_end = 10
    

class KeymastersKeepMaximumGameCount(Range):
    """
    The maximum number of games to include when generating Keymaster's Keep challenges (1-10).
    """
    display_name = "Keymaster's Keep Maximum Game Count"
    default = 6
    range_start = 1
    range_end = 10
