from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DateEverythingArchipelagoOptions:
    date_everything_include_structural_objects: DEIncludeStructuralObjects
    date_everything_include_furniture_decor: DEIncludeFurnitureDecor
    date_everything_include_kitchen_appliances: DEIncludeKitchenAppliances
    date_everything_include_bathroom_items: DEIncludeBathroomItems
    date_everything_include_laundry_items: DEIncludeLaundryItems
    date_everything_include_office_bedroom: DEIncludeOfficeBedroom
    date_everything_include_misc_items: DEIncludeMiscItems
    date_everything_include_special_concepts: DEIncludeSpecialConcepts
    date_everything_include_dlc_characters: DEIncludeDLCCharacters
    date_everything_relationship_goals: DERelationshipGoals


class DateEverythingGame(Game):
    name = "Date Everything"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = DateEverythingArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []

        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective while exploring only HOUSE_AREA",
                data={"HOUSE_AREA": (self.house_areas, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective during TIME_OF_DAY",
                data={"TIME_OF_DAY": (self.time_periods, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective while maintaining EXISTING_RELATIONSHIP with other characters",
                data={"EXISTING_RELATIONSHIP": (self.relationship_outcomes, 1)},
            ),
            GameObjectiveTemplate(
                # S.P.E.C.S. are stat requirements for dialogue progression with specific characters
                # CHARM: charm-focused characters, POISE: stability/steadiness, SMARTS: intellectual characters,
                # EMPATHY: emotional/caring characters, SASS: sarcastic/witty characters
                label="Reach SPECS_TARGET points in SPECS_CATEGORY during this objective",
                data={
                    "SPECS_TARGET": (self.specs_targets, 1),
                    "SPECS_CATEGORY": (self.specs_categories, 1)
                },
            ),
        ])

        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Structural Objects (1-10)
        if self.include_structural_objects:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Achieve RELATIONSHIP_OUTCOME with STRUCTURAL_CHARACTER",
                    data={
                        "RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1),
                        "STRUCTURAL_CHARACTER": (self.structural_characters, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Get STRUCTURE_COUNT structural elements to RELATIONSHIP_OUTCOME status",
                    data={
                        "STRUCTURE_COUNT": (self.structure_counts, 1),
                        "RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Navigate Wallace (Wall) and Florence (Floor) relationships without conflict",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Furniture & Decor (11-30)
        if self.include_furniture_decor:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Achieve RELATIONSHIP_OUTCOME with FURNITURE_CHARACTER",
                    data={
                        "RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1),
                        "FURNITURE_CHARACTER": (self.furniture_characters, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Complete FURNITURE_COUNT furniture relationships across different rooms",
                    data={"FURNITURE_COUNT": (self.furniture_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Help Telly (Television) with entertainment choices and reach RELATIONSHIP_OUTCOME",
                    data={"RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Share a quick greeting with QUICK_CHARACTER",
                    data={"QUICK_CHARACTER": (self.all_characters, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Give a simple compliment to EASY_CHARACTER",
                    data={"EASY_CHARACTER": (self.all_characters, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Ask BASIC_CHARACTER about their day",
                    data={"BASIC_CHARACTER": (self.all_characters, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
            ])

        # Kitchen Appliances (31-42)
        if self.include_kitchen_appliances:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Achieve RELATIONSHIP_OUTCOME with KITCHEN_CHARACTER",
                    data={
                        "RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1),
                        "KITCHEN_CHARACTER": (self.kitchen_characters, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Help Stefan (Stove) with cooking tasks COOKING_COUNT times",
                    data={"COOKING_COUNT": (self.cooking_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Get APPLIANCE_COUNT kitchen appliances to work together harmoniously",
                    data={"APPLIANCE_COUNT": (self.appliance_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Offer a friendly wave to KITCHEN_GREETING_CHARACTER",
                    data={"KITCHEN_GREETING_CHARACTER": (self.kitchen_characters, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        # Bathroom Items (43-52)
        if self.include_bathroom_items:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Achieve RELATIONSHIP_OUTCOME with BATHROOM_CHARACTER",
                    data={
                        "RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1),
                        "BATHROOM_CHARACTER": (self.bathroom_characters, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Navigate Jean-Loo (Toilet) and Johnny Splash (Shower) bathroom politics",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Smile at BATHROOM_CHARACTER in passing",
                    data={"BATHROOM_CHARACTER": (self.bathroom_characters, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Get BATHROOM_COUNT bathroom items to RELATIONSHIP_OUTCOME status",
                    data={
                        "BATHROOM_COUNT": (self.bathroom_counts, 1),
                        "RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
            ])

        # Laundry Items (71-80)
        if self.include_laundry_items:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Achieve RELATIONSHIP_OUTCOME with LAUNDRY_CHARACTER",
                    data={
                        "RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1),
                        "LAUNDRY_CHARACTER": (self.laundry_characters, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Resolve the Harper (Hamper) and Dirk (Dirty Laundry) relationship drama",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Get Washford (Washing Machine) and Drysdale (Dryer) to work as a team",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Office & Bedroom (53-70)
        if self.include_office_bedroom:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Achieve RELATIONSHIP_OUTCOME with OFFICE_BEDROOM_CHARACTER",
                    data={
                        "RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1),
                        "OFFICE_BEDROOM_CHARACTER": (self.office_bedroom_characters, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Help Mac (Computer) with WORK_COUNT work projects",
                    data={"WORK_COUNT": (self.work_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Read Diana's (Diary) secrets to achieve RELATIONSHIP_OUTCOME",
                    data={"RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Give a thumbs up to OFFICE_CHARACTER",
                    data={"OFFICE_CHARACTER": (self.office_bedroom_characters, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        # Miscellaneous Items (81-90)
        if self.include_misc_items:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Achieve RELATIONSHIP_OUTCOME with MISC_CHARACTER",
                    data={
                        "RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1),
                        "MISC_CHARACTER": (self.misc_characters, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Help Tony (Toolbox) fix REPAIR_COUNT household problems",
                    data={"REPAIR_COUNT": (self.repair_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Solve Vaughn Trapp's (Mouse Trap) puzzle challenges",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Unlock secrets from Sophia (Safe) and Keith (Key) partnership",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Special Concepts (91-100)
        if self.include_special_concepts:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Achieve RELATIONSHIP_OUTCOME with CONCEPT_CHARACTER",
                    data={
                        "RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1),
                        "CONCEPT_CHARACTER": (self.concept_characters, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Transform TRANSFORMATION_TARGET into human form through deep connection",
                    data={"TRANSFORMATION_TARGET": (self.transformation_targets, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Confront Doug (Existential Dread) and achieve personal growth",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Survive NIGHTMARE_COUNT encounters with Nightmare and maintain sanity",
                    data={"NIGHTMARE_COUNT": (self.nightmare_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Handle Reggie (Rejection) gracefully and learn from the experience",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # DLC Characters (101-102)
        if self.include_dlc_characters:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Achieve RELATIONSHIP_OUTCOME with DLC_CHARACTER",
                    data={
                        "RELATIONSHIP_OUTCOME": (self.preferred_relationship_outcomes, 1),
                        "DLC_CHARACTER": (self.dlc_characters, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Navigate the luxury lifestyle of Lucinda Lavish (Deluxe Edition)",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_structural_objects(self) -> bool:
        return self.archipelago_options.date_everything_include_structural_objects.value

    @property
    def include_furniture_decor(self) -> bool:
        return self.archipelago_options.date_everything_include_furniture_decor.value

    @property
    def include_kitchen_appliances(self) -> bool:
        return self.archipelago_options.date_everything_include_kitchen_appliances.value

    @property
    def include_bathroom_items(self) -> bool:
        return self.archipelago_options.date_everything_include_bathroom_items.value

    @property
    def include_laundry_items(self) -> bool:
        return self.archipelago_options.date_everything_include_laundry_items.value

    @property
    def include_office_bedroom(self) -> bool:
        return self.archipelago_options.date_everything_include_office_bedroom.value

    @property
    def include_misc_items(self) -> bool:
        return self.archipelago_options.date_everything_include_misc_items.value

    @property
    def include_special_concepts(self) -> bool:
        return self.archipelago_options.date_everything_include_special_concepts.value

    @property
    def include_dlc_characters(self) -> bool:
        return self.archipelago_options.date_everything_include_dlc_characters.value

    @property
    def relationship_goals(self) -> str:
        return self.archipelago_options.date_everything_relationship_goals.value

    # Character lists based on actual Date Everything numbered characters
    @staticmethod
    def structural_characters() -> List[str]:
        return [
            "Wallace (Wall)", "Florence (Floor)", "Celia (Ceiling)", "Stella (Staircase)",
            "Dorian (Door)", "Wyndolyn (Window)", "Curt & Rod (Curtains)", "Shelley (Shelves)",
            "Hector (HVAC)"
        ]

    @staticmethod
    def furniture_characters() -> List[str]:
        return [
            "Abel (Table)", "Chairemi (Chair)", "Lux (Lamp)",
            "Prissy Plastique (Fake Plants)", "Timothy Timepiece (Kit-Cat Clock)", "Artt (Artwork)",
            "Koa (Couch)", "Dante (Fireplace)", "Telly (Television)", "Luna/Connie (Gaming Console)", "Keyes (Piano)",
            "Gaia (Globe)", "Captain Jacques Pierrot (Ship in a Bottle)", "Parker Bradley (Board Games)",
            "Mateo Manta (Blanket)", "Tina (Musical Triangle)"
        ]

    @staticmethod
    def kitchen_characters() -> List[str]:
        return [
            "Beverly (Mini-Bar)", "Mitchell Linn (Food)", "Cabrizzio (Cabinet)", "Sinclaire (Sink)",
            "Freddy Yeti (Fridge)", "Stefan (Stove)", "Luke Nukem (Microwave)", "Miranda (Toaster)",
            "Dishy (Dishwasher)", "Daisuke (Fine Tableware)", "Friar Errol (Air Fryer)", "Kopi (Coffee Maker)"
        ]

    @staticmethod
    def bathroom_characters() -> List[str]:
        return [
            "Amir (Mirror)", "Jean-Loo Pissoir (Toilet)",
            "Johnny Splash (Shower)", "Bathsheba (Bathtub)", "Rebel (Rubber Duck)", "Barry Styles (Makeup)",
            "Tyrell (Towel)", "Farya (First Aid Kit)", "Bobby Pinn (Bobby Pin)"
        ]

    @staticmethod
    def office_bedroom_characters() -> List[str]:
        return [
            "Phoenicia (Cell Phone)", "Dasha (Desk)", "Jerry (Junk Drawer)", "Penelope (Office Supplies)", "Mac (Computer)",
            "Willi (Your Work)", "Lyric (Books)", "Rongomaiwhenua (Geode)", "Chance (D20)",
            "Maggie (Magnifying Glass)", "Winnifred (Water Heater)", "Rainey (Record Player)",
            "Scandalabra (Candelabra)", "Arma (Smoke Alarm)", "Betty (Bed)", "Diana (Diary)",
            "Deenah (Daemon/Glitch)", "Ben-hwa (Sex Toy)", "Hero Hime (Anime Figure)", "Teddy (Teddy Bear)"
        ]

    @staticmethod
    def laundry_characters() -> List[str]:
        return [
            "Hanks (Hangers)", "Washford (Washing Machine)", "Drysdale (Dryer)",
            "Harper & Dirk (Hamper & Dirty Laundry)", "Tydus Andromache (Laundry Detergent)",
            "Henry Hoove (Vacuum)", "I, Ronaldini (Iron)"
        ]

    @staticmethod
    def misc_characters() -> List[str]:
        return [
            "Skylar (Date-viators)", "River (Water)", "Eddie & Volt (Electricity)", "Dolly (Dustbunny)",
            "Cam (Trashcan)", "Fantina (Fan)", "Stepford (Trophies/Awards)", "Tony (Toolbox)", "Beau (Cardboard Box)",
            "Keith (Key)", "Bodhi Windbreaker (80's Time Capsule)", "Vaughn Trapp (Mouse Trap)",
            "Sophia (Safe)", "Monique (Wallet)", "Kristof (Treadmill)", "Dunk Shuttlecock (Sports Equipment)"
        ]

    @staticmethod
    def concept_characters() -> List[str]:
        return [
            "Memoria (Nostalgia)", "Holly (Holiday Decor)", "Airyn (Air)", "Textbox-Chan (The Game Itself)",
            "The Sassy Chap (Developer's Mascot)", "Zoey Bennett (Ghost)", "xxXShadowl0rd420Xxx (Darkness)",
            "Doug (Existential Dread)", "Nightmare (Nightmare)", "Reggie (Rejection)"
        ]

    @staticmethod
    def dlc_characters() -> List[str]:
        return [
            "Lucinda Lavish (Deluxe Edition)", "Michael Transaction (Microtransactions)"
        ]

    @staticmethod
    def all_characters() -> List[str]:
        # Combine all character lists for quick/easy objectives
        all_chars = []
        all_chars.extend(DateEverythingGame.structural_characters())
        all_chars.extend(DateEverythingGame.furniture_characters())
        all_chars.extend(DateEverythingGame.kitchen_characters())
        all_chars.extend(DateEverythingGame.bathroom_characters())
        all_chars.extend(DateEverythingGame.office_bedroom_characters())
        all_chars.extend(DateEverythingGame.laundry_characters())
        all_chars.extend(DateEverythingGame.misc_characters())
        all_chars.extend(DateEverythingGame.concept_characters())
        all_chars.extend(DateEverythingGame.dlc_characters())
        return all_chars

    @staticmethod
    def relationship_outcomes() -> List[str]:
        return ["LOVE", "FRIENDS", "HATE"]

    # Dynamic relationship outcomes based on player goals
    def preferred_relationship_outcomes(self) -> List[str]:
        goals = self.relationship_goals
        if goals == "Love Focused":
            return ["LOVE", "LOVE", "LOVE", "FRIENDS", "HATE"]  # Weighted toward LOVE, with minimal HATE
        elif goals == "Friendship Focused":
            return ["FRIENDS", "FRIENDS", "FRIENDS", "LOVE", "HATE"]  # Weighted toward FRIENDS, with minimal HATE
        elif goals == "Hate Focused":
            return ["HATE", "HATE", "HATE", "FRIENDS", "LOVE"]  # Weighted toward HATE, with minimal positive outcomes
        elif goals == "Chaos Romance":
            return ["HATE", "LOVE", "FRIENDS", "HATE", "LOVE"]  # Organized chaotic mix
        else:  # Balanced Relationships
            return ["LOVE", "FRIENDS", "HATE"]  # Equal weight

    @staticmethod
    def house_areas() -> List[str]:
        return [
            "Kitchen", "Living Room", "Bedroom", "Upstairs Bathroom", "Downstairs Bathroom",
            "Laundry Room", "Office", "Attic", "Crawl Space", "Home Gym", "Dining Area", "Entrance"
        ]

    @staticmethod
    def time_periods() -> List[str]:
        # Date Everything day cycle: starts 9am, ends midnight (must sleep), 3 hours per phase
        return [
            "Morning (9am-12pm)", "Afternoon (12pm-3pm)", "Evening (3pm-6pm)",
            "Night (6pm-9pm)", "Late Night (9pm-12am)"
        ]

    @staticmethod
    def specs_categories() -> List[str]:
        # The five S.P.E.C.S. stats from Date Everything in correct acronym order
        return ["SMARTS", "POISE", "EMPATHY", "CHARM", "SASS"]

    @staticmethod
    def specs_targets() -> List[str]:
        return ["20", "30", "40", "50", "60", "70"]

    @staticmethod
    def transformation_targets() -> List[str]:
        # ALL characters in Date Everything can potentially be turned human - this is VERY difficult
        all_characters = []
        all_characters.extend(DateEverythingGame.structural_characters())
        all_characters.extend(DateEverythingGame.furniture_characters())
        all_characters.extend(DateEverythingGame.kitchen_characters())
        all_characters.extend(DateEverythingGame.bathroom_characters())
        all_characters.extend(DateEverythingGame.office_bedroom_characters())
        all_characters.extend(DateEverythingGame.laundry_characters())
        all_characters.extend(DateEverythingGame.misc_characters())
        all_characters.extend(DateEverythingGame.concept_characters())
        all_characters.extend(DateEverythingGame.dlc_characters())
        return all_characters

    # Ranges for relationship objectives
    @staticmethod
    def structure_counts() -> range:
        return range(3, 8, 1)

    @staticmethod
    def furniture_counts() -> range:
        return range(5, 15, 2)

    @staticmethod
    def cooking_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def appliance_counts() -> range:
        return range(4, 12, 2)

    @staticmethod
    def bathroom_counts() -> range:
        return range(3, 8, 1)

    @staticmethod
    def work_counts() -> range:
        return range(2, 8, 2)

    @staticmethod
    def nightmare_counts() -> range:
        return range(1, 4, 1)

    @staticmethod
    def repair_counts() -> range:
        return range(2, 6, 1)


# Archipelago Options
class DEIncludeStructuralObjects(DefaultOnToggle):
    """Include dating structural elements like walls, floors, and doors (Characters 1-10)."""
    display_name = "Include Structural Objects"

class DEIncludeFurnitureDecor(DefaultOnToggle):
    """Include dating furniture and decorative items (Characters 11-30)."""
    display_name = "Include Furniture & Decor"

class DEIncludeKitchenAppliances(DefaultOnToggle):
    """Include dating kitchen appliances and food-related items (Characters 31-42)."""
    display_name = "Include Kitchen Appliances"

class DEIncludeBathroomItems(DefaultOnToggle):
    """Include dating bathroom fixtures and personal care items (Characters 43-52)."""
    display_name = "Include Bathroom Items"

class DEIncludeLaundryItems(DefaultOnToggle):
    """Include dating laundry room items and cleaning supplies (Characters 71-80)."""
    display_name = "Include Laundry Items"

class DEIncludeOfficeBedroom(DefaultOnToggle):
    """Include dating office supplies, bedroom items, and personal belongings (Characters 53-70)."""
    display_name = "Include Office & Bedroom Items"

class DEIncludeMiscItems(DefaultOnToggle):
    """Include dating miscellaneous items like tools, keys, and storage (Characters 81-90)."""
    display_name = "Include Miscellaneous Items"

class DEIncludeSpecialConcepts(DefaultOnToggle):
    """Include dating abstract concepts and special characters (Characters 91-100)."""
    display_name = "Include Special Concepts"

class DEIncludeDLCCharacters(DefaultOnToggle):
    """Include dating DLC characters from the Lavish Edition (Characters 101-102)."""
    display_name = "Include DLC Characters"

class DERelationshipGoals(Choice):
    """What kind of relationship outcomes should you focus on?"""
    display_name = "Relationship Goals"
    option_love_focused = "Love Focused"
    option_friendship_focused = "Friendship Focused"
    option_hate_focused = "Hate Focused"
    option_balanced_relationships = "Balanced Relationships"
    option_chaos_romance = "Chaos Romance"
    default = "balanced_relationships"
