from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, Choice, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


# ===== Archipelago Options =====
@dataclass
class DanganronpaArchipelagoOptions:
    danganronpa_owned_games: "DanganronpaOwnedGames"
    danganronpa_enable_story_mode: "DanganronpaEnableStoryMode"
    danganronpa_enable_bonus_modes: "DanganronpaEnableBonusModes"
    danganronpa_include_investigation: "DanganronpaIncludeInvestigation"
    danganronpa_include_class_trial: "DanganronpaIncludeClassTrial"
    danganronpa_include_free_time: "DanganronpaIncludeFreeTime"
    danganronpa_include_report_card: "DanganronpaIncludeReportCard"
    danganronpa_include_skills: "DanganronpaIncludeSkills"
    danganronpa_include_presents: "DanganronpaIncludePresents"
    danganronpa_include_school_mode: "DanganronpaIncludeSchoolMode"
    danganronpa_include_island_mode: "DanganronpaIncludeIslandMode"
    danganronpa_include_utdp: "DanganronpaIncludeUTDP"
    danganronpa_include_extra_minigames: "DanganronpaIncludeExtraMinigames"
    danganronpa_include_collectibles: "DanganronpaIncludeCollectibles"
    danganronpa_logic_difficulty: "DanganronpaLogicDifficulty"
    danganronpa_action_difficulty: "DanganronpaActionDifficulty"
    danganronpa_include_bonus_presents: "DanganronpaIncludeBonusPresents"
    danganronpa_include_post_chapter_presents: "DanganronpaIncludePostChapterPresents"
    danganronpa_include_underwear_presents: "DanganronpaIncludeUnderwearPresents"
    danganronpa_include_summer_camp: "DanganronpaIncludeSummerCamp"


