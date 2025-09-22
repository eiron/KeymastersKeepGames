from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, Toggle, Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class Sims4ArchipelagoOptions:
    sims4_include_skills: Sims4IncludeSkills
    sims4_include_careers: Sims4IncludeCareers
    sims4_include_aspirations: Sims4IncludeAspirations
    sims4_include_relationships: Sims4IncludeRelationships
    sims4_include_collections: Sims4IncludeCollections
    sims4_include_creative_goals: Sims4IncludeCreativeGoals
    sims4_include_life_simulation: Sims4IncludeLifeSimulation
    sims4_include_achievements: Sims4IncludeAchievements
    sims4_difficulty_level: Sims4DifficultyLevel
    sims4_focus_style: Sims4FocusStyle


class TheSims4Game(Game):
    name = "The Sims 4"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = Sims4ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective with a Sim who has the TRAIT trait",
                data={"TRAIT": (self.personality_traits, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective while your Sim is EMOTION",
                data={"EMOTION": (self.emotions, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without using SKILL skill",
                data={"SKILL": (self.skills, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective before your Sim becomes AGE_STAGE",
                data={"AGE_STAGE": (self.age_stages, 1)},
            ),
        ])
        
        if self.difficulty_level in ["Hard", "Expert"]:
            constraints.extend([
                GameObjectiveTemplate(
                    label="Complete this objective without spending more than BUDGET simoleons",
                    data={"BUDGET": (self.budget_limits, 1)},
                ),
                GameObjectiveTemplate(
                    label="Complete this objective within SIM_DAYS days",
                    data={"SIM_DAYS": (self.time_limits, 1)},
                ),
            ])
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Skills Development
        if self.include_skills:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Level SKILL_TYPE to level SKILL_LEVEL",
                    data={
                        "SKILL_TYPE": (self.skills, 1),
                        "SKILL_LEVEL": (self.skill_levels, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Max out SKILL_COUNT different skills to level 10",
                    data={"SKILL_COUNT": (self.max_skill_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete the SKILL skill challenge",
                    data={"SKILL": (self.skills_with_challenges, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Have SKILL_GROUP_COUNT different Sims each master a skill in SKILL_GROUP_TYPE",
                    data={
                        "SKILL_GROUP_COUNT": (self.skill_group_counts, 1),
                        "SKILL_GROUP_TYPE": (self.skill_groups, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Career Progression
        if self.include_careers:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach level CAREER_LEVEL in the CAREER_TYPE career",
                    data={
                        "CAREER_LEVEL": (self.career_levels, 1),
                        "CAREER_TYPE": (self.careers, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete the CAREER career and reach the top of both branches",
                    data={"CAREER": (self.branching_careers, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Earn SALARY_AMOUNT simoleons from career work",
                    data={"SALARY_AMOUNT": (self.salary_amounts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Get promoted PROMOTION_COUNT times in any career",
                    data={"PROMOTION_COUNT": (self.promotion_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Have a household with CAREER_COUNT different career paths active",
                    data={"CAREER_COUNT": (self.household_career_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Aspiration Completion
        if self.include_aspirations:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the ASPIRATION aspiration",
                    data={"ASPIRATION": (self.aspirations, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete ASPIRATION_COUNT different aspirations",
                    data={"ASPIRATION_COUNT": (self.aspiration_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete MILESTONE_COUNT milestones from ASPIRATION_CATEGORY aspirations",
                    data={
                        "MILESTONE_COUNT": (self.milestone_counts, 1),
                        "ASPIRATION_CATEGORY": (self.aspiration_categories, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Obtain the ASPIRATION_REWARD trait",
                    data={"ASPIRATION_REWARD": (self.aspiration_rewards, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Relationship Building
        if self.include_relationships:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Have FRIEND_COUNT best friends",
                    data={"FRIEND_COUNT": (self.friend_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Get married and have RELATIONSHIP_LEVEL relationship level",
                    data={"RELATIONSHIP_LEVEL": (self.relationship_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Have CHILDREN_COUNT children and raise them to CHILD_AGE",
                    data={
                        "CHILDREN_COUNT": (self.children_counts, 1),
                        "CHILD_AGE": (self.child_ages, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Maintain HOUSEHOLD_SIZE household members with good relationships",
                    data={"HOUSEHOLD_SIZE": (self.household_sizes, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Build ROMANCE_COUNT romantic relationships",
                    data={"ROMANCE_COUNT": (self.romance_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Have ENEMY_COUNT enemies while maintaining FRIEND_COUNT friends",
                    data={
                        "ENEMY_COUNT": (self.enemy_counts, 1),
                        "FRIEND_COUNT": (self.concurrent_friend_counts, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Successfully seduce and marry SIM_COUNT different Sims in sequence",
                    data={"SIM_COUNT": (self.sequential_marriage_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Collection Hunting
        if self.include_collections:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete the COLLECTION collection",
                    data={"COLLECTION": (self.collections, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Find COLLECTIBLE_COUNT different COLLECTIBLE_TYPE",
                    data={
                        "COLLECTIBLE_COUNT": (self.collectible_counts, 1),
                        "COLLECTIBLE_TYPE": (self.collectible_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Discover all RARITY_LEVEL rarity items in any collection",
                    data={"RARITY_LEVEL": (self.rarity_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Sell collections worth COLLECTION_VALUE simoleons",
                    data={"COLLECTION_VALUE": (self.collection_values, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Creative Goals
        if self.include_creative_goals:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Create ARTWORK_COUNT ARTWORK_TYPE paintings",
                    data={
                        "ARTWORK_COUNT": (self.artwork_counts, 1),
                        "ARTWORK_TYPE": (self.artwork_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Write and publish BOOK_COUNT BOOK_TYPE",
                    data={
                        "BOOK_COUNT": (self.book_counts, 1),
                        "BOOK_TYPE": (self.book_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Build a house worth HOUSE_VALUE simoleons",
                    data={"HOUSE_VALUE": (self.house_values, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Program PROGRAM_COUNT different programs/games/apps",
                    data={"PROGRAM_COUNT": (self.program_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Perform PERFORMANCE_COUNT PERFORMANCE_TYPE performances",
                    data={
                        "PERFORMANCE_COUNT": (self.performance_counts, 1),
                        "PERFORMANCE_TYPE": (self.performance_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create a Cowplant and keep it alive for COWPLANT_DAYS days",
                    data={"COWPLANT_DAYS": (self.cowplant_survival_days, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Build and decorate ROOM_COUNT different themed rooms",
                    data={"ROOM_COUNT": (self.themed_room_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Life Simulation
        if self.include_life_simulation:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Age a Sim from STARTING_AGE to ENDING_AGE",
                    data={
                        "STARTING_AGE": (self.starting_ages, 1),
                        "ENDING_AGE": (self.ending_ages, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Host EVENT_COUNT successful PARTY_TYPE parties",
                    data={
                        "EVENT_COUNT": (self.event_counts, 1),
                        "PARTY_TYPE": (self.party_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Experience EMOTION_COUNT different emotions in one day",
                    data={"EMOTION_COUNT": (self.emotion_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Travel to and explore LOCATION_COUNT different lots",
                    data={"LOCATION_COUNT": (self.location_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete GHOST_OBJECTIVE as a ghost Sim",
                    data={"GHOST_OBJECTIVE": (self.ghost_objectives, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete EMOTION_CHALLENGE while SPECIFIC_EMOTION",
                    data={
                        "EMOTION_CHALLENGE": (self.emotion_challenges, 1),
                        "SPECIFIC_EMOTION": (self.emotions, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Have a Sim die from DEATH_CAUSE and become a ghost",
                    data={"DEATH_CAUSE": (self.death_causes, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Travel to space and discover SPACE_DISCOVERY",
                    data={"SPACE_DISCOVERY": (self.space_discoveries, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Graft GRAFT_COUNT different plant combinations",
                    data={"GRAFT_COUNT": (self.graft_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete NEEDS_CHALLENGE with unconventional restrictions",
                    data={"NEEDS_CHALLENGE": (self.needs_challenges, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Achievement Goals
        if self.include_achievements:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Achieve WEALTH_LEVEL wealth status",
                    data={"WEALTH_LEVEL": (self.wealth_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete GENERATION_COUNT generations of a family legacy",
                    data={"GENERATION_COUNT": (self.generation_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Have a Sim master every skill and complete every aspiration",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Build and maintain the perfect family with FAMILY_ACHIEVEMENT",
                    data={"FAMILY_ACHIEVEMENT": (self.family_achievements, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete CHALLENGE_TYPE challenge",
                    data={"CHALLENGE_TYPE": (self.challenge_types, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_skills(self) -> bool:
        return self.archipelago_options.sims4_include_skills.value

    @property
    def include_careers(self) -> bool:
        return self.archipelago_options.sims4_include_careers.value

    @property
    def include_aspirations(self) -> bool:
        return self.archipelago_options.sims4_include_aspirations.value

    @property
    def include_relationships(self) -> bool:
        return self.archipelago_options.sims4_include_relationships.value

    @property
    def include_collections(self) -> bool:
        return self.archipelago_options.sims4_include_collections.value

    @property
    def include_creative_goals(self) -> bool:
        return self.archipelago_options.sims4_include_creative_goals.value

    @property
    def include_life_simulation(self) -> bool:
        return self.archipelago_options.sims4_include_life_simulation.value

    @property
    def include_achievements(self) -> bool:
        return self.archipelago_options.sims4_include_achievements.value

    @property
    def difficulty_level(self) -> str:
        return self.archipelago_options.sims4_difficulty_level.value

    @property
    def focus_style(self) -> str:
        return self.archipelago_options.sims4_focus_style.value

    # Data lists
    @staticmethod
    def skills() -> List[str]:
        return [
            "Cooking", "Charisma", "Comedy", "Fishing", "Fitness", "Gardening",
            "Handiness", "Logic", "Mischief", "Painting", "Piano", "Programming",
            "Rocket Science", "Video Gaming", "Writing"
        ]

    @staticmethod
    def skills_with_challenges() -> List[str]:
        return [
            "Cooking", "Charisma", "Comedy", "Fishing", "Fitness", "Gardening",
            "Handiness", "Logic", "Mischief", "Painting", "Piano", "Programming",
            "Rocket Science", "Video Gaming", "Writing"
        ]

    @staticmethod
    def skill_groups() -> List[str]:
        return ["Creative", "Mental", "Physical", "Social"]

    @staticmethod
    def careers() -> List[str]:
        return [
            "Astronaut", "Criminal", "Culinary", "Entertainer", 
            "Painter", "Secret Agent", "Tech Guru", "Writer"
        ]

    @staticmethod
    def branching_careers() -> List[str]:
        return [
            "Astronaut", "Criminal", "Culinary", "Entertainer", 
            "Secret Agent", "Tech Guru", "Writer"
        ]

    @staticmethod
    def aspirations() -> List[str]:
        return [
            "Renaissance Sim", "Nerd Brain", "Creativity", "Popularity", 
            "Fortune", "Bodybuilder", "Outdoor Enthusiast", "Knowledge", 
            "Big Happy Family"
        ]

    @staticmethod
    def aspiration_categories() -> List[str]:
        return ["Creative", "Knowledge", "Love", "Nature", "Popularity", "Athletic", "Family", "Fortune"]

    @staticmethod
    def aspiration_rewards() -> List[str]:
        return [
            "Creative Visionary", "Handy", "Gregarious", "Alluring", "Beloved",
            "Long Lived", "Fresh Chef", "Speed Reader", "Entrepreneurial",
            "Domestic", "Great Kisser", "Gym Rat", "Green Thumb"
        ]

    @staticmethod
    def collections() -> List[str]:
        return ["Elements", "Crystals", "Metals", "Fish", "Frogs", "Space Rocks"]

    @staticmethod
    def collectible_types() -> List[str]:
        return ["Elements", "Crystals", "Metals", "Fish", "Frogs", "Space Rocks"]

    @staticmethod
    def rarity_levels() -> List[str]:
        return ["Common", "Uncommon", "Rare", "Very Rare", "Extraordinary"]

    @staticmethod
    def artwork_types() -> List[str]:
        return ["Mathematical", "Pop Art", "Realist", "Surreal", "Classic"]

    @staticmethod
    def book_types() -> List[str]:
        return ["Children's Books", "Fantasy", "Mystery", "Non-Fiction", "Sci-Fi", "Romance"]

    @staticmethod
    def performance_types() -> List[str]:
        return ["Comedy", "Piano", "Singing"]

    @staticmethod
    def party_types() -> List[str]:
        return ["House Party", "Birthday Party", "Dinner Party", "Wedding"]

    @staticmethod
    def emotions() -> List[str]:
        return [
            "Happy", "Sad", "Angry", "Uncomfortable", "Embarrassed", 
            "Playful", "Focused", "Confident", "Energized", "Inspired", 
            "Flirty", "Tense"
        ]

    @staticmethod
    def personality_traits() -> List[str]:
        return [
            "Active", "Ambitious", "Art Lover", "Bookworm", "Bro", "Cheerful",
            "Childish", "Clumsy", "Creative", "Evil", "Family-Oriented", "Foodie",
            "Geek", "Genius", "Gloomy", "Glutton", "Good", "Goofball", "Hates Children",
            "Hot-Headed", "Insane", "Jealous", "Lazy", "Loner", "Loves Outdoors",
            "Mean", "Music Lover", "Neat", "Noncommittal", "Outgoing", "Perfectionist",
            "Romantic", "Self-Assured", "Slob", "Snob", "Vegetarian"
        ]

    @staticmethod
    def age_stages() -> List[str]:
        return ["Young Adult", "Adult", "Elder"]

    @staticmethod
    def starting_ages() -> List[str]:
        return ["Child", "Teen", "Young Adult"]

    @staticmethod
    def ending_ages() -> List[str]:
        return ["Teen", "Young Adult", "Adult", "Elder"]

    @staticmethod
    def child_ages() -> List[str]:
        return ["Teen", "Young Adult", "Adult"]

    @staticmethod
    def wealth_levels() -> List[str]:
        return ["Comfortable", "Well-Off", "Wealthy", "Fabulously Wealthy"]

    @staticmethod
    def family_achievements() -> List[str]:
        return [
            "All Skills Maxed", "Multi-Generation Success", "Perfect Relationships",
            "Huge Extended Family", "Legacy Challenge Complete"
        ]

    @staticmethod
    def challenge_types() -> List[str]:
        return [
            "Legacy Challenge", "100 Baby Challenge", "Rags to Riches",
            "Black Widow Challenge", "Asylum Challenge", "Perfect Genetics",
            "Apocalypse Challenge", "Decades Challenge"
        ]

    @staticmethod
    def ghost_objectives() -> List[str]:
        return [
            "Max a skill as a ghost", "Complete an aspiration as a ghost",
            "Get married as a ghost", "Have a ghost baby", "Haunt other Sims",
            "Possess objects successfully"
        ]

    @staticmethod
    def emotion_challenges() -> List[str]:
        return [
            "Win a chess game", "Write a bestselling book", "Complete a masterpiece painting",
            "Cook a gourmet meal", "Exercise for 3 hours straight", "Successfully flirt with 5 Sims",
            "Tell 10 jokes", "Solve the impossible logic puzzle", "Win a video game tournament"
        ]

    @staticmethod
    def death_causes() -> List[str]:
        return [
            "Old Age", "Embarrassment", "Anger", "Hysteria",
            "Electrocution", "Fire", "Drowning", "Hunger"
        ]

    @staticmethod
    def space_discoveries() -> List[str]:
        return [
            "Sixam (Alien World)", "Space Rocks", "Alien Artifacts",
            "Space Prints", "Alien Crystals"
        ]

    @staticmethod
    def needs_challenges() -> List[str]:
        return [
            "Complete objectives with all needs in red", "Never sleep in a bed for 7 days",
            "Only eat food you've grown yourself", "Never use the bathroom indoors",
            "Maintain perfect needs for 14 days straight", "Live entirely off the grid"
        ]

    @staticmethod
    def relationship_levels() -> List[str]:
        return ["Good Friends", "Best Friends", "Soulmates"]

    # Ranges
    @staticmethod
    def skill_levels() -> range:
        return range(3, 11, 2)

    @staticmethod
    def max_skill_counts() -> range:
        return range(2, 8, 2)

    @staticmethod
    def skill_group_counts() -> range:
        return range(2, 5)

    @staticmethod
    def career_levels() -> range:
        return range(3, 11, 2)

    @staticmethod
    def salary_amounts() -> range:
        return range(10000, 100000, 10000)

    @staticmethod
    def promotion_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def household_career_counts() -> range:
        return range(2, 6)

    @staticmethod
    def aspiration_counts() -> range:
        return range(2, 6)

    @staticmethod
    def milestone_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def friend_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def children_counts() -> range:
        return range(2, 8, 2)

    @staticmethod
    def household_sizes() -> range:
        return range(4, 8)

    @staticmethod
    def romance_counts() -> range:
        return range(2, 6)

    @staticmethod
    def collectible_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def collection_values() -> range:
        return range(5000, 50000, 5000)

    @staticmethod
    def artwork_counts() -> range:
        return range(5, 25, 5)

    @staticmethod
    def book_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def house_values() -> range:
        return range(50000, 500000, 50000)

    @staticmethod
    def program_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def performance_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def event_counts() -> range:
        return range(3, 15, 3)

    @staticmethod
    def emotion_counts() -> range:
        return range(5, 12)

    @staticmethod
    def location_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def generation_counts() -> range:
        return range(3, 10)

    @staticmethod
    def budget_limits() -> range:
        return range(10000, 50000, 10000)

    @staticmethod
    def time_limits() -> range:
        return range(7, 30, 7)

    @staticmethod
    def graft_counts() -> range:
        return range(3, 12, 3)

    @staticmethod
    def enemy_counts() -> range:
        return range(2, 8, 2)

    @staticmethod
    def concurrent_friend_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def sequential_marriage_counts() -> range:
        return range(3, 8)

    @staticmethod
    def cowplant_survival_days() -> range:
        return range(7, 30, 7)

    @staticmethod
    def themed_room_counts() -> range:
        return range(3, 12, 3)


# Archipelago Options
class Sims4IncludeSkills(DefaultOnToggle):
    """Include skill development and mastery objectives."""
    display_name = "Include Skills Development"

class Sims4IncludeCareers(DefaultOnToggle):
    """Include career progression and work-related objectives."""
    display_name = "Include Career Progression"

class Sims4IncludeAspirations(DefaultOnToggle):
    """Include aspiration completion and life goal objectives."""
    display_name = "Include Aspiration Goals"

class Sims4IncludeRelationships(DefaultOnToggle):
    """Include relationship building, family, and social objectives."""
    display_name = "Include Relationship Building"

class Sims4IncludeCollections(DefaultOnToggle):
    """Include collectible hunting and collection completion objectives."""
    display_name = "Include Collection Hunting"

class Sims4IncludeCreativeGoals(DefaultOnToggle):
    """Include creative objectives like painting, writing, building, and programming."""
    display_name = "Include Creative Goals"

class Sims4IncludeLifeSimulation(DefaultOnToggle):
    """Include life simulation objectives like aging, emotions, and events."""
    display_name = "Include Life Simulation"

class Sims4IncludeAchievements(DefaultOnToggle):
    """Include achievement-style objectives and challenges."""
    display_name = "Include Achievement Goals"

class Sims4DifficultyLevel(Choice):
    """Sets the difficulty level for objectives and constraints."""
    display_name = "Difficulty Level"
    option_easy = "Easy"
    option_normal = "Normal"
    option_hard = "Hard"
    option_expert = "Expert"
    default = option_normal

class Sims4FocusStyle(Choice):
    """Focus objectives on specific gameplay styles."""
    display_name = "Focus Style"
    option_all = "All"
    option_creative = "Creative"
    option_social = "Social"
    option_achievement = "Achievement"
    default = option_all