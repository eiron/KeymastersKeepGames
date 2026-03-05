# Keymaster's Keep Games
Game implementations for Keymaster's Keep maintained by eiron

## 📋 Table of Contents
- [Universal Game Tester](#universal-game-tester-)
- [Include Option Standards](#include-option-standards)
- [Integration Guides](#integration-guides)
- [Meta-Game Implementations](#meta-game-implementations)
- [Individual Game Implementations](#individual-game-implementations)
- [Work in Progress](#work-in-progress)
- [Recent Updates](#recent-updates)

---

## Universal Game Tester 🔧

The **Universal Game Tester** (located in `UniversalGameTester/`) is a comprehensive testing and analysis tool that works with **ANY** Keymaster's Keep game implementation.

### Key Features

- **🔍 Automatic Discovery**: Scans directory for game implementation files
- **🎯 Universal Compatibility**: Works with any game module and custom option types
- **⚖️ Authentic Simulation**: Reproduces Keep's weighted objective selection system
- **📊 Comprehensive Analysis**: Provides detailed metrics on objectives, weights, features
- **🎮 Interactive Testing**: Menu-driven interface for testing individual games or full suites

### Usage

```bash
# Test all discovered game implementations
cd UniversalGameTester
python universal_game_tester.py

# Test a specific game
python universal_game_tester.py stardew_valley_game.py

# Test with shortened filename
python universal_game_tester.py hades
```

---

## Include Option Standards

All game implementations follow a standardized approach for include Toggle options:

- **Basic Content**: Fundamental options default to `True` for comprehensive objective generation
- **Specialized/Harder Content**: Speedruns, difficulty challenges default to `False`
- **Cursed/Tedious Modules**: Games like "Cursed Red Dead Redemption 2" default to `True` (players deliberately opt-in)

---

## Integration Guides

### Playnite Library Setup

Generate objectives from your Playnite games database.

**Requirements:**
1. Export database using [Json Library Import Export add-on](https://playnite.link/addons.html#JsonLibraryImportExport_888ab97e-ea1b-40e5-a2da-ef917aee0603)
2. Set path in KMK YAML: `playnite_library_json_path: C:/path/to/games.json`

### Steam Achievements Setup

Generate objectives from your Steam library via API.

**Requirements:**
1. Get API key: [https://steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey)
2. Set environment variable `STEAM_API_KEY`
3. Configure Steam ID in YAML options

### Archipelocal Setup

Real-world location-based exploration via Geoapify API.

**Requirements:**
See [ARCHIPELOCAL_SETUP.md](ARCHIPELOCAL_SETUP.md) for detailed instructions.

---

## Meta-Game Implementations

### Adventure/Experience Challenges
**File**: `adventure_experience.py`

Transform real-world adventure backlog into objectives.

**Categories**: Local Exploration, Cultural Experiences, Outdoor Activities, Culinary Adventures

**Sample**: `"VISIT Downtown District"`, `"ATTEMPT Rock Climbing"`, `"TRY International Restaurant"`

---

### Archipelago Multiworld Randomizer with Multiplayer
**File**: `archipelago_multiworld_randomizer_game_with_multiplayer.py`

Create objectives for participating in Archipelago multiworld sessions.

**Categories**: Multiworld Participation, Item Progression, Helper Activities, Community Engagement

**Sample**: `"Complete your sphere 1 progression items"`, `"Send 10 useful items to other players"`

---

### Archipelocal
**File**: `archipelocal_game.py`

Real-world exploration using Geoapify Places API. **Powered by [Geoapify](https://www.geoapify.com/)**

**Categories**: Food & Drink, Leisure & Tourism, Entertainment & Culture, Natural & Man-Made Sights, Shopping, Services

**Sample**: `"Visit Starbucks @ 40.78509, -73.96829 – 0.42 km • Cafe"`, `"Visit your 3rd-closest Park near your home"`

**Features**: Live place suggestions, lazy loading, flexible strategies, customizable distances, privacy-friendly

---

### Archipelagourmet
**File**: `archipelagourmet_game.py`

Recipes, restaurants, and random ingredient cooking challenges.

**Categories**: Recipes, Restaurants, Random Ingredient Challenges

**Sample**: `"Make [Recipe Name]"`, `"Make a meal using each of the following ingredients: {3-5 random ingredients}"`

**Features**: Dietary filtering, ingredient blacklist, customizable ingredient pool (1-10)

---

### Board Game Collection
**File**: `board_game_collection.py`

Physical board game exploration and mastery.

**Categories**: Strategy Games, Party Games, Solo Gaming, Learning New Games, Game Night Hosting

**Sample**: `"Learn and play 3 new games from your collection"`, `"Host a game night with 4+ different games"`

---

### Chapter Quest
**File**: `chapter_quest_game.py` | **Docs**: [CHAPTER_QUEST.md](CHAPTER_QUEST.md)

Transform reading list into gaming objectives with chapter-specific goals.

**Categories**: Individual Chapters, Book Completion, Genre Challenges, Author Challenges

**Sample**: `"[Fantasy Fiction] The Hobbit by J.R.R. Tolkien -> Read chapter 7"`, `"Genre Challenge: Read 2 chapters from a Science Fiction book"`

**Features**: Book configuration, meta-challenges, difficulty scaling, smart generation

---

### Chart Attack
**File**: `chart_attack_game.py`

Follow ranked charts (music, books, films, games, etc.) and pick specific positions.

**Sample**: `"Follow Billboard Hot 100 #7"`, `"Read Goodreads Fantasy #42"`

**Features**: Custom charts/verbs, position ranges, weighted selection, chart weighting

---

### Christmas/Holiday Challenges
**File**: `christmas_holiday_challenges.py`

Holiday activities from your seasonal backlog.

**Categories**: Decorations, Gifts, Baking, Traditions

**Sample**: `"SET UP Christmas Tree"`, `"MAKE Handmade Gift"`, `"CREATE Gingerbread House"`

---

### Creative Challenges
**File**: `creative_challenges.py`

Art projects, writing, photography, crafts from your creative backlog.

**Categories**: Art Projects, Writing, Photography, Crafts

**Sample**: `"CREATE Watercolor Painting"`, `"WRITE Short Story"`, `"CAPTURE Portrait Session"`

---

### Custom Categories
**File**: `custom_categories_game.py` | **Docs**: [CUSTOM_CATEGORIES.md](CUSTOM_CATEGORIES.md)

Fully customizable categories with weighted sub-tasks for personal goals.

**Sample**: `"[Fitness & Health] Complete a 30-minute workout"`, `"[Learning & Skills] Complete 3 tasks"`

**Features**: Category weight (0-100+), task weight (0-100+), task properties (difficult, time_consuming), 8 default categories

---

### Keymaster's Keep
**File**: `keymasters_keep.py`

Ultimate meta module for generating Keymaster's Keep challenges to play within Keep!

**Game Modes**: Keymaster's Challenge, Magic Key Heist

**Sample**: `"Complete a Keymaster's Challenge including the games: Celeste, Hollow Knight, and Slay the Spire"`

**Features**: Customizable game pool (120+ games default), challenge type selection, game count range (1-10)

---

### Music Listening
**File**: `music_listening.py`

Albums, artists, and playlists from your music backlog.

**Categories**: Albums, Artists, Playlists

**Sample**: `"LISTEN TO Album Title"`, `"EXPLORE Artist Name"`, `"COMPLETE Playlist Name"`

---

### Physical/Health Challenges
**File**: `physical_health_challenges.py`

Exercise, wellness, nutrition, movement from your fitness backlog.

**Categories**: Exercise, Wellness, Nutrition, Movement

**Sample**: `"COMPLETE Push-up Challenge"`, `"MAINTAIN Sleep Schedule"`, `"TRY Healthy Recipe"`

---

### Playnite Library
**File**: `playnite_library.py`

Generate objectives from your Playnite games database.

**Features**: All Playnite metadata support (tags, genres, features, platforms, categories, sources, series, scores, playtime), multiple ordering options

**Requirements**: See [Integration Guides](#integration-guides)

---

### Real-World Scavenger Hunt
**File**: `real_world_scavenger_hunt_game.py`

Comprehensive real-world exploration encouraging outdoor discovery and community engagement.

**Categories**: Photography, Location Hunting, Object Collection, Interaction, Nature, Cultural Discovery, Seasonal Activities, Community Engagement

**Sample**: `"Take a photo of A street musician"`, `"Find and visit A hidden garden"`, `"Collect 10 different Interesting rocks"`

**Features**: 500+ objectives, difficulty levels, travel scope options, constraints (transportation, time, weather)

---

### Really Boring Challenges
**File**: `really_boring_challenges_game.py`

Deliberately mundane everyday routine activities gamified.

**Categories**: Household Maintenance, Personal Organization, Digital Housekeeping, Routine Optimization, Administrative Tasks

**Sample**: `"Organize 50 digital files"`, `"Clean one room thoroughly"`, `"Update 3 different passwords"`

---

### Social/Connections Challenges
**File**: `social_connections.py`

Friend meetups, family activities, community events, networking from your social backlog.

**Categories**: Friend Meetups, Family Activities, Community Events, Networking

**Sample**: `"ARRANGE Coffee Meetup with Best Friend"`, `"VISIT Family Dinner with Family Member"`

**Features**: Customizable people lists (friends, family, colleagues)

---

### Steam Achievements
**File**: `steam_achievements_game.py`

Generate objectives from your Steam library and achievement progress via API.

**Categories**: Game Completion, Progress Goals, Mastery

**Sample**: `"Beat Elden Ring"`, `"Unlock at least 25% of the achievements in Hollow Knight"`

**Features**: Automatic library fetching, playtime filtering, smart filtering, exclusions, percentage ranges

**Requirements**: See [Integration Guides](#integration-guides)

---

### Watchlist
**File**: `watchlist.py`

Films and TV shows from your watchlist.

**Categories**: Films, TV Shows

**Sample**: `"WATCH Film Title"`, `"BINGE TV Series Title"`

---

## Individual Game Implementations

Alphabetically organized game-specific implementations. Games marked **[Details Needed]** have implementations but incomplete documentation.

---

### Alina of the Arena
**File**: `alina_of_the_arena_game.py`

[Details Needed]

---

### American Truck Simulator
**File**: `american_truck_simulator_game.py`

Trucking simulation covering deliveries, exploration, business management across USA.

**Categories**: Interstate Delivery, State Exploration, Truck Ownership, Long Haul, Heavy Haul, Business Objectives, DLC Content

**Sample**: `"Transport Electronics from Los Angeles to Phoenix"`, `"Complete deliveries to 3 different cities in Nevada"`

**Features**: Comprehensive DLC support (California to Missouri), specialized hauling, business management, realistic constraints

---

### Animal Crossing: New Horizons
**File**: `animal_crossing_new_horizons_game.py`

Island life simulation focusing on development, social interaction, decoration, seasonal activities.

**Categories**: Island Development, Social Interaction, Decoration & Design, Collection & Catalog, Seasonal Events

**Sample**: `"Develop 5 different Residential Areas"`, `"Achieve Best Friends relationship with 3 villagers"`

---

### Apex Legends
**File**: `apex_legends_game.py`

[Details Needed]

---

### Astronarch
**File**: `astronarch_game.py`

[Details Needed]

---

### Atomicrops
**File**: `atomicrops_game.py`

[Details Needed]

---

### Baba Is You
**File**: `baba_is_you_game.py`

[Details Needed]

---

### Backpack Hero
**File**: `backpack_hero_game.py`

[Details Needed]

---

### Baldur's Gate 3
**File**: `baldurs_gate_3_game.py`

Deep RPG covering character builds, story choices, companion relationships, tactical combat.

**Categories**: Character Builds, Story Progression, Companion Quests, Exploration, Combat Challenges, Social Encounters

**Sample**: `"Complete Act 1 with a Paladin/Warlock multiclass build"`, `"Achieve Romance relationship with Shadowheart"`

---

### Beyond the Long Night
**File**: `beyond_the_long_night_game.py`

[Details Needed]

---

### Bloodstained: Ritual of the Night
**File**: `bloodstained_ritual_of_the_night_game.py`

Comprehensive Metroidvania covering shard collection, exploration, boss battles, alchemy.

**Categories**: Shard Collection, Exploration, Boss Challenges, Alchemy & Crafting, Equipment Mastery, Speedrun Challenges

**Sample**: `"Collect 20 Conjure shards"`, `"Reach 90% map completion"`, `"Defeat Bloodless without using healing items"`

---

### Bloons TD 6
**File**: `bloons_td_6_game.py`

[Details Needed]

---

### BPM: BULLETS PER MINUTE
**File**: `bpm_bullets_per_minute_game.py`

[Details Needed]

---

### Brotato
**File**: `brotato_game.py`

Arena wave-based roguelite focused on weapon builds, character diversity, scaling economy.

**Categories**: Character Unlocks, Weapon Synergy Runs, Wave Survival, Boss & Elite Clears, Economic Scaling, Danger Levels

**Sample**: `"Clear Danger Level 5 with Ghost character"`, `"Reach 200% attack speed before wave 15"`

**Features**: Build diversity, difficulty scaling, resource economy, character progression, optional constraints

---

### Brutal Orchestra
**File**: `brutal_orchestra_game.py`

[Details Needed]

---

### Caves of Qud
**File**: `caves_of_qud_game.py`

Science-fantasy roguelike capturing mutation-driven exploration, faction dynamics, emergent survival.

**Categories**: Mutation Acquisition, Exploration & Biomes, Faction Reputation, Artifact Identification, Survival Milestones, Legend Hunts

**Sample**: `"Acquire 4 new mutations without visiting a Grit Gate vendor"`, `"Reach reputation Trusted with the Mechanimists"`

**Features**: Mutation depth, faction systems, biome exploration, artifact mastery, survival challenges, legendary hunts

---

### Chess.com
**File**: `chess_com_game.py`

Competitive chess objectives from live, rapid, blitz, bullet, puzzle, thematic training activities.

**Categories**: Rating Milestones, Time Control Diversity, Opening Exploration, Puzzle Streaks, Accuracy Goals, Win Condition Variety

**Sample**: `"Achieve 5-day puzzle streak"`, `"Reach 1450 Blitz rating"`, `"Play 10 rapid games using the French Defense as Black"`

**Features**: Multi time control targets, opening coverage, puzzle/tactics, accuracy metrics, improvement tracking

---

### Circadian Dice
**File**: `circadian_dice_game.py`

Dice-building roguelike emphasizing scenario strategy, face crafting, relic combinations.

**Categories**: Scenario Clears, Class Mastery, Relic Unlocks, High Score Targets, Status/Combo Challenges, Perfect/Efficient Turns

**Sample**: `"Clear Forest scenario with Alchemist at 3+ relics"`, `"Reach 25,000 score in Temple run"`

**Features**: Scenario variety, class progression, dice engineering, scoring milestones, efficiency challenges

---

### Cook, Serve, Delicious! 2!!
**File**: `cook_serve_delicious_2_game.py`

[Details Needed]

---

### Crypt of the NecroDancer
**File**: `crypt_of_the_necrodancer_game.py`

Rhythm-based roguelike spanning zone clears, character completion, boss mastery, DLC expansions.

**Categories**: Zone Progression, Character Victories, Boss Defeats, Rhythm/Cadence Challenges, Item/Shop Interaction, Mode Variants, DLC Content

**Sample**: `"Clear Zone 4 with Cadence without missing a beat"`, `"Defeat Dead Ringer using only shovel damage (Monk)"`

**Features**: DLC toggles (Amplified, Synchrony, Hatsune Miku, Shovel Knight), character depth, rhythm mastery, boss variants

---

### Cult of the Lamb
**File**: `cult_of_the_lamb_game.py`

Unique cult management and action covering cult building, follower management, combat crusades.

**Categories**: Cult Management, Combat & Crusades, Follower Care, Base Building, Resource Collection, Ritual Performance

**Sample**: `"Recruit 15 new cult followers"`, `"Defeat Leshy in combat"`, `"Perform 5 different Blessing rituals"`

---

### Cuphead
**File**: `cuphead_game.py`

[Details Needed]

---

### Cursed Red Dead Redemption 2
**File**: `cursed_red_dead_redemption_2_game.py`

Deliberately chaotic and humorous take on Wild West epic with absurd objectives.

**Categories**: Absurd Combat, Ridiculous Exploration, Chaotic Social Interactions, Silly Customization, Nonsense Activities

**Sample**: `"Kill 50 enemies using only throwing knives while wearing a fancy hat"`, `"Ride your horse backwards for 10 minutes straight"`

---

### Danganronpa Decadence
**File**: `danganronpa_decadence_game.py`

Visual novel murder mystery collection. Supports all four games in Decadence collection.

**Supported Games**: Trigger Happy Havoc (+ School Mode), Goodbye Despair (+ Island Mode), V3: Killing Harmony (+ UTDP), Ultimate Summer Camp

**Categories**: Story mode (investigations, trials, free time), bonus modes, extra minigames, collectibles

**Sample**: `"Achieve S rank in the chapter 3 class trial"`, `"Max out friendship with Kyoko Kirigiri"`

---

### Date Everything
**File**: `date_everything_game.py`

Whimsical dating simulation romancing household objects and abstract concepts with 100+ voice-acted characters.

**Categories**: Structural Objects, Furniture & Decor, Kitchen Appliances, Bathroom Items, Laundry Items, Office & Bedroom, Miscellaneous, Special Concepts, DLC

**Sample**: `"Achieve LOVE with Rebel (Rubber Duck)"`, `"Get 5 structural elements to FRIENDS status"`

---

### Dead Cells
**File**: `dead_cells_game.py`

Challenging metroidvania focused on combat mastery, weapon experimentation, biome progression.

**Categories**: Combat Mastery, Weapon Experimentation, Biome Progression, Mutation Builds, Speed Running

**Sample**: `"Defeat 25 different Elite enemies"`, `"Complete a run using only Survival weapons"`, `"Reach 3BC difficulty level"`

---

### Dead Estate
**File**: `dead_estate_game.py`

[Details Needed]

---

### Death Road to Canada
**File**: `death_road_to_canada_game.py`

[Details Needed]

---

### Despot's Game
**File**: `despots_game.py`

[Details Needed]

---

### Dicey Dungeons
**File**: `dicey_dungeons_game.py`

[Details Needed]

---

### Dungreed
**File**: `dungreed_game.py`

[Details Needed]

---

### Euro Truck Simulator 2
**File**: `euro_truck_simulator_2_game.py`

Trucking simulation covering deliveries, exploration, business management across Europe.

**Categories**: Delivery Objectives, Country Exploration, Truck Ownership, Long Distance, Special Transport, Business Objectives, DLC Content

**Sample**: `"Deliver Medical Supplies from Berlin to Paris"`, `"Complete the challenging 1800km route from London to Rome"`

**Features**: Comprehensive DLC support (Going East! to Greece), specialized hauling, business management, skill challenges

---

### Forward: Escape the Fold
**File**: `forward_escape_the_fold_game.py`

[Details Needed]

---

### Hades
**File**: `hades_game.py`

Roguelike action covering escape attempts, weapon mastery, relationship building, Zagreus's journey.

**Categories**: Escape Attempts, Weapon Mastery, Relationship Building, Boon Collection, House Upgrades, Narrative Progress, Challenge Runs

**Sample**: `"Complete 5 successful escape attempts"`, `"Master the Stygian Blade weapon"`, `"Max out relationship with Megaera"`

---

### Harvestella
**File**: `harvestella_game.py`

Farming RPG bringing full breadth of farming, exploration, combat, relationships, story, crafting, seasonal systems.

**Categories**: Farming Objectives, Exploration & Adventure, Combat Challenges, Relationship System, Story Progression, Crafting & Cooking, Seasonal & Collection

**Sample**: `"Harvest 50 crops across all seasons"`, `"Defeat 10 unique monsters in Quietus dungeons"`, `"Complete Chapter 5"`

**Features**: Dynamic crop/farming, exploration/dungeons, combat/jobs, relationships, story progression, crafting, collections

---

### Inscryption
**File**: `inscryption_game.py`

[Details Needed]

---

### Into the Breach
**File**: `into_the_breach_game.py`

[Details Needed]

---

### Just Dance
**File**: `just_dance_game.py`

Comprehensive rhythm gaming covering entire Just Dance franchise 2014-2025.

**Game Coverage**: Just Dance 2014-2025, Just Dance Unlimited, Just Dance+, Regional Exclusives

**Categories**: Base Game Completion, Subscription Service Mastery, Regional Content Exploration, Score Achievement

**Sample**: `"Perfect 25 songs from Just Dance 2023 base tracklist"`, `"Complete 15 dances from Just Dance Unlimited"`

**Features**: Comprehensive song libraries, accurate track lists, regional exclusives, subscription services, granular customization

---

### Just King
**File**: `just_king_game.py`

[Details Needed]

---

### Minecraft
**File**: `minecraft_game.py`

Expansive sandbox covering building projects, exploration, resource gathering, redstone, farming, combat.

**Categories**: Building Projects, Exploration & Adventure, Resource Gathering, Redstone Engineering, Farming & Automation, Combat Challenges

**Sample**: `"Build a 50x50 Castle structure"`, `"Explore 10 different Ocean Monuments"`, `"Create an automated Crop farm"`

---

### Monster Roadtrip
**File**: `monster_roadtrip_game.py`

[Details Needed]

---

### Neophyte
**File**: `neophyte_game.py`

[Details Needed]

---

### One Step From Eden
**File**: `one_step_from_eden_game.py`

[Details Needed]

---

### Pawnbarian
**File**: `pawnbarian_game.py`

[Details Needed]

---

### Revita
**File**: `revita_game.py`

[Details Needed]

---

### Rocksmith 2014
**File**: `rocksmith_2014_game.py`

[Details Needed]

---

### Spelunky
**File**: `spelunky_game.py`

[Details Needed]

---

### Spelunky 2
**File**: `spelunky_2_game.py`

[Details Needed]

---

### Stardew Valley
**File**: `stardew_valley_game.py`

Comprehensive farming simulation covering all aspects of Pelican Town life.

**Categories**: Farm Management, Relationship Building, Exploration & Combat, Crafting & Collection, Seasonal Activities, Community Goals

**Sample**: `"Earn 50000g through Crop sales"`, `"Reach 8 hearts relationship level with Abigail"`, `"Complete 15 different Community Center bundles"`

---

### Super Dungeon Maker
**File**: `super_dungeon_maker_game.py`

[Details Needed]

---

### The Binding of Isaac: Rebirth
**File**: `the_binding_of_isaac_rebirth_game_plus_unlock_conditions.py`

Massive roguelike covering extensive content of Rebirth and DLCs (Afterbirth, Afterbirth+, Repentance).

**Categories**: Character Victories, Boss Defeats, Challenge Runs, Item Collection, Transformations, Specific Achievements, Modded Characters

**Sample**: `"Defeat The Lamb as The Lost"`, `"Complete Challenge #34 (Ultra Hard)"`

**Features**: Full DLC support (auto-adjusts), all 34 characters including Tainted, deep integration, hardcore constraints, **modded character support via OptionSet**

---

### The Binding of Isaac: Wrath of the Lamb
**File**: `the_binding_of_isaac_wrath_of_the_lamb_game.py`

Module for original Flash game covering base game, Wrath of the Lamb expansion, Eternal Edition.

**Categories**: Character Victories, Boss Defeats, Challenge Runs, Eternal Edition Challenges

**Sample**: `"Defeat Satan as Judas"`, `"Complete Challenge #6 (The Doctors Revenge!)"`, `"Defeat Mom in Hard Mode (Eternal Edition)"`

**Features**: Classic content, expansion toggles (WotL, Eternal Edition), Eternal challenges, character & boss tracking

---

### The Sims 4
**File**: `the_sims_4_game.py`

Comprehensive life simulation covering all aspects of Sim life across base game and expansions.

**Categories**: Skill Mastery, Career Progression, Relationship Building, Aspiration Completion, Creative Building, Emotional Challenges, Collection Goals, Life Events, Expansion Content

**Sample**: `"Master the Painting skill to level 10"`, `"Build a SOULMATE relationship with another Sim"`, `"Experience the MORTIFIED emotion"`

**Features**: Comprehensive coverage of skills, careers, aspirations, collections, emotions from base game + DLC, auto-adapts based on content

---

### The Void Rains Upon Her Heart
**File**: `void_rains_upon_her_heart_game.py`

[Details Needed]

---

### Wario Ware: Get It Together!
**File**: `wario_ware_get_it_together_game.py`

[Details Needed]

---

### Wikipedia Game
**File**: `wikipedia_game.py`

[Details Needed]

---

### Wipeout HD Fury
**File**: `wipeout_hd_fury_game.py`

[Details Needed]

---

## Work in Progress

Games currently under development in the `WIP/` directory.

---

### The Ranch of Rivershine
**Directory**: `WIP/The Ranch of Rivershine/`

Cozy horse ranch simulation — care for horses, train skills, compete in events, breed foals, farm crops, and explore Rivershine.

**Categories**: Horse Training, Horse Care, Competitions, Breeding, Exploration, Farming, Wild Horses, Social, Crafting, Riding Arena, Ranch Upgrades

---

## Recent Updates

**March 2026:**
- README cleanup: removed deployment-only entries not present in this repo, added 5 missing game entries (Dungreed, Forward: Escape the Fold, Into the Breach, Rocksmith 2014, Spelunky 2)
- Added file reference for Cook, Serve, Delicious! 2!!
- Removed broken file references (Against the Storm, Awaria — files not in this repo)
- Added Work in Progress section (The Ranch of Rivershine)

**January 2026:**
- README reorganized with table of contents, alphabetized game lists, clearer sections
- All game files mapped to implementations for easier navigation

**November 2025:**

**New Modules:**
- **Brotato**: Arena roguelite with character unlocks, weapon synergy, danger levels
- **Circadian Dice**: Dice-building roguelike with scenario clears, class mastery, relic unlocks
- **Crypt of the NecroDancer**: Rhythm roguelike with zone progression, DLC content (Amplified, Synchrony, Hatsune Miku, Shovel Knight)
- **Chess.com Integration**: Competitive chess with puzzle streaks, rating milestones, accuracy goals
- **Caves of Qud**: Science-fantasy roguelike with mutation acquisition, faction reputation, survival milestones

**Systemic Improvements:**
- **Binding of Isaac Modded Characters**: Added OptionSet for user-defined modded characters
- **Toggle Standardization**: Converted older DefaultOnToggle to consistent Toggle patterns
- **Constraint Reclassification**: Caves of Qud limb dismemberment moved to optional constraint

**Benefits**: Improved extensibility (user-supplied characters), clarity (uniform toggle access), accuracy (constraint vs objective classification)
