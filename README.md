# KeymastersKeepGames
Keymaster's Keep games maintained by eiron

## Universal Game Tester 🔧

The **Universal Game Tester** (located in `UniversalGameTester/`) is a comprehensive testing and analysis tool that works with **ANY** Keymaster's Keep game implementation. It automatically discovers, loads, and tests game modules regardless of their structure, option types, or complexity.

### Key Features

- **🔍 Automatic Discovery**: Scans directory for game implementation files using pattern recognition
- **🎯 Universal Compatibility**: Works with any game module, including custom option types and complex data structures
- **⚖️ Authentic Simulation**: Reproduces the Keep's weighted objective selection system for realistic testing
- **📊 Comprehensive Analysis**: Provides detailed metrics on objectives, weights, features, and complexity
- **🎮 Interactive Testing**: Menu-driven interface for testing individual games or running full test suites

### Usage

```bash
# Test all discovered game implementations
cd UniversalGameTester
python universal_game_tester.py

# Test a specific game implementation
python universal_game_tester.py stardew_valley_game.py

# Test with shortened filename
python universal_game_tester.py hades
```

### What It Tests

- **Dynamic Objective Generation**: Simulates the Keep's weighted selection process
- **Option System Compatibility**: Validates all option types (Toggle, Choice, Range, OptionSet, custom types)
- **Template Population**: Tests objective template data population with real values
- **Constraint Systems**: Analyzes optional constraint templates
- **Feature Detection**: Identifies relationship systems, difficulty scaling, and special features
- **Import Resolution**: Handles relative imports and missing dependencies automatically

### Sample Output

```
🎮 TESTING: Date Everything Game
📊 IMPLEMENTATION ANALYSIS:
   • Total Objectives: 29
   • Complexity Score: 86
   • Weight Distribution:
     - Weight 10: 9 objectives █████████
     - Weight 8: 2 objectives ██
   • Features: Relationship System
   • Categories: 10 options available

🎯 DYNAMIC OBJECTIVE SELECTION:
   1. 🔥 Achieve LOVE with Rebel (Rubber Duck)
      └─ Weight: 10 | 😊 | ⏰ 📊x2 ⚖️10
   2. ⭐ Get 5 structural elements to FRIENDS status
      └─ Weight: 8 | 💪 | ⏰ 📊x2 ⚖️8
```

### Technical Details

The tester handles:
- **Custom Option Classes**: Automatically resolves string type annotations to actual classes
- **Dynamic Mocking**: Creates universal mock environment for all possible imports
- **Robust Error Handling**: Gracefully handles import failures, missing attributes, and malformed data
- **Weight-Based Selection**: Implements the same probabilistic selection system used by the Keep
- **Cross-Platform Compatibility**: Works on Windows, Mac, and Linux

This tool is essential for validating that game implementations will work correctly within the Keymaster's Keep ecosystem before deployment.

---

## Include Option Standards

All game implementations follow a standardized approach for include Toggle options:

- **Basic Content**: All fundamental include options default to `True` for better objective generation
- **Specialized/Harder Content**: Options for speedruns, difficulty challenges, or specialized content default to `False` 
- **Cursed/Tedious Modules**: Games like "Cursed Red Dead Redemption 2" and "Really Boring Challenges" have all options default to `True`, as players are deliberately opting into that content type

This ensures that casual players get comprehensive objective generation by default, while preserving the option to disable challenging or specialized content categories.

---

## Game Implementation Modules

## Adventure/Experience Challenges
A meta-game in which the options generated will be local exploration, cultural experiences, outdoor activities, and culinary adventures from the player's adventure backlog, paired with appropriate actions.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This features separate objective templates for different types of adventure activities, with actions tailored to each category:

Local Exploration: ``"VISIT Downtown District"`` or ``"PHOTOGRAPH Historic Neighborhood"``
Cultural Experiences: ``"ATTEND Live Theater Show"`` or ``"PARTICIPATE IN Cultural Workshop"``
Outdoor Activities: ``"ATTEMPT Rock Climbing"`` or ``"CONQUER Hiking Trail"``
Culinary Adventures: ``"TRY International Restaurant"`` or ``"SAMPLE Wine Tasting"``

