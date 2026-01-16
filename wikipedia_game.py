from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle, DefaultOnToggle, Range

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class WikipediaGameArchipelagoOptions:
    wikipedia_game_include_specific_paths: WikipediaGameIncludeSpecificPaths
    wikipedia_game_include_category_paths: WikipediaGameIncludeCategoryPaths
    wikipedia_game_include_random_paths: WikipediaGameIncludeRandomPaths
    wikipedia_game_max_clicks: WikipediaGameMaxClicks


class WikipediaGame(Game):
    name = "Wikipedia Game"
    platform = KeymastersKeepGamePlatforms.WEB

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PC
    ]

    is_adult_only_or_unrated = False

    options_cls = WikipediaGameArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="No using the search function",
                data={},
            ),
            GameObjectiveTemplate(
                label="No using 'Ctrl+F' to find links on page",
                data={},
            ),
            GameObjectiveTemplate(
                label="No clicking on disambiguation or list pages",
                data={},
            ),
            GameObjectiveTemplate(
                label="Must stay on English Wikipedia (no language switching)",
                data={},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        objectives += self.base_objectives()
        
        if self.include_specific_paths:
            objectives += self.specific_path_objectives()
            
        if self.include_category_paths:
            objectives += self.category_path_objectives()

        if self.include_random_paths:
            objectives += self.random_path_objectives()
        
        return objectives
    
    def base_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            # Countries to countries (easier)
            GameObjectiveTemplate(
                label="Get from START_COUNTRY to END_COUNTRY in EASY_CLICKS clicks or fewer",
                data={
                    "START_COUNTRY": (self.countries, 1),
                    "END_COUNTRY": (self.countries, 1),
                    "EASY_CLICKS": (self.easy_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            # Animals to foods (standard)
            GameObjectiveTemplate(
                label="Get from ANIMAL to FOOD in STANDARD_CLICKS clicks or fewer",
                data={
                    "ANIMAL": (self.animals, 1),
                    "FOOD": (self.foods, 1),
                    "STANDARD_CLICKS": (self.standard_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            # Technology to historical event (hard)
            GameObjectiveTemplate(
                label="Get from TECHNOLOGY to HISTORICAL_EVENT in HARD_CLICKS clicks or fewer",
                data={
                    "TECHNOLOGY": (self.technologies, 1),
                    "HISTORICAL_EVENT": (self.historical_events, 1),
                    "HARD_CLICKS": (self.hard_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=6,
            ),
            # Video game to philosophical concept (hard)
            GameObjectiveTemplate(
                label="Get from VIDEO_GAME to PHILOSOPHY in HARD_CLICKS clicks or fewer",
                data={
                    "VIDEO_GAME": (self.video_games, 1),
                    "HARD_CLICKS": (self.hard_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=6,
            ),
            # Meme to country (standard)
            GameObjectiveTemplate(
                label="Get from MEME to COUNTRY in STANDARD_CLICKS clicks or fewer",
                data={
                    "MEME": (self.memes, 1),
                    "COUNTRY": (self.countries, 1),
                    "STANDARD_CLICKS": (self.standard_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            # Starter to finisher (expert, very generous clicks)
            GameObjectiveTemplate(
                label="Get from STARTER to FINISHER in EXPERT_CLICKS clicks or fewer",
                data={
                    "STARTER": (self.start_articles, 1),
                    "FINISHER": (self.end_articles, 1),
                    "EXPERT_CLICKS": (self.expert_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
        ]
    
    def specific_path_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Get from START_ARTICLE to END_ARTICLE in MAX_CLICKS clicks or fewer",
                data={
                    "START_ARTICLE": (self.start_articles, 1),
                    "END_ARTICLE": (self.end_articles, 1),
                    "MAX_CLICKS": (self.max_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=7,
            ),
        ]

    def category_path_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Get from START_CATEGORY to END_CATEGORY in MAX_CLICKS clicks or fewer",
                data={
                    "START_CATEGORY": (self.categories, 1),
                    "END_CATEGORY": (self.categories, 1),
                    "MAX_CLICKS": (self.max_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Get from CATEGORY article to 'Philosophy' in MAX_CLICKS clicks or fewer",
                data={
                    "CATEGORY": (self.categories, 1),
                    "MAX_CLICKS": (self.max_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
        ]

    def random_path_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use 'Random Article' button twice, get from first to second in MAX_CLICKS clicks",
                data={
                    "MAX_CLICKS": (self.max_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Click 'Random Article' 3 times, visit all 3 articles starting from any of them in MAX_CLICKS clicks",
                data={
                    "MAX_CLICKS": (self.max_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Get from 'Random Article' to 'Today's Featured Article' in MAX_CLICKS clicks",
                data={
                    "MAX_CLICKS": (self.max_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=12,
            ),
            GameObjectiveTemplate(
                label="Get from article about ARCHIPELAGO_GAME to END_ARTICLE in MAX_CLICKS clicks",
                data={
                    "ARCHIPELAGO_GAME": (self.archipelago_games, 1),
                    "END_ARTICLE": (self.end_articles, 1),
                    "MAX_CLICKS": (self.max_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Get from 'Today's Featured Article' to CATEGORY in MAX_CLICKS clicks",
                data={
                    "CATEGORY": (self.categories, 1),
                    "MAX_CLICKS": (self.max_clicks_range, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
        ]
    
    @property
    def include_specific_paths(self) -> bool:
        return self.archipelago_options.wikipedia_game_include_specific_paths.value
    
    @property
    def include_category_paths(self) -> bool:
        return self.archipelago_options.wikipedia_game_include_category_paths.value

    @property
    def include_random_paths(self) -> bool:
        return self.archipelago_options.wikipedia_game_include_random_paths.value
    
    @property
    def max_clicks(self) -> int:
        return self.archipelago_options.wikipedia_game_max_clicks.value
    
    @property
    def max_clicks_range(self) -> range:
        """Returns a range centered around the max_clicks setting"""
        base = self.max_clicks
        return range(max(3, base - 2), min(15, base + 3))
    
    @property
    def easy_clicks_range(self) -> range:
        """More lenient range for easier paths."""
        base = self.max_clicks
        return range(max(3, base - 3), max(4, base))

    @property
    def standard_clicks_range(self) -> range:
        """Default range for standard difficulty paths."""
        base = self.max_clicks
        return range(max(3, base - 2), base + 2)

    @property
    def hard_clicks_range(self) -> range:
        """More generous range for harder paths."""
        base = self.max_clicks
        return range(base, min(18, base + 5))

    @property
    def expert_clicks_range(self) -> range:
        """Most generous range for expert-level paths."""
        base = self.max_clicks
        return range(base + 1, min(20, base + 7))

    @staticmethod
    def start_articles() -> List[str]:
        """Returns list of interesting start articles"""
        return [
            "Cow",
            "Pig",
            "Sheep",
            "Dolphin",
            "Octopus",
            "Platypus",
            "Axolotl",
            "Tardigrade",
            "Mantis shrimp",
            "Penguin",
            "Eagle",
            "Owl",
            
            # Chemical compounds and elements
            "Vitamin C",
            "Water",
            "Carbon",
            "Oxygen",
            "Hydrogen",
            "Iron",
            "Gold",
            "Salt",
            "DNA",
            
            # Geographic locations
            "Texas",
            "California",
            "New York City",
            "London",
            "Paris",
            "Tokyo",
            "Antarctica",
            "Mount Everest",
            "Eiffel Tower",
            "Great Wall of China",
            "Pyramids of Giza",
            "Stonehenge",
            "Atlantis",
            
            # Abstract/philosophical
            "Real life",
            "Time",
            "Space",
            "Love",
            "Death",
            "Consciousness",
            "Free will",
            "Infinity",
            
            # Meta Wikipedia articles
            "Wikipedia",
            "List of video games notable for negative reception",
            "List of English words containing Q not followed by U",
            "List of common misconceptions",
            "Wikipedia:Unusual articles",
            "List of lists of lists",
            "List of fictional colors",
            "List of fictional languages",
            "List of Internet phenomena",
            "Category:Categories",
            
            # Disambiguation pages
            "Pyramid (disambiguation)",
            "Orange (disambiguation)",
            "Turkey (disambiguation)",
            "Java (disambiguation)",
            "Mercury (disambiguation)",
            "Apple (disambiguation)",
            "Amazon (disambiguation)",
            "Bank (disambiguation)",
            "Bat (disambiguation)",
            "Crane (disambiguation)",
            
            # Film soundtracks and albums
            "Footloose (2011 soundtrack)",
            "Shrek 2 (soundtrack)",
            "Frozen (soundtrack)",
            "The Social Network (soundtrack)",
            "Guardians of the Galaxy (soundtrack)",
            "Tron: Legacy (soundtrack)",
            "The Lion King (soundtrack)",
            
            # Fictional languages
            "Klingon language",
            "Elvish languages",
            "Dothraki language",
            "Na'vi language",
            "Newspeak",
            "Pig Latin",
            "Esperanto",
            
            # Gaming hardware
            "PlayStation Vita",
            "Sega Dreamcast",
            "Nintendo Virtual Boy",
            "Ouya",
            "Steam Deck",
            "Game Boy Color",
            "Nintendo 64",
            "PlayStation 2",
            "Xbox",
            "Nintendo 64",
            "PlayStation 2",
            "Xbox",
            
            # Historical figures
            "Napoleon",
            "Albert Einstein",
            "Cleopatra",
            "Leonardo da Vinci",
            "Marie Curie",
            "Genghis Khan",
            "Abraham Lincoln",
            "Nikola Tesla",
            "Galileo Galilei",
            "Isaac Newton",
            "Charles Darwin",
            "Joan of Arc",
            "Queen Victoria",
            "Julius Caesar",
            
            # Historical events
            "World War II",
            "World War I",
            "French Revolution",
            "American Revolution",
            "Moon landing",
            "Fall of the Berlin Wall",
            "Renaissance",
            "Industrial Revolution",
            "Age of Enlightenment",
            
            # Food and drink
            "Pizza",
            "Banana",
            "Chocolate",
            "Coffee",
            "Tea",
            "Sushi",
            "Potato",
            "Avocado",
            "Pineapple",
            "Sriracha",
            "Bread",
            "Cheese",
            "Hamburger",
            "Hot dog",
            "Ice cream",
            "Cookie",
            
            # Technology and companies
            "Apple Inc.",
            "Microsoft",
            "Tesla, Inc.",
            "Google",
            "Amazon (company)",
            "Facebook",
            "Twitter",
            "Internet",
            "Artificial intelligence",
            "Blockchain",
            "Quantum computing",
            "Smartphone",
            "Computer",
            
            # Video games
            "Video game",
            "Minecraft",
            "The Legend of Zelda",
            "Pokémon",
            "Super Mario Bros.",
            "Tetris",
            "Dark Souls",
            "Among Us",
            "Fortnite",
            "Elden Ring",
            "The Sims",
            "Grand Theft Auto V",
            "Speedrunning",
            "Esports",
            "Portal (video game)",
            "Half-Life",
            "Doom (1993 video game)",
            
            # Internet culture and memes
            "Rickrolling",
            "Doge (meme)",
            "Pepe the Frog",
            "Loss (comic)",
            "Wojak",
            "Shrek",
            "Big Chungus",
            "Stonks",
            "Distracted boyfriend",
            "Hide the Pain Harold",
            "Woman yelling at a cat",
            
            # Social media and platforms
            "YouTube",
            "Reddit",
            "4chan",
            "Twitch (service)",
            "Discord",
            "TikTok",
            "Instagram",
            "Snapchat",
            
            # Music
            "The Beatles",
            "Queen (band)",
            "Beethoven",
            "Mozart",
            "Bach",
            "Elvis Presley",
            "Michael Jackson",
            "Guitar",
            "Piano",
            "Drums",
            "Violin",
            "Jazz",
            "Rock music",
            "Hip hop music",
            "K-pop",
            "Vocaloid",
            "Dubstep",
            
            # Sports
            "Basketball",
            "Baseball",
            "Soccer",
            "American football",
            "Tennis",
            "Golf",
            "Cricket",
            "Rugby",
            "Swimming",
            
            # Athletes
            "Michael Jordan",
            "Serena Williams",
            "Muhammad Ali",
            "Usain Bolt",
            "Lionel Messi",
            "Cristiano Ronaldo",
            
            # Science concepts
            "Periodic table",
            "Evolution",
            "Photosynthesis",
            "Global warming",
            "Dinosaur",
            "Bacteria",
            "Mitochondria",
            "Gravity",
            "Electricity",
            "Magnetism",
            "Atom",
            "Cell (biology)",
            
            # Pop culture franchises
            "Shakespeare",
            "Star Wars",
            "Harry Potter",
            "The Lord of the Rings",
            "Marvel Cinematic Universe",
            "DC Comics",
            "Anime",
            "Manga",
            "James Bond",
            "Doctor Who",
            "Star Trek",
            
            # Art
            "Mona Lisa",
            "The Scream",
            "The Starry Night",
            "Guernica",
            "The Persistence of Memory",
            
            # Philosophy
            "Democracy",
            "Existentialism",
            
            # Conspiracy theories and mysteries
            "42 (number)",
            "Area 51",
            "Bermuda Triangle",
            "Flat Earth",
            "Moon landing conspiracy theories",
            "Illuminati",
            "Roswell incident",
            "Crop circle",
            
            # Film and TV
            "The Room (film)",
            "Citizen Kane",
            "The Godfather",
            "Pulp Fiction",
            "Breaking Bad",
            "Game of Thrones",
            "The Simpsons",
            "Friends",
            
            # Fundamental concepts
            "Chess",
            "Mathematics",
            "Music",
            "Color",
            "Number",
            "Alphabet",
            "Fire",
            "Wheel",
            "Language",
            "Writing",
            "Book",
        ]
    
    @staticmethod
    def end_articles() -> List[str]:
        """Returns list of interesting end articles"""
        return [
            # The classic Philosophy destination
            "Philosophy",
            
            # Quirky/memetic finishers
            "Milky Way (chocolate bar)",
            "Egg",
            "Handshake",
            "Shark Tank",
            "Second Life",
            "Kirby (character)",
            "42 (number)",
            "Selfie",
            "Banana for scale",
            "Murphy's law",
            "Rubber duck debugging",
            "The cake is a lie",
            "Easter egg (media)",
            "Wilhelm scream",
            "Red herring",
            "MacGuffin",
            "Deus ex machina",
            "Fourth wall",
            "Trope",
            
            # Meta and unusual destinations
            "Wikipedia",
            "Internet",
            "Language",
            "Communication",
            "Information",
            "Knowledge",
            "Truth",
            "Reality",
            "Existence",
            "Consciousness",
            "Memory",
            "Perception",
            
            # Major world countries
            "France",
            "Germany",
            "Russia",
            "Italy",
            "Spain",
            "Portugal",
            "Greece",
            "Japan",
            "China",
            "India",
            "United States",
            "United Kingdom",
            "Canada",
            "Australia",
            "Brazil",
            "Mexico",
            "Argentina",
            "Egypt",
            "South Africa",
            "Nigeria",
            "Ethiopia",
            "Republic of Ireland",
            "Netherlands",
            "Belgium",
            "Switzerland",
            "Austria",
            "Poland",
            "Sweden",
            "Norway",
            "Denmark",
            
            # Small/unique countries
            "Vatican City",
            "Monaco",
            "Liechtenstein",
            "San Marino",
            "Luxembourg",
            "Andorra",
            "Malta",
            "Iceland",
            
            # Historical civilizations and empires
            "Ancient Greece",
            "Ancient Rome",
            "Ancient Egypt",
            "Byzantine Empire",
            "Ottoman Empire",
            "Holy Roman Empire",
            "Roman Empire",
            "Persian Empire",
            "Mongol Empire",
            "British Empire",
            "Aztec Empire",
            "Inca Empire",
            
            # Historical figures
            "Steve Jobs",
            "Bill Gates",
            "Adolf Hitler",
            "Winston Churchill",
            "Michael Jordan",
            "Charles Darwin",
            "Shakespeare",
            "Isaac Newton",
            "Socrates",
            "Aristotle",
            "Plato",
            "Martin Luther King Jr.",
            "Mahatma Gandhi",
            "Nelson Mandela",
            "Buddha",
            "Jesus",
            "Muhammad",
            "Confucius",
            "Alexander the Great",
            "Napoleon Bonaparte",
            
            # Sciences and fields of study
            "Mathematics",
            "Biology",
            "Physics",
            "Chemistry",
            "Nuclear physics",
            "Quantum mechanics",
            "Astronomy",
            "Geology",
            "Anthropology",
            "Archaeology",
            "Psychology",
            "Sociology",
            "Neuroscience",
            "Genetics",
            "Ecology",
            "Zoology",
            "Botany",
            "Medicine",
            "Engineering",
            
            # Philosophy and abstract concepts
            "Love",
            "Hate",
            "Fear",
            "Joy",
            "Anger",
            "Democracy",
            "Existentialism",
            "Capitalism",
            "Communism",
            "Socialism",
            "Fascism",
            "Anarchism",
            "Religion",
            "Atheism",
            "Ethics",
            "Justice",
            "Freedom",
            "Liberty",
            "Equality",
            "Death",
            "Life",
            "Infinity",
            "Time",
            "Space",
            "Morality",
            "Virtue",
            "Nihilism",
            "Stoicism",
            "Hedonism",
            
            # Arts and culture movements
            "Renaissance",
            "Impressionism",
            "Expressionism",
            "Modernism",
            "Surrealism",
            "Baroque",
            "Romanticism",
            "Cubism",
            "Dadaism",
            "Postmodernism",
            "Realism",
            "Minimalism",
            
            # Art forms
            "Opera",
            "Ballet",
            "Literature",
            "Poetry",
            "Theater",
            "Cinema",
            "Photography",
            "Sculpture",
            "Painting",
            "Dance",
            "Animation",
            "Comics",
            
            # Literary and poetic forms
            "Iambic pentameter",
            "Sonnet",
            "Haiku",
            "Free verse",
            "Epic poetry",
            "Alliteration",
            "Metaphor",
            "Simile",
            "Irony",
            "Satire",
            
            # Technology and innovation
            "Economics",
            "Climate change",
            "Space exploration",
            "Robotics",
            "Computer",
            "iPhone",
            "Android (operating system)",
            "Touchscreen",
            "GPS",
            "Bluetooth",
            "Wi-Fi",
            "Electricity",
            "Wheel",
            "Fire",
            "Agriculture",
            "Industrial Revolution",
            "Printing press",
            "Telegraph",
            "Telephone",
            "Radio",
            "Television",
            "Microprocessor",
            "Transistor",
            "Semiconductor",
            
            # Gaming concepts
            "Game theory",
            "Role-playing game",
            "Roguelike",
            "Metroidvania",
            "Platformer",
            "First-person shooter",
            "Multiplayer online battle arena",
            "Battle royale game",
            "Dungeon crawl",
            "Permadeath",
            "Procedural generation",
            "Microtransaction",
            "Downloadable content",
            "Loot box",
            "Free-to-play",
            "Pay-to-win",
            "Dungeon Master",
            "Game mechanics",
            "Level design",
            
            # Gaming platforms
            "Nintendo",
            "PlayStation",
            "Xbox",
            "Steam (service)",
            "Indie game",
            "Virtual reality",
            "Arcade game",
            "Board game",
            "Tabletop role-playing game",
            "Card game",
            
            # Internet and modern culture
            "Meme",
            "Social media",
            "Cryptocurrency",
            "Bitcoin",
            "Streaming media",
            "Viral video",
            "Emoji",
            "GIF",
            "Podcast",
            "Blog",
            "Wiki",
            "Open source",
            "Crowdfunding",
            "Influencer",
            
            # Nature and geography
            "Ocean",
            "Pacific Ocean",
            "Atlantic Ocean",
            "Desert",
            "Sahara",
            "Rainforest",
            "Amazon rainforest",
            "Volcano",
            "Island",
            "River",
            "Cave",
            "Mountain",
            "Forest",
            "Tundra",
            "Savanna",
            "Wetland",
            
            # Abstract scientific concepts
            "Chaos theory",
            "Paradox",
            "Symmetry",
            "Entropy",
            "Gravity",
            "Light",
            "Sound",
            "Energy",
            "Matter",
            "Atom",
            "Molecule",
            "Photon",
            "Electron",
            "Proton",
            "Neutron",
            
            # War and conflict
            "War",
            "Peace",
            "Revolution",
            "Empire",
            "Colonialism",
            "Imperialism",
            "Diplomacy",
            "Treaty",
            
            # Pop culture and media
            "Science fiction",
            "Fantasy",
            "Horror fiction",
            "Comedy",
            "Satire",
            "Parody",
            "Tragedy",
            "Drama",
            "Romance",
            
            # Sports and games
            "Chess",
            "Go (game)",
            "Poker",
            "Martial arts",
            "Olympic Games",
            "Sport",
            "Competition",
            
            # Fundamental concepts
            "Money",
            "Currency",
            "Gold",
            "Law",
            "Constitution",
            "Education",
            "School",
            "University",
            "Architecture",
            "Fashion",
            "Food",
            "Cooking",
            "Sleep",
            "Dream",
            "Work",
            "Art",
            "Science",
            "Culture",
            "Society",
            "Civilization",
            "History",
            "Geography",
            "Music",
            "Rhythm",
            "Harmony",
            "Melody",
            
            # Languages
            "Latin",
            "Ancient Greek",
            "Sanskrit",
            "Hebrew",
            "Arabic",
            "Mandarin Chinese",
            "English language",
            "Spanish language",
            "French language",
            "Sign language",
            "Braille",
            "Morse code",
            
            # Linguistic concepts
            "Grammar",
            "Syntax",
            "Semantics",
            "Phonetics",
            "Rhetoric",
            "Linguistics",
            "Etymology",
            
            # Narrative concepts
            "Narrative",
            "Plot (narrative)",
            "Character (arts)",
            "Protagonist",
            "Antagonist",
            "Hero",
            "Villain",
            "Archetype",
            
            # Mythology and folklore
            "Cthulhu",
            "Lovecraftian horror",
            "Greek mythology",
            "Norse mythology",
            "Egyptian mythology",
            "Roman mythology",
            "Celtic mythology",
            "Dragon",
            "Vampire",
            "Werewolf",
            "Zombie",
            "Ghost",
            "Folklore",
            "Urban legend",
            "Fairy tale",
            "Legend",
            "Myth",
            
            # Human interactions
            "Handshake",
            "Hug",
            "Kiss",
            "Wave (gesture)",
            "Smile",
            "Laughter",
            "Cry",
            "Empathy",
            "Sympathy",
            "Friendship",
            "Family",
            
            # Food items
            "Egg",
            "Milk",
            "Flour",
            "Salt",
            "Sugar",
            "Butter",
            "Rice",
            "Wheat",
            "Corn",
            "Potato",
            "Tomato",
            
            # Advanced philosophical concepts
            "Epistemology",
            "Ontology",
            "Metaphysics",
            "Phenomenology",
            "Aesthetics",
            "Logic",
            "Reason",
            
            # Cultural concepts
            "The meaning of life",
            "Collective unconscious",
            "Zeitgeist",
            "Cultural hegemony",
        ]
    
    @staticmethod
    def archipelago_games() -> List[str]:
        """Archipelago and Keymaster's Keep games with Wikipedia articles"""
        return [
            "The Legend of Zelda",
            "Dark Souls",
            "Minecraft",
            "Pokémon",
            "Final Fantasy",
            "Super Mario Bros.",
            "Sonic the Hedgehog",
            "Metroid",
            "Castlevania",
            "Mega Man",
            "Donkey Kong Country",
            "Super Metroid",
            "The Witness",
            "Hollow Knight",
            "Celeste (video game)",
            "Undertale",
            "Stardew Valley",
            "Terraria",
            "Factorio",
            "Risk of Rain",
            "Timespinner",
            "A Link to the Past",
            "Ocarina of Time",
            "Majora's Mask",
            "Rogue Legacy",
            "Slay the Spire",
            "Hades (video game)",
            "StarCraft",
            "Warcraft III",
            "Super Mario World",
            "Super Mario 64",
            "Kirby (series)",
            "Pokémon Red and Blue",
            "Overcooked",
            "Final Fantasy VII",
            "Secret of Mana",
            "Chrono Trigger",
        ]
    
    @staticmethod
    def categories() -> List[str]:
        """Common categories for dynamic path generation"""
        return [
            "a country",
            "a historical figure",
            "an animal",
            "a scientific concept",
            "a food",
            "a sport",
            "a technology",
            "a work of art",
            "a philosophical concept",
            "a musical instrument",
            "a body of water",
            "a chemical element",
            "a city",
            "a disease",
            "a language",
            "a religion",
            "a planet",
            "a book",
            "a movie",
            "an invention",
            "a mountain",
            "a political system",
            "a war",
            "an empire",
            "a scientist",
            "an artist",
            "a mathematician",
            "a building",
            "a natural phenomenon",
            "a mythological figure",
        ]

    # -- Providers for base objective placeholders --
    @staticmethod
    def countries() -> List[str]:
        return [
            "France", "Germany", "Italy", "Spain", "Portugal", "Greece", "Japan", "China",
            "India", "United States", "United Kingdom", "Canada", "Australia", "Brazil", "Mexico",
            "Argentina", "Egypt", "South Africa", "Nigeria", "Ethiopia", "Republic of Ireland",
            "Netherlands", "Belgium", "Switzerland", "Austria", "Poland", "Sweden", "Norway",
            "Denmark", "Vatican City", "Monaco", "Liechtenstein", "San Marino", "Luxembourg"
        ]

    @staticmethod
    def animals() -> List[str]:
        return [
            "Chicken", "Cat", "Dog", "Horse", "Cow", "Pig", "Sheep", "Dolphin", "Octopus",
            "Platypus", "Axolotl", "Tardigrade", "Mantis shrimp", "Penguin", "Eagle", "Owl"
        ]

    @staticmethod
    def foods() -> List[str]:
        return [
            "Pizza", "Banana", "Chocolate", "Coffee", "Tea", "Sushi", "Potato", "Avocado",
            "Pineapple", "Sriracha", "Bread", "Cheese", "Hamburger", "Hot dog", "Ice cream", "Cookie"
        ]

    @staticmethod
    def technologies() -> List[str]:
        return [
            "Internet", "Artificial intelligence", "Quantum computing", "Smartphone", "Computer",
            "iPhone", "Android (operating system)", "Touchscreen", "GPS", "Bluetooth", "Wi-Fi",
            "Microprocessor", "Transistor", "Semiconductor", "Printing press", "Electricity"
        ]

    @staticmethod
    def historical_events() -> List[str]:
        return [
            "World War II", "World War I", "French Revolution", "American Revolution", "Moon landing",
            "Fall of the Berlin Wall", "Industrial Revolution", "Age of Enlightenment", "Renaissance"
        ]

    @staticmethod
    def video_games() -> List[str]:
        return [
            "Minecraft", "The Legend of Zelda", "Pokémon", "Super Mario Bros.", "Tetris", "Dark Souls",
            "Portal (video game)", "Half-Life", "Doom (1993 video game)", "The Sims", "Grand Theft Auto V"
        ]

    @staticmethod
    def memes() -> List[str]:
        return [
            "Rickrolling", "Doge (meme)", "Pepe the Frog", "Loss (comic)", "Wojak", "Big Chungus",
            "Stonks", "Distracted boyfriend", "Hide the Pain Harold", "Woman yelling at a cat"
        ]


# Archipelago Options
class WikipediaGameIncludeSpecificPaths(DefaultOnToggle):
    """
    Indicates whether to include objectives with specific pre-defined Wikipedia paths
    (e.g., 'Napoleon' to 'France', 'Banana' to 'Germany').
    """
    display_name = "Wikipedia Game: Include Specific Paths"


class WikipediaGameIncludeCategoryPaths(Toggle):
    """
    Indicates whether to include objectives with category-based paths
    (e.g., 'a country' to 'a scientist'). Disabled by default because
    specific article paths tend to feel more focused.
    """
    display_name = "Wikipedia Game: Include Category Paths"
    default = 0


class WikipediaGameIncludeRandomPaths(Toggle):
    """
    Indicates whether to include objectives using Wikipedia's Random Article feature.
    These are more challenging as the start/end articles are unknown.
    """
    display_name = "Wikipedia Game: Include Random Paths"


class WikipediaGameMaxClicks(Range):
    """
    Maximum number of clicks allowed for Wikipedia path objectives.
    Lower values make the game more challenging.
    """
    display_name = "Wikipedia Game: Maximum Clicks"
    range_start = 3
    range_end = 10
    default = 6
