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
    
    # Expansion Pack DLC
    sims4_include_get_to_work: Sims4IncludeGetToWork
    sims4_include_get_together: Sims4IncludeGetTogether
    sims4_include_city_living: Sims4IncludeCityLiving
    sims4_include_cats_and_dogs: Sims4IncludeCatsAndDogs
    sims4_include_seasons: Sims4IncludeSeasons
    sims4_include_get_famous: Sims4IncludeGetFamous
    sims4_include_island_living: Sims4IncludeIslandLiving
    sims4_include_discover_university: Sims4IncludeDiscoverUniversity
    sims4_include_eco_lifestyle: Sims4IncludeEcoLifestyle
    sims4_include_snowy_escape: Sims4IncludeSnowyEscape
    sims4_include_cottage_living: Sims4IncludeCottageLiving
    sims4_include_high_school_years: Sims4IncludeHighSchoolYears
    sims4_include_growing_together: Sims4IncludeGrowingTogether
    sims4_include_horse_ranch: Sims4IncludeHorseRanch
    sims4_include_for_rent: Sims4IncludeForRent
    sims4_include_lovestruck: Sims4IncludeLovestruck
    
    # Game Pack DLC
    sims4_include_vampires: Sims4IncludeVampires
    sims4_include_parenthood: Sims4IncludeParenthood
    sims4_include_jungle_adventure: Sims4IncludeJungleAdventure
    sims4_include_stranger_ville: Sims4IncludeStrangerVille
    sims4_include_realm_of_magic: Sims4IncludeRealmOfMagic
    sims4_include_star_wars: Sims4IncludeStarWars
    sims4_include_dream_home_decorator: Sims4IncludeDreamHomeDecorator
    sims4_include_my_wedding_stories: Sims4IncludeMyWeddingStories
    sims4_include_werewolves: Sims4IncludeWerewolves
    
    # Additional Base Game Categories
    sims4_include_social_experiments: Sims4IncludeSocialExperiments
    sims4_include_economic_challenges: Sims4IncludeEconomicChallenges
    sims4_include_behavioral_quirks: Sims4IncludeBehavioralQuirks
    sims4_include_reputation_challenges: Sims4IncludeReputationChallenges
    sims4_include_experimental_living: Sims4IncludeExperimentalLiving
    sims4_include_routine_breaking: Sims4IncludeRoutineBreaking
    sims4_include_random_events: Sims4IncludeRandomEvents


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
                    label="Reach level CAREER_LEVEL in the CAREER_NAME career",
                    data={
                        "CAREER_LEVEL": (self.career_levels, 1),
                        "CAREER_NAME": (self.careers, 1)
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

        # DLC Content - Expansion Packs
        
        # Get to Work DLC
        if self.include_get_to_work:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach level CAREER_LEVEL in the CAREER_TYPE career",
                    data={
                        "CAREER_TYPE": (self.get_to_work_careers, 1),
                        "CAREER_LEVEL": (self.career_levels, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Master the SKILL skill from Get to Work",
                    data={"SKILL": (self.get_to_work_skills, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Own and operate a retail store for DAYS days",
                    data={"DAYS": (self.retail_store_days, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Get Together DLC
        if self.include_get_together:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Master the SKILL skill from Get Together",
                    data={"SKILL": (self.get_together_skills, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create and lead a club with MEMBER_COUNT members",
                    data={"MEMBER_COUNT": (self.club_member_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Visit LOCATION_COUNT different locations in Windenburg",
                    data={"LOCATION_COUNT": (self.windenburg_location_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # City Living DLC
        if self.include_city_living:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach level CAREER_LEVEL in the CAREER_NAME career",
                    data={
                        "CAREER_NAME": (self.city_living_careers, 1),
                        "CAREER_LEVEL": (self.career_levels, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Attend FESTIVAL_COUNT different festivals in San Myshuno",
                    data={"FESTIVAL_COUNT": (self.festival_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Live in an apartment in DISTRICT",
                    data={"DISTRICT": (self.city_living_locations, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Cats & Dogs DLC
        if self.include_cats_and_dogs:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Become a veterinarian and reach level CAREER_LEVEL",
                    data={"CAREER_LEVEL": (self.career_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Own and care for PET_COUNT pets",
                    data={"PET_COUNT": (self.pet_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Train a pet to learn TRICK_COUNT tricks",
                    data={"TRICK_COUNT": (self.trick_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Seasons DLC
        if self.include_seasons:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Experience all four seasons and complete ACTIVITY",
                    data={"ACTIVITY": (self.seasons_activities, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create and celebrate a custom holiday",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Reach level LEVEL in the Gardening career",
                    data={"LEVEL": (self.career_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Get Famous DLC
        if self.include_get_famous:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Become a famous CAREER_NAME and reach level CAREER_LEVEL",
                    data={
                        "CAREER_NAME": (self.get_famous_careers, 1),
                        "CAREER_LEVEL": (self.career_levels, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Reach FAME_LEVEL star fame level",
                    data={"FAME_LEVEL": (self.fame_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Master the SKILL skill from Get Famous",
                    data={"SKILL": (self.get_famous_skills, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Island Living DLC
        if self.include_island_living:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Become a mermaid and explore the ocean",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Reach level CAREER_LEVEL in the Conservationist career",
                    data={"CAREER_LEVEL": (self.career_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Clean up the ocean and improve Sulani's environment",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Discover University DLC
        if self.include_discover_university:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Graduate with a degree in DEGREE",
                    data={"DEGREE": (self.discover_university_degrees, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Join and participate in ORGANIZATION_COUNT university organizations",
                    data={"ORGANIZATION_COUNT": (self.organization_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Master the SKILL skill from Discover University",
                    data={"SKILL": (self.discover_university_skills, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Eco Lifestyle DLC
        if self.include_eco_lifestyle:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach level CAREER_LEVEL in the Civil Designer career",
                    data={"CAREER_LEVEL": (self.career_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Master the SKILL skill from Eco Lifestyle",
                    data={"SKILL": (self.eco_lifestyle_skills, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Improve your neighborhood's eco footprint to Green",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Snowy Escape DLC
        if self.include_snowy_escape:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Master the SKILL skill from Snowy Escape",
                    data={"SKILL": (self.snowy_escape_skills, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Experience hot springs and achieve relaxation benefits",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete LIFESTYLE_COUNT different lifestyles",
                    data={"LIFESTYLE_COUNT": (self.lifestyle_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Cottage Living DLC
        if self.include_cottage_living:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Master the Cross-Stitching skill to level 10",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Raise and care for ANIMAL_COUNT farm animals",
                    data={"ANIMAL_COUNT": (self.farm_animal_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Participate in Finchwick Fair and win CONTEST_COUNT contests",
                    data={"CONTEST_COUNT": (self.contest_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # High School Years DLC
        if self.include_high_school_years:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Graduate high school with honors",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Attend prom and become prom royalty",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Join and excel in ACTIVITY_COUNT high school activities",
                    data={"ACTIVITY_COUNT": (self.high_school_activity_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Growing Together DLC
        if self.include_growing_together:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Achieve MILESTONE_COUNT family milestones",
                    data={"MILESTONE_COUNT": (self.family_milestone_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Raise a Sim from infant to young adult",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Build strong family dynamics and compatibility",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Horse Ranch DLC
        if self.include_horse_ranch:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Master the SKILL skill from Horse Ranch",
                    data={"SKILL": (self.horse_ranch_skills, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Raise and train HORSE_COUNT horses",
                    data={"HORSE_COUNT": (self.horse_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Win COMPETITION_COUNT horse competitions",
                    data={"COMPETITION_COUNT": (self.competition_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # For Rent DLC
        if self.include_for_rent:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Become a landlord and manage PROPERTY_COUNT rental properties",
                    data={"PROPERTY_COUNT": (self.property_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Maintain high tenant satisfaction for MONTH_COUNT months",
                    data={"MONTH_COUNT": (self.rental_month_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Lovestruck DLC  
        if self.include_lovestruck:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Experience new romantic interactions in Ciudad Enamorada",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Create COUPLE_COUNT successful romantic relationships",
                    data={"COUPLE_COUNT": (self.couple_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # DLC Content - Game Packs

        # StrangerVille Game Pack
        if self.include_stranger_ville:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Solve the StrangerVille mystery completely",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Reach level CAREER_LEVEL in the Military career",
                    data={"CAREER_LEVEL": (self.career_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Investigate and document EVIDENCE_COUNT pieces of evidence",
                    data={"EVIDENCE_COUNT": (self.evidence_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Star Wars Game Pack
        if self.include_star_wars:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Master the SKILL skill from Star Wars",
                    data={"SKILL": (self.star_wars_skills, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Choose a faction and complete their storyline",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Build and customize a lightsaber",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Dream Home Decorator Game Pack
        if self.include_dream_home_decorator:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Reach level CAREER_LEVEL in the Interior Designer career",
                    data={"CAREER_LEVEL": (self.career_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete CLIENT_COUNT interior design projects successfully",
                    data={"CLIENT_COUNT": (self.design_client_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Achieve perfect client satisfaction on PERFECT_COUNT projects",
                    data={"PERFECT_COUNT": (self.perfect_project_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # My Wedding Stories Game Pack
        if self.include_my_wedding_stories:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Plan and execute a perfect wedding ceremony",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Host WEDDING_COUNT different wedding events",
                    data={"WEDDING_COUNT": (self.wedding_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Experience a destination wedding in Tartosa",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Vampires Game Pack
        if self.include_vampires:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Become a vampire and reach rank RANK",
                    data={"RANK": (self.vampire_ranks, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Master the SKILL skill from Vampires",
                    data={"SKILL": (self.vampires_skills, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create a vampire coven with MEMBER_COUNT vampires",
                    data={"MEMBER_COUNT": (self.vampire_coven_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Parenthood Game Pack
        if self.include_parenthood:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Raise a child with all positive character values",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Master the Parenting skill to level 10",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Guide CHILD_COUNT children from toddler to young adult",
                    data={"CHILD_COUNT": (self.child_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        # Jungle Adventure Game Pack
        if self.include_jungle_adventure:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Master the SKILL skill from Jungle Adventure",
                    data={"SKILL": (self.jungle_adventure_skills, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Explore TEMPLE_COUNT ancient temples in Selvadorada",
                    data={"TEMPLE_COUNT": (self.temple_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Find and collect ARTIFACT_COUNT rare artifacts",
                    data={"ARTIFACT_COUNT": (self.artifact_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Realm of Magic Game Pack
        if self.include_realm_of_magic:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Become a spellcaster and master SPELL_COUNT spells",
                    data={"SPELL_COUNT": (self.spell_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Reach rank RANK as a spellcaster",
                    data={"RANK": (self.spellcaster_ranks, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Create POTION_COUNT different magical potions",
                    data={"POTION_COUNT": (self.potion_counts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Werewolves Game Pack
        if self.include_werewolves:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Become a werewolf and master your abilities",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Lead or join a werewolf pack in Moonwood Mill",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete the werewolf storyline and choose your path",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Social Experiments
        if self.include_social_experiments:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Isolate your Sim from all social contact for ISOLATION_PERIOD",
                    data={"ISOLATION_PERIOD": (self.isolation_periods, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Start daily SOCIAL_CONFLICT with SOCIAL_TARGET",
                    data={
                        "SOCIAL_CONFLICT": (self.social_conflicts, 1),
                        "SOCIAL_TARGET": (self.social_targets, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Befriend exactly 10 Sims then cut contact with all of them",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Become enemies with every household member",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Economic Challenges  
        if self.include_economic_challenges:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Live on exactly §BUDGET_AMOUNT for 30 days",
                    data={"BUDGET_AMOUNT": (self.budget_amounts, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Experience a WEALTH_TRANSITION storyline",
                    data={"WEALTH_TRANSITION": (self.wealth_transitions, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Survive by ECONOMIC_ACTIVITY only",
                    data={"ECONOMIC_ACTIVITY": (self.economic_activities, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Own nothing but essentials - sell all luxury items",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        # Behavioral Quirks
        if self.include_behavioral_quirks:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Adopt the quirky behavior of QUIRKY_BEHAVIOR",
                    data={"QUIRKY_BEHAVIOR": (self.quirky_behaviors, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Follow a strict diet of FOOD_RESTRICTION",
                    data={"FOOD_RESTRICTION": (self.food_restrictions, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Develop the strange habit of STRANGE_HABIT",
                    data={"STRANGE_HABIT": (self.strange_habits, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Never use the same interaction twice in one day",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Reputation Challenges
        if self.include_reputation_challenges:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Become known as the NEGATIVE_REPUTATION",
                    data={"NEGATIVE_REPUTATION": (self.negative_reputations, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Engage in DISRUPTIVE_ACTIVITY daily",
                    data={"DISRUPTIVE_ACTIVITY": (self.disruptive_activities, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Start a COMMUNITY_CONFLICT with neighbors",
                    data={"COMMUNITY_CONFLICT": (self.community_conflicts, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Get kicked out of every community lot you visit",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Experimental Living
        if self.include_experimental_living:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Build and live in a house with UNCONVENTIONAL_HOUSING",
                    data={"UNCONVENTIONAL_HOUSING": (self.unconventional_housing, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Live with the restriction of UNUSUAL_RESTRICTION",
                    data={"UNUSUAL_RESTRICTION": (self.unusual_restrictions, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Experiment with LIVING_EXPERIMENT",
                    data={"LIVING_EXPERIMENT": (self.living_experiments, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Move houses every 7 days for a month",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Routine Breaking
        if self.include_routine_breaking:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Implement ROUTINE_CHANGE every week",
                    data={"ROUTINE_CHANGE": (self.routine_changes, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Engage in CHAOS_ACTIVITY whenever bored",
                    data={"CHAOS_ACTIVITY": (self.chaos_activities, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Set UNPREDICTABLE_GOAL as your main life goal",
                    data={"UNPREDICTABLE_GOAL": (self.unpredictable_goals, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Never do the same activity two days in a row",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                ),
            ])

        # Random Events
        if self.include_random_events:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Survive and recover from DISASTER_TYPE",
                    data={"DISASTER_TYPE": (self.disaster_types, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete a SURVIVAL_CHALLENGE scenario",
                    data={"SURVIVAL_CHALLENGE": (self.survival_challenges, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Navigate through CHAOS_SCENARIO",
                    data={"CHAOS_SCENARIO": (self.chaos_scenarios, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Create and resolve 5 different emergencies in one week",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3,
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

    # DLC Property checks
    @property
    def include_get_to_work(self) -> bool:
        return self.archipelago_options.sims4_include_get_to_work.value

    @property
    def include_get_together(self) -> bool:
        return self.archipelago_options.sims4_include_get_together.value

    @property
    def include_city_living(self) -> bool:
        return self.archipelago_options.sims4_include_city_living.value

    @property
    def include_cats_and_dogs(self) -> bool:
        return self.archipelago_options.sims4_include_cats_and_dogs.value

    @property
    def include_seasons(self) -> bool:
        return self.archipelago_options.sims4_include_seasons.value

    @property
    def include_get_famous(self) -> bool:
        return self.archipelago_options.sims4_include_get_famous.value

    @property
    def include_island_living(self) -> bool:
        return self.archipelago_options.sims4_include_island_living.value

    @property
    def include_discover_university(self) -> bool:
        return self.archipelago_options.sims4_include_discover_university.value

    @property
    def include_eco_lifestyle(self) -> bool:
        return self.archipelago_options.sims4_include_eco_lifestyle.value

    @property
    def include_snowy_escape(self) -> bool:
        return self.archipelago_options.sims4_include_snowy_escape.value

    @property
    def include_cottage_living(self) -> bool:
        return self.archipelago_options.sims4_include_cottage_living.value

    @property
    def include_high_school_years(self) -> bool:
        return self.archipelago_options.sims4_include_high_school_years.value

    @property
    def include_growing_together(self) -> bool:
        return self.archipelago_options.sims4_include_growing_together.value

    @property
    def include_horse_ranch(self) -> bool:
        return self.archipelago_options.sims4_include_horse_ranch.value

    @property
    def include_for_rent(self) -> bool:
        return self.archipelago_options.sims4_include_for_rent.value

    @property
    def include_lovestruck(self) -> bool:
        return self.archipelago_options.sims4_include_lovestruck.value

    @property
    def include_vampires(self) -> bool:
        return self.archipelago_options.sims4_include_vampires.value

    @property
    def include_parenthood(self) -> bool:
        return self.archipelago_options.sims4_include_parenthood.value

    @property
    def include_jungle_adventure(self) -> bool:
        return self.archipelago_options.sims4_include_jungle_adventure.value

    @property
    def include_stranger_ville(self) -> bool:
        return self.archipelago_options.sims4_include_stranger_ville.value

    @property
    def include_realm_of_magic(self) -> bool:
        return self.archipelago_options.sims4_include_realm_of_magic.value

    @property
    def include_star_wars(self) -> bool:
        return self.archipelago_options.sims4_include_star_wars.value

    @property
    def include_dream_home_decorator(self) -> bool:
        return self.archipelago_options.sims4_include_dream_home_decorator.value

    @property
    def include_my_wedding_stories(self) -> bool:
        return self.archipelago_options.sims4_include_my_wedding_stories.value

    @property
    def include_werewolves(self) -> bool:
        return self.archipelago_options.sims4_include_werewolves.value

    # Additional Base Game Categories Properties
    @property
    def include_social_experiments(self) -> bool:
        return self.archipelago_options.sims4_include_social_experiments.value

    @property
    def include_economic_challenges(self) -> bool:
        return self.archipelago_options.sims4_include_economic_challenges.value

    @property
    def include_behavioral_quirks(self) -> bool:
        return self.archipelago_options.sims4_include_behavioral_quirks.value

    @property
    def include_reputation_challenges(self) -> bool:
        return self.archipelago_options.sims4_include_reputation_challenges.value

    @property
    def include_experimental_living(self) -> bool:
        return self.archipelago_options.sims4_include_experimental_living.value

    @property
    def include_routine_breaking(self) -> bool:
        return self.archipelago_options.sims4_include_routine_breaking.value

    @property
    def include_random_events(self) -> bool:
        return self.archipelago_options.sims4_include_random_events.value

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

    # DLC-Specific Ranges
    @staticmethod
    def retail_store_days() -> range:
        return range(7, 30, 7)

    @staticmethod
    def club_member_counts() -> range:
        return range(4, 8)

    @staticmethod
    def windenburg_location_counts() -> range:
        return range(3, 5)

    @staticmethod
    def festival_counts() -> range:
        return range(3, 6)

    @staticmethod
    def pet_counts() -> range:
        return range(2, 6)

    @staticmethod
    def trick_counts() -> range:
        return range(3, 8)

    @staticmethod
    def fame_levels() -> range:
        return range(3, 6)

    @staticmethod
    def organization_counts() -> range:
        return range(2, 4)

    @staticmethod
    def lifestyle_counts() -> range:
        return range(2, 5)

    @staticmethod
    def farm_animal_counts() -> range:
        return range(4, 8)

    @staticmethod
    def contest_counts() -> range:
        return range(2, 5)

    @staticmethod
    def high_school_activity_counts() -> range:
        return range(2, 4)

    @staticmethod
    def family_milestone_counts() -> range:
        return range(5, 12)

    @staticmethod
    def horse_counts() -> range:
        return range(2, 5)

    @staticmethod
    def competition_counts() -> range:
        return range(3, 8)

    @staticmethod
    def property_counts() -> range:
        return range(2, 5)

    @staticmethod
    def rental_month_counts() -> range:
        return range(3, 8)

    @staticmethod
    def couple_counts() -> range:
        return range(2, 5)

    @staticmethod
    def evidence_counts() -> range:
        return range(5, 10)

    @staticmethod
    def design_client_counts() -> range:
        return range(5, 12)

    @staticmethod
    def perfect_project_counts() -> range:
        return range(3, 8)

    @staticmethod
    def wedding_counts() -> range:
        return range(2, 5)

    @staticmethod
    def vampire_ranks() -> range:
        return range(3, 6)

    @staticmethod
    def vampire_coven_counts() -> range:
        return range(3, 6)

    @staticmethod
    def university_organization_counts() -> range:
        return range(2, 4)

    @staticmethod
    def temple_counts() -> range:
        return range(2, 4)

    @staticmethod
    def artifact_counts() -> range:
        return range(5, 10)

    @staticmethod
    def spell_counts() -> range:
        return range(5, 15)

    @staticmethod
    def spellcaster_ranks() -> range:
        return range(3, 6)

    @staticmethod
    def potion_counts() -> range:
        return range(3, 8)

    @staticmethod
    def child_counts() -> range:
        return range(2, 5)


    # DLC-Specific Data Lists
    
    # Get to Work DLC
    @staticmethod
    def get_to_work_careers() -> List[str]:
        return [
            "Doctor", "Detective", "Scientist"
        ]
    
    @staticmethod
    def get_to_work_skills() -> List[str]:
        return [
            "Rocket Science", "Photography", "Baking"
        ]
    
    @staticmethod
    def get_to_work_locations() -> List[str]:
        return [
            "Magnolia Promenade", "Hospital", "Police Station", "Science Lab"
        ]

    # Get Together DLC
    @staticmethod
    def get_together_skills() -> List[str]:
        return [
            "DJ Mixing", "Dancing"
        ]
    
    @staticmethod
    def get_together_locations() -> List[str]:
        return [
            "Windenburg", "Von Haunt Estate", "Bluffs", "Cafe"
        ]

    # City Living DLC  
    @staticmethod
    def city_living_careers() -> List[str]:
        return [
            "Politician", "Social Media", "Critic"
        ]
    
    @staticmethod
    def city_living_locations() -> List[str]:
        return [
            "San Myshuno", "Arts Quarter", "Fashion District", "Spice Market"
        ]
    
    @staticmethod
    def city_living_festivals() -> List[str]:
        return [
            "Spice Festival", "GeekCon", "Romance Festival", "Flea Market", "Humor & Hijinks Festival"
        ]

    # Cats & Dogs DLC
    @staticmethod
    def cats_and_dogs_careers() -> List[str]:
        return [
            "Veterinarian"
        ]
    
    @staticmethod
    def cats_and_dogs_skills() -> List[str]:
        return [
            "Veterinarian"
        ]
    
    @staticmethod
    def cats_and_dogs_locations() -> List[str]:
        return [
            "Brindleton Bay", "Sable Square", "Whiskerman's Wharf", "Dachshund's Creek"
        ]

    # Seasons DLC
    @staticmethod
    def seasons_careers() -> List[str]:
        return [
            "Gardener"
        ]
    
    @staticmethod
    def seasons_activities() -> List[str]:
        return [
            "Ice Skating", "Skiing", "Snowboarding", "Beach Activities", "Holiday Celebrations"
        ]

    # Get Famous DLC
    @staticmethod
    def get_famous_careers() -> List[str]:
        return [
            "Actor"
        ]
    
    @staticmethod
    def get_famous_skills() -> List[str]:
        return [
            "Acting", "Media Production"
        ]
    
    @staticmethod
    def get_famous_locations() -> List[str]:
        return [
            "Del Sol Valley", "Starlight Boulevard", "Mirage Park", "Pinnacles"
        ]

    # Island Living DLC
    @staticmethod
    def island_living_careers() -> List[str]:
        return [
            "Conservationist"
        ]
    
    @staticmethod
    def island_living_locations() -> List[str]:
        return [
            "Sulani", "Ohan'ali Town", "Lani St. Taz", "Mua Pel'am"
        ]

    # Discover University DLC
    @staticmethod
    def discover_university_skills() -> List[str]:
        return [
            "Research and Debate", "Robotics"
        ]
    
    @staticmethod
    def discover_university_degrees() -> List[str]:
        return [
            "Biology", "Computer Science", "Economics", "Fine Art", "History", "Language and Literature", 
            "Physics", "Psychology", "Villainy", "Distinguished"
        ]

    # Eco Lifestyle DLC
    @staticmethod
    def eco_lifestyle_careers() -> List[str]:
        return [
            "Civil Designer"
        ]
    
    @staticmethod
    def eco_lifestyle_skills() -> List[str]:
        return [
            "Fabrication", "Juice Fizzing"
        ]

    # Snowy Escape DLC
    @staticmethod
    def snowy_escape_skills() -> List[str]:
        return [
            "Skiing", "Snowboarding", "Rock Climbing"
        ]
    
    @staticmethod
    def snowy_escape_locations() -> List[str]:
        return [
            "Mt. Komorebi", "Yukimatsu", "Wakaba", "Senbamachi"
        ]

    # Cottage Living DLC
    @staticmethod
    def cottage_living_skills() -> List[str]:
        return [
            "Cross-Stitching"
        ]
    
    @staticmethod
    def cottage_living_locations() -> List[str]:
        return [
            "Henford-on-Bagley", "Bramblewood", "Old New Henford", "The Bramble"
        ]

    # Horse Ranch DLC
    @staticmethod
    def horse_ranch_skills() -> List[str]:
        return [
            "Horse Riding", "Nectar Making", "Ranch"
        ]
    
    @staticmethod
    def horse_ranch_locations() -> List[str]:
        return [
            "Chestnut Ridge", "Galloping Gulch", "New Appaloosa", "Riders' Glen"
        ]

    # Vampires Game Pack
    @staticmethod
    def vampires_skills() -> List[str]:
        return [
            "Vampire Lore", "Pipe Organ"
        ]
    
    @staticmethod
    def vampires_locations() -> List[str]:
        return [
            "Forgotten Hollow", "Vlad's Lair", "Garliclauter Mansion"
        ]

    # Parenthood Game Pack
    @staticmethod
    def parenthood_skills() -> List[str]:
        return [
            "Parenting"
        ]

    # Jungle Adventure Game Pack
    @staticmethod
    def jungle_adventure_skills() -> List[str]:
        return [
            "Archaeology", "Selvadoradian Culture"
        ]
    
    @staticmethod
    def jungle_adventure_locations() -> List[str]:
        return [
            "Selvadorada", "Belomisia Jungle", "Puerto Llamante Marketplace"
        ]

    # StrangerVille Game Pack
    @staticmethod
    def stranger_ville_careers() -> List[str]:
        return [
            "Military"
        ]
    
    @staticmethod
    def stranger_ville_locations() -> List[str]:
        return [
            "StrangerVille", "Desert Bloom Park", "The Crater", "Secret Lab"
        ]

    # Realm of Magic Game Pack
    @staticmethod
    def realm_of_magic_skills() -> List[str]:
        return [
            "Spellcasting"
        ]
    
    @staticmethod
    def realm_of_magic_locations() -> List[str]:
        return [
            "Glimmerbrook", "Magic Realm", "Casters Alley", "The Gardens"
        ]

    # Star Wars Game Pack
    @staticmethod
    def star_wars_skills() -> List[str]:
        return [
            "Lightsaber", "Force"
        ]
    
    @staticmethod
    def star_wars_locations() -> List[str]:
        return [
            "Batuu", "Black Spire Outpost", "Resistance Encampment", "First Order Territory"
        ]

    # Dream Home Decorator Game Pack
    @staticmethod
    def dream_home_decorator_careers() -> List[str]:
        return [
            "Interior Designer"
        ]

    # Werewolves Game Pack
    @staticmethod
    def werewolves_locations() -> List[str]:
        return [
            "Moonwood Mill", "Grimtooth Bar", "The Library", "Howling Point"
        ]

    # Additional Base Game Categories Data Lists
    
    # Social Experiments
    @staticmethod
    def isolation_periods() -> List[str]:
        return ["3 days", "7 days", "14 days", "30 days"]
    
    @staticmethod
    def social_conflicts() -> List[str]:
        return ["arguments", "fights", "insults", "pranks", "gossip"]
    
    @staticmethod
    def social_targets() -> List[str]:
        return ["neighbors", "coworkers", "strangers", "family members", "roommates"]

    # Economic Challenges
    @staticmethod
    def budget_amounts() -> List[str]:
        return ["100", "500", "1000", "2000", "5000"]
    
    @staticmethod
    def wealth_transitions() -> List[str]:
        return ["rags to riches", "riches to rags", "middle class to poor", "poor to wealthy"]
    
    @staticmethod
    def economic_activities() -> List[str]:
        return ["dumpster diving", "stealing", "bargaining", "thrift shopping", "freeloading"]

    # Behavioral Quirks
    @staticmethod
    def quirky_behaviors() -> List[str]:
        return ["nocturnal schedule", "only cold showers", "talking to mirrors", "eating standing up", "backwards walking"]
    
    @staticmethod
    def food_restrictions() -> List[str]:
        return ["only grilled cheese", "vegetarian only", "no cooked food", "single ingredient meals", "expired food only"]
    
    @staticmethod
    def strange_habits() -> List[str]:
        return ["speaking to plants", "counting everything", "avoiding certain colors", "ritual behaviors", "collecting trash"]

    # Reputation Challenges
    @staticmethod
    def negative_reputations() -> List[str]:
        return ["neighborhood menace", "party crasher", "gossip spreader", "troublemaker", "social pariah"]
    
    @staticmethod
    def disruptive_activities() -> List[str]:
        return ["loud music at night", "stealing newspapers", "pranking neighbors", "starting rumors", "being rude to everyone"]
    
    @staticmethod
    def community_conflicts() -> List[str]:
        return ["homeowners association disputes", "noise complaints", "property line arguments", "pet conflicts", "parking disputes"]

    # Experimental Living
    @staticmethod
    def unconventional_housing() -> List[str]:
        return ["no walls", "all glass", "only one room", "no doors", "outdoor only"]
    
    @staticmethod
    def unusual_restrictions() -> List[str]:
        return ["no electricity", "no plumbing", "no furniture", "no decorations", "minimalist extreme"]
    
    @staticmethod
    def living_experiments() -> List[str]:
        return ["communal everything", "no privacy", "constant guests", "living in public spaces", "nomadic lifestyle"]

    # Routine Breaking
    @staticmethod
    def routine_changes() -> List[str]:
        return ["daily schedule flip", "weekly job change", "monthly move", "constant redecoration", "skill rotation"]
    
    @staticmethod
    def chaos_activities() -> List[str]:
        return ["random skill practice", "spontaneous travel", "impulsive purchases", "career hopping", "relationship cycling"]
    
    @staticmethod
    def unpredictable_goals() -> List[str]:
        return ["dice-determined actions", "random emotion pursuit", "stranger interaction challenges", "location roulette", "activity lottery"]

    # Random Events
    @staticmethod
    def disaster_types() -> List[str]:
        return ["house fires", "flooding", "burglary", "appliance breakdowns", "relationship drama"]
    
    @staticmethod
    def survival_challenges() -> List[str]:
        return ["rebuild after fire", "recover from bankruptcy", "start over homeless", "survive natural disasters", "overcome family tragedy"]
    
    @staticmethod
    def chaos_scenarios() -> List[str]:
        return ["multiple emergencies", "cascading failures", "social meltdowns", "career disasters", "health crises"]


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
    default = "normal"

class Sims4FocusStyle(Choice):
    """Focus objectives on specific gameplay styles."""
    display_name = "Focus Style"
    option_all = "All"
    option_creative = "Creative"
    option_social = "Social"
    option_achievement = "Achievement"
    default = "all"


# DLC Options - Expansion Packs
class Sims4IncludeGetToWork(Toggle):
    """Include Get to Work content: active careers (Doctor, Detective, Scientist), aliens, retail ownership."""
    display_name = "Include Get to Work"

class Sims4IncludeGetTogether(Toggle):
    """Include Get Together content: clubs, Windenburg, DJ skill."""
    display_name = "Include Get Together"

class Sims4IncludeCityLiving(Toggle):
    """Include City Living content: apartments, San Myshuno, festivals, careers."""
    display_name = "Include City Living"

class Sims4IncludeCatsAndDogs(Toggle):
    """Include Cats & Dogs content: pets, veterinarian career, Brindleton Bay."""
    display_name = "Include Cats & Dogs"

class Sims4IncludeSeasons(Toggle):
    """Include Seasons content: weather, holidays, gardening career."""
    display_name = "Include Seasons"

class Sims4IncludeGetFamous(Toggle):
    """Include Get Famous content: acting career, fame system, Del Sol Valley."""
    display_name = "Include Get Famous"

class Sims4IncludeIslandLiving(Toggle):
    """Include Island Living content: mermaids, conservationist career, Sulani."""
    display_name = "Include Island Living"

class Sims4IncludeDiscoverUniversity(Toggle):
    """Include Discover University content: university, degrees, organizations."""
    display_name = "Include Discover University"

class Sims4IncludeEcoLifestyle(Toggle):
    """Include Eco Lifestyle content: civil designer career, eco footprint, Evergreen Harbor."""
    display_name = "Include Eco Lifestyle"

class Sims4IncludeSnowyEscape(Toggle):
    """Include Snowy Escape content: skiing, hot springs, lifestyles, Mt. Komorebi."""
    display_name = "Include Snowy Escape"

class Sims4IncludeCottageLiving(Toggle):
    """Include Cottage Living content: farming, animals, Henford-on-Bagley."""
    display_name = "Include Cottage Living"

class Sims4IncludeHighSchoolYears(Toggle):
    """Include High School Years content: teen gameplay, prom, graduation."""
    display_name = "Include High School Years"

class Sims4IncludeGrowingTogether(Toggle):
    """Include Growing Together content: family dynamics, milestones, San Sequoia."""
    display_name = "Include Growing Together"

class Sims4IncludeHorseRanch(Toggle):
    """Include Horse Ranch content: horses, nectar making, Chestnut Ridge."""
    display_name = "Include Horse Ranch"

class Sims4IncludeForRent(Toggle):
    """Include For Rent content: property rental, Tomarang."""
    display_name = "Include For Rent"

class Sims4IncludeLovestruck(Toggle):
    """Include Lovestruck content: romantic relationships, Ciudad Enamorada."""
    display_name = "Include Lovestruck"


# DLC Options - Game Packs
class Sims4IncludeVampires(Toggle):
    """Include Vampires content: vampire gameplay, Forgotten Hollow."""
    display_name = "Include Vampires"

class Sims4IncludeParenthood(Toggle):
    """Include Parenthood content: parenting skill, character values."""
    display_name = "Include Parenthood"

class Sims4IncludeJungleAdventure(Toggle):
    """Include Jungle Adventure content: archaeology, Selvadorada."""
    display_name = "Include Jungle Adventure"

class Sims4IncludeStrangerVille(Toggle):
    """Include StrangerVille content: mystery solving, military career."""
    display_name = "Include StrangerVille"

class Sims4IncludeRealmOfMagic(Toggle):
    """Include Realm of Magic content: spellcasters, Glimmerbrook."""
    display_name = "Include Realm of Magic"

class Sims4IncludeStarWars(Toggle):
    """Include Star Wars content: Batuu, lightsabers, Force powers."""
    display_name = "Include Star Wars: Journey to Batuu"

class Sims4IncludeDreamHomeDecorator(Toggle):
    """Include Dream Home Decorator content: interior decorator career."""
    display_name = "Include Dream Home Decorator"

class Sims4IncludeMyWeddingStories(Toggle):
    """Include My Wedding Stories content: wedding events, Tartosa."""
    display_name = "Include My Wedding Stories"

class Sims4IncludeWerewolves(Toggle):
    """Include Werewolves content: werewolf gameplay, Moonwood Mill."""
    display_name = "Include Werewolves"

# Additional Base Game Categories
class Sims4IncludeSocialExperiments(DefaultOnToggle):
    """Include experimental social scenarios and unusual relationship dynamics."""
    display_name = "Include Social Experiments"

class Sims4IncludeEconomicChallenges(DefaultOnToggle):
    """Include financial challenges, poverty simulations, and economic gameplay."""
    display_name = "Include Economic Challenges"

class Sims4IncludeBehavioralQuirks(DefaultOnToggle):
    """Include unusual behavior patterns, quirky lifestyles, and trait experiments."""
    display_name = "Include Behavioral Quirks"

class Sims4IncludeReputationChallenges(DefaultOnToggle):
    """Include negative reputation goals, social chaos, and neighborhood conflicts."""
    display_name = "Include Reputation Challenges"

class Sims4IncludeExperimentalLiving(DefaultOnToggle):
    """Include unconventional housing, unusual living situations, and lifestyle experiments."""
    display_name = "Include Experimental Living"

class Sims4IncludeRoutineBreaking(DefaultOnToggle):
    """Include anti-routine challenges, constant change, and unpredictable gameplay."""
    display_name = "Include Routine Breaking"

class Sims4IncludeRandomEvents(Toggle):
    """Include disaster management, chaos survival, and random event challenges."""
    display_name = "Include Random Events"