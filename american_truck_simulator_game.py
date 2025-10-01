from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, TextChoice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class AmericanTruckSimulatorArchipelagoOptions:
    ats_include_interstate_delivery: ATSIncludeInterstateDelivery
    ats_include_state_exploration: ATSIncludeStateExploration
    ats_include_truck_ownership: ATSIncludeTruckOwnership
    ats_include_long_haul: ATSIncludeLongHaul
    ats_include_heavy_haul: ATSIncludeHeavyHaul
    ats_include_business_objectives: ATSIncludeBusinessObjectives
    ats_include_dlc_content: ATSIncludeDlcContent
    ats_difficulty_level: ATSDifficultyLevel


class AmericanTruckSimulatorGame(Game):
    name = "American Truck Simulator"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = AmericanTruckSimulatorArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective with perfect DOT compliance (no violations)",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective with FUEL_ECONOMY average fuel economy",
                data={"FUEL_ECONOMY": (self.fuel_economy_levels, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without any truck or cargo damage",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective using only TRUCK_BRAND trucks",
                data={"TRUCK_BRAND": (self.truck_brands, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective during DRIVING_TIME local time",
                data={"DRIVING_TIME": (self.driving_times, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective in WEATHER conditions",
                data={"WEATHER": (self.weather_conditions, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective using scenic routes (25% longer travel time)",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective using manual transmission only",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective with perfect parking scores only",
                data={},
            ),
            GameObjectiveTemplate(
                label="Cross state lines unnecessarily during this objective",
                data={},
            ),
        ])
        
        return constraints
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = []

        # Interstate delivery objectives (most common in American trucking)
        if self.include_interstate_delivery:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Transport CARGO from ORIGIN to DESTINATION",
                    data={
                        "CARGO": (self.cargo_types, 1),
                        "ORIGIN": (self.cities, 1),
                        "DESTINATION": (self.cities, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=18,
                ),
            ])

        # State exploration objectives
        if self.include_state_exploration:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete deliveries to COUNT different cities in STATE",
                    data={
                        "COUNT": (self.city_counts, 1),
                        "STATE": (self.states, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
            ])

        # Truck ownership objectives (American truck culture)
        if self.include_truck_ownership:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Purchase and own a TRUCK_BRAND truck",
                    data={"TRUCK_BRAND": (self.truck_brands, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=7,
                ),
            ])

        # Long haul coast-to-coast routes
        if self.include_long_haul:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the 1500+ mile journey from Los Angeles to Houston",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete the 2100+ mile journey from Seattle to Dallas",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete the 1200+ mile journey from San Francisco to Denver",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete the 1000+ mile journey from Phoenix to Kansas City",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete the 1700+ mile journey from Portland to Oklahoma City",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
            ])

        # Heavy haul objectives (American heavy haul)
        if self.include_heavy_haul:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Transport oversized SPECIAL_CARGO from ORIGIN to DESTINATION with permits",
                    data={
                        "SPECIAL_CARGO": (self.special_cargo, 1),
                        "ORIGIN": (self.cities, 1),
                        "DESTINATION": (self.cities, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=5,
                ),
            ])

        # Business expansion objectives
        if self.include_business_objectives:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Hire DRIVER_COUNT AI drivers and establish GARAGE_COUNT garages in different states",
                    data={
                        "DRIVER_COUNT": (self.cargo_delivery_counts, 1),
                        "GARAGE_COUNT": (self.garage_counts, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Earn REVENUE in total revenue from deliveries",
                    data={"REVENUE": (self.business_revenue_targets, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Drive MILES miles across America's highways",
                    data={"MILES": (self.milestone_miles, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # American trucking culture objectives
        game_objective_templates.extend([
            GameObjectiveTemplate(
                label="Visit and rest at COUNT different truck stops across America",
                data={"COUNT": (self.rest_stop_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Achieve perfect parking scores on COUNT different deliveries",
                data={"COUNT": (self.parking_score_counts, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Successfully navigate urban environments in COUNT major cities",
                data={"COUNT": (self.major_city_counts, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ])

        # DLC-specific objectives
        if self.include_dlc_content:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete COUNT deliveries across the DLC_REGION expansion region",
                    data={
                        "COUNT": (self.dlc_delivery_counts, 1),
                        "DLC_REGION": (self.dlc_regions, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=6,
                ),
            ])

        # Specialized transport objectives
        game_objective_templates.extend([
            GameObjectiveTemplate(
                label="Complete COUNT hazardous materials deliveries with perfect safety record",
                data={"COUNT": (self.hazmat_delivery_counts, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Successfully transport COUNT oversized loads requiring escort vehicles",
                data={"COUNT": (self.oversized_load_counts, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ])

        return game_objective_templates

    @property 
    def include_interstate_delivery(self) -> bool:
        return self.archipelago_options.ats_include_interstate_delivery.value

    @property
    def include_state_exploration(self) -> bool:
        return self.archipelago_options.ats_include_state_exploration.value

    @property
    def include_truck_ownership(self) -> bool:
        return self.archipelago_options.ats_include_truck_ownership.value

    @property
    def include_long_haul(self) -> bool:
        return self.archipelago_options.ats_include_long_haul.value

    @property
    def include_heavy_haul(self) -> bool:
        return self.archipelago_options.ats_include_heavy_haul.value

    @property
    def include_business_objectives(self) -> bool:
        return self.archipelago_options.ats_include_business_objectives.value

    @property
    def include_dlc_content(self) -> bool:
        return self.archipelago_options.ats_include_dlc_content.value

    @property
    def difficulty_level(self) -> str:
        return self.archipelago_options.ats_difficulty_level.value

    # Data lists
    @staticmethod
    def states() -> List[str]:
        """States available in ATS (including DLCs) - verified from official spreadsheet data"""
        return [
            "California", "Nevada", "Arizona", "New Mexico", "Oregon", "Washington", 
            "Utah", "Idaho", "Colorado", "Wyoming", "Montana", "Texas", "Oklahoma", 
            "Kansas", "Nebraska", "Arkansas", "Missouri"
        ]

    @staticmethod
    def cities() -> List[str]:
        """Major cities across America - verified from official spreadsheet data"""
        return [
            # Arizona (Arizona DLC)
            "Clifton", "Camp Verde", "Flagstaff", "Grand Canyon Village", "Holbrook", "Kayenta", "Kingman", 
            "Nogales", "Page", "Phoenix", "San Simon", "Show Low", "Sierra Vista", "Tucson", "Yuma",
            # Arkansas (Arkansas DLC)
            "El Dorado", "Fayetteville", "Fort Smith", "Harrison", "Hot Springs", "Jonesboro", 
            "Little Rock", "Pine Bluff", "Springdale", "Texarkana",
            # California & Nevada (Base Game)
            "Bakersfield", "Barstow", "Blythe", "El Centro", "Eureka", "Fresno", "Hilt", "Huron", 
            "Indio", "Los Angeles", "Modesto", "Mojave", "Oakland", "Oxnard", "Redding", 
            "Sacramento", "San Diego", "San Francisco", "San Jose", "San Rafael", "Santa Cruz", 
            "Santa Maria", "Stockton", "Truckee", "Ukiah",
            "Carson City", "Elko", "Ely", "Jackpot", "Las Vegas", "Pioche", "Primm", "Reno", 
            "Tonopah", "Winnemucca",
            # Colorado (Colorado DLC)
            "Alamosa", "Burlington", "Colorado Springs", "Denver", "Durango", "Fort Collins", 
            "Grand Junction", "Lamar", "Montrose", "Pueblo", "Rangely", "Steamboat Springs", "Sterling",
            # Idaho (Idaho DLC)
            "Boise", "Coeur d'Alene", "Grangeville", "Idaho Falls", "Ketchum", "Lewiston", 
            "Nampa", "Pocatello", "Salmon", "Sandpoint", "Twin Falls",
            # Kansas (Kansas DLC)
            "Colby", "Dodge City", "Emporia", "Garden City", "Hays", "Hutchinson", "Junction City", 
            "Kansas City", "Marysville", "Phillipsburg", "Pittsburg", "Salina", "Topeka", "Wichita",
            # Missouri (Missouri DLC)
            "Cape Girardeau", "Columbia", "Jefferson City", "Joplin", "Kansas City", "Kirksville", 
            "Maryville", "Poplar Bluff", "Rolla", "Springfield", "St. Joseph", "St. Louis",
            # Montana (Montana DLC)
            "Billings", "Bozeman", "Butte", "Glasgow", "Glendive", "Great Falls", "Havre", 
            "Helena", "Kalispell", "Laurel", "Lewistown", "Miles City", "Missoula", "Sidney", "Thompson Falls",
            # Nebraska (Nebraska DLC)
            "Alliance", "Chadron", "Columbus", "Grand Island", "Lincoln", "McCook", "Norfolk", 
            "North Platte", "Omaha", "Scottsbluff", "Sidney", "Valentine",
            # New Mexico (New Mexico DLC)
            "Alamogordo", "Albuquerque", "Artesia", "Carlsbad", "Clovis", "Farmington", "Gallup", 
            "Hobbs", "Las Cruces", "Raton", "Roswell", "Santa Fe", "Socorro", "Tucumcari",
            # Oklahoma (Oklahoma DLC)
            "Ardmore", "Clinton", "Enid", "Guymon", "Idabel", "Lawton", "McAlester", 
            "Oklahoma City", "Tulsa", "Woodward",
            # Oregon (Oregon DLC)
            "Astoria", "Bend", "Burns", "Coos Bay", "Eugene", "Klamath Falls", "Lakeview", 
            "Medford", "Newport", "Ontario", "Pendleton", "Portland", "Salem", "The Dalles",
            # Texas (Texas DLC)
            "Abilene", "Amarillo", "Austin", "Beaumont", "Brownsville", "Corpus Christi", 
            "Dalhart", "Dallas", "Del Rio", "El Paso", "Fort Stockton", "Fort Worth", "Galveston", 
            "Houston", "Huntsville", "Junction", "Laredo", "Longview", "Lubbock", "Lufkin", 
            "McAllen", "Odessa", "San Angelo", "San Antonio", "Tyler", "Van Horn", "Victoria", 
            "Waco", "Wichita Falls",
            # Utah (Utah DLC)
            "Cedar City", "Logan", "Moab", "Ogden", "Price", "Provo", "Salina", 
            "Salt Lake City", "St. George", "Vernal",
            # Washington (Washington DLC)
            "Aberdeen", "Bellingham", "Colville", "Everett", "Grand Coulee", "Kennewick", 
            "Longview", "Olympia", "Omak", "Port Angeles", "Seattle", "Spokane", "Tacoma", 
            "Vancouver", "Wenatchee", "Yakima",
            # Wyoming (Wyoming DLC)
            "Cody", "Casper", "Cheyenne", "Evanston", "Gillette", "Jackson", "Laramie", 
            "Rawlins", "Riverton", "Rock Springs", "Sheridan"
        ]

    @staticmethod
    def truck_brands() -> List[str]:
        """American truck manufacturers in ATS"""
        return ["Freightliner", "International", "Kenworth", "Mack", "Peterbilt", "Volvo", "Western Star"]

    @staticmethod
    def truck_models() -> List[str]:
        """Specific truck models - verified from official spreadsheet data"""
        return [
            "Freightliner Cascadia 2019", "Freightliner Cascadia 2025",
            "International LoneStar", "International LT", "International 9900i", "International HX",
            "Kenworth T680 Classic", "Kenworth T680", "Kenworth W900", "Kenworth W990", 
            "Mack Anthem 2018", "Mack Pinnacle", "Mack Pioneer",
            "Peterbilt 389", "Peterbilt 579 Classic", "Peterbilt 579", "Peterbilt 589",
            "Volvo VNL 2014", "Volvo VNL 2018", "Volvo VNL 2024",
            "Western Star 49X", "Western Star 57X", "Western Star 5700XE"
        ]

    @staticmethod
    def cargo_types() -> List[str]:
        """Cargo types available in ATS"""
        return [
            "Food Products", "Machinery", "Electronics", "Chemicals", "Construction Materials",
            "Automotive Parts", "Textiles", "Paper Products", "Metal Products", "Glass Products",
            "Pharmaceutical", "Fuel", "Logs", "Containers", "Livestock", "Refrigerated Goods",
            "Agricultural Products", "Oil & Gas Equipment", "Mining Equipment", "Wind Energy Components"
        ]

    @staticmethod
    def special_cargo() -> List[str]:
        """Special/Heavy cargo from DLCs"""
        return [
            "Wind Turbine Blades", "Transformers", "Construction Vehicles", "Mining Trucks", 
            "Industrial Equipment", "Concrete Beams", "Steel Coils", "Mobile Cranes",
            "Farm Machinery", "JCB Equipment", "Forest Machinery", "Volvo Construction Equipment"
        ]

    @staticmethod
    def city_counts() -> List[int]:
        return [3, 4, 5]

    @staticmethod
    def fuel_economy_levels() -> List[str]:
        return ["7 MPG", "8 MPG", "9 MPG"]

    @staticmethod
    def driving_times() -> List[str]:
        return ["night (10 PM - 6 AM)", "early morning (6 AM - 10 AM)"]

    @staticmethod
    def weather_conditions() -> List[str]:
        return ["storms", "snow", "fog", "heavy rain"]

    @staticmethod
    def cargo_delivery_counts() -> List[int]:
        return [5, 8, 10]

    @staticmethod
    def garage_counts() -> List[int]:
        return [3, 4, 5]

    @staticmethod
    def rest_stop_counts() -> List[int]:
        return [15, 25, 35]

    @staticmethod
    def parking_score_counts() -> List[int]:
        return [15, 25, 35]

    @staticmethod
    def major_city_counts() -> List[int]:
        return [3, 5, 7]

    @staticmethod
    def dlc_delivery_counts() -> List[int]:
        return [4, 6, 8]

    @staticmethod
    def hazmat_delivery_counts() -> List[int]:
        return [10, 15, 20]

    @staticmethod
    def oversized_load_counts() -> List[int]:
        return [5, 10, 15]

    @staticmethod
    def business_revenue_targets() -> List[str]:
        return ["$1,000,000", "$2,000,000", "$5,000,000"]

    @staticmethod
    def milestone_miles() -> List[str]:
        return ["3,000", "3,000", "3,000", "6,000", "6,000", "12,000"]

    @staticmethod
    def long_haul_miles() -> List[int]:
        return [1000, 1500, 2000, 2500]

    @staticmethod
    def dlc_regions() -> List[str]:
        """DLC expansions - verified from official spreadsheet data"""
        return [
            "New Mexico", "Oregon", "Washington", "Utah", "Idaho", "Colorado", "Wyoming", 
            "Montana", "Texas", "Oklahoma", "Kansas", "Nebraska", "Arkansas", "Missouri"
        ]


# Option classes would typically be defined elsewhere, but including stubs for completeness
class ATSIncludeInterstateDelivery(DefaultOnToggle):
    """Include interstate delivery objectives"""
    display_name = "Include Interstate Delivery"

class ATSIncludeStateExploration(DefaultOnToggle):
    """Include state exploration objectives"""
    display_name = "Include State Exploration"

class ATSIncludeTruckOwnership(DefaultOnToggle):
    """Include truck ownership objectives"""
    display_name = "Include Truck Ownership"

class ATSIncludeLongHaul(DefaultOnToggle):
    """Include long haul objectives"""
    display_name = "Include Long Haul"

class ATSIncludeHeavyHaul(DefaultOnToggle):
    """Include heavy haul objectives"""
    display_name = "Include Heavy Haul"

class ATSIncludeBusinessObjectives(DefaultOnToggle):
    """Include business objectives"""
    display_name = "Include Business Objectives"

class ATSIncludeDlcContent(DefaultOnToggle):
    """Include DLC content objectives"""
    display_name = "Include DLC Content"

class ATSDifficultyLevel(TextChoice):
    """Set the difficulty level for objectives"""
    display_name = "Difficulty Level"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    
    default = 1
