from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class EuroTruckSimulator2ArchipelagoOptions:
    ets2_include_delivery_objectives: ETS2IncludeDeliveryObjectives
    ets2_include_country_exploration: ETS2IncludeCountryExploration
    ets2_include_truck_ownership: ETS2IncludeTruckOwnership
    ets2_include_long_distance: ETS2IncludeLongDistance
    ets2_include_special_transport: ETS2IncludeSpecialTransport
    ets2_include_business_objectives: ETS2IncludeBusinessObjectives
    ets2_include_dlc_content: ETS2IncludeDlcContent
    ets2_difficulty_level: ETS2DifficultyLevel


class EuroTruckSimulator2Game(Game):
    name = "Euro Truck Simulator 2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = EuroTruckSimulator2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective with FUEL_EFFICIENCY fuel efficiency rating",
                data={"FUEL_EFFICIENCY": (self.fuel_efficiency_levels, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective TIME_PRESSURE faster than standard time",
                data={"TIME_PRESSURE": (self.time_pressure_levels, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without any cargo or truck damage",
                data={},
            ),
            GameObjectiveTemplate(
                label="Complete this objective using only TRUCK_BRAND trucks",
                data={"TRUCK_BRAND": (self.truck_brands, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective during DRIVING_TIME hours",
                data={"DRIVING_TIME": (self.driving_times, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective in WEATHER conditions",
                data={"WEATHER": (self.weather_conditions, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective taking economical routes (avoid toll roads)",
                data={},
            ),
        ])
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = []

        # Delivery objectives (most common)
        if self.include_delivery_objectives:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Deliver CARGO from ORIGIN to DESTINATION",
                    data={
                        "CARGO": (self.cargo_types, 1),
                        "ORIGIN": (self.cities, 1),
                        "DESTINATION": (self.cities, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=15,
                ),
            ])

        # Country exploration objectives
        if self.include_country_exploration:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete deliveries to COUNT different cities in COUNTRY",
                    data={
                        "COUNT": (self.city_counts, 1),
                        "COUNTRY": (self.countries, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=8,
                ),
            ])

        # Truck ownership objectives
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

        # Long distance challenges
        if self.include_long_distance:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the challenging 1800km route from London to Rome",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete the challenging 2500km route from Stockholm to Madrid",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete the challenging 1900km route from Berlin to Moscow",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete the challenging 1400km route from Paris to Warsaw",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete the challenging 1300km route from Amsterdam to Budapest",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
            ])

        # Special cargo objectives
        if self.include_special_transport:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Transport SPECIAL_CARGO from ORIGIN to DESTINATION with special handling",
                    data={
                        "SPECIAL_CARGO": (self.special_cargo, 1),
                        "ORIGIN": (self.cities, 1),
                        "DESTINATION": (self.cities, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=4,
                ),
            ])

        # Business growth objectives
        if self.include_business_objectives:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Hire DRIVER_COUNT AI drivers and establish GARAGE_COUNT garages",
                    data={
                        "DRIVER_COUNT": (self.business_delivery_counts, 1),
                        "GARAGE_COUNT": (self.business_garage_counts, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Earn REVENUE in total revenue from deliveries",
                    data={"REVENUE": (self.revenue_targets, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Skill development objectives
        game_objective_templates.extend([
            GameObjectiveTemplate(
                label="Complete COUNT deliveries with excellent fuel efficiency ratings",
                data={"COUNT": (self.special_transport_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Successfully complete COUNT deliveries with perfect parking scores",
                data={"COUNT": (self.dangerous_goods_counts, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
        ])

        # DLC exploration objectives  
        if self.include_dlc_content:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete COUNT deliveries in the DLC_REGION expansion area",
                    data={
                        "COUNT": (self.dlc_delivery_counts, 1),
                        "DLC_REGION": (self.dlc_regions, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        # European-specific objectives
        game_objective_templates.extend([
            GameObjectiveTemplate(
                label="Complete deliveries through COUNT different European toll systems efficiently",
                data={"COUNT": (self.toll_system_counts, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete COUNT deliveries without any traffic violations across Europe",
                data={"COUNT": (self.violation_free_counts, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ])

        return game_objective_templates

    @property 
    def include_delivery_objectives(self) -> bool:
        return self.archipelago_options.ets2_include_delivery_objectives.value

    @property
    def include_country_exploration(self) -> bool:
        return self.archipelago_options.ets2_include_country_exploration.value

    @property
    def include_truck_ownership(self) -> bool:
        return self.archipelago_options.ets2_include_truck_ownership.value

    @property
    def include_long_distance(self) -> bool:
        return self.archipelago_options.ets2_include_long_distance.value

    @property
    def include_special_transport(self) -> bool:
        return self.archipelago_options.ets2_include_special_transport.value

    @property
    def include_business_objectives(self) -> bool:
        return self.archipelago_options.ets2_include_business_objectives.value

    @property
    def include_dlc_content(self) -> bool:
        return self.archipelago_options.ets2_include_dlc_content.value

    @property
    def difficulty_level(self) -> str:
        return self.archipelago_options.ets2_difficulty_level.value

    # Data lists
    @staticmethod
    def countries() -> List[str]:
        """Countries available in ETS2 (including DLCs) - verified from official spreadsheet data"""
        return [
            "Germany", "United Kingdom", "France", "Italy", "Netherlands", "Belgium", 
            "Austria", "Switzerland", "Czech Republic", "Slovakia", "Poland", "Hungary",
            "Lithuania", "Latvia", "Estonia", "Russia", "Denmark", "Sweden", "Norway",
            "Finland", "Spain", "Portugal", "Romania", "Bulgaria", "Serbia", "Croatia",
            "Slovenia", "Bosnia and Herzegovina", "Montenegro", "North Macedonia", "Albania",
            "Luxembourg", "Turkey", "Kosovo", "Greece"
        ]

    @staticmethod
    def cities() -> List[str]:
        """Major cities across Europe - enhanced with official spreadsheet data"""
        return [
            # Germany
            "Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt am Main", "Stuttgart", "Düsseldorf", "Dortmund", "Bremen", "Hannover",
            "Kassel", "Kiel", "Leipzig", "Magdeburg", "Mannheim", "Nürnberg", "Osnabrück", "Rostock", "Travemünde", "Dresden", "Erfurt", "Duisburg",
            # UK
            "London", "Manchester", "Birmingham", "Liverpool", "Edinburgh", "Glasgow", "Cardiff", "Newcastle-upon-Tyne", "Sheffield", "Cambridge",
            "Aberdeen", "Dover", "Felixstowe", "Grimsby", "Plymouth", "Southampton", "Swansea", "Carlisle",
            # France  
            "Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Strasbourg", "Nantes", "Bordeaux", "Lille", "Rennes",
            "Calais", "Dijon", "Metz", "Le Havre", "Le Mans", "Limoges", "Montpellier", "Orléans", "Clermont-Ferrand", "Brest", "La Rochelle",
            # Italy
            "Rome", "Milan", "Naples", "Turin", "Palermo", "Genoa", "Bologna", "Florence", "Bari", "Venice",
            "Verona", "Trieste", "Ancona", "Catania", "Livorno", "Messina", "Parma", "Pescara", "Taranto", "Cagliari", "Sassari", "Olbia",
            # Netherlands
            "Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven", "Groningen",
            # Belgium
            "Brussels", "Antwerp", "Ghent", "Charleroi", "Liège", "Bruges",
            # Other European cities from official data
            "Vienna", "Graz", "Salzburg", "Innsbruck", "Linz", "Klagenfurt am Wörthersee", # Austria
            "Zurich", "Geneva", "Bern", # Switzerland
            "Prague", "Brno", "Ostrava", # Czech Republic  
            "Warsaw", "Kraków", "Gdańsk", "Poznań", "Wrocław", "Łódź", "Szczecin", "Katowice", "Lublin", "Białystok", "Olsztyn", # Poland
            "Budapest", "Debrecen", "Pécs", "Szeged", # Hungary
            "Bratislava", "Košice", "Banská Bystrica", # Slovakia
            "Stockholm", "Göteborg", "Malmö", "Uppsala", "Västerås", "Örebro", "Linköping", "Helsingborg", "Jönköping", # Sweden
            "Oslo", "Bergen", "Stavanger", "Kristiansand", # Norway
            "Copenhagen", "Aalborg", "Odense", "Esbjerg", "Frederikshavn", "Gedser", "Hirtshals", # Denmark
            "Helsinki", "Tampere", "Turku", "Pori", "Kotka", "Naantali", "Kouvola", "Lahti", "Loviisa", "Olkiluoto", # Finland
            "Madrid", "Barcelona", "Sevilla", "Valencia", "Bilbao", "Granada", "Córdoba", "Málaga", "Zaragoza", "Santander", "A Coruña", "Vigo", # Spain
            "Lisbon", "Porto", "Faro", "Coimbra", "Évora", "Guarda", "Beja", "Setúbal", "Sines", "Olhão", # Portugal
            "Bucharest", "Cluj-Napoca", "Timișoara", "Iași", "Constanța", "Craiova", "Brașov", "Galati", "Pitești", "Bacău", # Romania
            "Sofia", "Plovdiv", "Varna", "Burgas", "Ruse", "Pleven", "Veliko Tarnovo", "Pernik", "Karlovo", "Pirdop", "Kozloduy", # Bulgaria
            "Zagreb", "Split", "Rijeka", "Osijek", "Zadar", # Croatia
            "Belgrade", "Novi Sad", "Niš", "Kragujevac", # Serbia
            "Ljubljana", "Maribor", "Koper", "Novo Mesto", # Slovenia
            "Sarajevo", "Banja Luka", "Tuzla", "Zenica", "Mostar", "Bihać", "Karakaj", # Bosnia and Herzegovina
            "Podgorica", "Nikšić", "Bijelo Polje", # Montenegro
            "Skopje", "Bitola", # North Macedonia
            "Tirana", "Durrës", "Fier", "Vlorë", # Albania
            "Pristina", # Kosovo
            "Luxembourg", # Luxembourg
            "Istanbul", "Edirne", "Tekirdağ", # Turkey
            "Athens", "Thessaloniki", "Patras", "Iraklion", "Larissa", "Kavala", "Rhodes", "Chania", "Lamia", "Kalamata", # Greece
            "Vilnius", "Kaunas", "Klaipėda", "Šiauliai", "Panevėžys", "Utena", "Mažeikiai", # Lithuania
            "Riga", "Daugavpils", "Liepāja", "Ventspils", "Rēzekne", "Valmiera", # Latvia
            "Tallinn", "Tartu", "Narva", "Pärnu", "Kunda", "Paldiski", # Estonia
            "Saint Petersburg", "Kaliningrad", "Pskov", "Vyborg", "Luga", "Sosnovy Bor" # Russia
        ]

    @staticmethod
    def truck_brands() -> List[str]:
        """Truck manufacturers in ETS2"""
        return ["Scania", "Volvo", "Mercedes-Benz", "MAN", "Iveco", "DAF", "Renault"]

    @staticmethod
    def cargo_types() -> List[str]:
        """Cargo types available"""
        return [
            "Food Products", "Machinery", "Electronics", "Chemicals", "Construction Materials",
            "Automotive Parts", "Textiles", "Paper Products", "Metal Products", "Glass Products",
            "Pharmaceutical", "Fuel", "Logs", "Containers", "Livestock", "Refrigerated Goods",
            "Heavy Cargo", "Oversized Cargo", "Hazardous Materials", "Agricultural Products"
        ]

    @staticmethod
    def special_cargo() -> List[str]:
        """Special cargo from DLCs"""
        return [
            "Wind Turbine Parts", "Bridge Sections", "Industrial Equipment", "Mining Equipment",
            "Construction Vehicles", "Transformers", "Concrete Beams", "Steel Coils"
        ]

    @staticmethod
    def dlc_regions() -> List[str]:
        """DLC regions - verified from official spreadsheet data"""
        return [
            "Going East! (Poland, Czech Republic, Slovakia, Hungary)",
            "Scandinavia (Denmark, Norway, Sweden)",
            "Vive la France! (France expansion)",
            "Italia (Italy expansion)", 
            "Beyond the Baltic Sea (Lithuania, Latvia, Estonia, parts of Russia and Finland)",
            "Road to the Black Sea (Romania, Bulgaria, parts of Turkey)",
            "Iberia (Spain, Portugal)",
            "West Balkans (Croatia, Serbia, Slovenia, Bosnia and Herzegovina, Montenegro, North Macedonia, Albania, Kosovo)",
            "Greece (Greece expansion)"
        ]

    @staticmethod
    def fuel_efficiency_levels() -> List[str]:
        return ["Good", "Excellent"]

    @staticmethod
    def time_pressure_levels() -> List[str]:
        return ["20%", "30%"]

    @staticmethod
    def driving_times() -> List[str]:
        return ["night (22:00-06:00)", "early morning (06:00-10:00)"]

    @staticmethod
    def weather_conditions() -> List[str]:
        return ["rain", "snow", "fog"]

    @staticmethod
    def city_counts() -> List[int]:
        return [3, 4, 5]

    @staticmethod
    def dlc_delivery_counts() -> List[int]:
        return [3, 5, 7]

    @staticmethod
    def toll_system_counts() -> List[int]:
        return [3, 5, 7]

    @staticmethod
    def violation_free_counts() -> List[int]:
        return [15, 20, 25]

    @staticmethod
    def business_delivery_counts() -> List[int]:
        return [3, 5, 8]

    @staticmethod
    def business_garage_counts() -> List[int]:
        return [2, 3, 4]

    @staticmethod
    def revenue_targets() -> List[str]:
        return ["€250,000", "€500,000", "€1,000,000"]

    @staticmethod
    def special_transport_counts() -> List[int]:
        return [10, 15, 20]

    @staticmethod
    def dangerous_goods_counts() -> List[int]:
        return [15, 20, 25]

    @staticmethod
    def long_distance_km() -> List[int]:
        return [1400, 1800, 2200, 2500]


# Option classes would typically be defined elsewhere, but including stubs for completeness
class ETS2IncludeDeliveryObjectives(DefaultOnToggle):
    """Include delivery objectives"""
    display_name = "Include Delivery Objectives"

class ETS2IncludeCountryExploration(DefaultOnToggle):
    """Include country exploration objectives"""
    display_name = "Include Country Exploration"

class ETS2IncludeTruckOwnership(DefaultOnToggle):
    """Include truck ownership objectives"""
    display_name = "Include Truck Ownership"

class ETS2IncludeLongDistance(DefaultOnToggle):
    """Include long distance objectives"""
    display_name = "Include Long Distance"

class ETS2IncludeSpecialTransport(DefaultOnToggle):
    """Include special transport objectives"""
    display_name = "Include Special Transport"

class ETS2IncludeBusinessObjectives(DefaultOnToggle):
    """Include business objectives"""
    display_name = "Include Business Objectives"

class ETS2IncludeDlcContent(DefaultOnToggle):
    """Include DLC content objectives"""
    display_name = "Include DLC Content"

class ETS2DifficultyLevel(Choice):
    """Set the difficulty level for objectives"""
    display_name = "Difficulty Level"
    option_easy = "Easy"
    option_medium = "Medium"
    option_hard = "Hard"
    default = option_medium