class DanganronpaGame(Game):
    name = "Danganronpa Decadence"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
    ]
    is_adult_only_or_unrated = False
    options_cls = DanganronpaArchipelagoOptions

    # ===== Optional constraints =====
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = []

        if self.logic_difficulty in ["Mean", "Cruel"]:
            constraints.extend([
                GameObjectiveTemplate(
                    label="Complete this objective within DAYS in-game days",
                    data={"DAYS": (self.all_day_counts, 1)},
                ),
                GameObjectiveTemplate(
                    label="Complete this objective without any incorrect statements",
                    data={},
                ),
            ])

        if self.action_difficulty in ["Mean", "Cruel"]:
            constraints.extend([
                GameObjectiveTemplate(
                    label="Complete this objective with at least HEALTH percent health remaining",
                    data={"HEALTH": (self.all_health_thresholds, 1)},
                ),
                GameObjectiveTemplate(
                    label="Complete this objective without using Focus Gauge",
                    data={},
                ),
            ])

        if self.logic_difficulty == "Cruel" or self.action_difficulty == "Cruel":
            constraints.extend([
                GameObjectiveTemplate(label="Complete this objective without retrying", data={}),
                GameObjectiveTemplate(label="Complete this objective without equipping skills", data={}),
            ])

        return constraints

    # ===== Objective templates =====
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = []

        # STORY MODE
        if self.enable_story_mode:
            # Investigation
            if self.include_investigation:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Collect QUANTITY pieces of evidence in LOCATION (Story Mode)",
                        data={
                            "QUANTITY": (self.all_investigation_evidence_quantities, 1),
                            "LOCATION": (self.all_investigation_locations, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Finish all investigation tasks in chapter CHAPTER (Story Mode)",
                        data={"CHAPTER": (self.all_chapters, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=3,
                    ),
                    GameObjectiveTemplate(
                        label="Earn QUANTITY Monocoins during investigations (Story Mode)",
                        data={"QUANTITY": (self.all_monocoins_quantities, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Find a single piece of evidence in LOCATION (Story Mode)",
                        data={"LOCATION": (self.all_investigation_locations, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Complete a basic investigation task (Story Mode)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Examine an object in LOCATION (Story Mode)",
                        data={"LOCATION": (self.all_investigation_locations, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            # Class Trials
            if self.include_class_trial:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Achieve RANK rank in the chapter CHAPTER class trial (Story Mode)",
                        data={
                            "RANK": (self.all_trial_ranks, 1),
                            "CHAPTER": (self.all_chapters, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=4,
                    ),
                    GameObjectiveTemplate(
                        label="Clear QUANTITY segments of MECHANIC without mistakes (Story Mode)",
                        data={
                            "QUANTITY": (self.all_perfect_segment_counts, 1),
                            "MECHANIC": (self.all_trial_mechanics, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=3,
                    ),
                    GameObjectiveTemplate(
                        label="Win a Debate Scrum with at least HEALTH percent health remaining (Story Mode)",
                        data={"HEALTH": (self.all_health_thresholds, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Participate in a class trial segment (Story Mode)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Make a correct statement in a trial (Story Mode)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            # Free Time
            if self.include_free_time:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Max out friendship with STUDENT (Story Mode)",
                        data={"STUDENT": (self.all_students, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Spend QUANTITY Free Time sessions (Story Mode)",
                        data={"QUANTITY": (self.all_free_time_targets, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Have a single Free Time conversation with STUDENT (Story Mode)",
                        data={"STUDENT": (self.all_students, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Complete a basic Free Time event (Story Mode)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Spend time in the dorms (Story Mode)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            # Report Cards
            if self.include_report_card:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Complete the Report Card for STUDENT (Story Mode)",
                        data={"STUDENT": (self.all_students, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Complete Report Cards for QUANTITY different students (Story Mode)",
                        data={"QUANTITY": (self.all_report_card_counts, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=3,
                    ),
                ])

            # Skills
            if self.include_skills:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Obtain the SKILL skill (Story Mode)",
                        data={"SKILL": (self.all_skills, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Earn QUANTITY Hope Fragments (Story Mode)",
                        data={"QUANTITY": (self.all_hope_fragment_quantities, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

            # Presents
            if self.include_presents:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Obtain PRESENT from the MonoMono machine (Story Mode)",
                        data={"PRESENT": (self.all_presents, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Collect QUANTITY different presents (Story Mode)",
                        data={"QUANTITY": (self.all_present_quantities, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Collect QUANTITY different presents (Story Mode)",
                        data={"QUANTITY": (self.all_small_present_quantities, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Gift a Loved present to STUDENT (Story Mode)",
                        data={"STUDENT": (self.all_students, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Gift any present to STUDENT (Story Mode)",
                        data={"STUDENT": (self.all_students, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Visit LOCATION (Story Mode)",
                        data={"LOCATION": (self.all_locations, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Talk to STUDENT once (Story Mode)",
                        data={"STUDENT": (self.all_students, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

        # BONUS MODES
        if self.enable_bonus_modes:
            # School Mode (DR1)
            if "Danganronpa: Trigger Happy Havoc" in self.games_owned and self.include_school_mode:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Complete a School Mode project with DAYS days remaining (DR1)",
                        data={"DAYS": (self.all_school_mode_days, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=3,
                    ),
                    GameObjectiveTemplate(
                        label="Maintain top cleanliness for DAYS consecutive days in School Mode (DR1)",
                        data={"DAYS": (self.all_school_mode_days, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                ])

            # Island Mode (DR2)
            if "Danganronpa 2: Goodbye Despair" in self.games_owned and self.include_island_mode:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Earn all Hope Fragments for STUDENT in Island Mode (DR2)",
                        data={"STUDENT": (self.all_students, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=3,
                    ),
                    GameObjectiveTemplate(
                        label="Reach day DAY in Island Mode without failures (DR2)",
                        data={"DAY": (self.all_island_mode_days, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=4,
                    ),
                ])

            # UTDP (V3)
            if "Danganronpa V3: Killing Harmony" in self.games_owned and self.include_utdp:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Develop a character to level LEVEL in UTDP (V3)",
                        data={"LEVEL": (self.all_utdp_levels, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=4,
                    ),
                    GameObjectiveTemplate(
                        label="Clear floor FLOOR in Monokuma's Test (V3)",
                        data={"FLOOR": (self.all_monokuma_test_floors, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=3,
                    ),
                ])

        # EXTRA MINIGAMES
        if self.include_extra_minigames:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete MINIGAME once without damage",
                    data={"MINIGAME": (self.all_extra_minigames, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Survive DISTANCE meters in Death Road of Despair",
                    data={"DISTANCE": (self.all_death_road_distances, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Clear stage LEVEL in Magical Girl Monomi",
                    data={"LEVEL": (self.all_monogirl_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Play MINIGAME once",
                    data={"MINIGAME": (self.all_extra_minigames, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete a basic minigame level",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Play a simple minigame (Extra Minigames)",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete a quick puzzle (Extra Minigames)",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # COLLECTIBLES
        if self.include_collectibles:
            templates.extend([
                GameObjectiveTemplate(
                    label="Find QUANTITY Hidden Monokuma in chapter CHAPTER",
                    data={
                        "QUANTITY": (self.all_hidden_monokuma_counts, 1),
                        "CHAPTER": (self.all_chapters, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Collect all collectibles in LOCATION",
                    data={"LOCATION": (self.all_locations, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Find a single Hidden Monokuma",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Discover a collectible location",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Check a suspicious spot",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Summer Camp (Danganronpa S)
            if "Danganronpa S: Ultimate Summer Camp" in self.games_owned and self.include_summer_camp:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Reach turn TURN in Development Mode as CHARACTER (Summer Camp)",
                        data={
                            "TURN": (self.all_turn_counts, 1),
                            "CHARACTER": (self.all_summer_camp_characters, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Clear floor FLOOR in Tower of Despair using CHARACTERS (Summer Camp)",
                        data={
                            "FLOOR": (self.all_floors, 1),
                            "CHARACTERS": (self.all_summer_camp_characters, 4),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=4,
                    ),
                    GameObjectiveTemplate(
                        label="Clear floor FLOOR in Tower of Despair with a party that includes CHARACTER (Summer Camp)",
                        data={
                            "FLOOR": (self.all_floors, 1),
                            "CHARACTER": (self.all_summer_camp_characters, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=3,
                    ),
                    GameObjectiveTemplate(
                        label="Clear floor FLOOR in Tower of Despair with a party that includes CHARACTERS (Summer Camp)",
                        data={
                            "FLOOR": (self.all_floors, 1),
                            "CHARACTERS": (self.all_summer_camp_characters, 2),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=3,
                    ),
                    GameObjectiveTemplate(
                        label="Unlock a swimsuit outfit for CHARACTER in Summer Camp mode (Summer Camp)",
                        data={"CHARACTER": (self.all_swimsuit_students, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Collect QUANTITY Summer Camp presents (Summer Camp)",
                        data={"QUANTITY": (self.all_present_quantities, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Defeat BOSS in Summer Camp mode (Summer Camp)",
                        data={"BOSS": (self.all_summer_camp_bosses, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=3,
                    ),GameObjectiveTemplate(
                        label="Acquire a rare card from the MonoMono Machine (Summer Camp)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Play a single Summer Camp match (Summer Camp)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Visit a Summer Camp location (Summer Camp)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Interact with a facility in Summer Camp (Summer Camp)",
                        data={},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                ])

        return templates

    # ===== Static pools =====
    @staticmethod
    def all_chapters() -> List[int]:
        return [1, 2, 3, 4, 5, 6]

    @staticmethod
    def all_investigation_evidence_quantities() -> List[int]:
        return [5, 10, 15, 20]

    @staticmethod
    def all_investigation_locations() -> List[str]:
        return [
            "Classroom", "Dormitory", "Dining Hall", "Gym", "Library", "Warehouse",
            "Garden", "Music Room", "AV Room", "Factory", "Hospital", "Hotel",
            "Old Building", "Casino", "Ultimate Lab",
        ]

    @staticmethod
    def all_trial_ranks() -> List[str]:
        return ["A", "S"]

    @staticmethod
    def all_perfect_segment_counts() -> List[int]:
        return [1, 3, 5, 10]

    @staticmethod
    def all_trial_mechanics() -> List[str]:
        return [
            "Nonstop Debate", "Hangman's Gambit", "Bullet Time Battle", "Panic Talk Action",
            "Rebuttal Showdown", "Logic Dive", "Psyche Taxi", "Mind Mine",
            "Mass Panic Debate", "Debate Scrum", "V-Agree", "Lie Bullet",
        ]

    @staticmethod
    def all_health_thresholds() -> List[int]:
        return [25, 50, 75, 100]

    @staticmethod
    def all_free_time_targets() -> List[int]:
        return [3, 5, 10]

    @staticmethod
    def all_hope_fragment_quantities() -> List[int]:
        return [5, 10, 20, 30]

    @staticmethod
    def all_report_card_counts() -> List[int]:
        return [5, 10, 16]

    @staticmethod
    def all_present_quantities() -> List[int]:
        return [10, 20, 30, 50]

    @staticmethod
    def all_small_present_quantities() -> List[int]:
        return [3, 5, 7]

    @staticmethod
    def all_monocoins_quantities() -> List[int]:
        return [50, 100, 200, 300]

    @staticmethod
    def all_school_mode_days() -> List[int]:
        return [5, 10, 20, 30]

    @staticmethod
    def all_island_mode_days() -> List[int]:
        return [10, 20, 30]

    @staticmethod
    def all_utdp_levels() -> List[int]:
        return [20, 50, 99]

    @staticmethod
    def all_monokuma_test_floors() -> List[int]:
        return [10, 30, 50]

    @staticmethod
    def all_hidden_monokuma_counts() -> List[int]:
        return [5, 10, 20]

    @staticmethod
    def all_summer_camp_floors() -> List[int]:
        return [10, 30, 50, 100]

    @staticmethod
    def all_summer_camp_present_quantities() -> List[int]:
        return [10, 20, 30, 50]

    @staticmethod
    def all_death_road_distances() -> List[int]:
        return [100, 300, 500, 800]

    @staticmethod
    def all_monogirl_levels() -> List[int]:
        return [3, 5, 7, 10]

    @staticmethod
    def all_turn_counts() -> List[int]:
        return [1, 3, 5, 10, 20]

    @staticmethod
    def all_floors() -> List[int]:
        return [1, 5, 10, 30, 50, 100]

    @staticmethod
    def all_quantities() -> List[int]:
        return [1, 5, 10, 20, 30, 50, 100]

    @staticmethod
    def all_day_counts() -> List[int]:
        return [5, 10, 15, 20]

    def all_students(self) -> List[str]:
        students: List[str] = []
        games_owned: List[str] = self.games_owned
        # DR1
        if "Danganronpa: Trigger Happy Havoc" in games_owned:
            students.extend([
                "Makoto Naegi", "Kyoko Kirigiri", "Byakuya Togami", "Toko Fukawa",
                "Aoi Asahina", "Yasuhiro Hagakure", "Kiyotaka Ishimaru", "Mondo Owada",
                "Chihiro Fujisaki", "Leon Kuwata", "Sakura Ogami", "Hifumi Yamada",
                "Celestia Ludenberg", "Sayaka Maizono", "Junko Enoshima", "Mukuro Ikusaba",
            ])
        # DR2
        if "Danganronpa 2: Goodbye Despair" in games_owned:
            students.extend([
                "Hajime Hinata", "Nagito Komaeda", "Chiaki Nanami", "Sonia Nevermind",
                "Gundham Tanaka", "Kazuichi Soda", "Fuyuhiko Kuzuryu", "Peko Pekoyama",
                "Akane Owari", "Nekomaru Nidai", "Teruteru Hanamura", "Mahiru Koizumi",
                "Hiyoko Saionji", "Ibuki Mioda", "Mikan Tsumiki", "Ultimate Imposter",
            ])
        # V3
        if "Danganronpa V3: Killing Harmony" in games_owned:
            students.extend([
                "Shuichi Saihara", "Kaede Akamatsu", "Kaito Momota", "Maki Harukawa",
                "Rantaro Amami", "Ryoma Hoshi", "Kirumi Tojo", "Angie Yonaga",
                "Tenko Chabashira", "Himiko Yumeno", "Korekiyo Shinguji", "Miu Iruma",
                "Gonta Gokuhara", "Kokichi Oma", "K1-B0", "Tsumugi Shirogane",
            ])
        return students

    @staticmethod
    def all_locations() -> List[str]:
        return [
            "Hope's Peak Academy", "Jabberwock Island", "Hotel Mirai", "Old Building",
            "Rocketpunch Market", "Funhouse", "Great Grape Tower", "Ultimate Academy",
            "Casino", "Museum", "Library", "Factory", "Sewer", "Garden", "Gymnasium",
        ]

    @staticmethod
    def all_skills() -> List[str]:
        return [
            "Cool and Composed", "Neural Liberation", "Envious Influence", "Menacing Focus",
            "Algorithm", "Handiwork", "Breathing Technique", "High Voltage",
            "Psychic Focus", "Steady Aim", "Tranquility", "Kind Composure",
        ]

    # Canonical present lists for each game
    DR1_PRESENTS = [
        # 001-090 MonoMono Machine items
        "Mineral Water", "Cola Cola", "Civet Coffee", "Rose Hip Tea", "Sea Salt", "Potato Chips", "Prismatic Hardtack", "Black Croissant", "Sonic Cup-a-Noodle", "Royal Curry", "Ration", "Flotation Donut", "Overflowing Lunch Box", "Sunflower Seeds", "Birdseed", "Kitten Hairclip", "Everlasting Bracelet", "Love Status Ring", "Zoles Diamond", "Hope's Peak Ring", "Blueberry Perfume", "Scarab Brooch", "God of War Charm", "Mac's Gloves", "Glasses", "G-Sick", "Roller Slippers", "Red Scarf", "Bunny Earmuffs", "Fresh Bindings", "Jimmy Decay T-Shirt", "Emperor's Thong", "Hand Bra", "Waterlover", "Demon Angel Princess Figure", "Astral Boy Doll", "Shears", "Layering Shears", "Quality Chinchilla Cover", "Kirlian Camera", "Adorable Reactions Collection", "Tumbleweed", "Unending Dandelion", "Rose in Vitro", "Cherry Blossom Bouquet", "Rose Whip", "Zantetsuken", "Muramasa", "Raygun Zurion", "Golden Gun", "Berserker Armor", "Self-Destructing Cassette", "Silent Receiver", "Pretty Hungry Caterpillar", "Old Timey Radio", "Mr. Fastball", "Antique Doll", "Crystal Skull", "Golden Airplane", "Prince Shotoku's Globe", "Moon Rock", "Asura's Tears", "Secrets of the Omoplata", "Millennium Prize Problems", "The Funplane", "Project Zombie", "Pagan Dancer", "Tips & Tips", "Maiden's Handbag", "Kokeshi Dynamo", "The Second Button", "Someone's Graduation Album", "Vise", "Sacred Tree Sprig", "Pumice", "Oblaat", "Water Flute", "Bojobo Dolls", "Small Light", "Voice-Changing Bowtie", "Ancient Tour Tickets", "Novelist's Fountain Pen", "If Fax", "Cat-Dog Magazine", "Meteorite Arrowhead", "Chin Drill", "Green Costume", "Red Costume"
    ]
    DR1_BONUS = ["A Man's Fantasy", "Escape Button"]
    DR1_POST_CHAPTER = [
        # 8 post-chapter items (names can be filled in as needed)
    ]
    DR1_UNDERWEAR = [
        "Kiyotaka's Undergarments", "Byakuya's Undergarments", "Mondo's Undergarments", "Leon’s Undergarments", "Hifumi's Undergarments", "Yasuhiro's Undergarments", "Sayaka's Undergarments", "Kyoko's Undergarments", "Aoi's Undergarments", "Toko's Undergarments", "Sakura's Undergarments", "Celeste's Undergarments", "Junko's Undergarments", "Chihiro's Undergarments"
    ]

    DR2_PRESENTS = [
        # 001-108 MonoMono Machine items (abbreviated for brevity)
        "Mineral Water", "Ramune", "Coconut Juice", "Blue Ram", "Civet Coffee", "Cinnamon Tea", "Non-Alcoholic Wine", "Prepackaged Orzotto", "Chocolate Chip Jerky", "Cod Roe Baguette", "Gugelhupf Cake", "Hardtack of Hope", "Sweet Bun Bag", "Potato Chips", "Viva Ice", "Jabba's Natural Salt", "Cocoshimi", "Sunflower Seeds", "Coconut", "Iroha T-Shirt", "Brightly Colored Jeans", "Apron Dress", "Falkor's Muffler", "Fresh Bindings", "Queen’s Straitjacket", "Spy Spike", "Secret Boots", "Safety Half-Shoes", "Passionate Glasses", "Bvlbari's Gold", "Earring of Crushed Evil", "Silver Ring", "Hope's Peak Ring", "Spectre Ring", "Cloth Wrap Backpack", "Another Hope", "Jabbaian Jewelry", "Biggest Fantom", "Ubiquitous Handbook", "Millennium Prize Problems", "Tips & Tips 2nd Edition", "Ogami Clan Codex", "Men's Manma", "Kiss Note", "Black Rabbit Picture Book", "2.5D Headphones", "Radiosonde", "Male Cylinder", "Measuring Flask", "Razor Ramon HG", "Infrared Thermometer", "Flash Suppressor", "Lilienthal’s Wings", "Kirlian Photography", "Mr. Stapler", "Small Degenerated Reactor", "Many-Sided Dice Set", "The Funbox", "The Funplane", "American Clacker", "Power Gauntlet", "Mesopotamia", "Nitro Racer", "Slap Bracelet", "Gag Ball", "Kokeshi Dynamo", "Go Stone", "Message In a Bottle", "Old Timey Radio", "Antique Doll", "The Second Button", "Moon Rock", "Another Battle", "Desperation", "1000 Cherry Blossoms", "Paper '10th Act Verse'", "Marine Snow", "Gold Coated Sheath", "Mini Wave-Dissipaters", "Stardust", "Japanese Tea Cup", "Two-Sided Ukulele", "Collapsible Fishing Rod", "Bojobo Dolls", "Century Potpourri", "Absolute Tuning Fork", "Seven Sword", "Sand God's Storm Horn", "Memory Notebook", "Mukuro's Knife", "Broken Warhead", "Girl with the Bear Hairpin", "Bar", "Dip Pen", "Tissue", "Jabba the Frog", "Iguana Daughter", "Dull Kitchen Knife", "Occult Photo Frame", "Lust Setsugekka", "Rose In Vitro", "Skullhead Mask", "Compact Costume", "Angel's Fruit", "Bandage Wrap", "Secret Wind Sword Book", "Hagakure Crystal Ball", "Used Carrot"
    ]
    DR2_BONUS = ["Toy Camera", "Replica Sword", "An An Aan", "Man's Nut", "Summer Festival Tree", "R/C 4WD Battler Taro", "Wooden Stick", "Usami Strap", "Danganronpa IF"]
    DR2_POST_CHAPTER = [
        # 8 post-chapter items (names can be filled in as needed)
    ]
    DR2_UNDERWEAR = [
        "Nagito's Undergarments", "Byakuya's Undergarments", "Gundham's Undergarments", "Kazuichi's Undergarments", "Teruteru's Undergarments", "Nekomaru's Undergarments", "Fuyuhiko's Undergarments", "Akane's Undergarments", "Chiaki's Undergarments", "Sonia's Undergarments", "Hiyoko's Undergarments", "Mahiru's Undergarments", "Mikan's Undergarments", "Ibuki's Undergarments", "Peko's Undergarments"
    ]

    V3_PRESENTS = [
        # 001-113 MonoMono Machine items (abbreviated for brevity)
        "Oolong Tea", "Boba Tea", "Ginger Tea", "Cleopatra's Pearl Cocktail", "Non-Alcoholic Drink of Immortality", "Ketchup", "Sugar", "Olive Oil", "Astro Cake", "Bubble Gum Bomb", "Maple Fudge", "Greek Yogurt", "Bunny Apples", "Rock Hard Ice Cream", "Sukiyaki Caramel", "Candy Cigarette", "Gyoza In the Shape of a Face", "Silver Earring", "Crystal Bangle", "Striped Necktie", "Bondage Boots", "Ultimate Academy Bracelet", "Workout Clothes", "Mono-Jinbei", "Autumn-Colored Scarf", "Hand-Knit Sweater", "Cheer Coat Uniform", "Nail Brush", "Wearable Blanket", "Beret", "Ladybug Brooch", "Cufflinks", "Dog Tag", "White Robot Mustache", "Book of the Blackened", "Feelings of Ham", "Travel Journal", "Dreams Come True Spell Book", "Story of Tokono", "Spla-Teen Vogue", "Fun Book of Animals", "Latest Machine Parts Catalogue", "Stainless Tray", "Tennis Ball Set", "High-End Headphones", "Teddy Bear", "Milk Puzzle", "Illusion Rod", "Hand Mirror", "Prop Carrying Case", "Japanese Doll Wig", "Photoshop Software", "Sewing Kit", "Flame Thunder", "Tattered Music Score", "Indigo Hakama", "Fashionable Glasses", "Gold Origami", "Plastic Moon Buggy Model", "I'm a Picture Book Artist!", "Hand Grips", "Commemorative Medal Set", "Metronome", "Sketchbook", "Art Manikin", "Bird Food", "Proxilingual Device", "Gourd Insect Trap", "Potted Banyan Tree", "Pocket Tissue", "Dancing Haniwa", "Work Chair Of Doom", "3-Hit KO Sandbag", "Sports Towel", "Steel Glasses Case", "Robot Oil", "Clock-Shaped Gaming Console", "Everywhere Parasol", "Three-Layered Lunch Box", "Aluminum Water Bottle", "Jelly Balls", "Upbeat Humidifier", "Earnest Compass", "Semazen Doll", "Weathercock of Barcelous", "Pillow of Admiration", "46 Moves of the Killing Game", "Monkey's Paw", "Art Piece of Spring", "Electric Tempest", "Space Egg", "Super Lucky Button", "Sparkly Sheet", "Hammock", "Cleansing Air Freshener", "Flower for Floromancy"
    ]
    V3_BONUS = ["Variety Cushion", "Key of Love", "To Each Their Own Roulette", "Monomune", "Gun of Man's Passion", "Pure-White Practice Sword", "Dark Belt"]
    V3_POST_CHAPTER = [
        # 8 post-chapter items (names can be filled in as needed)
    ]
    V3_UNDERWEAR = [
        "Kaito's Undergarments", "Ryoma's Undergarments", "Rantaro's Undergarments", "Gonta's Undergarments", "Kokichi's Undergarments", "Korekiyo's Undergarments", "K1-B0's Built-In Parts", "Kirumi's Undergarments", "Himiko's Undergarments", "Maki's Undergarments", "Tenko's Undergarments", "Tsumugi's Undergarments", "Angie's Undergarments", "Miu's Undergarments", "Kaede's Undergarments"
    ]

    def all_presents(self) -> List[str]:
        presents = []
        games_owned = self.games_owned
        # DR1
        if "Danganronpa: Trigger Happy Havoc" in games_owned:
            presents.extend(self.DR1_PRESENTS)
            if self.include_bonus_presents:
                presents.extend(self.DR1_BONUS)
            if self.include_post_chapter_presents:
                presents.extend(self.DR1_POST_CHAPTER)
            if self.include_underwear_presents:
                presents.extend(self.DR1_UNDERWEAR)
        # DR2
        if "Danganronpa 2: Goodbye Despair" in games_owned:
            presents.extend(self.DR2_PRESENTS)
            if self.include_bonus_presents:
                presents.extend(self.DR2_BONUS)
            if self.include_post_chapter_presents:
                presents.extend(self.DR2_POST_CHAPTER)
            if self.include_underwear_presents:
                presents.extend(self.DR2_UNDERWEAR)
        # V3
        if "Danganronpa V3: Killing Harmony" in games_owned:
            presents.extend(self.V3_PRESENTS)
            if self.include_bonus_presents:
                presents.extend(self.V3_BONUS)
            if self.include_post_chapter_presents:
                presents.extend(self.V3_POST_CHAPTER)
            if self.include_underwear_presents:
                presents.extend(self.V3_UNDERWEAR)
        return presents

    @staticmethod
    def all_extra_minigames() -> List[str]:
        return [
            "Magical Girl Monomi",
            "Death Road of Despair",
            "Monokuma's Test",
        ]

    # ===== DefaultOnToggle accessors =====
    @property
    def enable_story_mode(self) -> bool:
        return self.archipelago_options.danganronpa_enable_story_mode.value

    @property
    def enable_bonus_modes(self) -> bool:
        return self.archipelago_options.danganronpa_enable_bonus_modes.value
    @property
    def include_investigation(self) -> bool:
        return self.archipelago_options.danganronpa_include_investigation.value

    @property
    def include_class_trial(self) -> bool:
        return self.archipelago_options.danganronpa_include_class_trial.value

    @property
    def include_free_time(self) -> bool:
        return self.archipelago_options.danganronpa_include_free_time.value

    @property
    def include_report_card(self) -> bool:
        return self.archipelago_options.danganronpa_include_report_card.value

    @property
    def include_skills(self) -> bool:
        return self.archipelago_options.danganronpa_include_skills.value

    @property
    def include_presents(self) -> bool:
        return self.archipelago_options.danganronpa_include_presents.value

    @property
    def include_school_mode(self) -> bool:
        return self.archipelago_options.danganronpa_include_school_mode.value

    @property
    def include_island_mode(self) -> bool:
        return self.archipelago_options.danganronpa_include_island_mode.value

    @property
    def include_utdp(self) -> bool:
        return self.archipelago_options.danganronpa_include_utdp.value

    @property
    def include_extra_minigames(self) -> bool:
        return self.archipelago_options.danganronpa_include_extra_minigames.value

    @property
    def include_collectibles(self) -> bool:
        return self.archipelago_options.danganronpa_include_collectibles.value

    # ===== Difficulty accessors =====
    @property
    def logic_difficulty(self) -> str:
        return self.archipelago_options.danganronpa_logic_difficulty.value

    @property
    def action_difficulty(self) -> str:
        return self.archipelago_options.danganronpa_action_difficulty.value

    # ===== Ownership helper =====
    @property
    def games_owned(self) -> List[str]:
        games_owned: List[str] = list(self.archipelago_options.danganronpa_owned_games.value)
        return sorted(games_owned)

    # Config defaultontoggles for present types
    @property
    def include_bonus_presents(self) -> bool:
        return self.archipelago_options.danganronpa_include_bonus_presents.value

    @property
    def include_post_chapter_presents(self) -> bool:
        return self.archipelago_options.danganronpa_include_post_chapter_presents.value

    @property
    def include_underwear_presents(self) -> bool:
        return self.archipelago_options.danganronpa_include_underwear_presents.value

    @property
    def include_summer_camp(self) -> bool:
        return self.archipelago_options.danganronpa_include_summer_camp.value

    @staticmethod
    def all_summer_camp_characters() -> List[str]:
        return [
            # DR1
            "Makoto Naegi", "Kyoko Kirigiri", "Byakuya Togami", "Toko Fukawa", "Aoi Asahina",
            "Yasuhiro Hagakure", "Kiyotaka Ishimaru", "Mondo Owada", "Chihiro Fujisaki",
            "Leon Kuwata", "Sakura Ogami", "Hifumi Yamada", "Celestia Ludenberg",
            "Sayaka Maizono", "Junko Enoshima", "Mukuro Ikusaba",
            # DR2
            "Hajime Hinata", "Nagito Komaeda", "Chiaki Nanami", "Sonia Nevermind",
            "Gundham Tanaka", "Kazuichi Soda", "Fuyuhiko Kuzuryu", "Peko Pekoyama",
            "Akane Owari", "Nekomaru Nidai", "Teruteru Hanamura", "Mahiru Koizumi",
            "Hiyoko Saionji", "Ibuki Mioda", "Mikan Tsumiki", "Ultimate Imposter",
            # V3
            "Shuichi Saihara", "Kaede Akamatsu", "Kaito Momota", "Maki Harukawa",
            "Rantaro Amami", "Ryoma Hoshi", "Kirumi Tojo", "Angie Yonaga",
            "Tenko Chabashira", "Himiko Yumeno", "Korekiyo Shinguji", "Miu Iruma",
            "Gonta Gokuhara", "Kokichi Oma", "K1-B0", "Tsumugi Shirogane",
            # Mascots
            "Monokuma", "Usami",
        ]

    @staticmethod
    def all_swimsuit_students() -> List[str]:
        return [
            # DR1
            "Makoto Naegi", "Kyoko Kirigiri", "Byakuya Togami", "Toko Fukawa",
            "Aoi Asahina", "Sayaka Maizono", "Celestia Ludenberg", "Junko Enoshima", "Mukuro Ikusaba",
            # DR2
            "Hajime Hinata", "Nagito Komaeda", "Chiaki Nanami", "Sonia Nevermind",
            "Ibuki Mioda", "Hiyoko Saionji", "Mahiru Koizumi", "Akane Owari",
            "Mikan Tsumiki", "Peko Pekoyama",
            # V3
            "Kaede Akamatsu", "Shuichi Saihara", "Maki Harukawa", "Kaito Momota",
            "Kokichi Oma", "Miu Iruma", "Angie Yonaga", "Tenko Chabashira",
            "Himiko Yumeno", "Tsumugi Shirogane",
        ]



    @staticmethod
    def all_summer_camp_bosses() -> List[str]:
        return [
        "Monobeast Alpha", "Monobeast Omega", "Usami Flower", "Ultimate Warrior Monokuma",
        "Tower Guardian", "Despair Queen Junko", "Secret Boss ???"
        ]



# ===== Ownership =====
class DanganronpaOwnedGames(OptionSet):
    """Select which Danganronpa games you own"""
    display_name = "Owned Games"
    default = [
        "Danganronpa: Trigger Happy Havoc",
        "Danganronpa 2: Goodbye Despair",
        "Danganronpa V3: Killing Harmony",
        "Danganronpa S: Ultimate Summer Camp"
    ]


# ===== Mode Filters =====
class DanganronpaEnableStoryMode(DefaultOnToggle):
    """Enable main story mode objectives and progression."""
    display_name = "Enable Story Mode Objectives"

class DanganronpaEnableBonusModes(DefaultOnToggle):
    """Enable bonus mode objectives and additional content."""
    display_name = "Enable Bonus Mode Objectives"

# ===== Category DefaultOnToggles =====
class DanganronpaIncludeInvestigation(DefaultOnToggle):
    """Include investigation and mystery-solving objectives."""
    display_name = "Include Investigation Objectives"

class DanganronpaIncludeClassTrial(DefaultOnToggle):
    """Include class trial and debate objectives."""
    display_name = "Include Class Trial Objectives"

class DanganronpaIncludeFreeTime(DefaultOnToggle):
    """Include free time and social interaction objectives."""
    display_name = "Include Free Time Objectives"

class DanganronpaIncludeReportCard(DefaultOnToggle):
    """Include report card and academic achievement objectives."""
    display_name = "Include Report Card Objectives"

class DanganronpaIncludeSkills(DefaultOnToggle):
    """Include skill development and talent objectives."""
    display_name = "Include Skill Objectives"

class DanganronpaIncludePresents(DefaultOnToggle):
    """Include present-giving and gift objectives."""
    display_name = "Include Present Objectives"

class DanganronpaIncludeSchoolMode(DefaultOnToggle):
    """Include school mode and educational objectives."""
    display_name = "Include School Mode Objectives"

class DanganronpaIncludeIslandMode(DefaultOnToggle):
    """Include island mode and vacation objectives."""
    display_name = "Include Island Mode Objectives"

class DanganronpaIncludeUTDP(DefaultOnToggle):
    """Include Ultimate Talent Development Plan objectives."""
    display_name = "Include UTDP Objectives"

class DanganronpaIncludeSummerCamp(DefaultOnToggle):
    """Include summer camp and team-building objectives."""
    display_name = "Include Summer Camp Objectives"

class DanganronpaIncludeExtraMinigames(DefaultOnToggle):
    """Include extra minigame and side activity objectives."""
    display_name = "Include Extra Minigame Objectives"

class DanganronpaIncludeCollectibles(DefaultOnToggle):
    """Include collectible hunting and completion objectives."""
    display_name = "Include Collectibles Objectives"

class DanganronpaIncludeBonusPresents(DefaultOnToggle):
    """Include bonus present and reward objectives."""
    display_name = "Include Bonus Presents"

class DanganronpaIncludePostChapterPresents(DefaultOnToggle):
    """Include post-chapter present and epilogue objectives."""
    display_name = "Include Post-Chapter Presents"

class DanganronpaIncludeUnderwearPresents(DefaultOnToggle):
    """Include underwear present and intimate objectives."""
    display_name = "Include Underwear Presents"

# ===== Difficulty =====
class DanganronpaLogicDifficulty(Choice):
    """Adjust the difficulty level for logic-based objectives."""
    display_name = "Logic Difficulty"
    option_gentle = "Gentle"
    option_kind = "Kind"
    option_mean = "Mean"
    option_cruel = "Cruel"
    default = "kind"

class DanganronpaActionDifficulty(Choice):
    """Adjust the difficulty level for action-based objectives."""
    display_name = "Action Difficulty"
    option_gentle = "Gentle"
    option_kind = "Kind"
    option_mean = "Mean"
    option_cruel = "Cruel"
    default = "kind"
