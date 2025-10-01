from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, TextChoice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ScavengerHuntArchipelagoOptions:
    scavenger_include_photography: ScavengerIncludePhotography
    scavenger_include_location_hunting: ScavengerIncludeLocationHunting
    scavenger_include_object_collection: ScavengerIncludeObjectCollection
    scavenger_include_interaction_challenges: ScavengerIncludeInteractionChallenges
    scavenger_include_nature_exploration: ScavengerIncludeNatureExploration
    scavenger_include_cultural_discovery: ScavengerIncludeCulturalDiscovery
    scavenger_include_seasonal_activities: ScavengerIncludeSeasonalActivities
    scavenger_include_community_engagement: ScavengerIncludeCommunityEngagement
    scavenger_difficulty_preference: ScavengerDifficultyPreference
    scavenger_travel_scope: ScavengerTravelScope
    scavenger_season_preference: ScavengerSeasonPreference


class ScavengerHuntGame(Game):
    name = "Real-World Scavenger Hunt"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = []

    is_adult_only_or_unrated = False

    options_cls = ScavengerHuntArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective within LOCATION_TYPE areas only",
                data={"LOCATION_TYPE": (self.location_restrictions, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective using TRANSPORTATION_METHOD",
                data={"TRANSPORTATION_METHOD": (self.transportation_methods, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective within TIME_LIMIT",
                data={"TIME_LIMIT": (self.time_constraints, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective with COMPANION_TYPE",
                data={"COMPANION_TYPE": (self.companion_types, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective during WEATHER_CONDITION",
                data={"WEATHER_CONDITION": (self.weather_conditions, 1)},
            ),
        ])
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Photography Challenges
        if self.include_photography:
            photo_templates = []
            
            if self.difficulty_preference in ["All", "Hard"]:
                photo_templates.extend([
                    GameObjectiveTemplate(
                        label="Photograph RARE_SUBJECT in natural lighting without flash",
                        data={"RARE_SUBJECT": (self.rare_photo_subjects, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Capture a photo of CHALLENGE_PHOTO during SPECIFIC_TIME",
                        data={
                            "CHALLENGE_PHOTO": (self.challenge_photos, 1),
                            "SPECIFIC_TIME": (self.specific_times, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=1,
                    ),
                ])
            
            photo_templates.extend([
                GameObjectiveTemplate(
                    label="Take a photo of PHOTO_SUBJECT",
                    data={"PHOTO_SUBJECT": (self.photo_subjects, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create a photo series of SERIES_COUNT PHOTO_THEME photos",
                    data={
                        "SERIES_COUNT": (self.photo_series_counts, 1),
                        "PHOTO_THEME": (self.photo_themes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Document COLOR_COUNT different examples of COLOR objects",
                    data={
                        "COLOR_COUNT": (self.color_counts, 1),
                        "COLOR": (self.colors, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Photograph ARCHITECTURE_COUNT different ARCHITECTURE_STYLE buildings",
                    data={
                        "ARCHITECTURE_COUNT": (self.architecture_counts, 1),
                        "ARCHITECTURE_STYLE": (self.architecture_styles, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])
            
            game_objective_templates.extend(photo_templates)

        # Location Hunting
        if self.include_location_hunting:
            location_templates = []
            
            if self.travel_scope in ["All", "Regional"]:
                location_templates.extend([
                    GameObjectiveTemplate(
                        label="Visit LANDMARK_COUNT historical landmarks",
                        data={"LANDMARK_COUNT": (self.landmark_counts, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Explore REGION_COUNT different neighborhoods or regions",
                        data={"REGION_COUNT": (self.region_counts, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                ])
            
            location_templates.extend([
                GameObjectiveTemplate(
                    label="Find and visit LOCATION_TYPE",
                    data={"LOCATION_TYPE": (self.discoverable_locations, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Locate ADDRESS_COUNT addresses with ADDRESS_FEATURE",
                    data={
                        "ADDRESS_COUNT": (self.address_counts, 1),
                        "ADDRESS_FEATURE": (self.address_features, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Visit SHOP_COUNT different SHOP_TYPE establishments",
                    data={
                        "SHOP_COUNT": (self.shop_counts, 1),
                        "SHOP_TYPE": (self.shop_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Find VENUE_COUNT venues that host ACTIVITY_TYPE",
                    data={
                        "VENUE_COUNT": (self.venue_counts, 1),
                        "ACTIVITY_TYPE": (self.venue_activities, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])
            
            game_objective_templates.extend(location_templates)

        # Object Collection
        if self.include_object_collection:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Collect ITEM_COUNT different COLLECTIBLE_CATEGORY items",
                    data={
                        "ITEM_COUNT": (self.item_counts, 1),
                        "COLLECTIBLE_CATEGORY": (self.collectible_categories, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Find and document SPECIMEN_COUNT SPECIMEN_TYPE specimens",
                    data={
                        "SPECIMEN_COUNT": (self.specimen_counts, 1),
                        "SPECIMEN_TYPE": (self.specimen_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Gather MATERIAL_COUNT samples of NATURAL_MATERIAL",
                    data={
                        "MATERIAL_COUNT": (self.material_counts, 1),
                        "NATURAL_MATERIAL": (self.natural_materials, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Locate TREASURE_COUNT pieces of URBAN_TREASURE",
                    data={
                        "TREASURE_COUNT": (self.treasure_counts, 1),
                        "URBAN_TREASURE": (self.urban_treasures, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Find VINTAGE_COUNT VINTAGE_ITEM at thrift stores or markets",
                    data={
                        "VINTAGE_COUNT": (self.vintage_counts, 1),
                        "VINTAGE_ITEM": (self.vintage_items, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Interaction Challenges
        if self.include_interaction_challenges:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Engage in CONVERSATION_COUNT conversations with PERSON_TYPE",
                    data={
                        "CONVERSATION_COUNT": (self.conversation_counts, 1),
                        "PERSON_TYPE": (self.person_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Learn SKILL_COUNT basic phrases in LOCAL_LANGUAGE",
                    data={
                        "SKILL_COUNT": (self.skill_counts, 1),
                        "LOCAL_LANGUAGE": (self.local_languages, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Participate in ACTIVITY",
                    data={"ACTIVITY": (self.public_activities, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Volunteer VOLUNTEER_HOURS hours for VOLUNTEER_CAUSE",
                    data={
                        "VOLUNTEER_HOURS": (self.volunteer_hours, 1),
                        "VOLUNTEER_CAUSE": (self.volunteer_causes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Attend EVENT_COUNT COMMUNITY_EVENT events",
                    data={
                        "EVENT_COUNT": (self.event_counts, 1),
                        "COMMUNITY_EVENT": (self.community_events, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Nature Exploration
        if self.include_nature_exploration:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Identify SPECIES_COUNT different WILDLIFE_TYPE species",
                    data={
                        "SPECIES_COUNT": (self.species_counts, 1),
                        "WILDLIFE_TYPE": (self.wildlife_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Explore TRAIL_COUNT different TRAIL_TYPE trails",
                    data={
                        "TRAIL_COUNT": (self.trail_counts, 1),
                        "TRAIL_TYPE": (self.trail_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Document PLANT_COUNT PLANT_CATEGORY plants",
                    data={
                        "PLANT_COUNT": (self.plant_counts, 1),
                        "PLANT_CATEGORY": (self.plant_categories, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Visit PARK_COUNT different PARK_TYPE areas",
                    data={
                        "PARK_COUNT": (self.park_counts, 1),
                        "PARK_TYPE": (self.park_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Observe and record WEATHER_COUNT different weather patterns",
                    data={"WEATHER_COUNT": (self.weather_pattern_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Cultural Discovery
        if self.include_cultural_discovery:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Visit MUSEUM_COUNT MUSEUM_TYPE museums or galleries",
                    data={
                        "MUSEUM_COUNT": (self.museum_counts, 1),
                        "MUSEUM_TYPE": (self.museum_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Try CUISINE_COUNT different CUISINE_TYPE dishes",
                    data={
                        "CUISINE_COUNT": (self.cuisine_counts, 1),
                        "CUISINE_TYPE": (self.cuisine_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Learn about LOCAL_HISTORY",
                    data={"LOCAL_HISTORY": (self.local_history_topics, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Attend PERFORMANCE_COUNT PERFORMANCE_TYPE performances",
                    data={
                        "PERFORMANCE_COUNT": (self.performance_counts, 1),
                        "PERFORMANCE_TYPE": (self.performance_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Explore ART_COUNT examples of PUBLIC_ART",
                    data={
                        "ART_COUNT": (self.art_counts, 1),
                        "PUBLIC_ART": (self.public_art_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Seasonal Activities
        if self.include_seasonal_activities:
            seasonal_templates = []
            
            # Filter by season preference if specified
            if self.season_preference in ["Spring", "Summer", "Fall", "Winter"]:
                seasonal_templates.extend([
                    GameObjectiveTemplate(
                        label="Participate in SEASONAL_ACTIVITY during SEASON_PREFERENCE",
                        data={
                            "SEASONAL_ACTIVITY": (self.seasonal_activities, 1),
                            "SEASON_PREFERENCE": ([self.season_preference], 1)
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Experience WEATHER_ACTIVITY during SEASON_PREFERENCE weather",
                        data={
                            "WEATHER_ACTIVITY": (self.weather_activities, 1),
                            "SEASON_PREFERENCE": ([self.season_preference], 1)
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=2,
                    ),
                ])
            else:
                seasonal_templates.extend([
                    GameObjectiveTemplate(
                        label="Participate in SEASONAL_ACTIVITY during SEASON",
                        data={
                            "SEASONAL_ACTIVITY": (self.seasonal_activities, 1),
                            "SEASON": (self.seasons, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=2,
                    ),
                    GameObjectiveTemplate(
                        label="Experience WEATHER_ACTIVITY during specific weather",
                        data={"WEATHER_ACTIVITY": (self.weather_activities, 1)},
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=2,
                    ),
                ])
            
            seasonal_templates.extend([
                GameObjectiveTemplate(
                    label="Visit FESTIVAL_COUNT seasonal festivals or markets",
                    data={"FESTIVAL_COUNT": (self.festival_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Document SEASONAL_CHANGE_COUNT examples of seasonal changes",
                    data={"SEASONAL_CHANGE_COUNT": (self.seasonal_change_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])
            
            game_objective_templates.extend(seasonal_templates)

        # Community Engagement
        if self.include_community_engagement:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Support LOCAL_BUSINESS_COUNT local BUSINESS_TYPE businesses",
                    data={
                        "LOCAL_BUSINESS_COUNT": (self.local_business_counts, 1),
                        "BUSINESS_TYPE": (self.business_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Join or attend COMMUNITY_GROUP_COUNT COMMUNITY_GROUP meetings",
                    data={
                        "COMMUNITY_GROUP_COUNT": (self.community_group_counts, 1),
                        "COMMUNITY_GROUP": (self.community_groups, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Help with COMMUNITY_PROJECT",
                    data={"COMMUNITY_PROJECT": (self.community_projects, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Share LOCAL_KNOWLEDGE with SHARING_COUNT people",
                    data={
                        "LOCAL_KNOWLEDGE": (self.local_knowledge_topics, 1),
                        "SHARING_COUNT": (self.sharing_counts, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_photography(self) -> bool:
        return self.archipelago_options.scavenger_include_photography.value

    @property
    def include_location_hunting(self) -> bool:
        return self.archipelago_options.scavenger_include_location_hunting.value

    @property
    def include_object_collection(self) -> bool:
        return self.archipelago_options.scavenger_include_object_collection.value

    @property
    def include_interaction_challenges(self) -> bool:
        return self.archipelago_options.scavenger_include_interaction_challenges.value

    @property
    def include_nature_exploration(self) -> bool:
        return self.archipelago_options.scavenger_include_nature_exploration.value

    @property
    def include_cultural_discovery(self) -> bool:
        return self.archipelago_options.scavenger_include_cultural_discovery.value

    @property
    def include_seasonal_activities(self) -> bool:
        return self.archipelago_options.scavenger_include_seasonal_activities.value

    @property
    def include_community_engagement(self) -> bool:
        return self.archipelago_options.scavenger_include_community_engagement.value

    @property
    def difficulty_preference(self) -> str:
        return self.archipelago_options.scavenger_difficulty_preference.value

    @property
    def travel_scope(self) -> str:
        return self.archipelago_options.scavenger_travel_scope.value

    @property
    def season_preference(self) -> str:
        return self.archipelago_options.scavenger_season_preference.value

    # Data lists
    @staticmethod
    def photo_subjects() -> List[str]:
        return [
            "A street musician", "Colorful graffiti", "An interesting door", "A vintage sign",
            "A dog being walked", "Children playing", "A food truck", "Public art",
            "Someone reading", "A unique building", "A garden", "A bridge",
            "Street vendors", "A clock tower", "A fountain", "A mural",
            "A cat in a window", "Someone on a phone", "A delivery person", "A jogger",
            "A person with colorful hair", "Someone walking multiple dogs", "A busker",
            "A person in uniform", "Someone carrying flowers", "A cyclist", "A skateboarder",
            "Someone feeding birds", "A person reading a map", "Someone taking photos",
            "A person with an interesting hat", "Someone walking with a cane", "A couple holding hands",
            "A person wearing vintage clothing", "Someone with a backpack", "A person in costume",
            "Someone playing with a pet", "A person doing street art", "Someone on rollerblades",
            "A person with unique accessories", "Someone carrying groceries", "A person exercising",
            "Someone with a musical instrument", "A person wearing bright colors", "A street vendor",
            "Someone reading outdoors", "A person with tattoos", "Someone in professional attire",
            "A person walking barefoot", "Someone with a baby stroller", "A person feeding animals",
            "Someone doing yoga", "A person with a camera", "Someone in sports gear",
            "A person with unusual shoes", "Someone carrying art supplies", "A person on crutches",
            "Someone with face paint", "A person juggling", "Someone wearing headphones",
            "A person with a service animal", "Someone doing magic tricks", "A person painting",
            "Someone with unique jewelry", "A person doing mime", "Someone with a protest sign",
            "A person doing caricatures", "Someone with a unique vehicle", "A person selling crafts"
        ]

    @staticmethod
    def rare_photo_subjects() -> List[str]:
        return [
            "A rainbow after rain", "Wildlife in urban setting", "A perfect reflection",
            "Someone performing a skill", "A rare bird species", "Historic architecture detail",
            "A sunset/sunrise through buildings", "An interesting shadow pattern",
            "Lightning during a storm", "A double rainbow", "Fog rolling in", "Frost patterns",
            "A meteor or shooting star", "Aurora borealis", "A solar eclipse", "Unusual cloud formations",
            "A flash flood", "Steam rising from manholes", "Ice formations", "Snow on palm trees",
            "A person doing parkour", "Someone performing circus acts", "A flash mob",
            "A proposal happening", "A wedding party", "A parade float", "A protest march",
            "A fire truck in action", "An ambulance responding", "Police directing traffic",
            "Construction workers in action", "A tree being removed", "A building being demolished",
            "A helicopter landing", "A hot air balloon", "A vintage car rally", "A motorcycle parade",
            "Street art being created", "A chalk artist at work", "A sculpture being installed",
            "A time capsule being buried", "A cornerstone ceremony", "A ribbon cutting",
            "A flash freeze moment", "Water droplets in perfect formation", "Smoke rings",
            "A person's breath in cold air", "Light beams through fog", "Perfect geometric shadows",
            "Reflections in soap bubbles", "Light diffracting through water", "Steam patterns",
            "A rare animal in the wild", "An unusual insect", "A perfect spider web",
            "A bird of prey hunting", "A nocturnal animal during day", "Migration patterns",
            "Unusual animal behavior", "A rescue animal being freed", "Wildlife adaptation to urban life"
        ]

    @staticmethod
    def challenge_photos() -> List[str]:
        return [
            "A moving vehicle", "A person mid-jump", "Water in motion", "A flying bird",
            "Rush hour crowds", "A performer in action", "Wind affecting objects",
            "A reflection in puddles",
            "A spinning wheel", "A bouncing ball", "A falling leaf", "A flowing stream",
            "A swinging pendulum", "A rotating sign", "A fluttering flag", "A rippling water",
            "A person running", "A cyclist in motion", "A skateboarder performing tricks", "A dancer leaping",
            "A musician mid-performance", "A juggler with objects in air", "A magician during a trick",
            "A child on a swing", "A dog catching a frisbee", "A cat pouncing", "A bird taking flight",
            "A busy intersection", "A crowded market", "A packed stadium", "A bustling cafe",
            "A moving escalator", "A revolving door", "A carousel spinning", "A ferris wheel in motion",
            "Steam rising from coffee", "Smoke from a chimney", "Breath visible in cold air", "Fog rolling in",
            "Rain drops falling", "Snow in motion", "Hail bouncing", "Wind blowing leaves",
            "Waves crashing", "A fountain spraying", "A sprinkler in action", "A waterfall cascading",
            "A fire burning", "Sparks flying", "Lightning in the sky", "Fireworks exploding",
            "A person's shadow in motion", "Multiple exposures of movement", "Motion blur effects",
            "A spinning top", "A yo-yo in action", "A kite flying", "A balloon being released",
            "A soap bubble floating", "A coin being flipped", "Dice being rolled", "Cards being shuffled",
            "A clock's second hand moving", "A timer counting down", "A speedometer changing",
            "A person texting rapidly", "Someone typing on keyboard", "A printer in action",
            "A person painting", "Someone sculpting", "A chef cooking", "A barista making coffee"
        ]

    @staticmethod
    def photo_themes() -> List[str]:
        return [
            "Doors and Entrances", "Street Signs", "Public Transportation", "Local Wildlife",
            "Food and Dining", "People at Work", "Architectural Details", "Green Spaces",
            "Street Art", "Community Gathering Spots", "Vintage Elements", "Modern Design"
        ]

    @staticmethod
    def colors() -> List[str]:
        return [
            "Red", "Blue", "Yellow", "Green", "Purple", "Orange", "Pink", "Turquoise",
            "Gold", "Silver", "Black", "White", "Brown", "Maroon", "Navy", "Teal"
        ]

    @staticmethod
    def architecture_styles() -> List[str]:
        return [
            "Victorian", "Modern", "Art Deco", "Colonial", "Industrial", "Mid-Century",
            "Gothic", "Contemporary", "Brutalist", "Traditional", "Craftsman", "Mediterranean"
        ]

    @staticmethod
    def discoverable_locations() -> List[str]:
        return [
            "A hidden garden", "A historic plaque", "A community bulletin board",
            "A local landmark", "A scenic viewpoint", "A unique shop", "A street market",
            "A public library", "A community center", "A park with playground",
            "A coffee shop with local art", "A bookstore", "A thrift store",
            "A secret alley", "A rooftop garden", "A hidden staircase", "A tucked-away cafe",
            "An abandoned building", "A graffiti tunnel", "A pocket park", "A memorial bench",
            "A community garden", "A food co-op", "A maker space", "A recording studio",
            "A pottery studio", "A dance studio", "A martial arts dojo", "A climbing gym",
            "A vintage arcade", "A pinball museum", "A comic book store", "A used record shop",
            "A camera store", "A musical instrument shop", "A specialty spice shop", "A tea house",
            "A wine bar", "A craft brewery", "A distillery", "A cheese shop", "A chocolate shop",
            "A bakery with unique items", "A farmers market vendor", "A fish market",
            "A butcher shop", "A florist", "A plant nursery", "A seed library",
            "A tool library", "A repair cafe", "A community workshop", "A makerspace",
            "A co-working space", "A pop-up shop", "A mobile vendor", "A seasonal stand",
            "A historic house", "A heritage building", "A converted warehouse", "A old church",
            "A former school", "A repurposed factory", "A train station", "A lighthouse",
            "A water tower", "A bridge underpass", "A covered bridge", "A pedestrian overpass",
            "A observation deck", "A scenic overlook", "A hidden beach", "A secret swimming hole",
            "A natural spring", "A cave entrance", "A rock formation", "A waterfall",
            "A creek crossing", "A pond", "A marsh", "A meadow", "A grove of trees",
            "A giant tree", "A tree with a swing", "A labyrinth", "A sculpture garden",
            "A meditation garden", "A sensory garden", "A butterfly garden", "A herb garden"
        ]

    @staticmethod
    def address_features() -> List[str]:
        return [
            "Interesting house numbers", "Unique mailboxes", "Colorful front doors",
            "Garden displays", "Window decorations", "Porch decorations",
            "Street number murals", "Historic markers"
        ]

    @staticmethod
    def shop_types() -> List[str]:
        return [
            "Local cafes", "Independent bookstores", "Thrift shops", "Art galleries",
            "Farmers markets", "Food trucks", "Antique stores", "Craft shops",
            "Music stores", "Specialty food shops", "Plant nurseries", "Community markets"
        ]

    @staticmethod
    def venue_activities() -> List[str]:
        return [
            "Live music", "Art classes", "Book readings", "Community meetings",
            "Fitness activities", "Workshops", "Cultural events", "Educational talks",
            "Social gatherings", "Support groups", "Skill sharing", "Volunteer opportunities"
        ]

    @staticmethod
    def collectible_categories() -> List[str]:
        return [
            "Interesting rocks", "Unique leaves", "Business cards", "Event flyers",
            "Postcards", "Local stickers", "Maps", "Brochures", "Tickets",
            "Pressed flowers", "Feathers", "Shells", "Coins",
            "Bottle caps", "Vintage buttons", "Trading cards", "Matchbooks",
            "Keychains", "Magnets", "Pins", "Patches", "Stickers from restaurants",
            "Hotel soaps", "Sugar packets", "Tea bags", "Coasters", "Napkins with logos",
            "Concert wristbands", "Festival badges", "Library bookmarks", "Museum brochures",
            "Art gallery cards", "Recipe cards", "Seed packets", "Plant tags",
            "Wine corks", "Beer caps", "Coffee sleeves", "Food truck menus",
            "Local newspaper clippings", "Community newsletters", "Event programs",
            "Theater playbills", "Concert programs", "Sports tickets", "Parking stubs",
            "Public transit transfers", "Boarding passes", "Luggage tags", "Hotel key cards",
            "Shopping bags", "Fabric samples", "Paint chips", "Tile samples",
            "Wood samples", "Stone fragments", "Sand samples", "Soil samples",
            "Water in bottles", "Snow in containers", "Ice formations", "Frost patterns",
            "Bark pieces", "Seed pods", "Pine cones", "Acorns", "Nuts", "Berries (safe ones)",
            "Flower petals", "Grass samples", "Moss specimens", "Lichen samples",
            "Interesting shaped stones", "Smooth pebbles", "Colored glass", "Sea glass",
            "Driftwood pieces", "Coral fragments", "Unusual shells", "Crab shells",
            "Interesting bones", "Animal tracks (photos)", "Nest materials", "Eggshell fragments",
            "Butterfly wings (naturally shed)", "Insect casings", "Spider webs (preserved)",
            "Hair samples from pets", "Whiskers from cats", "Pet toys", "Collar tags"
        ]

    @staticmethod
    def specimen_types() -> List[str]:
        return [
            "Tree species", "Flower varieties", "Bird species", "Insect types",
            "Cloud formations", "Rock types", "Moss varieties", "Lichen species",
            "Fern species", "Grass types", "Weed varieties", "Vine species",
            "Shrub types", "Bush varieties", "Cactus species", "Succulent types",
            "Herb varieties", "Wildflower species", "Garden flower types", "Bulb plants",
            "Perennial varieties", "Annual species", "Biennial plants", "Native plants",
            "Invasive species", "Endangered plants", "Protected species", "Rare plants",
            "Fruit tree varieties", "Nut tree species", "Coniferous trees", "Deciduous trees",
            "Evergreen varieties", "Flowering trees", "Shade trees", "Street trees",
            "Butterfly species", "Moth varieties", "Beetle types", "Ant species",
            "Spider varieties", "Dragonfly species", "Bee types", "Wasp varieties",
            "Fly species", "Mosquito types", "Tick varieties", "Flea species",
            "Caterpillar types", "Grub varieties", "Larvae species", "Pupae forms",
            "Song bird species", "Water birds", "Birds of prey", "Scavenger birds",
            "Migratory birds", "Resident birds", "Nocturnal birds", "Diurnal birds",
            "Mammals in urban areas", "Rodent species", "Squirrel varieties", "Bat types",
            "Urban wildlife", "Domesticated animals", "Feral animals", "Pet varieties",
            "Reptile species", "Lizard types", "Snake varieties", "Turtle species",
            "Amphibian species", "Frog varieties", "Toad types", "Salamander species",
            "Fish species in local waters", "Freshwater fish", "Saltwater fish", "Aquarium fish",
            "Pond life", "Stream creatures", "Lake wildlife", "River species",
            "Cumulus clouds", "Stratus clouds", "Cirrus clouds", "Nimbus clouds",
            "Cumulonimbus formations", "Altocumulus patterns", "Cirrostratus layers", "Stratocumulus clusters"
        ]

    @staticmethod
    def natural_materials() -> List[str]:
        return [
            "Different soil types", "Various sand types", "Water samples",
            "Seed pods", "Pine cones", "Bark textures", "Stone varieties"
        ]

    @staticmethod
    def urban_treasures() -> List[str]:
        return [
            "Interesting manhole covers", "Unique street art", "Historic markers",
            "Hidden murals", "Architectural details", "Vintage elements",
            "Community messages", "Local memorial plaques",
            "Unusual door handles", "Decorative window shutters", "Ornate fire escapes",
            "Vintage street lamps", "Old neon signs", "Retro advertisements",
            "Historic building cornerstones", "Date stones in buildings", "Carved building details",
            "Gargoyles or decorative figures", "Unique weathervanes", "Interesting chimneys",
            "Decorative ironwork", "Stained glass windows", "Mosaic tiles",
            "Brick patterns", "Stone carvings", "Metal sculptures", "Fountain details",
            "Bridge decorations", "Tunnel artwork", "Underpass murals", "Sidewalk mosaics",
            "Manhole cover designs", "Storm drain artwork", "Utility box art",
            "Traffic signal box decorations", "Electrical box murals", "Fence art",
            "Wall textures", "Interesting shadows", "Light patterns", "Reflection art",
            "Mirror installations", "Interactive art pieces", "Kinetic sculptures",
            "Sound art installations", "Tactile art", "Aromatic gardens", "Edible landscaping",
            "Community message boards", "Poem displays", "Quote walls", "Story walks",
            "Time capsule markers", "Boundary stones", "Survey markers", "Mile markers",
            "Historical timeline displays", "Before/after photo displays", "Memory walls",
            "Community achievement displays", "Local hero memorials", "Cultural celebration markers",
            "Hidden geocaches", "QR code art", "Augmented reality markers", "Digital art displays",
            "Projection art", "Holographic displays", "Interactive light displays",
            "Motion-activated art", "Weather-responsive art", "Seasonal installations"
        ]

    @staticmethod
    def vintage_items() -> List[str]:
        return [
            "Old books", "Vintage postcards", "Retro clothing", "Antique tools",
            "Old photographs", "Vintage jewelry", "Classic records", "Historic maps",
            "Antique buttons", "Vintage fabric", "Old magazines", "Retro toys",
            "Classic board games", "Vintage puzzles", "Old playing cards", "Antique dishes",
            "Vintage glassware", "Retro kitchen utensils", "Old typewriters", "Vintage cameras",
            "Classic radios", "Old televisions", "Vintage phones", "Retro appliances",
            "Antique furniture", "Vintage lamps", "Old clocks", "Antique mirrors",
            "Vintage frames", "Old suitcases", "Retro luggage", "Antique trunks",
            "Vintage hats", "Old shoes", "Retro accessories", "Antique watches",
            "Vintage purses", "Old wallets", "Retro sunglasses", "Antique pins",
            "Vintage brooches", "Old cufflinks", "Retro belt buckles", "Antique combs",
            "Vintage perfume bottles", "Old medicine bottles", "Retro containers", "Antique tins",
            "Vintage advertising signs", "Old promotional items", "Retro packaging", "Antique labels",
            "Classic car parts", "Vintage motorcycle items", "Old bicycle parts", "Retro transportation memorabilia",
            "Military surplus items", "Vintage uniforms", "Old badges", "Retro patches",
            "Antique coins", "Vintage stamps", "Old currency", "Retro collectibles",
            "Classic movie posters", "Vintage concert tickets", "Old sheet music", "Retro album covers",
            "Antique instruments", "Vintage sports equipment", "Old gaming items", "Retro technology",
            "Classic scientific instruments", "Vintage medical equipment", "Old educational materials", "Retro office supplies",
            "Antique religious items", "Vintage holiday decorations", "Old ceremonial objects", "Retro cultural artifacts"
        ]

    @staticmethod
    def person_types() -> List[str]:
        return [
            "Local shop owners", "Street performers", "Dog walkers", "Gardeners",
            "Public transit operators", "Food vendors", "Artists", "Community volunteers",
            "Library staff", "Park workers", "Museum guides", "Neighbors",
            "Postal workers", "Delivery drivers", "Security guards", "Construction workers",
            "Maintenance staff", "Cleaning crews", "Landscapers", "Window washers",
            "Traffic controllers", "Parking attendants", "Taxi drivers", "Bus drivers",
            "Cyclists", "Joggers", "Dog trainers", "Pet groomers", "Veterinarians",
            "Teachers", "Students", "School staff", "Crossing guards", "Coaches",
            "Fitness instructors", "Personal trainers", "Massage therapists", "Barbers",
            "Hair stylists", "Nail technicians", "Tattoo artists", "Photographers",
            "Wedding planners", "Event coordinators", "Caterers", "Florists",
            "Musicians", "Dancers", "Actors", "Comedians", "Magicians", "Mimes",
            "Jugglers", "Balloon artists", "Face painters", "Caricature artists",
            "Street chalk artists", "Graffiti artists", "Muralists", "Sculptors",
            "Craft vendors", "Farmers market sellers", "Antique dealers", "Collectible traders",
            "Book sellers", "Art dealers", "Vintage clothing sellers", "Record collectors",
            "Chefs", "Bakers", "Baristas", "Bartenders", "Servers", "Kitchen staff",
            "Store clerks", "Cashiers", "Sales associates", "Customer service reps",
            "Repair technicians", "Mechanics", "Electricians", "Plumbers", "Carpenters",
            "Real estate agents", "Insurance agents", "Financial advisors", "Lawyers",
            "Doctors", "Nurses", "Therapists", "Social workers", "Firefighters",
            "Police officers", "EMTs", "Paramedics", "Dispatchers", "Military personnel"
        ]

    @staticmethod
    def local_languages() -> List[str]:
        return [
            "Spanish", "French", "Mandarin", "Sign Language", "Local dialect",
            "German", "Italian", "Portuguese", "Arabic", "Japanese", "Korean", "Hindi"
        ]

    @staticmethod
    def public_activities() -> List[str]:
        return [
            "A community cleanup", "A local festival", "A farmers market visit",
            "A public art walk", "A community garden workday", "A neighborhood meeting",
            "A cultural celebration", "A charity run/walk", "A street fair",
            "A block party", "A outdoor movie screening", "A concert in the park",
            "A food truck rally", "A craft fair", "A vintage market", "A car show",
            "A dog show", "A pet adoption event", "A wildlife presentation", "A nature walk",
            "A bird watching group", "A stargazing event", "A photography walk", "A sketching meetup",
            "A book club meeting", "A poetry reading", "A storytelling circle", "A debate club",
            "A language exchange", "A cultural exchange", "A cooking class", "A dance lesson",
            "A fitness class", "A yoga session", "A tai chi group", "A meditation circle",
            "A martial arts demonstration", "A self-defense class", "A first aid training", "A CPR class",
            "A gardening workshop", "A composting seminar", "A sustainability fair", "A green living expo",
            "A renewable energy demonstration", "A recycling drive", "An electronics collection",
            "A clothing swap", "A repair cafe", "A skill sharing workshop", "A tool library visit",
            "A makers market", "A craft workshop", "A pottery class", "A painting session",
            "A sculpture demonstration", "A jewelry making class", "A woodworking workshop", "A metalworking demo",
            "A technology meetup", "A coding bootcamp", "A digital literacy class", "A computer repair workshop",
            "A business networking event", "An entrepreneur meetup", "A startup pitch", "A career fair",
            "A job training session", "A resume workshop", "An interview prep class", "A financial literacy seminar",
            "A historical reenactment", "A heritage celebration", "A cultural festival", "A religious ceremony",
            "A wedding celebration", "A birthday party", "A graduation ceremony", "An anniversary celebration"
        ]

    @staticmethod
    def volunteer_causes() -> List[str]:
        return [
            "Environmental cleanup", "Community garden", "Food bank", "Animal shelter",
            "Elder care", "Youth programs", "Literacy programs", "Local arts",
            "Community events", "Habitat restoration", "Homeless support", "Education support"
        ]

    @staticmethod
    def community_events() -> List[str]:
        return [
            "Town halls", "Art openings", "Cultural festivals", "Seasonal celebrations",
            "Educational workshops", "Health fairs", "Music concerts", "Food festivals",
            "Craft fairs", "History walks", "Community markets", "Social mixers"
        ]

    @staticmethod
    def wildlife_types() -> List[str]:
        return [
            "Birds", "Squirrels", "Insects", "Urban wildlife", "Garden creatures",
            "Park animals", "Pond life", "Tree dwellers", "Ground animals"
        ]

    @staticmethod
    def trail_types() -> List[str]:
        return [
            "Walking trails", "Bike paths", "Nature trails", "Historic routes",
            "Scenic walkways", "Urban trails", "Waterfront paths", "Park loops"
        ]

    @staticmethod
    def plant_categories() -> List[str]:
        return [
            "Native wildflowers", "Garden plants", "Trees", "Shrubs", "Herbs",
            "Succulents", "Grasses", "Vines", "Flowering plants", "Fruit plants"
        ]

    @staticmethod
    def park_types() -> List[str]:
        return [
            "City parks", "Neighborhood parks", "Nature preserves", "Botanical gardens",
            "Community gardens", "Pocket parks", "Recreation areas", "Green spaces"
        ]

    @staticmethod
    def museum_types() -> List[str]:
        return [
            "Art", "History", "Science", "Natural history", "Cultural", "Specialty",
            "Community", "Children's", "Technology", "Local heritage"
        ]

    @staticmethod
    def cuisine_types() -> List[str]:
        return [
            "Local specialties", "International", "Street food", "Traditional",
            "Fusion", "Vegetarian", "Farm-to-table", "Ethnic", "Regional", "Artisanal"
        ]

    @staticmethod
    def local_history_topics() -> List[str]:
        return [
            "Founding of the area", "Notable residents", "Historic events", "Architecture evolution",
            "Cultural movements", "Economic development", "Transportation history", "Local legends"
        ]

    @staticmethod
    def performance_types() -> List[str]:
        return [
            "Music", "Theater", "Dance", "Poetry", "Storytelling", "Comedy",
            "Street performance", "Cultural shows", "Community productions"
        ]

    @staticmethod
    def public_art_types() -> List[str]:
        return [
            "Murals", "Sculptures", "Installations", "Street art", "Community art",
            "Memorial art", "Functional art", "Interactive art", "Historical markers"
        ]

    @staticmethod
    def seasonal_activities() -> List[str]:
        return [
            "Leaf collection", "Snow activities", "Spring flower viewing", "Summer festivals",
            "Fall harvest events", "Winter celebrations", "Seasonal sports", "Weather observation"
        ]

    @staticmethod
    def seasons() -> List[str]:
        return ["Spring", "Summer", "Fall", "Winter"]

    @staticmethod
    def weather_activities() -> List[str]:
        return [
            "Rain puddle photography", "Snow day exploration", "Sunny day picnic",
            "Foggy morning walk", "Windy day kite flying", "Storm watching"
        ]

    @staticmethod
    def business_types() -> List[str]:
        return [
            "Restaurants", "Shops", "Services", "Markets", "Cafes", "Bookstores",
            "Art studios", "Craft stores", "Food producers", "Entertainment venues"
        ]

    @staticmethod
    def community_groups() -> List[str]:
        return [
            "Neighborhood associations", "Cultural groups", "Hobby clubs", "Environmental groups",
            "Arts organizations", "Sports clubs", "Volunteer groups", "Educational groups"
        ]

    @staticmethod
    def community_projects() -> List[str]:
        return [
            "Community garden maintenance", "Neighborhood cleanup", "Local event organization",
            "Public art project", "History documentation", "Environmental improvement",
            "Youth program support", "Elder assistance", "Cultural preservation"
        ]

    @staticmethod
    def local_knowledge_topics() -> List[str]:
        return [
            "Best local spots", "Hidden gems", "Transportation tips", "Cultural events",
            "Seasonal activities", "Local history", "Community resources", "Safety information"
        ]

    @staticmethod
    def location_restrictions() -> List[str]:
        return [
            "Within walking distance", "Public transportation accessible", "Downtown area",
            "Residential neighborhoods", "Parks and nature areas", "Cultural districts"
        ]

    @staticmethod
    def transportation_methods() -> List[str]:
        return [
            "Walking only", "Bicycle", "Public transit", "Car", "Combination methods",
            "Eco-friendly transport", "Different method each day"
        ]

    @staticmethod
    def time_constraints() -> List[str]:
        return [
            "1 hour", "2 hours", "Half day", "Full day", "One week", "One month"
        ]

    @staticmethod
    def companion_types() -> List[str]:
        return [
            "Solo exploration", "With family", "With friends", "With community group",
            "With pets", "Meeting new people", "Guided group"
        ]

    @staticmethod
    def weather_conditions() -> List[str]:
        return [
            "Sunny weather", "Rainy day", "Overcast skies", "Windy conditions",
            "Snowy weather", "Any weather", "Perfect weather"
        ]

    @staticmethod
    def specific_times() -> List[str]:
        return [
            "Golden hour", "Blue hour", "Rush hour", "Early morning", "Late evening",
            "Midday", "Lunch time", "Weekend morning"
        ]

    # Ranges
    @staticmethod
    def photo_series_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def color_counts() -> range:
        return range(3, 12, 3)

    @staticmethod
    def architecture_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def landmark_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def region_counts() -> range:
        return range(3, 8, 2)

    @staticmethod
    def address_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def shop_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def venue_counts() -> range:
        return range(2, 8, 2)

    @staticmethod
    def item_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def specimen_counts() -> range:
        return range(5, 15, 5)

    @staticmethod
    def material_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def treasure_counts() -> range:
        return range(3, 8, 2)

    @staticmethod
    def vintage_counts() -> range:
        return range(2, 6, 2)

    @staticmethod
    def conversation_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def skill_counts() -> range:
        return range(5, 15, 5)

    @staticmethod
    def volunteer_hours() -> range:
        return range(2, 12, 2)

    @staticmethod
    def event_counts() -> range:
        return range(2, 8, 2)

    @staticmethod
    def species_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def trail_counts() -> range:
        return range(3, 8, 2)

    @staticmethod
    def plant_counts() -> range:
        return range(10, 30, 10)

    @staticmethod
    def park_counts() -> range:
        return range(3, 8, 2)

    @staticmethod
    def weather_pattern_counts() -> range:
        return range(3, 8, 2)

    @staticmethod
    def museum_counts() -> range:
        return range(2, 6, 2)

    @staticmethod
    def cuisine_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def performance_counts() -> range:
        return range(2, 6, 2)

    @staticmethod
    def art_counts() -> range:
        return range(5, 15, 5)

    @staticmethod
    def festival_counts() -> range:
        return range(2, 6, 2)

    @staticmethod
    def seasonal_change_counts() -> range:
        return range(5, 15, 5)

    @staticmethod
    def local_business_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def community_group_counts() -> range:
        return range(1, 5)

    @staticmethod
    def sharing_counts() -> range:
        return range(3, 10, 2)


# Archipelago Options
class ScavengerIncludePhotography(DefaultOnToggle):
    """Include photography and visual documentation objectives."""
    display_name = "Include Photography"

class ScavengerIncludeLocationHunting(DefaultOnToggle):
    """Include location discovery and exploration objectives."""
    display_name = "Include Location Hunting"

class ScavengerIncludeObjectCollection(DefaultOnToggle):
    """Include item collection and specimen gathering objectives."""
    display_name = "Include Object Collection"

class ScavengerIncludeInteractionChallenges(DefaultOnToggle):
    """Include social interaction and communication objectives."""
    display_name = "Include Interaction Challenges"

class ScavengerIncludeNatureExploration(DefaultOnToggle):
    """Include wildlife observation and nature study objectives."""
    display_name = "Include Nature Exploration"

class ScavengerIncludeCulturalDiscovery(DefaultOnToggle):
    """Include cultural learning and artistic exploration objectives."""
    display_name = "Include Cultural Discovery"

class ScavengerIncludeSeasonalActivities(DefaultOnToggle):
    """Include weather and season-specific objectives."""
    display_name = "Include Seasonal Activities"

class ScavengerIncludeCommunityEngagement(DefaultOnToggle):
    """Include community participation and local support objectives."""
    display_name = "Include Community Engagement"

class ScavengerDifficultyPreference(TextChoice):
    """Prefer certain difficulty levels for objectives."""
    display_name = "Difficulty Preference"
    option_all = 0
    option_easy = 1
    option_hard = 2
    default = 0

class ScavengerTravelScope(TextChoice):
    """Set the geographical scope for objectives."""
    display_name = "Travel Scope"
    option_all = 0
    option_local = 1
    option_regional = 2
    default = 0

class ScavengerSeasonPreference(TextChoice):
    """Focus seasonal activities on a specific season."""
    display_name = "Season Preference"
    option_all = 0
    option_spring = 1
    option_summer = 2
    option_fall = 3
    option_winter = 4
    default = 0
