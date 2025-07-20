# KeymastersKeepGames
Keymaster's Keep games maintained by eiron

## Archipelagourmet
A meta-game in which the options generarated will be recipes, and/or takeaway and restaurant options provided by the player.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This also features a submodule that include challenges of the type:
``"Make a meal using each of the following ingredients: {3-5 random ingredients}"``

This includes options for filtering by dietary requirements, as well as blocking unwanted ingredients and adding custom ingredients.
You can also set the range for the number of random ingredients from 1 through 10, though there is a chance too high a number will cause the challenge to be unreadable in the client!


## Watchlist
A meta-game in which the options generated will be films and TV shows from the player's watchlist, paired with appropriate viewing actions.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This features separate objective templates for films and television content, with actions tailored to each medium:

Films: ``"WATCH Film Title"`` or ``"FINISH Documentary Title"``
TV Shows: ``"BINGE TV Series Title"`` or ``"CATCH UP Miniseries Title"``

This includes options for customizing film selections, TV show selections, and their respective action lists. The system will only generate objectives for media types that have been configured, allowing for flexible use whether you prefer films, television, or both!


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

## Adventure/Experience Challenges
A meta-game in which the options generated will be local exploration, cultural experiences, outdoor activities, and culinary adventures from the player's adventure backlog, paired with appropriate actions.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This features separate objective templates for different types of adventure activities, with actions tailored to each category:

Local Exploration: ``"VISIT Downtown District"`` or ``"PHOTOGRAPH Historic Neighborhood"``
Cultural Experiences: ``"ATTEND Live Theater Show"`` or ``"PARTICIPATE IN Cultural Workshop"``
Outdoor Activities: ``"ATTEMPT Rock Climbing"`` or ``"CONQUER Hiking Trail"``
Culinary Adventures: ``"TRY International Restaurant"`` or ``"SAMPLE Wine Tasting"``

This includes options for customizing local exploration targets, cultural experiences, outdoor activities, culinary adventures, and their respective action lists. The system will only generate objectives for adventure categories that have been configured, allowing for flexible use whether you prefer local discovery, cultural immersion, outdoor challenges, food exploration, or all four!

## Creative Challenges
A meta-game in which the options generated will be art projects, writing endeavors, photography challenges, and craft projects from the player's creative backlog, paired with appropriate actions.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This features separate objective templates for different types of creative activities, with actions tailored to each medium:

Art Projects: ``"CREATE Watercolor Painting"`` or ``"REFINE Mixed Media Piece"``
Writing: ``"WRITE Short Story"`` or ``"REVISE Poetry Collection"``
Photography: ``"CAPTURE Portrait Session"`` or ``"MASTER Macro Challenge"``
Crafts: ``"MAKE Knitting Project"`` or ``"ATTEMPT Woodworking"``

This includes options for customizing art project selections, writing goals, photography challenges, craft projects, and their respective action lists. The system will only generate objectives for creative categories that have been configured, allowing for flexible use whether you focus on visual arts, writing, photography, crafting, or all four!

## Christmas/Holiday Challenges
A meta-game in which the options generated will be holiday decorations, gift preparations, baking projects, and festive traditions from the player's Christmas and holiday backlog, paired with appropriate seasonal actions.
Some default options are provided for clarity, but can easily be overwritten with whatever the player desires.

This features separate objective templates for different types of holiday activities, with actions tailored to each category:

Decorations: ``"SET UP Christmas Tree"`` or ``"ARRANGE Mantel Decorations"``
Gifts: ``"MAKE Handmade Gift"`` or ``"WRAP Secret Santa Gift"``
Baking: ``"MAKE Christmas Cookies"`` or ``"CREATE Gingerbread House"``
Traditions: ``"ENJOY Christmas Movie Marathon"`` or ``"ATTEND Christmas Market Visit"``

This includes options for customizing decoration plans, gift preparations, baking projects, holiday traditions, and their respective action lists. The system will only generate objectives for holiday categories that have been configured, allowing for flexible use whether you focus on decorating, gift-giving, holiday baking, festive traditions, or all four!

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
