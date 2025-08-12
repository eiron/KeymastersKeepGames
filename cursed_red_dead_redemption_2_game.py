from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle, Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CursedRedDeadRedemption2ArchipelagoOptions:
    cursedrdr2_include_animal_cruelty: CURSEDRDR2IncludeAnimalCruelty
    cursedrdr2_include_social_disasters: CURSEDRDR2IncludeSocialDisasters
    cursedrdr2_include_transportation_chaos: CURSEDRDR2IncludeTransportationChaos
    cursedrdr2_include_fashion_crimes: CURSEDRDR2IncludeFashionCrimes
    cursedrdr2_include_roleplay_nightmares: CURSEDRDR2IncludeRoleplayNightmares
    cursedrdr2_include_tedious_collections: CURSEDRDR2IncludeTediousCollections
    cursedrdr2_include_combat_absurdities: CURSEDRDR2IncludeCombatAbsurdities
    cursedrdr2_include_economy_destruction: CURSEDRDR2IncludeEconomyDestruction
    cursedrdr2_cursed_difficulty: CURSEDRDR2CursedDifficulty


class CursedRedDeadRedemption2Game(Game):
    name = "Cursed Red Dead Redemption 2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = True

    options_cls = CursedRedDeadRedemption2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective while maintaining minimum honor",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective while wearing only OUTFIT_STYLE",
                data={"OUTFIT_STYLE": (self.cursed_outfits, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without using fast travel",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective while constantly drunk",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective using only WEAPON_TYPE",
                data={"WEAPON_TYPE": (self.terrible_weapons, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective while being chased by BOUNTY_AMOUNT bounty hunters",
                data={"BOUNTY_AMOUNT": (self.bounty_levels, 1)},
            ),
        ])
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Animal Cruelty (Cursed animal interactions)
        if self.include_animal_cruelty:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Lasso ANIMAL_COUNT ANIMAL_TYPE and drag them behind your horse for DISTANCE_MILES miles",
                    data={
                        "ANIMAL_COUNT": (self.animal_counts, 1),
                        "ANIMAL_TYPE": (self.draggable_animals, 1),
                        "DISTANCE_MILES": (self.drag_distances, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Kill KILL_COUNT animals using only MURDER_METHOD",
                    data={
                        "KILL_COUNT": (self.mass_kill_counts, 1),
                        "MURDER_METHOD": (self.cursed_kill_methods, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Feed FEED_COUNT predators to alligators by leading them into swamps",
                    data={"FEED_COUNT": (self.sacrifice_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Create a pile of CORPSE_COUNT animal corpses and blow it up with dynamite",
                    data={"CORPSE_COUNT": (self.corpse_pile_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Social Disasters
        if self.include_social_disasters:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Antagonize every single NPC in TOWN until they all hate you",
                    data={"TOWN": (self.towns, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Start FIGHT_COUNT bar fights in different saloons within FIGHT_TIME hours",
                    data={
                        "FIGHT_COUNT": (self.fight_counts, 1),
                        "FIGHT_TIME": (self.fight_timeframes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Get kicked out of ESTABLISHMENT_COUNT establishments for inappropriate behavior",
                    data={"ESTABLISHMENT_COUNT": (self.establishment_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Ruin WEDDING_COUNT weddings by causing chaos during the ceremony",
                    data={"WEDDING_COUNT": (self.wedding_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Follow random NPCs for STALKING_HOURS hours without them noticing",
                    data={"STALKING_HOURS": (self.stalking_durations, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Transportation Chaos
        if self.include_transportation_chaos:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Steal TRAIN_COUNT trains and crash them into OBSTACLE",
                    data={
                        "TRAIN_COUNT": (self.train_counts, 1),
                        "OBSTACLE": (self.crash_targets, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Ride HORSE_COUNT stolen horses to death from exhaustion",
                    data={"HORSE_COUNT": (self.horse_abuse_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Drive a wagon backwards from ORIGIN to DESTINATION",
                    data={
                        "ORIGIN": (self.locations, 1),
                        "DESTINATION": (self.locations, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Launch yourself LAUNCH_DISTANCE feet using LAUNCH_METHOD",
                    data={
                        "LAUNCH_DISTANCE": (self.launch_distances, 1),
                        "LAUNCH_METHOD": (self.launch_methods, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Fashion Crimes
        if self.include_fashion_crimes:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Wear only CURSED_COMBO for DURATION days in-game",
                    data={
                        "CURSED_COMBO": (self.cursed_outfit_combinations, 1),
                        "DURATION": (self.outfit_durations, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Attend FORMAL_COUNT formal events wearing INAPPROPRIATE_OUTFIT",
                    data={
                        "FORMAL_COUNT": (self.formal_event_counts, 1),
                        "INAPPROPRIATE_OUTFIT": (self.inappropriate_outfits, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Never change clothes for HYGIENE_DAYS days and document NPC reactions",
                    data={"HYGIENE_DAYS": (self.hygiene_neglect_durations, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Roleplay Nightmares
        if self.include_roleplay_nightmares:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Live as a ROLEPLAY_CHARACTER for ROLEPLAY_DURATION days following strict rules",
                    data={
                        "ROLEPLAY_CHARACTER": (self.cursed_roleplay_characters, 1),
                        "ROLEPLAY_DURATION": (self.roleplay_durations, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Only communicate through COMMUNICATION_METHOD for COMMUNICATION_DURATION hours",
                    data={
                        "COMMUNICATION_METHOD": (self.cursed_communication_methods, 1),
                        "COMMUNICATION_DURATION": (self.communication_durations, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Pretend to be PROFESSION and convince CONVINCING_COUNT NPCs you're legitimate",
                    data={
                        "PROFESSION": (self.fake_professions, 1),
                        "CONVINCING_COUNT": (self.convincing_counts, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Tedious Collections
        if self.include_tedious_collections:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Collect ROCK_COUNT rocks and arrange them in perfect FORMATION",
                    data={
                        "ROCK_COUNT": (self.massive_collection_counts, 1),
                        "FORMATION": (self.rock_formations, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Document ITEM_COUNT instances of MUNDANE_ITEM by taking screenshots",
                    data={
                        "ITEM_COUNT": (self.documentation_counts, 1),
                        "MUNDANE_ITEM": (self.mundane_items, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Count and catalog every COUNTING_TARGET in COUNTING_LOCATION",
                    data={
                        "COUNTING_TARGET": (self.countable_things, 1),
                        "COUNTING_LOCATION": (self.large_areas, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Combat Absurdities
        if self.include_combat_absurdities:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Win DUEL_COUNT duels using only RIDICULOUS_WEAPON",
                    data={
                        "DUEL_COUNT": (self.duel_counts, 1),
                        "RIDICULOUS_WEAPON": (self.ridiculous_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Kill ENEMY_COUNT enemies by CREATIVE_METHOD",
                    data={
                        "ENEMY_COUNT": (self.creative_kill_counts, 1),
                        "CREATIVE_METHOD": (self.creative_kill_methods, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Rob BANK_COUNT banks using only ABSURD_STRATEGY",
                    data={
                        "BANK_COUNT": (self.bank_counts, 1),
                        "ABSURD_STRATEGY": (self.absurd_strategies, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Economy Destruction
        if self.include_economy_destruction:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Lose exactly $MONEY_AMOUNT through MONEY_LOSS_METHOD",
                    data={
                        "MONEY_AMOUNT": (self.specific_money_amounts, 1),
                        "MONEY_LOSS_METHOD": (self.money_loss_methods, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Buy ITEM_COUNT copies of WORTHLESS_ITEM and throw them all away",
                    data={
                        "ITEM_COUNT": (self.wasteful_counts, 1),
                        "WORTHLESS_ITEM": (self.worthless_items, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Donate your entire fortune to DONATION_TARGET and become completely broke",
                    data={"DONATION_TARGET": (self.donation_targets, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_animal_cruelty(self) -> bool:
        return self.archipelago_options.cursedrdr2_include_animal_cruelty.value

    @property
    def include_social_disasters(self) -> bool:
        return self.archipelago_options.cursedrdr2_include_social_disasters.value

    @property
    def include_transportation_chaos(self) -> bool:
        return self.archipelago_options.cursedrdr2_include_transportation_chaos.value

    @property
    def include_fashion_crimes(self) -> bool:
        return self.archipelago_options.cursedrdr2_include_fashion_crimes.value

    @property
    def include_roleplay_nightmares(self) -> bool:
        return self.archipelago_options.cursedrdr2_include_roleplay_nightmares.value

    @property
    def include_tedious_collections(self) -> bool:
        return self.archipelago_options.cursedrdr2_include_tedious_collections.value

    @property
    def include_combat_absurdities(self) -> bool:
        return self.archipelago_options.cursedrdr2_include_combat_absurdities.value

    @property
    def include_economy_destruction(self) -> bool:
        return self.archipelago_options.cursedrdr2_include_economy_destruction.value

    @property
    def cursed_difficulty(self) -> str:
        return self.archipelago_options.cursedrdr2_cursed_difficulty.value

    # Cursed Data Lists
    @staticmethod
    def draggable_animals() -> List[str]:
        return [
            "deer", "wolves", "cougars", "bears", "elk", "moose", "bison", "rams",
            "goats", "pronghorn", "foxes", "coyotes", "boars", "alligators"
        ]

    @staticmethod
    def cursed_kill_methods() -> List[str]:
        return [
            "throwing knives only", "fire bottles only", "ramming with horse", 
            "dynamite fishing", "falling damage", "train impacts", "drowning",
            "poison arrows only", "bare fists", "lasso strangulation"
        ]

    @staticmethod
    def cursed_outfits() -> List[str]:
        return [
            "nothing but underwear", "full winter gear in desert", "formal wear only",
            "mismatched everything", "one boot missing", "hat but no clothes",
            "bandana over eyes", "bright pink everything"
        ]

    @staticmethod
    def terrible_weapons() -> List[str]:
        return [
            "broken bottles", "bare fists", "throwing knives", "rocks", "slingshot",
            "antique pistol", "rusty knife", "wooden club", "lasso as weapon"
        ]

    @staticmethod
    def towns() -> List[str]:
        return [
            "Valentine", "Strawberry", "Rhodes", "Saint Denis", "Annesburg",
            "Van Horn", "Blackwater", "Armadillo", "Tumbleweed"
        ]

    @staticmethod
    def cursed_outfit_combinations() -> List[str]:
        return [
            "winter coat with shorts", "top hat with rags", "fancy vest with torn pants",
            "one elegant shoe and one work boot", "formal jacket with no shirt",
            "ball gown on Arthur", "mixed gang member outfits", "all stolen clothes"
        ]

    @staticmethod
    def inappropriate_outfits() -> List[str]:
        return [
            "full Micah cosplay", "enemy gang colors", "nothing but chaps",
            "woman's dress", "clown makeup and suit", "all black funeral attire",
            "bright yellow everything", "Christmas outfit in summer"
        ]

    @staticmethod
    def cursed_roleplay_characters() -> List[str]:
        return [
            "pacifist gunslinger", "vegan in 1899", "mute outlaw", "germaphobe cowboy",
            "aristocrat who refuses to get dirty", "outlaw who always tells the truth",
            "cowboy who's afraid of horses", "gunslinger who won't use guns"
        ]

    @staticmethod
    def cursed_communication_methods() -> List[str]:
        return [
            "only animal sounds", "speaking in rhymes", "only questions",
            "backwards sentences", "only singing", "interpretive dance",
            "only horse neighing", "medieval English only"
        ]

    @staticmethod
    def fake_professions() -> List[str]:
        return [
            "snake oil salesman", "fortune teller", "traveling preacher",
            "circus performer", "aristocrat", "government inspector",
            "famous gunslinger", "railroad executive", "oil tycoon"
        ]

    @staticmethod
    def mundane_items() -> List[str]:
        return [
            "fence posts", "wagon wheels", "horseshoes", "empty bottles",
            "broken crates", "hay bales", "water pumps", "hitching posts",
            "street lamps", "shop signs", "barrel hoops", "old boots"
        ]

    @staticmethod
    def countable_things() -> List[str]:
        return [
            "blades of grass", "individual stones", "fence pickets", "bird calls",
            "horse steps", "NPC blinks", "cloud shapes", "building windows",
            "gun shots heard", "footprints in mud"
        ]

    @staticmethod
    def ridiculous_weapons() -> List[str]:
        return [
            "empty bottles", "fish as clubs", "severed limbs", "railroad spikes",
            "horseshoes", "broken wagon wheels", "fence posts", "garden tools",
            "cooking pots", "musical instruments"
        ]

    @staticmethod
    def creative_kill_methods() -> List[str]:
        return [
            "explosive bait feeding", "train collision orchestration", "cliff pushing",
            "alligator feeding", "bridge collapse", "fire spreading", "drowning assistance",
            "dynamite surprise", "horse trampling", "building collapse"
        ]

    @staticmethod
    def absurd_strategies() -> List[str]:
        return [
            "naked intimidation", "bribing with dead animals", "singing loudly",
            "pretending to be a ghost", "using only compliments", "dancing menacingly",
            "speaking only in questions", "wearing disguises backwards"
        ]

    @staticmethod
    def money_loss_methods() -> List[str]:
        return [
            "poker with terrible bluffs", "buying overpriced items", "tipping excessively",
            "losing on purpose at dominoes", "buying rounds for entire saloons",
            "gambling on rigged games", "investing in obvious scams"
        ]

    @staticmethod
    def worthless_items() -> List[str]:
        return [
            "broken pocket watches", "empty tin cans", "worn shoes", "torn hats",
            "broken spectacles", "rusty spoons", "cracked mirrors", "moldy bread"
        ]

    @staticmethod
    def donation_targets() -> List[str]:
        return [
            "camp funds", "beggars", "churches", "random strangers", "rival gangs",
            "law enforcement", "businesses you robbed", "grave sites"
        ]

    @staticmethod
    def crash_targets() -> List[str]:
        return [
            "other trains", "buildings", "bridges", "cliff faces", "water", "trees",
            "camps", "towns", "oil derricks", "mountains"
        ]

    @staticmethod
    def launch_methods() -> List[str]:
        return [
            "dynamite catapult", "horse collision", "train impact", "cliff jumping",
            "explosion surfing", "wagon catapult", "geyser riding", "bridge collapse"
        ]

    @staticmethod
    def rock_formations() -> List[str]:
        return [
            "perfect circle", "pyramid", "spiral", "face profile", "animal shape",
            "geometric pattern", "maze design", "replica building", "map outline"
        ]

    @staticmethod
    def large_areas() -> List[str]:
        return [
            "entire New Hanover", "all of Lemoyne", "West Elizabeth", "New Austin",
            "Grizzlies", "Heartlands", "Great Plains", "Bayou Nwa", "Roanoke Ridge"
        ]

    @staticmethod
    def locations() -> List[str]:
        return [
            "Valentine", "Saint Denis", "Strawberry", "Rhodes", "Blackwater",
            "Annesburg", "Van Horn", "Armadillo", "Tumbleweed", "Colter"
        ]

    # Ranges for cursed objectives
    @staticmethod
    def animal_counts() -> range:
        return range(10, 100, 10)

    @staticmethod
    def drag_distances() -> range:
        return range(1, 10, 1)

    @staticmethod
    def mass_kill_counts() -> range:
        return range(50, 200, 25)

    @staticmethod
    def sacrifice_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def corpse_pile_counts() -> range:
        return range(20, 100, 20)

    @staticmethod
    def fight_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def fight_timeframes() -> range:
        return range(1, 12, 2)

    @staticmethod
    def establishment_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def wedding_counts() -> range:
        return range(1, 5, 1)

    @staticmethod
    def stalking_durations() -> range:
        return range(2, 24, 4)

    @staticmethod
    def train_counts() -> range:
        return range(1, 10, 2)

    @staticmethod
    def horse_abuse_counts() -> range:
        return range(5, 30, 5)

    @staticmethod
    def launch_distances() -> range:
        return range(50, 500, 50)

    @staticmethod
    def outfit_durations() -> range:
        return range(3, 30, 5)

    @staticmethod
    def formal_event_counts() -> range:
        return range(2, 10, 2)

    @staticmethod
    def hygiene_neglect_durations() -> range:
        return range(7, 30, 7)

    @staticmethod
    def roleplay_durations() -> range:
        return range(5, 50, 10)

    @staticmethod
    def communication_durations() -> range:
        return range(2, 24, 4)

    @staticmethod
    def convincing_counts() -> range:
        return range(5, 30, 5)

    @staticmethod
    def massive_collection_counts() -> range:
        return range(100, 1000, 100)

    @staticmethod
    def documentation_counts() -> range:
        return range(50, 500, 50)

    @staticmethod
    def duel_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def creative_kill_counts() -> range:
        return range(10, 50, 10)

    @staticmethod
    def bank_counts() -> range:
        return range(1, 5, 1)

    @staticmethod
    def specific_money_amounts() -> range:
        return range(100, 5000, 200)

    @staticmethod
    def wasteful_counts() -> range:
        return range(20, 100, 20)

    @staticmethod
    def bounty_levels() -> range:
        return range(100, 1500, 200)


# Archipelago Options
class CURSEDRDR2IncludeAnimalCruelty(Toggle):
    """Include absolutely cursed animal-related objectives."""
    display_name = "Include Animal Cruelty"
    default = True

class CURSEDRDR2IncludeSocialDisasters(Toggle):
    """Include socially destructive and chaotic objectives."""
    display_name = "Include Social Disasters"
    default = True

class CURSEDRDR2IncludeTransportationChaos(Toggle):
    """Include vehicle and transportation mayhem objectives."""
    display_name = "Include Transportation Chaos"
    default = True

class CURSEDRDR2IncludeFashionCrimes(Toggle):
    """Include terrible outfit and appearance objectives."""
    display_name = "Include Fashion Crimes"
    default = True

class CURSEDRDR2IncludeRoleplayNightmares(Toggle):
    """Include painful roleplay restriction objectives."""
    display_name = "Include Roleplay Nightmares"
    default = True

class CURSEDRDR2IncludeTediousCollections(Toggle):
    """Include mind-numbingly boring collection objectives."""
    display_name = "Include Tedious Collections"
    default = True

class CURSEDRDR2IncludeCombatAbsurdities(Toggle):
    """Include ridiculous and impractical combat objectives."""
    display_name = "Include Combat Absurdities"
    default = True

class CURSEDRDR2IncludeEconomyDestruction(Toggle):
    """Include money-wasting and economy-breaking objectives."""
    display_name = "Include Economy Destruction"
    default = True

class CURSEDRDR2CursedDifficulty(Choice):
    """How cursed should the objectives be?"""
    display_name = "Cursed Difficulty"
    option_mildly_cursed = "Mildly Cursed"
    option_quite_cursed = "Quite Cursed"
    option_extremely_cursed = "Extremely Cursed"
    option_absolutely_diabolical = "Absolutely Diabolical"
    default = option_quite_cursed