This includes options for customizing local exploration targets, cultural experiences, outdoor activities, culinary adventures, and their respective action lists. The system will only generate objectives for adventure categories that have been configured, allowing for flexible use whether you prefer local discovery, cultural immersion, outdoor challenges, food exploration, or all four!

## Archipelagourmet
A meta-game in which the options generarated will be recipes, and/or takeaway and restaurant options provided by the player.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This also features a submodule that include challenges of the type:
``"Make a meal using each of the following ingredients: {3-5 random ingredients}"``

This includes options for filtering by dietary requirements, as well as blocking unwanted ingredients and adding custom ingredients.
You can also set the range for the number of random ingredients from 1 through 10, though there is a chance too high a number will cause the challenge to be unreadable in the client!

## Christmas/Holiday Challenges
A meta-game in which the options generated will be holiday decorations, gift preparations, baking projects, and festive traditions from the player's Christmas and holiday backlog, paired with appropriate seasonal actions.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This features separate objective templates for different types of holiday activities, with actions tailored to each category:

Decorations: ``"SET UP Christmas Tree"`` or ``"ARRANGE Mantel Decorations"``
Gifts: ``"MAKE Handmade Gift"`` or ``"WRAP Secret Santa Gift"``
Baking: ``"MAKE Christmas Cookies"`` or ``"CREATE Gingerbread House"``
Traditions: ``"ENJOY Christmas Movie Marathon"`` or ``"ATTEND Christmas Market Visit"``

This includes options for customizing decoration plans, gift preparations, baking projects, holiday traditions, and their respective action lists. The system will only generate objectives for holiday categories that have been configured, allowing for flexible use whether you focus on decorating, gift-giving, holiday baking, festive traditions, or all four!

## Creative Challenges
A meta-game in which the options generated will be art projects, writing endeavors, photography challenges, and craft projects from the player's creative backlog, paired with appropriate actions.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This features separate objective templates for different types of creative activities, with actions tailored to each medium:

Art Projects: ``"CREATE Watercolor Painting"`` or ``"REFINE Mixed Media Piece"``
Writing: ``"WRITE Short Story"`` or ``"REVISE Poetry Collection"``
Photography: ``"CAPTURE Portrait Session"`` or ``"MASTER Macro Challenge"``
Crafts: ``"MAKE Knitting Project"`` or ``"ATTEMPT Woodworking"``

This includes options for customizing art project selections, writing goals, photography challenges, craft projects, and their respective action lists. The system will only generate objectives for creative categories that have been configured, allowing for flexible use whether you focus on visual arts, writing, photography, crafting, or all four!

## Keymaster's Keep
The ultimate meta module for generating challenges to play Keymaster's Keep itself! This module creates objectives for playing Keymaster's Keep in its two game modes: Keymaster's Challenge and Magic Key Heist, using the comprehensive game selection pool from the actual Keymaster's Keep configuration.

This features objective templates that mirror the two main game modes, with games selected from the real Keymaster's Keep pool:

Keymaster's Challenge: ``"Complete a Keymaster's Challenge including the games: Celeste, Hollow Knight, and Slay the Spire"``
Magic Key Heist: ``"Complete a Magic Key Heist including the games: Balatro and Enter the Gungeon"``

