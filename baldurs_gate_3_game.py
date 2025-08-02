from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle, Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BaldursGate3ArchipelagoOptions:
    bg3_include_character_builds: BG3IncludeCharacterBuilds
    bg3_include_story_progression: BG3IncludeStoryProgression
    bg3_include_companion_quests: BG3IncludeCompanionQuests
    bg3_include_exploration: BG3IncludeExploration
    bg3_include_combat_challenges: BG3IncludeCombatChallenges
    bg3_include_social_encounters: BG3IncludeSocialEncounters
    bg3_include_collectibles: BG3IncludeCollectibles
    bg3_include_achievement_hunting: BG3IncludeAchievementHunting
    bg3_difficulty_preference: BG3DifficultyPreference
    bg3_playstyle_focus: BG3PlaystyleFocus


class BaldursGate3Game(Game):
    name = "Baldur's Gate 3"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XSXS,
        KeymastersKeepGamePlatforms.MAC,
    ]

    is_adult_only_or_unrated = False

    options_cls = BaldursGate3ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints = []
        
        constraints.extend([
            GameObjectiveTemplate(
                label="Complete this objective using only DAMAGE_TYPE damage",
                data={"DAMAGE_TYPE": (self.damage_types, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective with PARTY_COMPOSITION party",
                data={"PARTY_COMPOSITION": (self.party_compositions, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective without using FORBIDDEN_ABILITY",
                data={"FORBIDDEN_ABILITY": (self.forbidden_abilities, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective on DIFFICULTY_SETTING difficulty",
                data={"DIFFICULTY_SETTING": (self.difficulty_settings, 1)},
            ),
            GameObjectiveTemplate(
                label="Complete this objective with ROLEPLAY_RESTRICTION roleplay restriction",
                data={"ROLEPLAY_RESTRICTION": (self.roleplay_restrictions, 1)},
            ),
        ])
        
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        game_objective_templates: List[GameObjectiveTemplate] = list()

        # Character Builds
        if self.include_character_builds:
            build_templates = []
            
            if self.difficulty_preference in ["All", "Hard"]:
                build_templates.extend([
                    GameObjectiveTemplate(
                        label="Complete Act 1 with a MULTICLASS_BUILD multiclass build",
                        data={"MULTICLASS_BUILD": (self.multiclass_builds, 1)},
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Complete a major boss fight using only CANTRIP_TYPE cantrips",
                        data={"CANTRIP_TYPE": (self.cantrip_types, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    ),
                ])
            
            build_templates.extend([
                GameObjectiveTemplate(
                    label="Create and play a CLASS character to level LEVEL_RANGE",
                    data={
                        "CLASS": (self.character_classes, 1),
                        "LEVEL_RANGE": (self.level_ranges, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Experiment with SUBCLASS_COUNT different SUBCLASS_TYPE subclasses",
                    data={
                        "SUBCLASS_COUNT": (self.subclass_counts, 1),
                        "SUBCLASS_TYPE": (self.subclass_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Build a character focused on ABILITY_FOCUS",
                    data={"ABILITY_FOCUS": (self.ability_focuses, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete FEAT_COUNT different character builds using FEAT_TYPE feats",
                    data={
                        "FEAT_COUNT": (self.feat_counts, 1),
                        "FEAT_TYPE": (self.feat_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])
            
            game_objective_templates.extend(build_templates)

        # Story Progression
        if self.include_story_progression:
            story_templates = []
            
            if self.playstyle_focus in ["All", "Story"]:
                story_templates.extend([
                    GameObjectiveTemplate(
                        label="Complete Act ACT_NUMBER with STORY_CHOICE story choice",
                        data={
                            "ACT_NUMBER": (self.act_numbers, 1),
                            "STORY_CHOICE": (self.major_story_choices, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Experience ENDING_TYPE ending",
                        data={"ENDING_TYPE": (self.ending_types, 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1,
                    ),
                ])
            
            story_templates.extend([
                GameObjectiveTemplate(
                    label="Complete QUEST_COUNT QUEST_TYPE quests",
                    data={
                        "QUEST_COUNT": (self.quest_counts, 1),
                        "QUEST_TYPE": (self.quest_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Discover LORE_COUNT pieces of LORE_CATEGORY lore",
                    data={
                        "LORE_COUNT": (self.lore_counts, 1),
                        "LORE_CATEGORY": (self.lore_categories, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Make CHOICE_COUNT significant choices that impact STORY_IMPACT",
                    data={
                        "CHOICE_COUNT": (self.choice_counts, 1),
                        "STORY_IMPACT": (self.story_impacts, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])
            
            game_objective_templates.extend(story_templates)

        # Companion Quests
        if self.include_companion_quests:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Complete COMPANION's personal quest line",
                    data={"COMPANION": (self.companions, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Achieve RELATIONSHIP_LEVEL relationship with COMPANION_TARGET",
                    data={
                        "RELATIONSHIP_LEVEL": (self.relationship_levels, 1),
                        "COMPANION_TARGET": (self.companion_targets, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Experience ROMANCE_COUNT different romance storylines",
                    data={"ROMANCE_COUNT": (self.romance_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Help COMPANION_COUNT companions resolve their PERSONAL_CONFLICT",
                    data={
                        "COMPANION_COUNT": (self.companion_counts, 1),
                        "PERSONAL_CONFLICT": (self.personal_conflicts, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Recruit and maintain PARTY_SIZE party members throughout ACT_SCOPE",
                    data={
                        "PARTY_SIZE": (self.party_sizes, 1),
                        "ACT_SCOPE": (self.act_scopes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Exploration
        if self.include_exploration:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Discover SECRET_COUNT secret areas in LOCATION_TYPE",
                    data={
                        "SECRET_COUNT": (self.secret_counts, 1),
                        "LOCATION_TYPE": (self.location_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Explore AREA_COUNT different areas in REGION",
                    data={
                        "AREA_COUNT": (self.area_counts, 1),
                        "REGION": (self.regions, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Find and interact with INTERACTION_COUNT ENVIRONMENTAL_FEATURE",
                    data={
                        "INTERACTION_COUNT": (self.interaction_counts, 1),
                        "ENVIRONMENTAL_FEATURE": (self.environmental_features, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Discover WAYPOINT_COUNT waypoints across different regions",
                    data={"WAYPOINT_COUNT": (self.waypoint_counts, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Find TREASURE_COUNT hidden TREASURE_TYPE treasures",
                    data={
                        "TREASURE_COUNT": (self.treasure_counts, 1),
                        "TREASURE_TYPE": (self.treasure_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Combat Challenges
        if self.include_combat_challenges:
            combat_templates = []
            
            if self.difficulty_preference in ["All", "Hard"]:
                combat_templates.extend([
                    GameObjectiveTemplate(
                        label="Defeat BOSS without any party members dying",
                        data={"BOSS": (self.challenging_bosses, 1)},
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Complete ENCOUNTER_COUNT encounters using only TACTICAL_APPROACH",
                        data={
                            "ENCOUNTER_COUNT": (self.encounter_counts, 1),
                            "TACTICAL_APPROACH": (self.tactical_approaches, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=1,
                    ),
                ])
            
            combat_templates.extend([
                GameObjectiveTemplate(
                    label="Defeat ENEMY_COUNT different ENEMY_TYPE enemies",
                    data={
                        "ENEMY_COUNT": (self.enemy_counts, 1),
                        "ENEMY_TYPE": (self.enemy_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Win SPELL_COUNT battles using primarily SPELL_SCHOOL spells",
                    data={
                        "SPELL_COUNT": (self.spell_counts, 1),
                        "SPELL_SCHOOL": (self.spell_schools, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Successfully use ENVIRONMENTAL_COUNT environmental COMBAT_INTERACTION in combat",
                    data={
                        "ENVIRONMENTAL_COUNT": (self.environmental_counts, 1),
                        "COMBAT_INTERACTION": (self.combat_interactions, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])
            
            game_objective_templates.extend(combat_templates)

        # Social Encounters
        if self.include_social_encounters:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Successfully pass SKILL_CHECK_COUNT SKILL_TYPE skill checks",
                    data={
                        "SKILL_CHECK_COUNT": (self.skill_check_counts, 1),
                        "SKILL_TYPE": (self.skill_types, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Resolve DIALOGUE_COUNT conflicts through DIALOGUE_APPROACH",
                    data={
                        "DIALOGUE_COUNT": (self.dialogue_counts, 1),
                        "DIALOGUE_APPROACH": (self.dialogue_approaches, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Convince NPC_COUNT NPCs to SOCIAL_OUTCOME",
                    data={
                        "NPC_COUNT": (self.npc_counts, 1),
                        "SOCIAL_OUTCOME": (self.social_outcomes, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete INTERACTION_COUNT social interactions using SOCIAL_STAT",
                    data={
                        "INTERACTION_COUNT": (self.social_interaction_counts, 1),
                        "SOCIAL_STAT": (self.social_stats, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Collectibles
        if self.include_collectibles:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Collect ITEM_COUNT different ITEM_CATEGORY items",
                    data={
                        "ITEM_COUNT": (self.item_counts, 1),
                        "ITEM_CATEGORY": (self.item_categories, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Find BOOK_COUNT BOOK_TYPE books and read them",
                    data={
                        "BOOK_COUNT": (self.book_counts, 1),
                        "BOOK_TYPE": (self.book_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Discover ARTIFACT_COUNT magical ARTIFACT_TYPE artifacts",
                    data={
                        "ARTIFACT_COUNT": (self.artifact_counts, 1),
                        "ARTIFACT_TYPE": (self.artifact_types, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Acquire GOLD_AMOUNT gold through ACQUISITION_METHOD",
                    data={
                        "GOLD_AMOUNT": (self.gold_amounts, 1),
                        "ACQUISITION_METHOD": (self.acquisition_methods, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        # Achievement Hunting
        if self.include_achievement_hunting:
            game_objective_templates.extend([
                GameObjectiveTemplate(
                    label="Unlock ACHIEVEMENT_COUNT ACHIEVEMENT_CATEGORY achievements",
                    data={
                        "ACHIEVEMENT_COUNT": (self.achievement_counts, 1),
                        "ACHIEVEMENT_CATEGORY": (self.achievement_categories, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete SPEEDRUN_CATEGORY speedrun challenge",
                    data={"SPEEDRUN_CATEGORY": (self.speedrun_categories, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Achieve COMPLETION_GOAL in a single playthrough",
                    data={"COMPLETION_GOAL": (self.completion_goals, 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        return game_objective_templates

    # Property checks
    @property
    def include_character_builds(self) -> bool:
        return self.archipelago_options.bg3_include_character_builds.value

    @property
    def include_story_progression(self) -> bool:
        return self.archipelago_options.bg3_include_story_progression.value

    @property
    def include_companion_quests(self) -> bool:
        return self.archipelago_options.bg3_include_companion_quests.value

    @property
    def include_exploration(self) -> bool:
        return self.archipelago_options.bg3_include_exploration.value

    @property
    def include_combat_challenges(self) -> bool:
        return self.archipelago_options.bg3_include_combat_challenges.value

    @property
    def include_social_encounters(self) -> bool:
        return self.archipelago_options.bg3_include_social_encounters.value

    @property
    def include_collectibles(self) -> bool:
        return self.archipelago_options.bg3_include_collectibles.value

    @property
    def include_achievement_hunting(self) -> bool:
        return self.archipelago_options.bg3_include_achievement_hunting.value

    @property
    def difficulty_preference(self) -> str:
        return self.archipelago_options.bg3_difficulty_preference.value

    @property
    def playstyle_focus(self) -> str:
        return self.archipelago_options.bg3_playstyle_focus.value

    # Data lists
    @staticmethod
    def character_classes() -> List[str]:
        return [
            "Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk",
            "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"
        ]

    @staticmethod
    def multiclass_builds() -> List[str]:
        return [
            "Paladin/Warlock", "Fighter/Rogue", "Barbarian/Fighter", "Sorcerer/Warlock",
            "Bard/Warlock", "Ranger/Rogue", "Cleric/Fighter", "Druid/Barbarian",
            "Monk/Rogue", "Wizard/Fighter", "Paladin/Bard", "Sorcerer/Bard",
            "Warlock/Fighter", "Ranger/Fighter", "Cleric/Bard", "Druid/Monk"
        ]

    @staticmethod
    def subclass_types() -> List[str]:
        return [
            "Barbarian subclasses", "Bard subclasses", "Cleric subclasses", "Druid subclasses",
            "Fighter subclasses", "Monk subclasses", "Paladin subclasses", "Ranger subclasses",
            "Rogue subclasses", "Sorcerer subclasses", "Warlock subclasses", "Wizard subclasses"
        ]

    @staticmethod
    def ability_focuses() -> List[str]:
        return [
            "Strength-based melee", "Dexterity-based finesse", "Intelligence-based casting",
            "Wisdom-based support", "Charisma-based social", "Constitution tank build",
            "High mobility", "Area control", "Burst damage", "Sustained damage",
            "Crowd control", "Battlefield manipulation", "Healing support", "Buff/debuff specialist"
        ]

    @staticmethod
    def feat_types() -> List[str]:
        return [
            "Combat feats", "Spellcasting feats", "Social feats", "Utility feats",
            "Racial feats", "Movement feats", "Defensive feats", "Offensive feats"
        ]

    @staticmethod
    def companions() -> List[str]:
        return [
            "Shadowheart", "Astarion", "Gale", "Lae'zel", "Wyll", "Karlach",
            "Halsin", "Minthara", "Minsc", "Jaheira"
        ]

    @staticmethod
    def companion_targets() -> List[str]:
        return [
            "Shadowheart", "Astarion", "Gale", "Lae'zel", "Wyll", "Karlach",
            "Halsin", "Minthara", "Minsc", "Jaheira", "any companion", "multiple companions"
        ]

    @staticmethod
    def relationship_levels() -> List[str]:
        return [
            "High approval", "Romance", "Medium approval", "Low approval",
            "Disapproval", "Hostile", "Devoted", "Close friendship"
        ]

    @staticmethod
    def personal_conflicts() -> List[str]:
        return [
            "Past trauma", "Family issues", "Moral dilemmas", "Personal growth",
            "Identity crises", "Redemption arcs", "Power struggles", "Love conflicts"
        ]

    @staticmethod
    def major_story_choices() -> List[str]:
        return [
            "Saving the Grove", "Dealing with the Absolute", "Handling the tadpole",
            "Confronting the Dead Three", "Alliance decisions", "Sacrifice choices",
            "Power vs morality", "Companion fate decisions"
        ]

    @staticmethod
    def ending_types() -> List[str]:
        return [
            "Hero ending", "Anti-hero ending", "Villain ending", "Sacrifice ending",
            "Power ending", "Redemption ending", "Tragic ending", "Mysterious ending"
        ]

    @staticmethod
    def quest_types() -> List[str]:
        return [
            "Main story", "Companion personal", "Side quests", "Faction quests",
            "Exploration quests", "Collection quests", "Combat challenges", "Social quests"
        ]

    @staticmethod
    def lore_categories() -> List[str]:
        return [
            "Forgotten Realms history", "Baldur's Gate history", "Deity lore", "Planar knowledge",
            "Magical theory", "Political intrigue", "Ancient civilizations", "Monster ecology",
            "Artifact history", "Spell origins", "Character backgrounds", "World events"
        ]

    @staticmethod
    def story_impacts() -> List[str]:
        return [
            "Companion relationships", "World state", "Available endings", "Quest outcomes",
            "NPC fates", "Settlement outcomes", "Political changes", "Power balances"
        ]

    @staticmethod
    def regions() -> List[str]:
        return [
            "Wilderness", "Underdark", "Act 2 Shadow-Cursed Lands", "Act 3 Baldur's Gate",
            "Githyanki Creche", "Goblin Camp", "Druid Grove", "Mountain Pass"
        ]

    @staticmethod
    def location_types() -> List[str]:
        return [
            "Dungeons", "Ruins", "Caves", "Temples", "Towers", "Underground areas",
            "Hidden chambers", "Secret passages", "Abandoned settlements", "Magical locations"
        ]

    @staticmethod
    def environmental_features() -> List[str]:
        return [
            "Ancient runes", "Magical portals", "Shrines", "Statues", "Murals",
            "Puzzles", "Traps", "Hidden switches", "Magical barriers", "Ritual circles"
        ]

    @staticmethod
    def treasure_types() -> List[str]:
        return [
            "Magical weapons", "Armor sets", "Spell scrolls", "Potions", "Gems",
            "Gold hoards", "Rare materials", "Artifacts", "Books", "Equipment"
        ]

    @staticmethod
    def enemy_types() -> List[str]:
        return [
            "Undead", "Fiends", "Aberrations", "Constructs", "Dragons", "Giants",
            "Humanoids", "Beasts", "Fey", "Elementals", "Celestials", "Monstrosities"
        ]

    @staticmethod
    def challenging_bosses() -> List[str]:
        return [
            "Ketheric Thorm", "Orin the Red", "Lord Enver Gortash", "The Netherbrain",
            "Cazador Szarr", "Sarevok", "Viconia DeVir", "The Elder Brain"
        ]

    @staticmethod
    def spell_schools() -> List[str]:
        return [
            "Evocation", "Abjuration", "Enchantment", "Illusion", "Divination",
            "Necromancy", "Transmutation", "Conjuration"
        ]

    @staticmethod
    def tactical_approaches() -> List[str]:
        return [
            "Stealth and ambush", "Frontal assault", "Crowd control focus", "Ranged combat",
            "Environmental exploitation", "Spell combinations", "Summon armies", "Hit and run"
        ]

    @staticmethod
    def combat_interactions() -> List[str]:
        return [
            "Explosive barrels", "High ground advantages", "Elemental surfaces", "Pushes and shoves",
            "Environmental hazards", "Destructible cover", "Water/fire interactions", "Magical phenomena"
        ]

    @staticmethod
    def skill_types() -> List[str]:
        return [
            "Persuasion", "Deception", "Intimidation", "Investigation", "Insight",
            "Perception", "Stealth", "Sleight of Hand", "Athletics", "Acrobatics"
        ]

    @staticmethod
    def dialogue_approaches() -> List[str]:
        return [
            "Diplomatic negotiation", "Intimidation tactics", "Deceptive manipulation",
            "Honest persuasion", "Logical reasoning", "Emotional appeals", "Bribery", "Threats"
        ]

    @staticmethod
    def social_outcomes() -> List[str]:
        return [
            "Join your cause", "Provide information", "Offer assistance", "Change allegiances",
            "Reveal secrets", "Grant access", "Reduce hostility", "Form alliances"
        ]

    @staticmethod
    def social_stats() -> List[str]:
        return [
            "High Charisma", "High Intelligence", "High Wisdom", "Class features",
            "Racial abilities", "Background bonuses", "Spell assistance", "Item bonuses"
        ]

    @staticmethod
    def item_categories() -> List[str]:
        return [
            "Magical weapons", "Armor pieces", "Accessories", "Consumables", "Spell components",
            "Quest items", "Books and scrolls", "Tools and kits", "Art objects", "Trade goods"
        ]

    @staticmethod
    def book_types() -> List[str]:
        return [
            "Lore books", "Spell tomes", "History books", "Diaries and journals", "Religious texts",
            "Technical manuals", "Poetry collections", "Fiction novels", "Maps and charts", "Research notes"
        ]

    @staticmethod
    def artifact_types() -> List[str]:
        return [
            "Legendary weapons", "Artifact armor", "Powerful accessories", "Magical tools",
            "Spell focus items", "Planar artifacts", "Divine relics", "Ancient technology"
        ]

    @staticmethod
    def acquisition_methods() -> List[str]:
        return [
            "Merchant trading", "Quest rewards", "Looting enemies", "Treasure hunting",
            "Pickpocketing", "Gambling", "Performance", "Crafting and selling"
        ]

    @staticmethod
    def achievement_categories() -> List[str]:
        return [
            "Combat achievements", "Story achievements", "Exploration achievements", "Social achievements",
            "Character achievements", "Collection achievements", "Challenge achievements", "Hidden achievements"
        ]

    @staticmethod
    def speedrun_categories() -> List[str]:
        return [
            "Any% completion", "100% completion", "Act 1 speedrun", "Single class speedrun",
            "No death run", "Pacifist run", "Evil playthrough", "Good playthrough"
        ]

    @staticmethod
    def completion_goals() -> List[str]:
        return [
            "All achievements", "All companions recruited", "All areas explored", "All books read",
            "All legendary items found", "All endings seen", "All romance options", "Perfect approval ratings"
        ]

    @staticmethod
    def damage_types() -> List[str]:
        return [
            "Fire", "Cold", "Lightning", "Acid", "Poison", "Necrotic", "Radiant",
            "Psychic", "Thunder", "Force", "Piercing", "Slashing", "Bludgeoning"
        ]

    @staticmethod
    def party_compositions() -> List[str]:
        return [
            "All spellcasters", "All martial", "Balanced party", "Support focused",
            "Damage focused", "Tank heavy", "Stealth specialists", "Social specialists"
        ]

    @staticmethod
    def forbidden_abilities() -> List[str]:
        return [
            "Long rest", "Short rest", "Healing spells", "Resurrection", "Fast travel",
            "Save scumming", "Respec", "Consumables", "Summons", "Environmental kills"
        ]

    @staticmethod
    def difficulty_settings() -> List[str]:
        return [
            "Explorer", "Balanced", "Tactician", "Honour Mode"
        ]

    @staticmethod
    def roleplay_restrictions() -> List[str]:
        return [
            "Pacifist approach", "Evil only choices", "Good only choices", "Chaotic behavior",
            "Lawful behavior", "Never lie", "Always intimidate", "Never use magic"
        ]

    @staticmethod
    def cantrip_types() -> List[str]:
        return [
            "Damage cantrips", "Utility cantrips", "Support cantrips", "Control cantrips"
        ]

    @staticmethod
    def act_numbers() -> List[str]:
        return ["1", "2", "3"]

    @staticmethod
    def act_scopes() -> List[str]:
        return ["Act 1", "Act 2", "Act 3", "entire game"]

    # Ranges
    @staticmethod
    def level_ranges() -> range:
        return range(5, 13, 2)

    @staticmethod
    def subclass_counts() -> range:
        return range(2, 6, 2)

    @staticmethod
    def feat_counts() -> range:
        return range(2, 8, 2)

    @staticmethod
    def quest_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def lore_counts() -> range:
        return range(10, 40, 10)

    @staticmethod
    def choice_counts() -> range:
        return range(5, 15, 5)

    @staticmethod
    def romance_counts() -> range:
        return range(2, 5)

    @staticmethod
    def companion_counts() -> range:
        return range(2, 6)

    @staticmethod
    def party_sizes() -> range:
        return range(3, 5)

    @staticmethod
    def secret_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def area_counts() -> range:
        return range(5, 15, 5)

    @staticmethod
    def interaction_counts() -> range:
        return range(5, 20, 5)

    @staticmethod
    def waypoint_counts() -> range:
        return range(10, 30, 10)

    @staticmethod
    def treasure_counts() -> range:
        return range(10, 30, 10)

    @staticmethod
    def enemy_counts() -> range:
        return range(20, 60, 20)

    @staticmethod
    def spell_counts() -> range:
        return range(5, 15, 5)

    @staticmethod
    def environmental_counts() -> range:
        return range(5, 15, 5)

    @staticmethod
    def encounter_counts() -> range:
        return range(10, 30, 10)

    @staticmethod
    def skill_check_counts() -> range:
        return range(20, 60, 20)

    @staticmethod
    def dialogue_counts() -> range:
        return range(10, 30, 10)

    @staticmethod
    def npc_counts() -> range:
        return range(5, 15, 5)

    @staticmethod
    def social_interaction_counts() -> range:
        return range(15, 45, 15)

    @staticmethod
    def item_counts() -> range:
        return range(20, 80, 20)

    @staticmethod
    def book_counts() -> range:
        return range(10, 30, 10)

    @staticmethod
    def artifact_counts() -> range:
        return range(3, 10, 2)

    @staticmethod
    def gold_amounts() -> range:
        return range(10000, 50000, 10000)

    @staticmethod
    def achievement_counts() -> range:
        return range(5, 20, 5)


# Archipelago Options
class BG3IncludeCharacterBuilds(Toggle):
    """Include character build experimentation and multiclassing objectives."""
    display_name = "Include Character Builds"

class BG3IncludeStoryProgression(Toggle):
    """Include main story and narrative choice objectives."""
    display_name = "Include Story Progression"

class BG3IncludeCompanionQuests(Toggle):
    """Include companion relationship and personal quest objectives."""
    display_name = "Include Companion Quests"

class BG3IncludeExploration(Toggle):
    """Include world exploration and discovery objectives."""
    display_name = "Include Exploration"

class BG3IncludeCombatChallenges(Toggle):
    """Include tactical combat and boss fight objectives."""
    display_name = "Include Combat Challenges"

class BG3IncludeSocialEncounters(Toggle):
    """Include dialogue, persuasion, and social interaction objectives."""
    display_name = "Include Social Encounters"

class BG3IncludeCollectibles(Toggle):
    """Include item collection and treasure hunting objectives."""
    display_name = "Include Collectibles"

class BG3IncludeAchievementHunting(Toggle):
    """Include achievement and completion challenge objectives."""
    display_name = "Include Achievement Hunting"

class BG3DifficultyPreference(Choice):
    """Prefer certain difficulty levels for objectives."""
    display_name = "Difficulty Preference"
    option_all = "All"
    option_easy = "Easy"
    option_hard = "Hard"
    default = option_all

class BG3PlaystyleFocus(Choice):
    """Focus objectives on specific playstyles."""
    display_name = "Playstyle Focus"
    option_all = "All"
    option_combat = "Combat"
    option_story = "Story"
    option_exploration = "Exploration"
    default = option_all