This includes options for customizing the game selection pool, challenge types, and game count ranges. Players can:
- **Edit Game Selection**: Add, remove, or weight games in the selection pool (defaults to the 120+ games currently available)
- **Choose Challenge Types**: Select which game modes to include (Keymaster's Challenge, Magic Key Heist, or both)
- **Set Game Count Range**: Configure minimum (1-10) and maximum (1-10) games per challenge (defaults to 2-6)

This creates a truly recursive meta-gaming experience where Keymaster's Keep challenges you to play the very games that Keymaster's Keep was designed to manage! Just like with other modules, players can completely customize their experience by editing the game selection to match their preferences and library.

## Music Listening
A meta-game in which the options generated will be albums, artists, and playlists from the player's music listening backlog, paired with appropriate listening actions.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This features separate objective templates for different types of musical content, with actions tailored to each category:

Albums: ``"LISTEN TO Album Title"`` or ``"ANALYZE Soundtrack Title"``
Artists: ``"EXPLORE Artist Name"`` or ``"STUDY DISCOGRAPHY Composer Name"``
Playlists: ``"COMPLETE Playlist Name"`` or ``"SHUFFLE THROUGH Mix Name"``

This includes options for customizing album selections, artist selections, playlist selections, and their respective action lists. The system will only generate objectives for music categories that have been configured, allowing for flexible use whether you prefer exploring specific albums, discovering new artists, working through playlists, or all three!

## Physical/Health Challenges
A meta-game in which the options generated will be exercises, wellness activities, nutrition goals, and movement challenges from the player's health and fitness backlog, paired with appropriate actions.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This features separate objective templates for different types of health activities, with actions tailored to each category:

Exercise: ``"COMPLETE Push-up Challenge"`` or ``"PRACTICE Strength Circuit"``
Wellness: ``"MAINTAIN Sleep Schedule"`` or ``"ESTABLISH Morning Routine"``
Nutrition: ``"TRY Healthy Recipe"`` or ``"TRACK Water Intake"``
Movement: ``"COMPLETE 10,000 Steps"`` or ``"PRACTICE Morning Stretch"``

This includes options for customizing exercise selections, wellness activities, nutrition goals, movement challenges, and their respective action lists. The system will only generate objectives for health categories that have been configured, allowing for flexible use whether you focus on structured exercise, general wellness, nutrition tracking, daily movement, or all four!

## Really Boring Challenges
A deliberately mundane module that transforms everyday, routine activities into gaming objectives, celebrating the art of finding engagement in the most ordinary tasks.

Core Categories: ``Household Maintenance``, ``Personal Organization``, ``Digital Housekeeping``, ``Routine Optimization``, ``Administrative Tasks``, ``Basic Self-Care``

Sample Objectives: ``"Organize 50 digital files"`` or ``"Clean one room thoroughly"`` or ``"Update 3 different passwords"``

## Real-World Scavenger Hunt
A comprehensive real-world exploration game that encourages getting outside, discovering your local area, and engaging with your community. This module turns your surroundings into a game world with objectives focused on photography, location discovery, object collection, social interaction, nature exploration, cultural experiences, seasonal activities, and community engagement.

This features 8 major categories of real-world objectives:

Photography Challenges: ``"Take a photo of A street musician"`` or ``"Photograph Lightning during a storm in natural lighting without flash"``
Location Hunting: ``"Find and visit A hidden garden"`` or ``"Visit 3 different Local cafes establishments"``
Object Collection: ``"Collect 10 different Interesting rocks items"`` or ``"Find 2 Vintage postcards at thrift stores or markets"``
Interaction Challenges: ``"Engage in 3 conversations with Local shop owners"`` or ``"Learn 5 basic phrases in Spanish"``
Nature Exploration: ``"Identify 10 different Birds species"`` or ``"Explore 3 different Walking trails trails"``
Cultural Discovery: ``"Visit 2 Art museums or galleries"`` or ``"Try 3 different Local specialties dishes"``
Seasonal Activities: ``"Participate in Leaf collection during Fall"`` or ``"Experience Rain puddle photography during specific weather"``
Community Engagement: ``"Support 3 local Restaurants businesses"`` or ``"Help with Community garden maintenance"``

This includes extensive customization options with hundreds of possible targets, activities, and constraints. Players can:
- **Focus Areas**: Choose from 8 different activity categories
- **Difficulty Levels**: Easy, hard, or all challenge types
- **Travel Scope**: Local, regional, or unlimited exploration
- **Constraints**: Transportation methods, time limits, weather conditions, companions

The module contains over 500 different objectives across photography subjects, discoverable locations, collectible items, people to meet, activities to try, and seasonal experiences. It's designed to encourage exploration, community connection, and getting outside your normal routine!

## Social/Connections Challenges
A meta-game in which the options generated will be friend meetups, family activities, community events, and networking opportunities from the player's social backlog, paired with appropriate social actions and customizable lists of people to interact with.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This features separate objective templates for different types of social activities, with actions tailored to each category:

Friend Meetups: ``"ARRANGE Coffee Meetup with Best Friend"`` or ``"CATCH UP WITH Game Night with College Friend"``
Family Activities: ``"VISIT Family Dinner with Family Member"`` or ``"SPEND TIME WITH Holiday Visit with Family Member"``
Community Events: ``"ATTEND Local Festival"`` or ``"VOLUNTEER FOR Community Meeting"``
Networking: ``"NETWORK AT Professional Meetup"`` or ``"PARTICIPATE IN Industry Conference"``

This includes options for customizing meetup types, family activities, community events, networking opportunities, and their respective action lists. Most importantly, it includes a **People Selection** option where you can list actual friends, family members, colleagues, and other people you want to connect with. The system will only generate objectives for social categories that have been configured, allowing for flexible use whether you focus on friend connections, family time, community involvement, professional networking, or all four!

## Watchlist
A meta-game in which the options generated will be films and TV shows from the player's watchlist, paired with appropriate viewing actions.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This features separate objective templates for films and television content, with actions tailored to each medium:

Films: ``"WATCH Film Title"`` or ``"FINISH Documentary Title"``
TV Shows: ``"BINGE TV Series Title"`` or ``"CATCH UP Miniseries Title"``

This includes options for customizing film selections, TV show selections, and their respective action lists. The system will only generate objectives for media types that have been configured, allowing for flexible use whether you prefer films, television, or both!

## Individual Game Modules

### Animal Crossing: New Horizons
An island life simulation module focusing on island development, social interaction, decoration, and seasonal activities across the charming world of Animal Crossing.

Core Categories: ``Island Development``, ``Social Interaction``, ``Decoration & Design``, ``Collection & Catalog``, ``Seasonal Events``, ``Achievement Goals``

Sample Objectives: ``"Develop 5 different Residential Areas areas"`` or ``"Achieve Best Friends relationship with 3 villagers"`` or ``"Collect 25 different Fish species"``

### Archipelago Multiworld Randomizer
A meta-gaming module that creates objectives for participating in Archipelago multiworld randomizer sessions, covering the collaborative puzzle-solving experience of linked randomized games.

Core Categories: ``Multiworld Participation``, ``Item Progression``, ``Helper Activities``, ``Community Engagement``, ``Technical Setup``, ``Game Coordination``

Sample Objectives: ``"Complete your sphere 1 progression items"`` or ``"Send 10 useful items to other players"`` or ``"Help troubleshoot another player's connection issues"``

### Baldur's Gate 3
A deep RPG module covering character builds, story choices, companion relationships, tactical combat, exploration, and the rich narrative possibilities of Faerûn.

Core Categories: ``Character Builds``, ``Story Progression``, ``Companion Quests``, ``Exploration``, ``Combat Challenges``, ``Social Encounters``, ``Collectibles``, ``Achievement Hunting``

Sample Objectives: ``"Complete Act 1 with a Paladin/Warlock multiclass build"`` or ``"Achieve Romance relationship with Shadowheart"`` or ``"Successfully pass 20 Persuasion skill checks"``

### Bloodstained: Ritual of the Night
A comprehensive Metroidvania module covering shard collection, exploration, boss battles, alchemy, equipment mastery, and Miriam's quest for answers.

Core Categories: ``Shard Collection``, ``Exploration``, ``Boss Challenges``, ``Alchemy & Crafting``, ``Equipment Mastery``, ``Completion Goals``, ``Speedrun Challenges``

Sample Objectives: ``"Collect 20 Conjure shards"`` or ``"Reach 90% map completion"`` or ``"Defeat Bloodless without using healing items"``

### Board Game Collection
A physical gaming module focused on exploring and mastering your board game collection, from quick card games to complex strategy epics, with emphasis on both solo and group play.

Core Categories: ``Strategy Games``, ``Party Games``, ``Solo Gaming``, ``Learning New Games``, ``Game Night Hosting``, ``Collection Management``

Sample Objectives: ``"Learn and play 3 new games from your collection"`` or ``"Host a game night with 4+ different games"`` or ``"Complete a solo campaign game"``

### Cult of the Lamb
A unique cult management and action module covering cult building, follower management, combat crusades, and the dark humor of leading a woodland cult.

Core Categories: ``Cult Management``, ``Combat & Crusades``, ``Follower Care``, ``Base Building``, ``Resource Collection``, ``Ritual Performance``, ``Story Progression``

Sample Objectives: ``"Recruit 15 new cult followers"`` or ``"Defeat Leshy in combat"`` or ``"Perform 5 different Blessing rituals"``

### Danganronpa Decadence
A collection of visual novel murder mystery games featuring students trapped in deadly games. This module supports objectives across all four included games in the Decadence collection.

**Supported Games:**
- Danganronpa: Trigger Happy Havoc (with School Mode)
- Danganronpa 2: Goodbye Despair (with Island Mode)  
- Danganronpa V3: Killing Harmony (with UTDP mode)
- Danganronpa S: Ultimate Summer Camp

**Core Categories:**
- Story mode objectives: investigations, class trials, free time activities, report cards, skills, and presents
- Bonus mode objectives: School Mode, Island Mode, UTDP, and Summer Camp challenges
- Extra minigames: Death Road of Despair, Magical Girl Monomi, and challenge modes
- Collectibles: Hidden Monokuma hunting and location-based collection goals

Sample Objectives: ``"Achieve S rank in the chapter 3 class trial"`` or ``"Max out friendship with Kyoko Kirigiri"`` or ``"Clear 5 segments of Nonstop Debate without mistakes"`` or ``"Reach turn 50 in Development Mode as Makoto Naegi"`` or ``"Clear floor 30 in Tower of Despair with a party that includes Hajime Hinata"``

The module provides comprehensive coverage of all gameplay modes and mechanics across the entire Danganronpa collection.

### Date Everything
A whimsical dating simulation module where you romance household objects and abstract concepts in your own home. Features 100+ fully voice-acted characters from structural elements to existential dread, with branching relationships and transformation possibilities.

Core Categories: ``Structural Objects``, ``Furniture & Decor``, ``Kitchen Appliances``, ``Bathroom Items``, ``Laundry Items``, ``Office & Bedroom``, ``Miscellaneous Items``, ``Special Concepts``, ``DLC Characters``

Sample Objectives: ``"Achieve LOVE with Rebel (Rubber Duck)"`` or ``"Get 5 structural elements to FRIENDS status"`` or ``"Transform Teddy (Teddy Bear) into human form through deep connection"``

### Dead Cells
A challenging metroidvania module focused on combat mastery, weapon experimentation, biome progression, and the brutal but rewarding world of the Prisoner's journey.

Core Categories: ``Combat Mastery``, ``Weapon Experimentation``, ``Biome Progression``, ``Mutation Builds``, ``Speed Running``, ``Achievement Hunting``

Sample Objectives: ``"Defeat 25 different Elite enemies"`` or ``"Complete a run using only Survival weapons"`` or ``"Reach 3BC difficulty level"``

### Hades
A roguelike action module covering escape attempts, weapon mastery, relationship building with gods and underworld denizens, and the compelling narrative of Zagreus's journey.

Core Categories: ``Escape Attempts``, ``Weapon Mastery``, ``Relationship Building``, ``Boon Collection``, ``House Upgrades``, ``Narrative Progress``, ``Challenge Runs``

Sample Objectives: ``"Complete 5 successful escape attempts"`` or ``"Master the Stygian Blade weapon"`` or ``"Max out relationship with Megaera"``

### Harvestella
A farming RPG module that brings the full breadth of Harvestella's systems to Keymaster's Keep. This implementation covers farming, exploration, combat, relationships, story progression, crafting, cooking, and seasonal events, with robust support for all major gameplay features and option types.

Core Categories: ``Farming Objectives``, ``Exploration & Adventure``, ``Combat Challenges``, ``Relationship System``, ``Story Progression``, ``Crafting & Cooking``, ``Seasonal & Collection Goals``

Sample Objectives: ``"Harvest 50 crops across all seasons"`` or ``"Defeat 10 unique monsters in Quietus dungeons"`` or ``"Reach max relationship with a main character"`` or ``"Complete Chapter 5 and restore all Seaslight crystals"``

Features:
- Dynamic crop selection, farming goals, and seasonal objectives
- Exploration of locations, dungeons, and rare material collection
- Combat with monsters, bosses, and job mastery
- Relationship events and character-specific objectives
- Story progression, chapter completion, and seasonal dungeon unlocks
- Crafting, equipment upgrades, and recipe mastery
- Collection goals for items, recipes, monsters, and more

Harvestella brings all its farming, adventure, and relationship systems to Keymaster's Keep.

### Just Dance
A comprehensive rhythm gaming module covering the entire Just Dance franchise from 2014 through 2025, with support for base game tracks, regional exclusives, subscription content (Just Dance Unlimited), and premium content (Just Dance+).

Game Coverage: ``Just Dance 2014-2025``, ``Just Dance Unlimited Subscription``, ``Just Dance+ Premium Content``, ``Regional Exclusives`` (China, France, Japan, Benelux, Germany, Italy, Southeast Asia, and more)

Core Categories: ``Base Game Completion``, ``Subscription Service Mastery``, ``Regional Content Exploration``, ``Score Achievement``, ``Song Collection``, ``Dance Challenge Completion``

Sample Objectives: ``"Perfect 25 songs from Just Dance 2023 base tracklist"`` or ``"Complete 15 dances from Just Dance Unlimited subscription"`` or ``"Master 5 songs from Just Dance+ premium content"`` or ``"Achieve 4+ stars on 20 regional exclusive tracks"``

Features comprehensive song libraries with accurate track lists, regional exclusives, platform-specific content, and both subscription services. Supports granular customization of which games you own, which DLC/subscription content you have access to, and which regional exclusives are available in your region.

### Minecraft
An expansive sandbox module covering building projects, exploration, resource gathering, redstone engineering, and the limitless creativity of the block world.

Core Categories: ``Building Projects``, ``Exploration & Adventure``, ``Resource Gathering``, ``Redstone Engineering``, ``Farming & Automation``, ``Combat Challenges``, ``Creative Builds``

Sample Objectives: ``"Build a 50x50 Castle structure"`` or ``"Explore 10 different Ocean Monuments"`` or ``"Create an automated Crop farm system"``

### Red Dead Redemption 2 (Cursed Edition)
A deliberately chaotic and humorous take on the Wild West epic, featuring intentionally absurd objectives that subvert the serious tone of Arthur Morgan's story with ridiculous challenges.

Core Categories: ``Absurd Combat``, ``Ridiculous Exploration``, ``Chaotic Social Interactions``, ``Silly Customization``, ``Nonsense Activities``, ``Bizarre Challenges``

Sample Objectives: ``"Kill 50 enemies using only throwing knives while wearing a fancy hat"`` or ``"Ride your horse backwards for 10 minutes straight"`` or ``"Get a 1000 dollar bounty in Valentine by only antagonizing people"``

### Stardew Valley
A comprehensive farming simulation module covering all aspects of Pelican Town life, from crop management and animal care to community relationships and cave exploration.

Core Categories: ``Farm Management``, ``Relationship Building``, ``Exploration & Combat``, ``Crafting & Collection``, ``Seasonal Activities``, ``Community Goals``, ``Achievement Hunting``

Sample Objectives: ``"Earn 50000g through Crop sales"`` or ``"Reach 8 hearts relationship level with Abigail"`` or ``"Complete 15 different Community Center bundles"``

### The Sims 4
A comprehensive life simulation module covering all aspects of Sim life across the base game and expansion packs, from skill development and career progression to relationships, emotions, and creative building challenges.

Core Categories: ``Skill Mastery``, ``Career Progression``, ``Relationship Building``, ``Aspiration Completion``, ``Creative Building``, ``Emotional Challenges``, ``Collection Goals``, ``Life Events``, ``Expansion Content``

Sample Objectives: ``"Master the Painting skill to level 10"`` or ``"Reach the top of the Writer career branch"`` or ``"Build a SOULMATE relationship with another Sim"`` or ``"Complete the Renaissance Sim aspiration"`` or ``"Build a 50,000 simoleon house with a CONFIDENT emotion focus"`` or ``"Experience the MORTIFIED emotion"`` or ``"Collect 15 different Space Rocks"``

Features comprehensive objectives covering skills, careers, aspirations, collections, emotions, and creative building challenges from both base game and expansion pack content. Includes expanded career paths, additional skills, new aspirations, and exclusive collections from DLC packs. The module automatically adapts objectives based on available content, ensuring players can engage with their full Sims 4 library.
