from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import DefaultOnToggle, OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


@dataclass
class Rocksmith2014ArchipelagoOptions:
    rocksmith_2014_song_selection: Rocksmith2014SongSelection
    rocksmith_2014_dlc_packs_owned: Rocksmith2014DlcPacksOwned
    rocksmith_2014_owned_song_overrides: Rocksmith2014OwnedSongOverrides
    rocksmith_2014_excluded_songs: Rocksmith2014ExcludedSongs
    rocksmith_2014_cdlc_songs: Rocksmith2014CdlcSongs
    rocksmith_2014_available_arrangements: Rocksmith2014AvailableArrangements
    rocksmith_2014_include_rs1_import_songs: Rocksmith2014IncludeRs1ImportSongs
    rocksmith_2014_include_score_attack: Rocksmith2014IncludeScoreAttack
    rocksmith_2014_include_lessons: Rocksmith2014IncludeLessons
    rocksmith_2014_include_session_mode: Rocksmith2014IncludeSessionMode
    rocksmith_2014_include_guitarcade: Rocksmith2014IncludeGuitarcade
    rocksmith_2014_include_missions: Rocksmith2014IncludeMissions


class Rocksmith2014Game(Game):
    name = "Rocksmith 2014"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.X360,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = Rocksmith2014ArchipelagoOptions

    @property
    def include_score_attack(self) -> bool:
        return self.archipelago_options.rocksmith_2014_include_score_attack.value

    @property
    def include_lessons(self) -> bool:
        return self.archipelago_options.rocksmith_2014_include_lessons.value

    @property
    def include_session_mode(self) -> bool:
        return self.archipelago_options.rocksmith_2014_include_session_mode.value

    @property
    def include_guitarcade(self) -> bool:
        return self.archipelago_options.rocksmith_2014_include_guitarcade.value

    @property
    def include_missions(self) -> bool:
        return self.archipelago_options.rocksmith_2014_include_missions.value

    @property
    def include_rs1_import_songs(self) -> bool:
        return self.archipelago_options.rocksmith_2014_include_rs1_import_songs.value

    @property
    def available_arrangements(self) -> List[str]:
        return sorted(self.archipelago_options.rocksmith_2014_available_arrangements.value)

    @property
    def dlc_packs_owned(self) -> List[str]:
        return sorted(self.archipelago_options.rocksmith_2014_dlc_packs_owned.value)

    @property
    def owned_song_overrides(self) -> List[str]:
        return sorted(self.archipelago_options.rocksmith_2014_owned_song_overrides.value)

    @property
    def excluded_songs(self) -> List[str]:
        return sorted(self.archipelago_options.rocksmith_2014_excluded_songs.value)

    @property
    def cdlc_songs(self) -> List[str]:
        return sorted(self.archipelago_options.rocksmith_2014_cdlc_songs.value)

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(label="No Riff Repeater usage", data={}),
            GameObjectiveTemplate(label="No pausing during a song", data={}),
            GameObjectiveTemplate(label="No visual note highway (audio only) for one song", data={}),
            GameObjectiveTemplate(label="Use a clean tone only", data={}),
            GameObjectiveTemplate(label="Play standing up", data={}),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Play SONG on ARRANGEMENT",
                data={
                    "SONG": (self.songs, 1),
                    "ARRANGEMENT": (self.arrangements, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Reach MASTERY% mastery on SONG (ARRANGEMENT)",
                data={
                    "MASTERY": (self.mastery_targets, 1),
                    "SONG": (self.songs, 1),
                    "ARRANGEMENT": (self.arrangements, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Practice TECHNIQUE for DURATION",
                data={
                    "TECHNIQUE": (self.techniques, 1),
                    "DURATION": (self.practice_durations, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a Riff Repeater section at TEMPO% with ACCURACY% accuracy",
                data={
                    "TEMPO": (self.tempo_targets, 1),
                    "ACCURACY": (self.accuracy_targets, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
        ]

        if self.include_score_attack:
            templates.append(
                GameObjectiveTemplate(
                    label="Earn RANK in Score Attack for SONG (ARRANGEMENT)",
                    data={
                        "RANK": (self.score_attack_ranks, 1),
                        "SONG": (self.songs, 1),
                        "ARRANGEMENT": (self.arrangements, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
            )

        if self.include_lessons:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete LESSON",
                    data={
                        "LESSON": (self.lessons, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            )

        if self.include_session_mode:
            templates.append(
                GameObjectiveTemplate(
                    label="Play Session Mode for DURATION focusing on STYLE",
                    data={
                        "DURATION": (self.session_durations, 1),
                        "STYLE": (self.session_styles, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            )

        if self.include_guitarcade:
            templates.append(
                GameObjectiveTemplate(
                    label="Play a round of GUITARCADE_GAME",
                    data={
                        "GUITARCADE_GAME": (self.guitarcade_games, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            )

        if self.include_missions:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete MISSION",
                    data={
                        "MISSION": (self.missions, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            )

        return templates

    def songs(self) -> List[str]:
        songs = list(self.archipelago_options.rocksmith_2014_song_selection.value)

        if self.include_rs1_import_songs:
            songs.extend(RS1_IMPORT_SONGS)

        for pack in self.dlc_packs_owned:
            songs.extend(DLC_PACK_SONGS.get(pack, []))

        songs.extend(self.owned_song_overrides)
        songs.extend(self.cdlc_songs)

        excluded = set(self.excluded_songs)

        unique = []
        seen = set()
        for song in songs:
            if song in excluded or song in seen:
                continue
            seen.add(song)
            unique.append(song)

        return sorted(unique)

    def arrangements(self) -> List[str]:
        return self.available_arrangements

    @staticmethod
    def mastery_targets() -> List[int]:
        return [50, 70, 85, 95, 100]

    @staticmethod
    def practice_durations() -> List[str]:
        return ["10 minutes", "15 minutes", "20 minutes", "30 minutes"]

    @staticmethod
    def tempo_targets() -> List[int]:
        return [70, 80, 90, 100]

    @staticmethod
    def accuracy_targets() -> List[int]:
        return [90, 95, 98]

    @staticmethod
    def score_attack_ranks() -> List[str]:
        return ["Bronze", "Silver", "Gold", "Platinum"]

    @staticmethod
    def lessons() -> List[str]:
        return [
            "Basic fretting",
            "Basic strumming",
            "Power chords",
            "Open chords",
            "Barre chords",
            "Scales and patterns",
            "Bends and vibrato",
            "Slides and shifts",
            "Hammer-ons and pull-offs",
            "Palm muting",
        ]

    @staticmethod
    def techniques() -> List[str]:
        return [
            "Alternate picking",
            "Chord changes",
            "String skipping",
            "Arpeggios",
            "Dynamics and accents",
            "Rhythm precision",
            "Lead phrasing",
            "Bass groove",
        ]

    @staticmethod
    def session_durations() -> List[str]:
        return ["10 minutes", "15 minutes", "20 minutes", "30 minutes"]

    @staticmethod
    def session_styles() -> List[str]:
        return ["Rock", "Blues", "Metal", "Funk", "Country", "Jazz", "Pop", "Indie"]

    @staticmethod
    def guitarcade_games() -> List[str]:
        return [
            "Ducks Redux",
            "Super Ducks",
            "String Skip Saloon",
            "Return to Castle Chordead",
            "Ninja Slide",
            "Scale Warriors",
            "Harmonic Heist",
            "Gone Wailin'",
        ]

    @staticmethod
    def missions() -> List[str]:
        return [
            "Master your first song",
            "Improve accuracy to 90%",
            "Reach 70% mastery on a song",
            "Complete a lesson set",
            "Play 3 songs in a row",
        ]

BASE_SONGS = [
    "Aching Head - Self-Destruct",
    "Aerosmith - Walk This Way",
    "Alice Cooper - No More Mr. Nice Guy",
    "Alice in Chains - Stone",
    "Arctic Monkeys - R U Mine?",
    "Avenged Sevenfold - Bat Country",
    "B'z - Ultra Soul",
    "Bedowyn - Snarling of Beasts",
    "Bob Dylan - Knockin' on Heaven's Door",
    "Boston - Peace of Mind",
    "Bush - Machinehead",
    "Crimson - Don't Stop",
    "The Dear Hunter - Stuck on a Wire Out on a Fence (Orange)",
    "Def Leppard - Pour Some Sugar on Me",
    "Deftones - My Own Summer (Shove It)",
    "Disonaur - Sea to Swallow",
    "EarlyRise - Wasteland",
    "Fang Island - Chompers",
    "Foo Fighters - Everlong",
    "Gold Motel - Brand New Kind of Blue",
    "Green Day - X-Kid",
    "Hail the Sun - Eight-Ball, Coroner's Pocket",
    "Iron Maiden - The Trooper",
    "Jack White - Sixteen Saltines",
    "JAWS - Stay In",
    "Joe Satriani - Satch Boogie",
    "Karawan - Desolate Motion",
    "The Kinks - You Really Got Me",
    "Kiss - Rock and Roll All Nite",
    "La Sera - Love That's Gone",
    "Magic Wands - Black Magic",
    "Mastodon - Blood and Thunder",
    "Matt Montgomery, Brian McCune, Brendan West - On Top of the World",
    "Minus the Bear - Cold Company",
    "Monster Truck - Sweet Mountain River",
    "Muse - Knights of Cydonia",
    "Nirvana - Heart-Shaped Box",
    "Oasis - Don't Look Back in Anger",
    "Pantera - Cemetery Gates",
    "Paramore - Now",
    "PAWS - Sore Tummy",
    "Playground Kings - Self Trap",
    "The Police - Every Breath You Take",
    "Queen - We Are the Champions",
    "R.E.M. - Losing My Religion",
    "Radiohead - Paranoid Android",
    "Ramones - Blitzkrieg Bop",
    "Ratt - Round and Round",
    "Red Fang - Wires",
    "Rise Against - Savior",
    "The Rolling Stones - Paint It Black",
    "Rush - The Spirit of Radio",
    "Sabaka - Monochromic",
    "Screaming Females - Rotten Apple",
    "The Shins - For a Fool",
    "Slayer - War Ensemble",
    "The Smashing Pumpkins - The Chimera",
    "Splashh - All I Wanna Do",
    "System of a Down - Hypnotize",
    "Tak Matsumoto - Go Further",
    "Tom Petty and the Heartbreakers - Mary Jane's Last Dance",
    "Ubisoft - Rocksmith 2012 Theme",
    "Versus Them - Impossible Dreams",
    "Weezer - Say It Ain't So",
    "White Zombie - Thunder Kiss '65",
    "The Who - My Generation",
]

# Rocksmith 1 import songs. Populate with importable tracks (excluding non-licensed).
RS1_IMPORT_SONGS: list[str] = [
    'The Animals - House of the Rising Sun',
    'Best Coast - When I\'m With You',
    'The Black Keys - I Got Mine',
    'The Black Keys - Next Girl',
    'Blur - Song 2',
    'The Boxer Rebellion - Step Out of the Car',
    'Brian Adan McCune - Ricochet',
    'The Cribs - We Share the Same Skies',
    'The Cure - Boys Don\'t Cry',
    'Dan Auerbach - I Want Some More',
    'David Bowie - Rebel Rebel',
    'The Dead Weather - I Can\'t Hear You',
    'Disonaur - Space Ostrich',
    'Franz Ferdinand - Take Me Out',
    'The Horrors - Do You Remember',
    'Incubus - I Miss You',
    'Interpol - Slow Hands',
    'Jarvis Cocker - Angela',
    'Jenny O. - Well OK Honey',
    'Kings of Leon - Use Somebody',
    'Lenny Kravitz - Are You Gonna Go My Way',
    'Little Barrie - Surf Hell',
    'Lynyrd Skynyrd - Sweet Home Alabama',
    'Muse - Unnatural Selection',
    'Muse - Plug In Baby',
    'Nirvana - In Bloom',
    'Nirvana - Breed',
    'Pixies - Where is My Mind?',
    'Queens of the Stone Age - Go With the Flow',
    'Radiohead - High and Dry',
    'RapScallions - California Brain',
    'Red Fang - Number Thirteen',
    'Red Hot Chili Peppers - Higher Ground',
    'The Rolling Stones - (I Can\'t Get No) Satisfaction',
    'The Rolling Stones - The Spider and the Fly',
    'The Rolling Stones - Play with Fire',
    'Sigur Rós - Gobbledigook',
    'Silversun Pickups - Panic Switch',
    'Soundgarden - Outshined',
    'Spoon - Me and the Bean',
    'Stone Temple Pilots - Between the Lines',
    'Stone Temple Pilots - Vasoline',
    'The Strokes - Under Cover of Darkness',
    'Taddy Porter - Mean Bitch',
    'Titus Andronicus - A More Perfect Union',
    'Tom Petty & The Heartbreakers - Good Enough',
    'Velvet Revolver - Slither',
    'Versus Them - Six AM Salvation',
    'White Denim - Burnished',
    'The White Stripes - Icky Thump',
    'The xx - Islands',
    'The Yellow Moon Band - Chimney',
]

# DLC packs mapped to their song lists.
# Format: {"Pack Name": ["Artist - Song", ...], ...}
DLC_PACK_SONGS: dict[str, list[str]] = {
    '2000s Mix III': [
        'Band of Horses - The Funeral',
        'Hinder - Lips of an Angel',
        'Kelly Clarkson - Breakaway',
    ],
    '2000s Mix IV': [
        'Dropkick Murphys - Johnny, I Hardly Knew Ya',
        'Modest Mouse - Dashboard',
        'Theory of a Deadman - Bad Girlfriend',
    ],
    '2000s Mix Pack': [
        'Against Me! - Thrash Unreal',
        'Between the Buried and Me - Selkies: The Endless Obsession',
        'Panic! at the Disco - Nine in the Afternoon',
    ],
    '2000s Mix Pack II': [
        'Crossfade - Cold',
        'Shinedown - Simple Man',
        'The Fray - How to Save a Life',
    ],
    '2000s Mix V': [
        'Drowning Pool - Bodies',
        "Fountains of Wayne - Stacy's Mom",
        'blink-182 - Always',
    ],
    '2000s Mix VI': [
        'Andrew W.K. - Party Hard',
        'Angels & Airwaves - The Adventure',
        'Coldplay - Shiver',
    ],
    '2010s Mix III': [
        'Bring Me the Horizon - Can You Feel My Heart',
        'Passenger - Let Her Go',
        'The Gaslight Anthem - 45',
    ],
    '2010s Mix IV': [
        'Bastille - Pompeii',
        'James Bay - Hold Back The River',
        'Two Door Cinema Club - What You Know',
    ],
    '2010s Mix Song Pack': [
        'Fall Out Boy - My Songs Know What You Did in the Dark (Light Em Up)',
        'Hail the Sun - Burn Nice and Slow (The Formative Years)',
        'The Neighbourhood - Sweater Weather',
    ],
    '2010s Mix Song Pack II': [
        'Awolnation - Sail',
        'Black Veil Brides - In The End',
        'Walk The Moon - Shut Up And Dance',
    ],
    '2010s Mix V': [
        'Coldplay - Paradise',
        "Elle King - Ex's & Oh's",
        'The War on Drugs - Red Eyes',
    ],
    '3 Doors Down 3-Song Pack': [
        '3 Doors Down - Kryptonite',
        '3 Doors Down - Loser',
        "3 Doors Down - When I'm Gone",
    ],
    '3 Doors Down II': [
        '3 Doors Down - Away From The Sun',
        '3 Doors Down - Be Like That',
        '3 Doors Down - Here Without You',
        "3 Doors Down - It's Not My Time",
        '3 Doors Down - Let Me Go',
    ],
    '311 3-Song Pack': [
        '311 - Amber',
        '311 - Beautiful Disaster',
        '311 - Down',
    ],
    '38 Special 3-Song Pack': [
        '38 Special - Caught Up In You',
        '38 Special - Hold On Loosely',
        '38 Special - Rockin’ Into The Night',
    ],
    '5 Seconds of Summer': [
        '5 Seconds of Summer - Amnesia',
        '5 Seconds of Summer - She Looks So Perfect',
        "5 Seconds of Summer - She's Kinda Hot",
    ],
    "50's Singles": [
        'Bill Haley & His Comets - Rock around the Clock',
        'Ritchie Valens - La Bamba',
        'The Champs - Tequila',
    ],
    '60s Mix II': [
        "Booker T. & the M.G.'s - Green Onions",
        'Jefferson Airplane - Somebody To Love',
        "The Mamas & The Papas - California Dreamin'",
    ],
    '60s Mix III': [
        'Deep Purple - Hush',
        'Joe South - Games People Play',
        'The Youngbloods - Get Together',
    ],
    '60s Mix Pack': [
        'Jefferson Airplane - White Rabbit',
        'Shocking Blue - Venus',
        'The Doors - Love Me Two Times',
    ],
    '70s Mix II': [
        'Jim Croce - Time in a Bottle',
        'Peter Frampton - Do You Feel Like We Do',
        'Thin Lizzy - Cowboy Song',
    ],
    '70s Mix III': [
        'Golden Earring - Radar Love',
        "Grand Funk Railroad - We're an American Band",
        'Jethro Tull - Aqualung',
    ],
    '70s Mix IV': [
        'Buzzcocks - Ever Fallen In Love',
        'George Thorogood & The Destroyers - Who Do You Love',
        'Steve Miller Band - Jungle Love',
    ],
    '70s Mix Song Pack': [
        'George Baker Selection - Little Green Bag',
        'The Clash - I Fought the Law',
        'Thin Lizzy - Emerald',
    ],
    '70s Mix V': [
        'Commodores - Brick House',
        'Funkadelic - Maggot Brain',
        'The Hollies - Long Cool Woman in a Black Dress',
    ],
    '70s Mix VI': [
        "Carly Simon - You're So Vain",
        'Chicago - Saturday in the Park',
        'George Benson - Breezin',
    ],
    '70s Rock Singles': [
        'Deep Purple - Highway Star',
        'Lynyrd Skynyrd - Simple Man',
        'Ted Nugent - Stranglehold',
    ],
    "80's Mix Pack": [
        'Devo - Girl U Want',
        'Extreme - Play With Me',
        'Judas Priest - Electric Eye',
    ],
    '80s Mix III': [
        'Black Flag - Rise Above',
        'Queen - I Want It All',
        'REO Speedwagon - Take It On The Run',
    ],
    '80s Mix IV': [
        'Huey Lewis and the News - Hip to Be Square',
        'Ratt - Lay It Down',
        'Steve Winwood - Higher Love',
    ],
    '80s Mix Pack II': [
        'Kenny Loggins - Footloose',
        "Simple Minds - Don't You (Forget About Me)",
        'Twisted Sister - I Wanna Rock',
    ],
    '80s Mix V': [
        'Billy Squier - Lonely Is The Night',
        "Earth, Wind & Fire - Let's Groove",
        'Styx - Too Much Time on My Hands',
    ],
    '80s Mix VI': [
        'A-ha - Take On Me',
        'Poison - Fallen Angel',
        'The Georgia Satellites - Keep Your Hands to Yourself',
    ],
    '90s Mix II': [
        'Eve 6 - Inside Out',
        'Hole - Violet',
        'Tonic - If You Could Only See',
    ],
    '90s Mix III': [
        "Spin Doctors - Little Miss Can't Be Wrong",
        'Supergrass - Alright',
        'Tom Cochrane - Life Is a Highway',
    ],
    '90s Mix IV': [
        'Godsmack - Keep Away',
        'New Radicals - You Get What You Give',
        'Veruca Salt - Volcano Girls',
    ],
    '90s Mix Song Pack': [
        'Everclear - Santa Monica',
        'Filter - Hey Man Nice Shot',
        'Reel Big Fish - Beer',
    ],
    '90s Mix V': [
        'Helmet - Unsung',
        'Joe Satriani - Summer Song',
        'Type O Negative - Christian Woman',
    ],
    '90s Mix VI': [
        'Green Day - When I Come Around',
        'Joan Osborne - One of Us',
        "Stone Temple Pilots - Trippin' On a Hole in a Paper Heart",
    ],
    '90s Rock Singles': [
        'Everclear - Father of Mine',
        'Silverchair - Tomorrow',
        'Spin Doctors - Two Princes',
    ],
    'A Day to Remember 5-Song Pack': [
        'A Day to Remember - All I Want',
        'A Day to Remember - All Signs Point to Lauderdale',
        'A Day to Remember - If It Means a Lot to You',
        "A Day to Remember - It's Complicated",
        'A Day to Remember - The Downfall of Us All',
    ],
    'ABBA Song Pack': [
        'ABBA - Dancing Queen',
        'ABBA - Fernando',
        'ABBA - Mamma Mia',
    ],
    'AFI 4-Song Pack': [
        "AFI - Girl's Not Grey",
        'AFI - Miss Murder',
        'AFI - Silver and Cold',
        'AFI - Totalimmortal',
    ],
    'Aerosmith 5-Song Pack': [
        'Aerosmith - Dream On',
        'Aerosmith - Legendary Child',
        'Aerosmith - Oh Yeah',
        'Aerosmith - Same Old Song and Dance',
        'Aerosmith - Sweet Emotion',
    ],
    'Aerosmith Song Pack II': [
        'Aerosmith - Crazy',
        'Aerosmith - Love In An Elevator',
        "Aerosmith - Train Kept a Rollin'",
    ],
    'Airbourne Pack': [
        'Airbourne - Blonde, Bad and Beautiful',
        "Airbourne - Runnin' Wild",
        'Airbourne - Too Much, Too Young, Too Fast',
    ],
    'Alabama Shakes Pack': [
        'Alabama Shakes - Always Alright',
        "Alabama Shakes - Don't Wanna Fight",
        'Alabama Shakes - Gimme All Your Love',
        'Alabama Shakes - Hold On',
    ],
    'Alice Cooper Pack': [
        'Alice Cooper - Billion Dollar Babies',
        'Alice Cooper - Poison',
        "Alice Cooper - School's Out",
    ],
    'Alice in Chains 5-Song Pack': [
        'Alice in Chains - Check My Brain',
        'Alice in Chains - Hollow',
        'Alice in Chains - Man in the Box',
        'Alice in Chains - Them Bones',
        'Alice in Chains - Would?',
    ],
    'Alice in Chains II': [
        'Alice in Chains - Down In A Hole',
        'Alice in Chains - Heaven Beside You',
        'Alice in Chains - No Excuses',
        'Alice in Chains - Nutshell',
        'Alice in Chains - Rooster',
    ],
    'All That Remains Song Pack': [
        'All That Remains - Six',
        'All That Remains - This Calling',
        'All That Remains - Two Weeks',
    ],
    'All Time Low Song Pack': [
        'All Time Low - Dear Maria, Count Me In',
        'All Time Low - Somewhere in Neverland',
        'All Time Low - Weightless',
    ],
    'Alter Bridge 4-Song Pack': [
        'Alter Bridge - Blackbird',
        'Alter Bridge - Isolation',
        'Alter Bridge - Rise Today',
        'Alter Bridge - Ties That Bind',
    ],
    'Alternative Rock Singles': [
        'Dinosaur Jr. - Feel the Pain',
        'Fuel - Hemorrhage (In My Hands)',
        'Lit - My Own Worst Enemy',
        'Stone Sour - Through Glass',
        'Yellowcard - Ocean Avenue',
    ],
    'Amaranthe Pack': [
        'Amaranthe - Amaranthine',
        'Amaranthe - Drop Dead Cynical',
        'Amaranthe - The Nexus',
    ],
    'Amon Amarth Pack': [
        'Amon Amarth - Death in Fire',
        'Amon Amarth - Guardians of Asgaard',
        'Amon Amarth - The Pursuit of Vikings',
        'Amon Amarth - Twilight of the Thunder God',
        'Amon Amarth - War of the Gods',
    ],
    'Anniversary Song Pack': [
        'Bob Marley & The Wailers - Three Little Birds',
        'Elvis Presley - Suspicious Minds',
        'Jackson 5 - I Want You Back',
        'OutKast - Hey Ya!',
        'Train - Drops of Jupiter',
        'fun. - Some Nights',
    ],
    'Anthrax 4-Song Pack': [
        'Anthrax - Caught In A Mosh',
        'Anthrax - Got The Time',
        'Anthrax - Indians',
        'Anthrax - Madhouse',
    ],
    'Arena Rock Singles': [
        'Autograph - Turn Up the Radio',
        'Billy Squier - The Stroke',
        'Dio - Holy Diver',
        "Poison - Nothin' But A Good Time",
        'Winger - Seventeen',
    ],
    'Audioslave 5-Song Pack': [
        'Audioslave - Be Yourself',
        'Audioslave - Cochise',
        'Audioslave - I Am the Highway',
        'Audioslave - Like a Stone',
        'Audioslave - Show Me How to Live',
    ],
    'Avenged Sevenfold 3-Song Pack': [
        'Avenged Sevenfold - Afterlife',
        'Avenged Sevenfold - Beast and the Harlot',
        'Avenged Sevenfold - Nightmare',
    ],
    'Avril Lavigne Pack': [
        'Avril Lavigne - Complicated',
        "Avril Lavigne - I'm With You",
        'Avril Lavigne - My Happy Ending',
        'Avril Lavigne - Sk8er Boi',
        "Avril Lavigne - When You're Gone",
    ],
    "B'z 3-Song Pack": [
        "B'z - Easy Come, Easy Go!",
        "B'z - Giri Giri chop",
        "B'z - juice",
    ],
    'Bachman-Turner Overdrive Pack': [
        'Bachman-Turner Overdrive - Let It Ride',
        "Bachman-Turner Overdrive - Takin' Care of Business",
        "Bachman-Turner Overdrive - You Ain't Seen Nothing Yet",
    ],
    'Bachsmith 2 5-Song Pack': [
        'Frédéric Chopin - Funeral March',
        'Jacques Offenbach - The Can-Can',
        'Ludwig van Beethoven - Ode to Joy',
        'Pyotr Ilyich Tchaikovsky - Notecracker Medley',
        'Wolfgang Amadeus Mozart - Symphony No. 40',
    ],
    'Bachsmith 5-Song Pack': [
        'Edvard Grieg - In the Hall of the Mountain King',
        'Johann Sebastian Bach - "Little" Fugue in G minor',
        'Ludwig van Beethoven - Moonlight Sonata: Adagio Sostenuto',
        'Richard Wagner - Ride of the Valkyries',
        'Wolfgang Amadeus Mozart - Rondo alla Turca',
    ],
    'Bad Religion Song Pack': [
        'Bad Religion - 21st Century (Digital Boy)',
        'Bad Religion - American Jesus',
        'Bad Religion - Infected',
        'Bad Religion - Sorrow',
    ],
    'Beastie Boys Pack': [
        'Beastie Boys - Fight for Your Right',
        'Beastie Boys - No Sleep Till Brooklyn',
        'Beastie Boys - Sabotage',
    ],
    'Biffy Clyro 5-Song Pack': [
        'Biffy Clyro - Black Chandelier',
        'Biffy Clyro - Bubbles',
        'Biffy Clyro - Many of Horror',
        'Biffy Clyro - Mountains',
        "Biffy Clyro - Stingin' Belle",
    ],
    'Billy Talent 5-Song Pack': [
        'Billy Talent - Devil in a Midnight Mass',
        'Billy Talent - Fallen Leaves',
        'Billy Talent - Red Flag',
        'Billy Talent - Try Honesty',
        'Billy Talent - Viking Death March',
    ],
    'Black Label Society Song Pack': [
        'Black Label Society - Overlord',
        'Black Label Society - Stillborn',
        'Black Label Society - Suicide Messiah',
    ],
    'Blink-182 3-Song Pack': [
        'Blink-182 - All The Small Things',
        'Blink-182 - Dammit',
        "Blink-182 - What's My Age Again?",
    ],
    'Bloodhound Gang Pack': [
        'Bloodhound Gang - Foxtrot Uniform Charlie Kilo',
        'Bloodhound Gang - The Bad Touch',
        'Bloodhound Gang - The Ballad of Chasey Lain',
    ],
    'Blue Öyster Cult 3-Song Pack': [
        "Blue Öyster Cult - (Don't Fear) The Reaper",
        "Blue Öyster Cult - Burnin' For You",
        'Blue Öyster Cult - Godzilla',
    ],
    'Blues Hits': [
        'Albert King with Stevie Ray Vaughan - Born Under a Bad Sign',
        'B.B. King - The Thrill is Gone',
        'The Blues Brothers - Soul Man',
    ],
    'Blues Rock Song Pack': [
        'Joe Bonamassa - Sloe Gin',
        'Kenny Wayne Shepherd - Blue on Black',
        'Philip Sayce - Out Of My Mind',
    ],
    'Blues Song Pack': [
        'Bobby "Blue" Bland - Ain’t No Love In The Heart Of The City',
        'Freddie King - Hide Away',
        'Howlin’ Wolf - Spoonful',
        'John Lee Hooker - Boom Boom',
        'Johnny Winter - Be Careful with a Fool',
    ],
    'Blues Song Pack II': [
        'John Lee Hooker - One Bourbon, One Scotch, One Beer',
        'Wes Montgomery - West Coast Blues',
        'Willie Dixon - Back Door Man',
    ],
    'Blues Song Pack III': [
        'Freddie King - Going Down',
        'John Lee Hooker - San Francisco',
        'Shuggie Otis - Bootie Cooler',
    ],
    'Bob Dylan 3-Song Pack': [
        'Bob Dylan - Just Like a Woman',
        'Bob Dylan - Like a Rolling Stone',
        'Bob Dylan - Subterranean Homesick Blues',
    ],
    'Bob Marley and the Wailers Pack': [
        'Bob Marley and the Wailers - Buffalo Soldier',
        'Bob Marley and the Wailers - Could You Be Loved',
        'Bob Marley and the Wailers - Is This Love',
        'Bob Marley and the Wailers - No Woman, No Cry',
        'Bob Marley and the Wailers - Redemption Song',
    ],
    'Bon Jovi 5-Song Pack': [
        'Bon Jovi - Blaze of Glory',
        "Bon Jovi - It's My Life",
        "Bon Jovi - Livin' on a Prayer",
        'Bon Jovi - Wanted Dead or Alive',
        'Bon Jovi - You Give Love a Bad Name',
    ],
    'Boston 3-Song Pack': [
        "Boston - Don't Look Back",
        'Boston - Foreplay/Long Time',
        'Boston - Hitch a Ride',
    ],
    'Brad Paisley Pack': [
        'Brad Paisley - Mud on the Tires',
        'Brad Paisley - Ticks',
        'Brad Paisley ft. Alison Krauss - Whiskey Lullaby',
    ],
    'Brand New Song Pack': [
        "Brand New - Okay I Believe You, But My Tommy Gun Don't",
        'Brand New - Sic Transit Gloria... Glory Fades',
        'Brand New - The Quiet Things That No One Ever Knows',
    ],
    'Breaking Benjamin Song Pack': [
        'Breaking Benjamin - Blow Me Away',
        'Breaking Benjamin - Polyamorous',
        'Breaking Benjamin - So Cold',
    ],
    'Bullet for My Valentine 5-Song Pack': [
        'Bullet for My Valentine - Hand of Blood',
        'Bullet for My Valentine - Hearts Burst into Fire',
        'Bullet for My Valentine - Scream Aim Fire',
        "Bullet for My Valentine - Tears Don't Fall",
        'Bullet for My Valentine - Your Betrayal',
    ],
    'Bush 4-Song Pack': [
        'Bush - Comedown',
        'Bush - Everything Zen',
        'Bush - Glycerine',
        'Bush - Swallowed',
    ],
    'Cake 5-Song Pack': [
        'Cake - I Will Survive',
        'Cake - Never There',
        'Cake - Short Skirt/Long Jacket',
        'Cake - Stickshifts and Safetybelts',
        'Cake - The Distance',
    ],
    'Cat Stevens Pack': [
        'Cat Stevens - Father and Son',
        'Cat Stevens - Morning Has Broken',
        'Cat Stevens - Wild World',
    ],
    'Chevelle Song Pack': [
        'Chevelle - Hats Off to the Bull',
        'Chevelle - The Red',
        'Chevelle - Vitamin R (Leading Us Along)',
    ],
    'Chris Stapleton Song Pack': [
        'Chris Stapleton - Nobody to Blame',
        'Chris Stapleton - Parachute',
        'Chris Stapleton - Tennessee Whiskey',
    ],
    'Christmas Classics': [
        "Brenda Lee - Rockin' Around The Christmas Tree",
        'Chuck Berry - Run, Rudolph, Run',
        'Elvis Presley - Blue Christmas',
        'Gene Autry - Rudolph The Red-Nosed Reindeer',
    ],
    'Chuck Berry Pack': [
        'Chuck Berry - Johnny B. Goode',
        'Chuck Berry - School Day (Ring! Ring! Goes the Bell)',
        'Chuck Berry - You Never Can Tell',
    ],
    'Classic Country Song Pack': [
        "Hank Williams - I'm So Lonesome I Could Cry",
        'Roger Miller - King of the Road',
        'Willie Nelson - On the Road Again',
    ],
    'Classic Melody Pack': [
        'The Notetrackers - Amazing Grace',
        'The Notetrackers - Frere Jacques',
        'The Notetrackers - When the Saints Go Marching In',
    ],
    'Classic Riff Singles': [
        'Dio - Rainbow in the Dark',
        'Motörhead - Ace of Spades',
        'Rick Derringer - Rock and Roll, Hoochie Koo',
        'Styx - Renegade',
        'Warrant - Cherry Pie',
    ],
    'Classic Singles': [
        "Bill Withers - Ain't No Sunshine",
        'James Gang - Funk #49',
        'Roy Buchanan - Sweet Dreams',
    ],
    'Coldplay Pack': [
        'Coldplay - Clocks',
        'Coldplay - Fix You',
        'Coldplay - In My Place',
        'Coldplay - The Scientist',
        'Coldplay - Viva La Vida',
        'Coldplay - Yellow',
    ],
    'Collective Soul 5-Song Pack': [
        'Collective Soul - December',
        'Collective Soul - Gel',
        'Collective Soul - Heavy',
        'Collective Soul - Shine',
        'Collective Soul - The World I Know',
    ],
    'Creed 5-Song Pack': [
        'Creed - Higher',
        'Creed - My Own Prison',
        'Creed - My Sacrifice',
        'Creed - One Last Breath',
        'Creed - With Arms Wide Open',
    ],
    'Creedence Clearwater Revival': [
        'Creedence Clearwater Revival - Bad Moon Rising',
        'Creedence Clearwater Revival - Fortunate Son',
        'Creedence Clearwater Revival - Proud Mary',
    ],
    'Crobot 3-Song Pack': [
        'Crobot - Fly On The Wall',
        'Crobot - Legend Of The Spaceborne Killer',
        'Crobot - Nowhere To Hide',
    ],
    'Cyndi Lauper Pack': [
        'Cyndi Lauper - Girls Just Want To Have Fun',
        'Cyndi Lauper - Time After Time',
        'Cyndi Lauper - True Colors',
    ],
    'Daughtry Song Pack': [
        'Daughtry - Feels Like Tonight',
        'Daughtry - Home',
        'Daughtry - Over You',
    ],
    'Deftones 4-Song Pack': [
        'Deftones - Be Quiet and Drive (Far Away)',
        'Deftones - Change (In the House of Flies)',
        'Deftones - Digital Bath',
        'Deftones - Hole in the Earth',
    ],
    'Dethklok 3-Song Pack': [
        'Dethklok - Awaken',
        'Dethklok - Go Into The Water',
        'Dethklok - Thunderhorse',
    ],
    'Dethklok II': [
        'Dethklok - Black Fire Upon Us',
        'Dethklok - Bloodlines',
        'Dethklok - Murmaider',
    ],
    'Disturbed 3-Song Pack': [
        'Disturbed - Asylum',
        'Disturbed - Down with the Sickness',
        'Disturbed - Voices',
    ],
    'Disturbed Song Pack II': [
        'Disturbed - Indestructible',
        'Disturbed - Inside the Fire',
        'Disturbed - Stricken',
        'Disturbed - Ten Thousand Fists',
        'Disturbed - The Night',
    ],
    'Dream Theater Song Pack': [
        'Dream Theater - Metropolis—Part I: "The Miracle and the Sleeper"',
        'Dream Theater - On the Backs of Angels',
        'Dream Theater - Pull Me Under',
    ],
    'Duran Duran 3-Song Pack': [
        'Duran Duran - Hungry Like The Wolf',
        'Duran Duran - Ordinary World',
        'Duran Duran - Rio',
    ],
    'Earth, Wind & Fire 3 Song Pack': [
        'Earth, Wind & Fire - September',
        'Earth, Wind & Fire - Shining Star',
        'Earth, Wind & Fire - Sing a Song',
    ],
    'Evanescence Pack': [
        "Evanescence - Everybody's Fool",
        'Evanescence - Going Under',
        'Evanescence - My Immortal',
    ],
    'Faith No More Song Pack': [
        'Faith No More - Digging the Grave',
        'Faith No More - Epic',
        'Faith No More - Falling to Pieces',
        'Faith No More - From Out of Nowhere',
        'Faith No More - Midlife Crisis',
    ],
    'Fall Out Boy 5-Song Pack': [
        "Fall Out Boy - America's Suitehearts",
        'Fall Out Boy - Dance, Dance',
        "Fall Out Boy - I Don't Care",
        "Fall Out Boy - Sugar, We're Goin Down",
        'Fall Out Boy - Thnks fr th Mmrs',
    ],
    'Female Lead Singles': [
        'Flyleaf - All Around Me',
        'Halestorm - Love Bites (So Do I)',
        'Heart - Crazy on You',
    ],
    'Five Finger Death Punch Pack': [
        'Five Finger Death Punch - Bad Company',
        'Five Finger Death Punch - The Bleeding',
        'Five Finger Death Punch - Wrong Side of Heaven',
    ],
    'Flyleaf Song Pack': [
        'Flyleaf - Again',
        'Flyleaf - Cassie',
        'Flyleaf - Fully Alive',
        'Flyleaf - Missing',
    ],
    'Foo Fighters 5-Song Pack': [
        'Foo Fighters - Best of You',
        'Foo Fighters - My Hero',
        'Foo Fighters - Times Like These',
        'Foo Fighters - Walk',
        'Foo Fighters - Wheels',
    ],
    'Foo Fighters II 5-Song Pack': [
        'Foo Fighters - Learn to Fly',
        'Foo Fighters - Long Road to Ruin',
        'Foo Fighters - Monkey Wrench',
        'Foo Fighters - Rope',
        'Foo Fighters - The Pretender',
    ],
    'Foreigner 5-Song Pack': [
        'Foreigner - Cold as Ice',
        'Foreigner - Double Vision',
        'Foreigner - Feels Like the First Time',
        'Foreigner - Hot Blooded',
        'Foreigner - Juke Box Hero',
    ],
    'Four Tops Pack': [
        'Four Tops - Bernadette',
        "Four Tops - I Can't Help Myself (Sugar Pie Honey Bunch)",
        "Four Tops - It's the Same Old Song",
        "Four Tops - Reach Out I'll Be There",
    ],
    'Funk Hits': [
        'Chic - Good Times',
        'Parliament - Give Up the Funk (Tear the Roof off the Sucker)',
        'Rick James - Super Freak',
    ],
    'Garbage 3-Song Pack': [
        "Garbage - I Think I'm Paranoid",
        'Garbage - Only Happy When it Rains',
        'Garbage - Stupid Girl',
    ],
    'Gary Moore Pack': [
        'Gary Moore - Over The Hills And Far Away',
        'Gary Moore - Still Got The Blues',
        'Gary Moore - The Loner',
    ],
    'Ghost Pack': [
        'Ghost - Cirice',
        'Ghost - He Is',
        'Ghost - Ritual',
        'Ghost - Year Zero',
    ],
    'Godsmack 5-Song Pack': [
        'Godsmack - Awake',
        "Godsmack - Cryin' Like a Bitch",
        'Godsmack - I Stand Alone',
        'Godsmack - Love-Hate-Sex-Pain',
        'Godsmack - Voodoo',
    ],
    'Golden Bomber 3-Song Pack': [
        'Golden Bomber - Death Mental',
        'Golden Bomber - Earphone',
        'Golden Bomber - Memeshikute',
    ],
    'Good Charlotte Song Pack': [
        'Good Charlotte - Girls & Boys',
        'Good Charlotte - I Just Wanna Live',
        'Good Charlotte - Lifestyles of the Rich & Famous',
        'Good Charlotte - The Anthem',
        'Good Charlotte - The River',
    ],
    'Grateful Dead Pack': [
        'Grateful Dead - Casey Jones',
        'Grateful Dead - Friend of the Devil',
        'Grateful Dead - Sugar Magnolia',
        "Grateful Dead - Truckin'",
        "Grateful Dead - Uncle John's Band",
    ],
    'Great White Song Pack': [
        'Great White - House of Broken Love',
        'Great White - Once Bitten, Twice Shy',
        'Great White - Rock Me',
    ],
    'Green Day 3-Song Pack': [
        'Green Day - American Idiot',
        'Green Day - Basket Case',
        'Green Day - Oh Love',
    ],
    'Green Day II': [
        'Green Day - 21 Guns',
        'Green Day - Bang Bang',
        'Green Day - Good Riddance (Time of Your Life)',
        'Green Day - Longview',
        'Green Day - Wake Me Up When September Ends',
    ],
    'Green Day III': [
        'Green Day - Boulevard of Broken Dreams',
        'Green Day - Holiday',
        'Green Day - Jesus of Suburbia',
        'Green Day - Know Your Enemy',
        'Green Day - Welcome to Paradise',
    ],
    'Green Day IV': [
        'Green Day - Brain Stew',
        'Green Day - Father of All...',
        'Green Day - Fire, Ready, Aim',
    ],
    'Greta Van Fleet II': [
        'Greta Van Fleet - Edge Of Darkness',
        'Greta Van Fleet - When The Curtain Falls',
        "Greta Van Fleet - You're The One",
    ],
    'Greta Van Fleet Pack': [
        'Greta Van Fleet - Black Smoke Rising',
        'Greta Van Fleet - Highway Tune',
        'Greta Van Fleet - Safari Song',
    ],
    'Haim Song Pack': [
        "Haim - Don't Save Me",
        'Haim - Forever',
        'Haim - The Wire',
    ],
    'Halestorm Pack': [
        'Halestorm - I Get Off',
        'Halestorm - I Miss the Misery',
        'Halestorm - Mz. Hyde',
    ],
    'Heart Pack': [
        'Heart - Alone',
        'Heart - Straight On',
        'Heart - What About Love',
    ],
    'Hit Singles 4 4-Song Pack': [
        'A Perfect Circle - The Outsider',
        'Loverboy - Working For The Weekend',
        'Sublime - Badfish',
        'The Doobie Brothers - Long Train Runnin',
    ],
    'Hit Singles II Song Pack': [
        'David Bowie - Ziggy Stardust',
        'Def Leppard - Hysteria',
        'Foghat - Slow Ride',
        'Wolfmother - Joker and the Thief',
    ],
    'Hit Singles III 4-Song Pack': [
        'Asia - Heat Of The Moment',
        'Semisonic - Closing Time',
        'Wild Cherry - Play That Funky Music',
        'Wolfmother - Woman',
    ],
    'Hit Singles Song Pack': [
        'Def Leppard - Rock of Ages',
        'Fleetwood Mac - Go Your Own Way',
        'Jet - Are You Gonna Be My Girl',
        'Kansas - Dust in the Wind',
    ],
    'Hit Singles V 4-Song Pack': [
        'Eddie Cochran - Summertime Blues',
        'Edgar Winter - Free Ride',
        'Hoobastank - The Reason',
        "The Cars - My Best Friend's Girl",
    ],
    'Holiday 3-Song Pack': [
        'Brian Adam McCune - God Rest Ye Merry, Gentlemen',
        'Seth Chapla - Carol of the Bells',
        'Versus Them - We Three Kings',
    ],
    'Hotei 3-Song Pack': [
        'Hotei - Bambina',
        'Hotei - Battle Without Honor or Humanity',
        'Hotei - Thrill',
    ],
    'Imagine Dragons 3-Song Pack': [
        'Imagine Dragons - Demons',
        "Imagine Dragons - It's Time",
        'Imagine Dragons - Radioactive',
    ],
    'Incubus 3-Song Pack': [
        'Incubus - Anna Molly',
        'Incubus - Love Hurts',
        'Incubus - Wish You Were Here',
    ],
    'Incubus Pack II': [
        'Incubus - Drive',
        'Incubus - Megalomaniac',
        'Incubus - Pardon Me',
        'Incubus - Stellar',
    ],
    'Independence Day Song Pack': [
        'Boston - The Star-Spangled Banner/4th of July Reprise',
        'Brooks & Dunn - Only in America',
        'Don McLean - American Pie',
        'James Brown - Living in America',
    ],
    'Indie Rock': [
        'Aranbee Pop Symphony Orchestra - Bitter Sweet Symphony',
        'Snow Patrol - Chasing Cars',
        'X Ambassadors - Renegades',
    ],
    'Indie Rock Hits': [
        'Gary Clark Jr. - Bright Lights',
        'Grace Potter & The Nocturnals - Paris (Ooh La La)',
        'The Shins - Caring Is Creepy',
    ],
    'Indigo Girls Pack': [
        'Indigo Girls - Closer to Fine',
        'Indigo Girls - Galileo',
        'Indigo Girls - Power of Two',
    ],
    'Interpol Pack': [
        'Interpol - All The Rage Back Home',
        'Interpol - Evil',
        'Interpol - Obstacle 1',
        'Interpol - PDA',
    ],
    'Iron Maiden 5-Song Pack': [
        'Iron Maiden - 2 Minutes to Midnight',
        'Iron Maiden - Aces High',
        'Iron Maiden - Fear of the Dark',
        'Iron Maiden - Run to the Hills',
        'Iron Maiden - The Number of the Beast',
    ],
    "Jane's Addiction 5-Song Pack": [
        "Jane's Addiction - Been Caught Stealing",
        "Jane's Addiction - Jane Says",
        "Jane's Addiction - Just Because",
        "Jane's Addiction - Mountain Song",
        "Jane's Addiction - Superhero",
    ],
    'Janis Joplin Song Pack': [
        'Big Brother and the Holding Company - Piece of My Heart',
        'Big Brother and the Holding Company - Summertime',
        'Janis Joplin - Me and Bobby McGee',
    ],
    'Jeff Buckley 3-Song Pack': [
        'Jeff Buckley - Grace',
        'Jeff Buckley - Hallelujah',
        'Jeff Buckley - Last Goodbye',
    ],
    'Jimi Hendrix 12-Song Pack': [
        'The Jimi Hendrix Experience - Bold as Love',
        'The Jimi Hendrix Experience - Castles Made of Sand',
        'The Jimi Hendrix Experience - Fire',
        'The Jimi Hendrix Experience - Foxey Lady',
        'The Jimi Hendrix Experience - Freedom',
        'The Jimi Hendrix Experience - If 6 Was 9',
        'The Jimi Hendrix Experience - Little Wing',
        'The Jimi Hendrix Experience - Manic Depression',
        'The Jimi Hendrix Experience - Purple Haze',
        'The Jimi Hendrix Experience - Red House',
        'The Jimi Hendrix Experience - The Wind Cries Mary',
        'The Jimi Hendrix Experience - Voodoo Child (Slight Return)',
    ],
    'Jimmy Eat World Pack': [
        'Jimmy Eat World - Bleed American',
        'Jimmy Eat World - Sweetness',
        'Jimmy Eat World - The Middle',
    ],
    'Joan Jett Pack': [
        'Joan Jett & the Blackhearts - Crimson and Clover',
        'Joan Jett & the Blackhearts - I Hate Myself for Loving You',
        'Joan Jett - Bad Reputation',
    ],
    'John Mellencamp Song Pack': [
        'John Mellencamp - Jack & Diane',
        'John Mellencamp - Pink Houses',
        'John Mellencamp - Small Town',
    ],
    'Johnny Cash Song Pack I': [
        'Johnny Cash - Big River',
        'Johnny Cash - Folsom Prison Blues',
        'Johnny Cash - Give My Love to Rose',
        'Johnny Cash - Hey, Porter',
        'Johnny Cash - Jackson',
    ],
    'Johnny Cash Song Pack II': [
        'Johnny Cash - Cry! Cry! Cry!',
        'Johnny Cash - Get Rhythm',
        'Johnny Cash - I Walk the Line',
        'Johnny Cash - Ring of Fire',
        "Johnny Cash - Sunday Mornin' Comin' Down",
    ],
    'Joni Mitchell Pack': [
        'Joni Mitchell - A Case Of You',
        'Joni Mitchell - Big Yellow Taxi',
        'Joni Mitchell - Both Sides, Now',
    ],
    'Joy Division Song Pack': [
        'Joy Division - Disorder',
        'Joy Division - Love Will Tear Us Apart',
        'Joy Division - Transmission',
    ],
    'Judas Priest 3-Song Pack': [
        'Judas Priest - Breaking the Law',
        'Judas Priest - Living After Midnight',
        'Judas Priest - Painkiller',
    ],
    'KT Tunstall': [
        'KT Tunstall - Black Horse and the Cherry Tree',
        'KT Tunstall - Other Side Of The World',
        'KT Tunstall - Suddenly I See',
    ],
    'Kaiser Chiefs Pack': [
        'Kaiser Chiefs - I Predict A Riot',
        'Kaiser Chiefs - Never Miss A Beat',
        'Kaiser Chiefs - Ruby',
    ],
    'Kaleo': [
        'KALEO - All the Pretty Girls',
        'KALEO - No Good',
        'KALEO - Way Down We Go',
    ],
    'Kelly Clarkson Song Pack': [
        'Kelly Clarkson - Behind These Hazel Eyes',
        'Kelly Clarkson - My Life Would Suck Without You',
        'Kelly Clarkson - Since U Been Gone',
    ],
    'Killswitch Engage 3-Song Pack': [
        'Killswitch Engage - Holy Diver',
        'Killswitch Engage - My Curse',
        'Killswitch Engage - The End of Heartache',
    ],
    'Kiss 3-Song Pack': [
        'Kiss - Detroit Rock City',
        "Kiss - Heaven's On Fire",
        "Kiss - I Was Made for Lovin' You",
    ],
    'Kiss Song Pack 2': [
        'Kiss - God of Thunder',
        'Kiss - Love Gun',
        'Kiss - Strutter',
    ],
    'Lady Gaga Pack': [
        'Lady Gaga - Bad Romance',
        'Lady Gaga - Paparazzi',
        'Lady Gaga - Poker Face',
        'Lady Gaga - You and I',
    ],
    'Lamb of God 3-Song Pack': [
        'Lamb of God - Ghost Walking',
        'Lamb of God - Laid to Rest',
        'Lamb of God - Walk With Me in Hell',
    ],
    'Linkin Park 6-Song Pack': [
        'Linkin Park - Bleed It Out',
        'Linkin Park - Guilty All the Same',
        'Linkin Park - In The End',
        'Linkin Park - Numb',
        'Linkin Park - One Step Closer',
        "Linkin Park - What I've Done",
    ],
    'Live Pack': [
        'Live - All Over You',
        'Live - I Alone',
        'Live - Lightning Crashes',
        'Live - Selling the Drama',
        "Live - The Dolphin's Cry",
    ],
    'Love Singles Song Pack': [
        'Bill Withers - Lovely Day',
        'Steve Vai - For the Love of God',
        "The Cure - Friday I'm in Love",
    ],
    'Lynyrd Skynyrd Song Pack': [
        'Lynyrd Skynyrd - Call Me the Breeze',
        'Lynyrd Skynyrd - Gimme Three Steps',
        "Lynyrd Skynyrd - Tuesday's Gone",
    ],
    'Manic Street Preachers': [
        'Manic Street Preachers - A Design for Life',
        'Manic Street Preachers - If You Tolerate This Your Children Will Be Next',
        'Manic Street Preachers - Motorcycle Emptiness',
    ],
    'Marilyn Manson Pack': [
        'Marilyn Manson - Coma White',
        'Marilyn Manson - The Beautiful People',
        'Marilyn Manson - Tourniquet',
    ],
    'Maroon 5 3-Song Pack': [
        'Maroon 5 - Harder to Breathe',
        'Maroon 5 - Misery',
        'Maroon 5 - She Will Be Loved',
    ],
    'Mastodon 3-Song Pack': [
        'Mastodon - Black Tongue',
        'Mastodon - Colony of Birchmen',
        'Mastodon - Oblivion',
    ],
    'Matchbox Twenty 5-Song Pack': [
        'Matchbox Twenty - 3AM',
        "Matchbox Twenty - How Far We've Come",
        'Matchbox Twenty - Push',
        "Matchbox Twenty - She's So Mean",
        'Matchbox Twenty - Unwell',
    ],
    'Megadeth 3-Song Pack': [
        'Megadeth - Hangar 18',
        'Megadeth - Public Enemy No. 1',
        'Megadeth - Symphony of Destruction',
    ],
    'Megadeth Song Pack II': [
        'Megadeth - A Tout Le Monde',
        'Megadeth - Holy Wars… The Punishment Due',
        'Megadeth - Peace Sells',
        'Megadeth - Tornado Of Souls',
        'Megadeth - Trust',
    ],
    'Melissa Etheridge Song Pack': [
        'Melissa Etheridge - Come to My Window',
        'Melissa Etheridge - I Want To Come Over',
        "Melissa Etheridge - I'm The Only One",
    ],
    'Metal Mix': [
        'Darkthrone - Transilvanian Hunger',
        'Morbid Angel - Immortal Rites',
        'Testament - Souls of Black',
    ],
    'Metal Mix Pack II': [
        'Children of Bodom - Are You Dead Yet?',
        'Death - Crystal Mountain',
        'Machine Head - Davidian',
    ],
    'Mix Tape Song Pack': [
        'Blue Swede - Hooked on a Feeling',
        'David Bowie - Moonage Daydream',
        "Marvin Gaye & Tammi Terrell - Ain't No Mountain High Enough",
        'Raspberries - Go All the Way',
        'Redbone - Come and Get Your Love',
    ],
    'Muddy Waters Pack': [
        'Muddy Waters - Honey Bee',
        "Muddy Waters - I Can't Be Satisfied",
        'Muddy Waters - Mannish Boy',
        'Muddy Waters - Still a Fool',
    ],
    'Mumford & Sons Pack': [
        'Mumford & Sons - I Will Wait',
        'Mumford & Sons - Little Lion Man',
        'Mumford & Sons - The Cave',
    ],
    'Muse 5-Song Pack': [
        'Muse - Hysteria',
        'Muse - Muscle Museum',
        'Muse - Stockholm Syndrome',
        'Muse - Supermassive Black Hole',
        'Muse - Time Is Running Out',
    ],
    'My Chemical Romance 3-Song Pack': [
        'My Chemical Romance - Na Na Na (Na Na Na Na Na Na Na Na Na)',
        'My Chemical Romance - Planetary (GO!)',
        'My Chemical Romance - Welcome to the Black Parade',
    ],
    'My Chemical Romance II 5-Song Pack': [
        'My Chemical Romance - Dead!',
        'My Chemical Romance - Famous Last Words',
        'My Chemical Romance - Helena',
        "My Chemical Romance - I'm Not Okay (I Promise)",
        'My Chemical Romance - Teenagers',
    ],
    'Mötley Crüe 5-Song Pack': [
        'Mötley Crüe - Dr. Feelgood',
        'Mötley Crüe - Girls Girls Girls',
        'Mötley Crüe - Home Sweet Home',
        'Mötley Crüe - Kickstart My Heart',
        'Mötley Crüe - Shout At The Devil',
    ],
    'NOFX Pack': [
        'NOFX - Bob',
        'NOFX - Linoleum',
        'NOFX - Seeing Double At The Triple Rock',
        "NOFX - Stickin' In My Eye",
    ],
    'New Found Glory Pack': [
        'New Found Glory - All Downhill From Here',
        'New Found Glory - Hit or Miss',
        'New Found Glory - My Friends Over You',
    ],
    'Nickelback 3-Song Pack': [
        'Nickelback - Bottoms Up',
        'Nickelback - How You Remind Me',
        'Nickelback - Rockstar',
    ],
    'Night Ranger Pack': [
        'Night Ranger - (You Can Still) Rock in America',
        "Night Ranger - Don't Tell Me You Love Me",
        'Night Ranger - Sister Christian',
    ],
    'No Doubt 3-Song Pack': [
        "No Doubt - Don't Speak",
        'No Doubt - Ex-Girlfriend',
        'No Doubt - Spiderwebs',
    ],
    'Norah Jones Pack': [
        'Norah Jones - Come Away With Me',
        "Norah Jones - Don't Know Why",
        'Norah Jones - Sunrise',
    ],
    'Oasis 5-Song Pack': [
        'Oasis - Champagne Supernova',
        'Oasis - Live Forever',
        'Oasis - Some Might Say',
        'Oasis - Supersonic',
        'Oasis - Wonderwall',
    ],
    'Opeth Song Pack': [
        'Opeth - Blackwater Park',
        'Opeth - Bleak',
        'Opeth - Ghost of Perdition',
    ],
    'P.O.D Pack': [
        'P.O.D - Alive',
        'P.O.D - Boom',
        'P.O.D - Youth of the Nation',
    ],
    'Pantera 3-Song Pack': [
        'Pantera - Cowboys from Hell',
        'Pantera - Domination',
        'Pantera - Walk',
    ],
    'Papa Roach 3-Song Pack': [
        'Papa Roach - Getting Away With Murder',
        'Papa Roach - Last Resort',
        'Papa Roach - Scars',
    ],
    'Paramore Pack': [
        "Paramore - Ain't It Fun",
        'Paramore - Brick by Boring Brick',
        'Paramore - Crushcrushcrush',
        'Paramore - Pressure',
        'Paramore - Still Into You',
        'Paramore - The Only Exception',
    ],
    'Paramore Song Pack II': [
        'Paramore - Ignorance',
        'Paramore - Misery Business',
        'Paramore - Rose-Colored Boy',
    ],
    'Pat Benatar Song Pack': [
        'Pat Benatar - Heartbreaker',
        'Pat Benatar - Hell Is For Children',
        'Pat Benatar - We Belong',
    ],
    'Pearl Jam 3-Song Pack': [
        'Pearl Jam - Alive',
        'Pearl Jam - Black',
        'Pearl Jam - Jeremy',
    ],
    'Pearl Jam II': [
        'Pearl Jam - Do The Evolution',
        'Pearl Jam - Even Flow',
        'Pearl Jam - Last Exit',
        'Pearl Jam - Rearviewmirror',
        'Pearl Jam - Yellow Ledbetter',
    ],
    'Pixies Song Pack': [
        'Pixies - Debaser',
        'Pixies - Hey',
        'Pixies - Monkey Gone to Heaven',
        'Pixies - Wave of Mutilation',
    ],
    'Player Picks Song Pack': [
        'Accept - Balls to the Wall',
        'Edgar Winter Group - Frankenstein',
        'Free - All Right Now',
        'Tesla - Modern Day Cowboy',
    ],
    'Power Ballad Singles': [
        'Boston - Amanda',
        "Cinderella - Don't Know What You Got (Till It's Gone)",
        'Extreme - More Than Words',
        'Poison - Every Rose Has Its Thorn',
        'Tesla - Love Song',
    ],
    'Primus Song Pack': [
        'Primus - Jerry Was a Race Car Driver',
        'Primus - South Park Theme',
        'Primus - Tommy the Cat',
        "Primus - Wynona's Big Brown Beaver",
    ],
    'Queen 5-Song Pack': [
        'Queen - Bohemian Rhapsody',
        'Queen - Fat Bottomed Girls',
        'Queen - Keep Yourself Alive',
        'Queen - Killer Queen',
        'Queen - Stone Cold Crazy',
    ],
    'Queen Pack II': [
        "Queen - Don't Stop Me Now",
        'Queen - Love Of My Life',
        'Queen - Tie Your Mother Down',
        'Queen - We Will Rock You',
    ],
    'Queen Pack III': [
        'Queen - Hammer To Fall',
        'Queen - I Want To Break Free',
        'Queen - Somebody To Love',
    ],
    'Queens of the Stone Age 5-Song Pack': [
        "Queens of the Stone Age - 3's and 7's",
        'Queens of the Stone Age - I Appear Missing',
        'Queens of the Stone Age - Little Sister',
        'Queens of the Stone Age - Make It wit Chu',
        'Queens of the Stone Age - No One Knows',
    ],
    'Queensrÿche Song Pack': [
        'Queensrÿche - Eyes of a Stranger',
        "Queensrÿche - I Don't Believe in Love",
        'Queensrÿche - Jet City Woman',
    ],
    'R.E.M. 5-Song Pack': [
        'R.E.M. - Everybody Hurts',
        'R.E.M. - Shiny Happy People',
        'R.E.M. - The One I Love',
        "R.E.M. - What's the Frequency, Kenneth?",
        'R.E.M. - Überlin',
    ],
    'Radiohead 5-Song Pack': [
        'Radiohead - Creep',
        'Radiohead - Just',
        'Radiohead - Karma Police',
        'Radiohead - My Iron Lung',
        'Radiohead - Optimistic',
    ],
    'Radiohead II': [
        'Radiohead - No Surprises',
        'Radiohead - Street Spirit (Fade Out)',
        'Radiohead - There, There',
    ],
    'Radiohead III': [
        'Radiohead - Airbag',
        'Radiohead - Fake Plastic Trees',
        'Radiohead - Jigsaw Falling Into Place',
    ],
    'Rage Against the Machine 7-Song Pack': [
        'Rage Against the Machine - Bombtrack',
        'Rage Against the Machine - Bulls on Parade',
        'Rage Against the Machine - Down Rodeo',
        'Rage Against the Machine - Killing In The Name',
        'Rage Against the Machine - Know Your Enemy',
        'Rage Against the Machine - Renegades of Funk',
        'Rage Against the Machine - Wake Up',
    ],
    'Rancid 4 Song Pack': [
        'Rancid - Fall Back Down',
        'Rancid - Maxwell Murder',
        'Rancid - Ruby Soho',
        'Rancid - Time Bomb',
    ],
    'Regal Singles Song Pack': [
        'Queen - Another One Bites the Dust',
        'Queensrÿche - Silent Lucidity',
        'Stevie Wonder - Sir Duke',
        'The Subways - Rock & Roll Queen',
        'Toadies - Possum Kingdom',
    ],
    'Riot Grrrl Song Pack': [
        'Babes in Toyland - Bruise Violet',
        "L7 - Pretend We're Dead",
        'Sleater-Kinney - Dig Me Out',
    ],
    'Rise Against 5-Song Pack': [
        'Rise Against - Give It All',
        'Rise Against - Make It Stop',
        'Rise Against - Prayer of the Refugee',
        'Rise Against - Satellite',
        'Rise Against - Swing Life Away',
    ],
    'Rise Against II Song Pack': [
        'Rise Against - Audience Of One',
        'Rise Against - Help Is On The Way',
        'Rise Against - Paper Wings',
        'Rise Against - Re-Education (Through Labor)',
        'Rise Against - Ready To Fall',
    ],
    'Rock Hits 00s': [
        'Modest Mouse - Float On',
        'Rise Against - The Good Left Undone',
        'The Vines - Get Free',
    ],
    'Rock Hits 1': [
        'Lynyrd Skynyrd - Free Bird',
        'Radiohead - Bodysnatchers',
        'The Black Keys - Tighten Up',
    ],
    'Rock Hits 2': [
        'T. Rex - 20th Century Boy',
        'Three Days Grace - I Hate Everything About You',
        'Vampire Weekend - Cousins',
    ],
    'Rock Hits 3': [
        'Evanescence - Bring Me to Life',
        'Foster the People - Pumped Up Kicks',
        'Maroon 5 - This Love',
    ],
    'Rock Hits 4': [
        'Pat Benatar - Hit Me with Your Best Shot',
        'The Knack - My Sharona',
    ],
    'Rock Hits 5': [
        'Finger Eleven - Paralyzer',
        'Lamb of God - Redneck',
        'The Darkness - I Believe in a Thing Called Love',
    ],
    'Rock Hits 60s': [
        'Creedence Clearwater Revival - Born on the Bayou',
        'Iron Butterfly - In-A-Gadda-Da-Vida',
    ],
    'Rock Hits 60s-70s': [
        'David Bowie - Space Oddity',
        'Heart - Barracuda',
    ],
    'Rock Hits 60s-70s 2': [
        'Cheap Trick - Surrender',
        'Steppenwolf - Born to Be Wild',
        'The Guess Who - American Woman',
    ],
    'Rock Hits 70s': [
        'Boston - More than a Feeling',
        'Deep Purple - Smoke on the Water',
    ],
    'Rock Hits 70s 2': [
        'Creedence Clearwater Revival - Have You Ever Seen the Rain?',
        'David Bowie - The Man Who Sold The World',
        'Dobie Gray - Drift Away',
        'Mountain - Mississippi Queen',
        'Sweet - Ballroom Blitz',
    ],
    'Rock Hits 70s-80s': [
        "Judas Priest - You've Got Another Thing Comin'",
        'Kansas - Carry On Wayward Son',
        'Ram Jam - Black Betty',
    ],
    'Rock Hits 80s': [
        'Europe - The Final Countdown',
        "Twisted Sister - We're Not Gonna Take It",
        'Whitesnake - Is This Love',
    ],
    'Rock Hits 80s 2': [
        'Living Colour - Cult of Personality',
        'Violent Femmes - Blister in the Sun',
    ],
    'Rock Hits 80s 3': [
        'Billy Idol - White Wedding',
        'Pixies - Here Comes Your Man',
        'Survivor - Eye of the Tiger',
    ],
    'Rock Hits 80s 4': [
        'Blondie - Call Me',
        "Rick Springfield - Jessie's Girl",
        'Tommy Tutone - 867-5309/Jenny',
    ],
    'Rock Hits 90s': [
        'Blind Melon - No Rain',
        'Eric Johnson - Cliffs of Dover',
    ],
    'Rockabilly Song Pack': [
        'Brian Setzer - Rock This Town',
        'Carl Perkins - Blue Suede Shoes',
        'Gene Vincent & His Blue Caps - Be-Bop-A-Lula',
        'Queen - Crazy Little Thing Called Love',
        'Ricky Nelson - Hello Mary Lou (Goodbye Heart)',
    ],
    'Rockin Covers II': [
        'Joan Jett and the Blackhearts - Louie Louie',
        'Nightwish - Over The Hills And Far Away',
        'Reel Big Fish - Take On Me',
    ],
    "Rockin' Covers Pack": [
        'Goldfinger - 99 Red Balloons',
        'Halestorm - Bad Romance',
        'Marilyn Manson - Tainted Love',
        'Seether - Careless Whisper',
    ],
    'Rocksmith Advanced Exercises, Vol. 1': [
        'The Notetrackers - Bass - Advanced Hammer-on/Pull-off Exercise 1',
        'The Notetrackers - Bass - Advanced Linear Playing Exercise 1',
        'The Notetrackers - Bass - Advanced Pull-on/Hammer-off Exercise 1',
        'The Notetrackers - Bass - Advanced String Skipping Exercise 1',
        'The Notetrackers - Bass - Advanced String Switching Exercise 1',
        'The Notetrackers - Guitar - Advanced Hammer-on/Pull-off Exercise 1',
        'The Notetrackers - Guitar - Advanced Linear Playing Exercise 1',
        'The Notetrackers - Guitar - Advanced Pull-on/Hammer-off Exercise 1',
        'The Notetrackers - Guitar - Advanced String Skipping Exercise 1',
        'The Notetrackers - Guitar - Advanced String Switching Exercise 1',
    ],
    'Rocksmith Advanced Exercises, Vol. 2': [
        'The Notetrackers - Bass – Advanced Hammer-on/Pull-off Exercise 2',
        'The Notetrackers - Bass – Advanced Linear Playing Exercise 2',
        'The Notetrackers - Bass – Advanced Pull-on/Hammer-off Exercise 2',
        'The Notetrackers - Bass – Advanced String Skipping Exercise 2',
        'The Notetrackers - Bass – Advanced String Switching Exercise 2',
        'The Notetrackers - Guitar – Advanced Hammer-on/Pull-off Exercise 2',
        'The Notetrackers - Guitar – Advanced Linear Playing Exercise 2',
        'The Notetrackers - Guitar – Advanced Pull-on/Hammer-off Exercise 2',
        'The Notetrackers - Guitar – Advanced String Skipping Exercise 2',
        'The Notetrackers - Guitar – Advanced String Switching Exercise 2',
    ],
    'Rocksmith Easy Exercises, Vol. 1': [
        'The Notetrackers - Bass - Easy Hammer-on Exercise 1',
        'The Notetrackers - Bass - Easy Linear Playing Exercise 1',
        'The Notetrackers - Bass - Easy Pull-off Exercise 1',
        'The Notetrackers - Bass - Easy String Skipping Exercise 1',
        'The Notetrackers - Bass - Easy String Switching Exercise 1',
        'The Notetrackers - Guitar - Easy Hammer-on Exercise 1',
        'The Notetrackers - Guitar - Easy Linear Playing Exercise 1',
        'The Notetrackers - Guitar - Easy Pull-off Exercise 1',
        'The Notetrackers - Guitar - Easy String Skipping Exercise 1',
        'The Notetrackers - Guitar - Easy String Switching Exercise 1',
    ],
    'Rocksmith Easy Exercises, Vol. 2': [
        'The Notetrackers - Bass - Easy Hammer-on/Pull-off Exercise 2',
        'The Notetrackers - Bass - Easy Linear Playing Exercise 2',
        'The Notetrackers - Bass - Easy Pull-on/Hammer-off Exercise 2',
        'The Notetrackers - Bass - Easy String Skipping Exercise 2',
        'The Notetrackers - Bass - Easy String Switching Exercise 2',
        'The Notetrackers - Guitar - Easy Hammer-on/Pull-off Exercise 2',
        'The Notetrackers - Guitar - Easy Linear Playing Exercise 2',
        'The Notetrackers - Guitar - Easy Pull-on/Hammer-off Exercise 2',
        'The Notetrackers - Guitar - Easy String Skipping Exercise 2',
        'The Notetrackers - Guitar - Easy String Switching Exercise 2',
    ],
    'Rocksmith Goes to the Movies 5-Song Pack': [
        'Alan Silvestri - Back to the Future',
        'Danny Elfman - Batman - Theme',
        'Howard Shore - A Knife In The Dark',
        'John Williams - Jurassic Park - Theme',
        'John Williams - Superman - Main Title',
    ],
    'Rocksmith Intermediate Exercises, Vol. 1': [
        'The Notetrackers - Bass - Intermediate Hammer-on/Pull-off Exercise 1',
        'The Notetrackers - Bass - Intermediate Linear Playing Exercise 1',
        'The Notetrackers - Bass - Intermediate Pull-off/Hammer-on Exercise 1',
        'The Notetrackers - Bass - Intermediate String Skipping Exercise 1',
        'The Notetrackers - Bass - Intermediate String Switching Exercise 1',
        'The Notetrackers - Guitar - Intermediate Hammer-on/Pull-off Exercise 1',
        'The Notetrackers - Guitar - Intermediate Linear Playing Exercise 1',
        'The Notetrackers - Guitar - Intermediate Pull-off/Hammer-on Exercise 1',
        'The Notetrackers - Guitar - Intermediate String Skipping Exercise 1',
        'The Notetrackers - Guitar - Intermediate String Switching Exercise 1',
    ],
    'Rocksmith Intermediate Exercises, Vol. 2': [
        'The Notetrackers - Bass - Intermediate Hammer-on/Pull-off Exercise 2',
        'The Notetrackers - Bass - Intermediate Linear Playing Exercise 2',
        'The Notetrackers - Bass - Intermediate Pull-on/Hammer-off Exercise 2',
        'The Notetrackers - Bass - Intermediate String Skipping Exercise 2',
        'The Notetrackers - Bass - Intermediate String Switching Exercise 2',
        'The Notetrackers - Guitar - Intermediate Hammer-on/Pull-off Exercise 2',
        'The Notetrackers - Guitar - Intermediate Linear Playing Exercise 2',
        'The Notetrackers - Guitar - Intermediate Pull-on/Hammer-off Exercise 2',
        'The Notetrackers - Guitar - Intermediate String Skipping Exercise 2',
        'The Notetrackers - Guitar - Intermediate String Switching Exercise 2',
    ],
    'Rolling Stones Pack': [
        'The Rolling Stones - Brown Sugar',
        'The Rolling Stones - Gimme Shelter',
        "The Rolling Stones - Jumpin' Jack Flash",
        'The Rolling Stones - Sympathy for the Devil',
    ],
    'Roxette Pack': [
        'Roxette - It Must Have Been Love',
        'Roxette - Listen To Your Heart',
        'Roxette - The Look',
    ],
    'Royal Blood Pack': [
        'Royal Blood - Figure It Out',
        'Royal Blood - Little Monster',
        'Royal Blood - Out of the Black',
    ],
    'Run-DMC Pack': [
        "Run-DMC - It's Tricky",
        'Run-DMC - King Of Rock',
        'Run-DMC - Rock Box',
    ],
    'Rush 5-Song Pack': [
        'Rush - Limelight',
        'Rush - Red Barchetta',
        'Rush - Subdivisions',
        'Rush - Tom Sawyer',
        'Rush - YYZ',
    ],
    'Rush Song Pack II': [
        'Rush - Closer to the Heart',
        'Rush - Fly by Night',
        'Rush - Freewill',
        'Rush - La Villa Strangiato',
        'Rush - Working Man',
    ],
    'Sabaton Song Pack': [
        'Sabaton - 40:1',
        'Sabaton - Ghost Division',
        'Sabaton - Primo Victoria',
    ],
    'Santana 3-Song Pack': [
        'Santana - Black Magic Woman/Gypsy Queen',
        'Santana - Oye Como Va',
        'Santana feat. Rob Thomas - Smooth',
    ],
    'Seether 3-Song Pack': [
        'Seether - Fake It',
        'Seether - Remedy',
        'Seether feat. Amy Lee - Broken',
    ],
    'Sevendust Song Pack': [
        "Sevendust - Angel's Son",
        'Sevendust - Black',
        'Sevendust - Praise',
    ],
    'Shamrock 5-Song Pack': [
        "Dropkick Murphys - I'm Shipping Up to Boston",
        'Flogging Molly - Drunken Lullabies',
        'Stiff Little Fingers - Alternative Ulster',
        'The Cranberries - Zombie',
        'Villagers - Becoming A Jackal',
    ],
    'Shania Twain Pack': [
        'Shania Twain - Man! I Feel Like A Woman',
        "Shania Twain - That Don't Impress Me Much",
        "Shania Twain - You're Still The One",
    ],
    'Sheryl Crow Pack': [
        'Sheryl Crow - If It Makes You Happy',
        'Sheryl Crow - My Favorite Mistake',
        'Sheryl Crow - Soak Up the Sun',
    ],
    'Shinedown 5-Song Pack': [
        'Shinedown - 45',
        'Shinedown - Bully',
        'Shinedown - Enemies',
        'Shinedown - Second Chance',
        'Shinedown - Sound of Madness',
    ],
    'Silverstein Song Pack': [
        'Silverstein - Bleeds No More',
        'Silverstein - My Heroine',
        'Silverstein - Smashed into Pieces',
        'Silverstein - Smile In Your Sleep',
    ],
    'Sixx:A.M. Song Pack': [
        'Sixx:A.M. - Life is Beautiful',
        'Sixx:A.M. - Stars',
        'Sixx:A.M. - This Is Gonna Hurt',
    ],
    'Skater Rock Pack': [
        'Bad Religion - You',
        'Goldfinger - Superman',
        'Lagwagon - May 16',
        'Millencolin - No Cigar',
        'Powerman 5000 - When Worlds Collide',
    ],
    'Skid Row Pack': [
        'Skid Row - 18 and Life',
        'Skid Row - I Remember You',
        'Skid Row - Monkey Business',
        'Skid Row - Slave to the Grind',
        'Skid Row - Youth Gone Wild',
    ],
    'Skillet 3-Song Pack': [
        'Skillet - Awake And Alive',
        'Skillet - Hero',
        'Skillet - Monster',
    ],
    'Slash 3-Song Pack': [
        'Slash - Anastasia',
        'Slash - Back from Cali',
        "Slash - You're a Lie",
    ],
    'Slayer 5-Song Pack': [
        'Slayer - Angel of Death',
        'Slayer - Dead Skin Mask',
        'Slayer - Raining Blood',
        'Slayer - Seasons in the Abyss',
        'Slayer - South of Heaven',
    ],
    'Social Distortion Song Pack': [
        'Social Distortion - Bad Luck',
        'Social Distortion - Ball and Chain',
        'Social Distortion - Reach for the Sky',
        'Social Distortion - Story of My Life',
    ],
    'Social Stars': [
        'Audrey and Kate - No Reason',
        'Set The Charge - Everything but Me',
        'The Dooo - Guitar Solos With Dooo #2 - Ascend',
    ],
    'Soul Hits': [
        "Marvin Gaye - What's Going On",
        "Otis Redding - (Sittin' On) The Dock of the Bay",
        'The Temptations - My Girl',
    ],
    'Soundgarden 5-Song Pack': [
        'Soundgarden - Black Hole Sun',
        'Soundgarden - Fell on Black Days',
        'Soundgarden - Jesus Christ Pose',
        'Soundgarden - Pretty Noose',
        'Soundgarden - Spoonman',
    ],
    'Spinal Tap 5-Song Pack': [
        'Spinal Tap - Big Bottom',
        'Spinal Tap - Gimme Some Money',
        'Spinal Tap - Sex Farm',
        'Spinal Tap - Stonehenge',
        "Spinal Tap - Tonight I'm Gonna Rock You Tonight",
    ],
    'Spooktacular Singles': [
        'Billy Talent - Devil on My Shoulder',
        'Focus - Hocus Pocus',
        'Motörhead - Killed by Death',
        "Oingo Boingo - Dead Man's Party",
    ],
    'Staind Song Pack': [
        "Staind - It's Been Awhile",
        'Staind - Outside',
        'Staind - So Far Away',
    ],
    'Stereophonics Pack': [
        'Stereophonics - Dakota',
        'Stereophonics - Maybe Tomorrow',
        'Stereophonics - The Bartender And The Thief',
    ],
    'Steve Miller Band Pack': [
        'Steve Miller Band - Fly Like an Eagle',
        'Steve Miller Band - Jet Airliner',
        "Steve Miller Band - Rock'n Me",
        'Steve Miller Band - Take the Money and Run',
        'Steve Miller Band - The Joker',
    ],
    'Stevie Ray Vaughn & DT Song Pack': [
        'Stevie Ray Vaughan & Double Trouble - Cold Shot',
        "Stevie Ray Vaughan & Double Trouble - Couldn't Stand the Weather",
        'Stevie Ray Vaughan & Double Trouble - Pride and Joy',
        "Stevie Ray Vaughan & Double Trouble - Scuttle Buttin'",
        'Stevie Ray Vaughan & Double Trouble - Texas Flood',
    ],
    'Stevie Wonder Song Pack': [
        'Stevie Wonder - I Wish',
        "Stevie Wonder - Sealed, Signed, Delivered I'm Yours",
        'Stevie Wonder - Superstition',
    ],
    'Stone Sour Song Pack': [
        'Stone Sour - Absolute Zero',
        'Stone Sour - Bother',
        "Stone Sour - Say You'll Haunt Me",
    ],
    'Stone Temple Pilots 6-Song Pack': [
        'Stone Temple Pilots - Big Empty',
        'Stone Temple Pilots - Creep',
        'Stone Temple Pilots - Interstate Love Song',
        'Stone Temple Pilots - Plush',
        'Stone Temple Pilots - Sex Type Thing',
        'Stone Temple Pilots - Wicked Garden',
    ],
    'Sublime 5-Song Pack': [
        'Sublime - Caress Me Down',
        'Sublime - Santería',
        'Sublime - Smoke Two Joints',
        'Sublime - What I Got',
        'Sublime - Wrong Way',
    ],
    'Sum 41 5-Song Pack': [
        'Sum 41 - Fat Lip',
        'Sum 41 - In Too Deep',
        'Sum 41 - Still Waiting',
        'Sum 41 - The Hell Song',
        "Sum 41 - We're All to Blame",
    ],
    'Surf Rock 3-Song Pack': [
        'Dick Dale - Misirlou',
        'The Surfaris - Wipe Out',
        "The Ventures - Walk Don't Run",
    ],
    'Surf Rock II': [
        "The Beach Boys - Surfin' U.S.A.",
        'The Chantays - Pipeline',
        'The Lively Ones - Surf Rider',
        'The Pyramids - Penetration',
    ],
    'System of a Down 3-Song Pack': [
        'System of a Down - Aerials',
        'System of a Down - B.Y.O.B.',
        'System of a Down - Toxicity',
    ],
    'Tegan and Sara Pack': [
        'Tegan and Sara - Call It Off',
        'Tegan and Sara - The Con',
        'Tegan and Sara - Walking with a Ghost',
    ],
    'Tenacious D 3-Song Pack': [
        'Tenacious D - Master Exploder',
        'Tenacious D - The Metal',
        'Tenacious D - Tribute',
    ],
    'The All-American Rejects 3 Song Pack': [
        'All-American Rejects - Dirty Little Secret',
        'All-American Rejects - Gives You Hell',
        'All-American Rejects - Move Along',
    ],
    'The Allman Brothers Band 3-Song Pack': [
        'The Allman Brothers Band - Jessica',
        'The Allman Brothers Band - Southbound',
        'The Allman Brothers Band - Whipping Post',
    ],
    'The Black Keys 3-Song Pack': [
        'The Black Keys - Gold on the Ceiling',
        'The Black Keys - Just Got to Be',
        'The Black Keys - Mind Eraser',
    ],
    'The Black Keys 5-Song Pack': [
        "The Black Keys - Howlin' for You",
        'The Black Keys - Little Black Submarines',
        'The Black Keys - Lonely Boy',
        'The Black Keys - Your Touch',
        'The Black Keys - thickfreakness',
    ],
    'The Cardigans Pack': [
        'The Cardigans - Erase/Rewind',
        'The Cardigans - Lovefool',
        'The Cardigans - My Favourite Game',
    ],
    'The Cars 5-Song Pack': [
        'The Cars - Bye Bye Love',
        'The Cars - Good Times Roll',
        'The Cars - Just What I Needed',
        "The Cars - Let's Go",
        "The Cars - You're All I've Got Tonight",
    ],
    'The Clash 3-Song Pack': [
        'The Clash - Guns of Brixton',
        'The Clash - London Calling',
        'The Clash - Should I Stay or Should I Go',
    ],
    'The Cure 3-Song Pack': [
        'The Cure - Just Like Heaven',
        'The Cure - Lovesong',
        'The Cure - The End of the World',
    ],
    'The Doors 3 Song Pack II': [
        'The Doors - Break On Through (To the Other Side)',
        'The Doors - L.A. Woman',
        'The Doors - People Are Strange',
    ],
    'The Doors 3-Song Pack': [
        'The Doors - Light My Fire',
        'The Doors - Riders on the Storm',
        'The Doors - Roadhouse Blues',
    ],
    'The Killers 5-Song Pack': [
        'The Killers - Mr. Brightside',
        'The Killers - Runaways',
        'The Killers - Somebody Told Me',
        'The Killers - Spaceman',
        'The Killers - When You Were Young',
    ],
    'The Libertines 3-Song Pack': [
        "The Libertines - Can't Stand Me Now",
        "The Libertines - Don't Look Back into the Sun",
        'The Libertines - What Katie Did',
    ],
    'The Misfits Song Pack': [
        'Misfits - Die, Die My Darling',
        'Misfits - Halloween',
        'Misfits - Last Caress',
        'Misfits - Where Eagles Dare',
    ],
    'The Monkees Pack': [
        'The Monkees - Last Train to Clarksville',
        'The Monkees - Pleasant Valley Sunday',
        'The Monkees - Valleri',
    ],
    'The Offspring 3-Song Pack': [
        "The Offspring - Come Out and Play (Keep 'Em Separated)",
        'The Offspring - Gone Away',
        'The Offspring - Self Esteem',
    ],
    'The Offspring II 5-Song Pack': [
        'The Offspring - All I Want',
        'The Offspring - Pretty Fly (For A White Guy)',
        'The Offspring - The Kids Aren’t Alright',
        'The Offspring - Want You Bad',
        "The Offspring - You're Gonna Go Far Kid",
    ],
    'The Police 3-Song Pack': [
        'The Police - Message in a Bottle',
        'The Police - Roxanne',
        'The Police - Synchronicity II',
    ],
    'The Pretenders Pack': [
        'The Pretenders - Back on the Chain Gang',
        'The Pretenders - Brass in Pocket',
        "The Pretenders - Don't Get Me Wrong",
        "The Pretenders - I'll Stand By You",
        'The Pretenders - Middle of the Road',
    ],
    'The Pretty Reckless Pack': [
        'The Pretty Reckless - Going To Hell',
        'The Pretty Reckless - Make Me Wanna Die',
        'The Pretty Reckless - My Medicine',
    ],
    'The Smashing Pumpkins 5-Song Pack': [
        'The Smashing Pumpkins - 1979',
        'The Smashing Pumpkins - Bullet with Butterfly Wings',
        'The Smashing Pumpkins - Disarm',
        'The Smashing Pumpkins - Today',
        'The Smashing Pumpkins - Tonight, Tonight',
    ],
    'The Stone Roses 3 Song Pack': [
        'The Stone Roses - I Wanna Be Adored',
        'The Stone Roses - Love Spreads',
        'The Stone Roses - She Bangs the Drums',
    ],
    'The Strokes 3-Song Pack': [
        'The Strokes - Juicebox',
        'The Strokes - Last Nite',
        'The Strokes - Reptilia',
    ],
    'The Strokes II': [
        'The Strokes - 12:51',
        'The Strokes - Someday',
        'The Strokes - Taken for a Fool',
        'The Strokes - You Only Live Once',
    ],
    'The White Stripes 5-Song Pack': [
        'The White Stripes - Blue Orchid',
        'The White Stripes - Fell in Love With a Girl',
        'The White Stripes - Seven Nation Army',
        'The White Stripes - The Hardest Button to Button',
        "The White Stripes - You Don't Know What Love Is (You Just Do as You're Told)",
    ],
    'The Who 5-Song Pack': [
        "The Who - Baba O'Riley",
        'The Who - Behind Blue Eyes',
        'The Who - Pinball Wizard',
        'The Who - The Seeker',
        'The Who - Who Are You',
    ],
    'The Zombies Pack': [
        "The Zombies - She's Not There",
        'The Zombies - Tell Her No',
        'The Zombies - Time of the Season',
    ],
    'Thin Lizzy 3-Song Pack': [
        "Thin Lizzy - Dancing in the Moonlight (It's Caught Me in Its Spotlight)",
        'Thin Lizzy - Jailbreak',
        'Thin Lizzy - The Boys Are Back In Town',
    ],
    'Third Eye Blind Pack': [
        "Third Eye Blind - How's It Going To Be",
        'Third Eye Blind - Jumper',
        'Third Eye Blind - Never Let You Go',
        'Third Eye Blind - Semi-Charmed Life',
    ],
    'Thirty Seconds to Mars 5-Song Pack': [
        'Thirty Seconds to Mars - Closer to the Edge',
        'Thirty Seconds to Mars - From Yesterday',
        'Thirty Seconds to Mars - Kings and Queens',
        'Thirty Seconds to Mars - The Kill',
        'Thirty Seconds to Mars - This is War',
    ],
    'Three Days Grace 5-Song Pack': [
        'Three Days Grace - Animal I Have Become',
        'Three Days Grace - Break',
        'Three Days Grace - Just Like You',
        'Three Days Grace - Never Too Late',
        'Three Days Grace - Riot',
    ],
    'Thrice Pack': [
        'Thrice - Deadbolt',
        'Thrice - Stare At the Sun',
        'Thrice - The Artist in the Ambulance',
    ],
    'Tom Petty 5-Song Pack': [
        'Tom Petty & The Heartbreakers - American Girl',
        'Tom Petty & The Heartbreakers - Learning to Fly',
        'Tom Petty & The Heartbreakers - Refugee',
        "Tom Petty - Free Fallin'",
        "Tom Petty - I Won't Back Down",
    ],
    'Trans-Siberian Orchestra Pack': [
        "Trans-Siberian Orchestra - A Mad Russian's Christmas",
        'Trans-Siberian Orchestra - Christmas Canon Rock',
        'Trans-Siberian Orchestra - Christmas Eve/Sarajevo 12/24',
        'Trans-Siberian Orchestra - O Come, All Ye Faithful/O Holy Night',
        'Trans-Siberian Orchestra - Wizards in Winter',
    ],
    'Trivium II Pack': [
        'Trivium - A Gunshot to the Head of Trepidation',
        'Trivium - Dying in Your Arms',
        'Trivium - Pull Harder on the Strings of Your Martyr',
    ],
    'Trivium Pack': [
        'Trivium - Built to Fall',
        'Trivium - In Waves',
        'Trivium - Strife',
    ],
    'U2 Pack': [
        'U2 - Beautiful Day',
        'U2 - Sunday Bloody Sunday',
        'U2 - Vertigo',
        'U2 - Where The Streets Have No Name',
        'U2 - With Or Without You',
    ],
    'UBI30: 1986 Song Pack': [
        "Cinderella - Nobody's Fool",
        'Kenny Loggins - Danger Zone',
        'Poison - Talk Dirty to Me',
        'Robert Palmer - Addicted To Love',
        'Survivor - Burning Heart',
    ],
    'Ubisoft Music Song Pack': [
        'Billy Martin - Strategy and Spying',
        "Brian Tyler - Assassin's Creed IV Black Flag Main Theme",
        "Jesper Kyd - Ezio's Family",
        'Power Glove - Blood Dragon Theme (Far Cry 3: Blood Dragon)',
        'The Road Vikings - The Ballad of Clutch Nixon',
    ],
    "Valentine's Day 4-Song Pack": [
        'Hall & Oates - You Make My Dreams',
        'Sister Hazel - All For You',
        'Sixpence None the Richer - Kiss Me',
        'Toto - Rosanna',
    ],
    'Variety Pack IX': [
        '311 - All Mixed Up',
        'Jack Johnson - Banana Pancakes',
        'James Bay - Let It Go',
        'Joe Satriani - Surfing With The Alien',
    ],
    'Variety Pack V': [
        'Iggy and The Stooges - Search And Destroy',
        'Marcy Playground - Sex And Candy',
        'Panic! At The Disco - The Ballad Of Mona Lisa',
        'Steel Panther - Eyes Of A Panther',
    ],
    'Variety Pack VI': [
        'Brian Setzer - Stray Cat Strut',
        'David Bowie - Suffragette City',
        'Gin Blossoms - Hey Jealousy',
        'The Fall Of Troy - F.C.P.R.E.M.I.X.',
    ],
    'Variety Pack VII': [
        'Modern English - I Melt With You',
        'OneRepublic - Counting Stars',
        'Rage Against The Machine - Take The Power Back',
        'The Calling - Wherever You Will Go',
    ],
    'Variety Pack VIII': [
        'Candlebox - Far Behind',
        'Kasabian - Underdog',
        'Steppenwolf - Magic Carpet Ride',
        'Tears For Fears - Everybody Wants To Rule The World',
    ],
    'Variety Pack X': [
        'Jace Everett - Bad Things',
        'Kiss - Lick It Up',
        'Pantera - Mouth for War',
        'X - Los Angeles',
    ],
    'Variety Pack XI': [
        'Bombay Bicycle Club - Your Eyes',
        'Escape the Fate - This War Is Ours (The Guillotine II)',
        "George Strait - All My Ex's Live in Texas",
        "The Flaming Lips - She Don't Use Jelly",
    ],
    'Variety Pack XII': [
        'Colin Hay - Down Under',
        'DragonForce - Through the Fire and Flames',
        "Elton John - Saturday Night's Alright for Fighting",
        'Rusted Root - Send Me on My Way',
    ],
    'Variety Pack XIII': [
        'Billy Joel - Only the Good Die Young',
        'George Thorogood & The Destroyers - Bad To The Bone',
        'Soul Asylum - Runaway Train',
        'The Red Jumpsuit Apparatus - Face Down',
    ],
    'Variety Pack XIV': [
        'Panic! At The Disco - I Write Sins Not Tragedies',
        'Pure Prairie League - Amie',
        'Temple Of The Dog - Hunger Strike',
        'The Outfield - Your Love',
    ],
    'Variety Pack XIX': [
        'Big Country - In A Big Country',
        'Bob Marley & The Wailers - Stir It Up',
        'The Meters - Cissy Strut',
        'White Zombie - More Human Than Human',
    ],
    'Variety Pack XV': [
        'Badfinger - Baby Blue',
        'Spacehog - In The Meantime',
        'The Shadows - Apache',
        'U2 - Bad',
    ],
    'Variety Pack XVI': [
        'Duane Eddy - Rebel Rouser',
        'Nina Simone - Feeling Good',
        'Pantera - This Love',
        "The Proclaimers - I'm Gonna Be (500 Miles)",
    ],
    'Variety Pack XVII': [
        'Alien Ant Farm - Movies',
        'David Bowie - Changes',
        'Grateful Dead - Touch Of Grey',
        'Lisa Loeb - Stay (I Missed You)',
    ],
    'Variety Pack XVIII': [
        'Beastie Boys - Gratitude',
        'Blink-182 - Stay Together for the Kids',
        "The Beach Boys - Surfin' Safari",
        'The Outlaws - Green Grass and High Tides',
    ],
    'Variety Pack XX': [
        "Deep Blue Something - Breakfast at Tiffany's",
        'Les Paul & Mary Ford - On The Sunny Side of the Street',
        'Thin Lizzy - Whiskey In The Jar',
        'Wheatus - Teenage Dirtbag',
    ],
    'Variety Pack XXI': [
        'Clutch - The Regulator',
        'Fuel - Shimmer',
        'Gin Blossoms - Found Out About You',
        'Warren Zevon - Werewolves of London',
    ],
    'Variety Pack XXII': [
        'Annihilator - Alison Hell',
        'Dishwalla - Counting Blue Cars',
        'Ghost - From The Pinnacle To The Pit',
        'Wanda Jackson - Long Tall Sally',
    ],
    'Variety Song Pack I': [
        'Arch Enemy - Nemesis',
        'Nazareth - Hair Of The Dog',
        'Of Monsters and Men - Little Talks',
        'The Presidents of the United States of America - Peaches',
    ],
    'Variety Song Pack II': [
        'Eagle-Eye Cherry - Save Tonight',
        'Kenny Rogers - The Gambler',
        'Queen and David Bowie - Under Pressure',
        'SR-71 - Right Now',
    ],
    'Variety Song Pack III': [
        'Joe Satriani - Always with Me, Always with You',
        'Pantera - 5 Minutes Alone',
        'Styx - Blue Collar Man (Long Nights)',
        'The Fratellis - Chelsea Dagger',
    ],
    'Variety Song Pack IV': [
        "A Day To Remember - I'm Made of Wax, Larry, What are You Made Of?",
        'A Flock of Seagulls - I Ran (So Far Away)',
        'Fleetwood Mac - Never Going Back Again',
        'Sepultura - Refuse/Resist',
    ],
    'Volbeat Song Pack': [
        "Volbeat - A Warrior's Call",
        'Volbeat - Fallen',
        'Volbeat - Heaven Nor Hell',
        'Volbeat - Lola Montez',
        'Volbeat - Still Counting',
    ],
    'Weezer 5-Song Pack': [
        'Weezer - Buddy Holly',
        'Weezer - Hash Pipe',
        'Weezer - Island in the Sun',
        'Weezer - My Name Is Jonas',
        'Weezer - Undone (The Sweater Song)',
    ],
    'Weezer Song Pack II': [
        'Weezer - Beverly Hills',
        'Weezer - Perfect Situation',
        'Weezer - Pork And Beans',
    ],
    'Women Who Rock 5-Song Pack': [
        "Flyleaf - I'm So Sick",
        'Hole - Celebrity Skin',
        'The Donnas - Take It Off',
        'The Pretty Reckless - Heaven Knows',
        'The Runaways - Cherry Bomb',
    ],
    'Women Who Rock II': [
        'Orianthi - According to You',
        "The Go-Go's - We Got the Beat",
        'Veruca Salt - Seether',
    ],
    'Wrestling Theme Song Pack': [
        'Jim Johnston - Break The Walls Down (Chris Jericho)',
        'Jim Johnston - Electrifying (The Rock)',
        "Jim Johnston - I Won't Do What You Tell Me (Stone Cold Steve Austin)",
    ],
    'Uncategorized Singles': [
        '9mm Parabellum Bullet - Atarashii Hikari',
        '9mm Parabellum Bullet - Punishment',
        'ACIDMAN - Shinsekai',
        'Albert King - The Sky Is Crying',
        'Band of Merrymakers - Joy to the World',
        'Band of Merrymakers - Must Be Christmas',
        'Chicago - 25 or 6 to 4',
        'DragonForce - Highway to Oblivion',
        'Kazuyoshi Saito - Yasashiku Naritai',
        'One Ok Rock - Liar',
        'One Ok Rock - NO SCARED',
        'Queens of the Stone Age - My God Is the Sun',
        'RIZE - PARADOX Taiso',
        'Rush - Headlong Flight',
        'Straightener - From Noon Till Dawn',
        'Straightener - ROCKSTEADY',
        'Tame Impala - Elephant',
        'The Birthday - stupid',
        'The Hives - Hate to Say I Told You So',
        'The Lumineers - Ho Hey',
        'The Smashing Pumpkins - Cherub Rock',
        'Them Crooked Vultures - Mind Eraser, No Chaser',
    ],
    'Yacht Rock Singles': [
        'Daryl Hall and John Oates - Kiss On My List',
        "Michael McDonald - I Keep Forgettin' (Every Time You're Near)",
        'Rupert Holmes - Escape (The Piña Colada Song)',
        'The Doobie Brothers - China Grove',
        'Toto - Hold the Line',
    ],
    'Yes Song Pack': [
        'Yes - Heart of the Sunrise',
        "Yes - I've Seen All Good People",
        'Yes - Owner of a Lonely Heart',
        'Yes - Roundabout',
        'Yes - Starship Trooper',
    ],
    'Zombie Song Pack': [
        'Rob Zombie - Dragula',
        'Rob Zombie - Living Dead Girl',
        'Rob Zombie - Superbeast',
        'White Zombie - Black Sunshine',
    ],
    'blink-182 II': [
        "blink-182 - Adam's Song",
        'blink-182 - Feeling This',
        'blink-182 - First Date',
        'blink-182 - I Miss You',
        'blink-182 - The Rock Show',
    ],
}

# A flat list of all known DLC pack names for convenience.
DLC_PACK_NAMES: list[str] = [
    '2000s Mix III',
    '2000s Mix IV',
    '2000s Mix Pack',
    '2000s Mix Pack II',
    '2000s Mix V',
    '2000s Mix VI',
    '2010s Mix III',
    '2010s Mix IV',
    '2010s Mix Song Pack',
    '2010s Mix Song Pack II',
    '2010s Mix V',
    '3 Doors Down 3-Song Pack',
    '3 Doors Down II',
    '311 3-Song Pack',
    '38 Special 3-Song Pack',
    '5 Seconds of Summer',
    "50's Singles",
    '60s Mix II',
    '60s Mix III',
    '60s Mix Pack',
    '70s Mix II',
    '70s Mix III',
    '70s Mix IV',
    '70s Mix Song Pack',
    '70s Mix V',
    '70s Mix VI',
    '70s Rock Singles',
    "80's Mix Pack",
    '80s Mix III',
    '80s Mix IV',
    '80s Mix Pack II',
    '80s Mix V',
    '80s Mix VI',
    '90s Mix II',
    '90s Mix III',
    '90s Mix IV',
    '90s Mix Song Pack',
    '90s Mix V',
    '90s Mix VI',
    '90s Rock Singles',
    'A Day to Remember 5-Song Pack',
    'ABBA Song Pack',
    'AFI 4-Song Pack',
    'Aerosmith 5-Song Pack',
    'Aerosmith Song Pack II',
    'Airbourne Pack',
    'Alabama Shakes Pack',
    'Alice Cooper Pack',
    'Alice in Chains 5-Song Pack',
    'Alice in Chains II',
    'All That Remains Song Pack',
    'All Time Low Song Pack',
    'Alter Bridge 4-Song Pack',
    'Alternative Rock Singles',
    'Amaranthe Pack',
    'Amon Amarth Pack',
    'Anniversary Song Pack',
    'Anthrax 4-Song Pack',
    'Arena Rock Singles',
    'Audioslave 5-Song Pack',
    'Avenged Sevenfold 3-Song Pack',
    'Avril Lavigne Pack',
    "B'z 3-Song Pack",
    'Bachman-Turner Overdrive Pack',
    'Bachsmith 2 5-Song Pack',
    'Bachsmith 5-Song Pack',
    'Bad Religion Song Pack',
    'Beastie Boys Pack',
    'Biffy Clyro 5-Song Pack',
    'Billy Talent 5-Song Pack',
    'Black Label Society Song Pack',
    'Blink-182 3-Song Pack',
    'Bloodhound Gang Pack',
    'Blue Öyster Cult 3-Song Pack',
    'Blues Hits',
    'Blues Rock Song Pack',
    'Blues Song Pack',
    'Blues Song Pack II',
    'Blues Song Pack III',
    'Bob Dylan 3-Song Pack',
    'Bob Marley and the Wailers Pack',
    'Bon Jovi 5-Song Pack',
    'Boston 3-Song Pack',
    'Brad Paisley Pack',
    'Brand New Song Pack',
    'Breaking Benjamin Song Pack',
    'Bullet for My Valentine 5-Song Pack',
    'Bush 4-Song Pack',
    'Cake 5-Song Pack',
    'Cat Stevens Pack',
    'Chevelle Song Pack',
    'Chris Stapleton Song Pack',
    'Christmas Classics',
    'Chuck Berry Pack',
    'Classic Country Song Pack',
    'Classic Melody Pack',
    'Classic Riff Singles',
    'Classic Singles',
    'Coldplay Pack',
    'Collective Soul 5-Song Pack',
    'Creed 5-Song Pack',
    'Creedence Clearwater Revival',
    'Crobot 3-Song Pack',
    'Cyndi Lauper Pack',
    'Daughtry Song Pack',
    'Deftones 4-Song Pack',
    'Dethklok 3-Song Pack',
    'Dethklok II',
    'Disturbed 3-Song Pack',
    'Disturbed Song Pack II',
    'Dream Theater Song Pack',
    'Duran Duran 3-Song Pack',
    'Earth, Wind & Fire 3 Song Pack',
    'Evanescence Pack',
    'Faith No More Song Pack',
    'Fall Out Boy 5-Song Pack',
    'Female Lead Singles',
    'Five Finger Death Punch Pack',
    'Flyleaf Song Pack',
    'Foo Fighters 5-Song Pack',
    'Foo Fighters II 5-Song Pack',
    'Foreigner 5-Song Pack',
    'Four Tops Pack',
    'Funk Hits',
    'Garbage 3-Song Pack',
    'Gary Moore Pack',
    'Ghost Pack',
    'Godsmack 5-Song Pack',
    'Golden Bomber 3-Song Pack',
    'Good Charlotte Song Pack',
    'Grateful Dead Pack',
    'Great White Song Pack',
    'Green Day 3-Song Pack',
    'Green Day II',
    'Green Day III',
    'Green Day IV',
    'Greta Van Fleet II',
    'Greta Van Fleet Pack',
    'Haim Song Pack',
    'Halestorm Pack',
    'Heart Pack',
    'Hit Singles 4 4-Song Pack',
    'Hit Singles II Song Pack',
    'Hit Singles III 4-Song Pack',
    'Hit Singles Song Pack',
    'Hit Singles V 4-Song Pack',
    'Holiday 3-Song Pack',
    'Hotei 3-Song Pack',
    'Imagine Dragons 3-Song Pack',
    'Incubus 3-Song Pack',
    'Incubus Pack II',
    'Independence Day Song Pack',
    'Indie Rock',
    'Indie Rock Hits',
    'Indigo Girls Pack',
    'Interpol Pack',
    'Iron Maiden 5-Song Pack',
    "Jane's Addiction 5-Song Pack",
    'Janis Joplin Song Pack',
    'Jeff Buckley 3-Song Pack',
    'Jimi Hendrix 12-Song Pack',
    'Jimmy Eat World Pack',
    'Joan Jett Pack',
    'John Mellencamp Song Pack',
    'Johnny Cash Song Pack I',
    'Johnny Cash Song Pack II',
    'Joni Mitchell Pack',
    'Joy Division Song Pack',
    'Judas Priest 3-Song Pack',
    'KT Tunstall',
    'Kaiser Chiefs Pack',
    'Kaleo',
    'Kelly Clarkson Song Pack',
    'Killswitch Engage 3-Song Pack',
    'Kiss 3-Song Pack',
    'Kiss Song Pack 2',
    'Lady Gaga Pack',
    'Lamb of God 3-Song Pack',
    'Linkin Park 6-Song Pack',
    'Live Pack',
    'Love Singles Song Pack',
    'Lynyrd Skynyrd Song Pack',
    'Manic Street Preachers',
    'Marilyn Manson Pack',
    'Maroon 5 3-Song Pack',
    'Mastodon 3-Song Pack',
    'Matchbox Twenty 5-Song Pack',
    'Megadeth 3-Song Pack',
    'Megadeth Song Pack II',
    'Melissa Etheridge Song Pack',
    'Metal Mix',
    'Metal Mix Pack II',
    'Mix Tape Song Pack',
    'Muddy Waters Pack',
    'Mumford & Sons Pack',
    'Muse 5-Song Pack',
    'My Chemical Romance 3-Song Pack',
    'My Chemical Romance II 5-Song Pack',
    'Mötley Crüe 5-Song Pack',
    'NOFX Pack',
    'New Found Glory Pack',
    'Nickelback 3-Song Pack',
    'Night Ranger Pack',
    'No Doubt 3-Song Pack',
    'Norah Jones Pack',
    'Oasis 5-Song Pack',
    'Opeth Song Pack',
    'P.O.D Pack',
    'Pantera 3-Song Pack',
    'Papa Roach 3-Song Pack',
    'Paramore Pack',
    'Paramore Song Pack II',
    'Pat Benatar Song Pack',
    'Pearl Jam 3-Song Pack',
    'Pearl Jam II',
    'Pixies Song Pack',
    'Player Picks Song Pack',
    'Power Ballad Singles',
    'Primus Song Pack',
    'Queen 5-Song Pack',
    'Queen Pack II',
    'Queen Pack III',
    'Queens of the Stone Age 5-Song Pack',
    'Queensrÿche Song Pack',
    'R.E.M. 5-Song Pack',
    'Radiohead 5-Song Pack',
    'Radiohead II',
    'Radiohead III',
    'Rage Against the Machine 7-Song Pack',
    'Rancid 4 Song Pack',
    'Regal Singles Song Pack',
    'Riot Grrrl Song Pack',
    'Rise Against 5-Song Pack',
    'Rise Against II Song Pack',
    'Rock Hits 00s',
    'Rock Hits 1',
    'Rock Hits 2',
    'Rock Hits 3',
    'Rock Hits 4',
    'Rock Hits 5',
    'Rock Hits 60s',
    'Rock Hits 60s-70s',
    'Rock Hits 60s-70s 2',
    'Rock Hits 70s',
    'Rock Hits 70s 2',
    'Rock Hits 70s-80s',
    'Rock Hits 80s',
    'Rock Hits 80s 2',
    'Rock Hits 80s 3',
    'Rock Hits 80s 4',
    'Rock Hits 90s',
    'Rockabilly Song Pack',
    'Rockin Covers II',
    "Rockin' Covers Pack",
    'Rocksmith Advanced Exercises, Vol. 1',
    'Rocksmith Advanced Exercises, Vol. 2',
    'Rocksmith Easy Exercises, Vol. 1',
    'Rocksmith Easy Exercises, Vol. 2',
    'Rocksmith Goes to the Movies 5-Song Pack',
    'Rocksmith Intermediate Exercises, Vol. 1',
    'Rocksmith Intermediate Exercises, Vol. 2',
    'Rolling Stones Pack',
    'Roxette Pack',
    'Royal Blood Pack',
    'Run-DMC Pack',
    'Rush 5-Song Pack',
    'Rush Song Pack II',
    'Sabaton Song Pack',
    'Santana 3-Song Pack',
    'Seether 3-Song Pack',
    'Sevendust Song Pack',
    'Shamrock 5-Song Pack',
    'Shania Twain Pack',
    'Sheryl Crow Pack',
    'Shinedown 5-Song Pack',
    'Silverstein Song Pack',
    'Sixx:A.M. Song Pack',
    'Skater Rock Pack',
    'Skid Row Pack',
    'Skillet 3-Song Pack',
    'Slash 3-Song Pack',
    'Slayer 5-Song Pack',
    'Social Distortion Song Pack',
    'Social Stars',
    'Soul Hits',
    'Soundgarden 5-Song Pack',
    'Spinal Tap 5-Song Pack',
    'Spooktacular Singles',
    'Staind Song Pack',
    'Stereophonics Pack',
    'Steve Miller Band Pack',
    'Stevie Ray Vaughn & DT Song Pack',
    'Stevie Wonder Song Pack',
    'Stone Sour Song Pack',
    'Stone Temple Pilots 6-Song Pack',
    'Sublime 5-Song Pack',
    'Sum 41 5-Song Pack',
    'Surf Rock 3-Song Pack',
    'Surf Rock II',
    'System of a Down 3-Song Pack',
    'Tegan and Sara Pack',
    'Tenacious D 3-Song Pack',
    'The All-American Rejects 3 Song Pack',
    'The Allman Brothers Band 3-Song Pack',
    'The Black Keys 3-Song Pack',
    'The Black Keys 5-Song Pack',
    'The Cardigans Pack',
    'The Cars 5-Song Pack',
    'The Clash 3-Song Pack',
    'The Cure 3-Song Pack',
    'The Doors 3 Song Pack II',
    'The Doors 3-Song Pack',
    'The Killers 5-Song Pack',
    'The Libertines 3-Song Pack',
    'The Misfits Song Pack',
    'The Monkees Pack',
    'The Offspring 3-Song Pack',
    'The Offspring II 5-Song Pack',
    'The Police 3-Song Pack',
    'The Pretenders Pack',
    'The Pretty Reckless Pack',
    'The Smashing Pumpkins 5-Song Pack',
    'The Stone Roses 3 Song Pack',
    'The Strokes 3-Song Pack',
    'The Strokes II',
    'The White Stripes 5-Song Pack',
    'The Who 5-Song Pack',
    'The Zombies Pack',
    'Thin Lizzy 3-Song Pack',
    'Third Eye Blind Pack',
    'Thirty Seconds to Mars 5-Song Pack',
    'Three Days Grace 5-Song Pack',
    'Thrice Pack',
    'Tom Petty 5-Song Pack',
    'Trans-Siberian Orchestra Pack',
    'Trivium II Pack',
    'Trivium Pack',
    'U2 Pack',
    'UBI30: 1986 Song Pack',
    'Ubisoft Music Song Pack',
    "Valentine's Day 4-Song Pack",
    'Variety Pack IX',
    'Variety Pack V',
    'Variety Pack VI',
    'Variety Pack VII',
    'Variety Pack VIII',
    'Variety Pack X',
    'Variety Pack XI',
    'Variety Pack XII',
    'Variety Pack XIII',
    'Variety Pack XIV',
    'Variety Pack XIX',
    'Variety Pack XV',
    'Variety Pack XVI',
    'Variety Pack XVII',
    'Variety Pack XVIII',
    'Variety Pack XX',
    'Variety Pack XXI',
    'Variety Pack XXII',
    'Variety Song Pack I',
    'Variety Song Pack II',
    'Variety Song Pack III',
    'Variety Song Pack IV',
    'Volbeat Song Pack',
    'Weezer 5-Song Pack',
    'Weezer Song Pack II',
    'Women Who Rock 5-Song Pack',
    'Women Who Rock II',
    'Wrestling Theme Song Pack',
    'Uncategorized Singles',
    'Yacht Rock Singles',
    'Yes Song Pack',
    'Zombie Song Pack',
    'blink-182 II',
]


class Rocksmith2014SongSelection(OptionSet):
    """
    Defines which songs can be selected.

    Replace the placeholders with songs you own or want to practice.
    """

    display_name = "Rocksmith 2014 Song Selection"

    default = BASE_SONGS


class Rocksmith2014DlcPacksOwned(OptionSet):
    """
    Defines which DLC packs are owned.

    Populate from the catalog once DLC packs are added.
    """

    display_name = "Rocksmith 2014 DLC Packs Owned"

    default = DLC_PACK_NAMES


class Rocksmith2014OwnedSongOverrides(OptionSet):
    """
    Additional songs to include regardless of pack toggles.
    """

    display_name = "Rocksmith 2014 Owned Song Overrides"

    default: list[str] = []


class Rocksmith2014ExcludedSongs(OptionSet):
    """
    Exclude specific songs even if they are in selected packs.
    """

    display_name = "Rocksmith 2014 Excluded Songs"

    default: list[str] = []


class Rocksmith2014CdlcSongs(OptionSet):
    """
    Community/Custom DLC (CDLC) songs.
    """

    display_name = "Rocksmith 2014 CDLC Songs"

    default: list[str] = []


class Rocksmith2014AvailableArrangements(OptionSet):
    """
    Select which arrangements can appear in objectives.
    """

    display_name = "Rocksmith 2014 Available Arrangements"

    default = [
        "Lead",
        "Rhythm",
        "Bass",
        "Alternate Lead",
        "Alternate Rhythm",
        "Bonus Arrangement",
    ]


class Rocksmith2014IncludeRs1ImportSongs(Toggle):
    """
    Include Rocksmith 1 import songs.
    """

    display_name = "Rocksmith 2014 Include RS1 Import Songs"


class Rocksmith2014IncludeScoreAttack(DefaultOnToggle):
    """
    Include Score Attack objectives.
    """

    display_name = "Rocksmith 2014 Include Score Attack"


class Rocksmith2014IncludeLessons(DefaultOnToggle):
    """
    Include lesson objectives.
    """

    display_name = "Rocksmith 2014 Include Lessons"


class Rocksmith2014IncludeSessionMode(DefaultOnToggle):
    """
    Include Session Mode objectives.
    """

    display_name = "Rocksmith 2014 Include Session Mode"


class Rocksmith2014IncludeGuitarcade(DefaultOnToggle):
    """
    Include Guitarcade objectives.
    """

    display_name = "Rocksmith 2014 Include Guitarcade"


class Rocksmith2014IncludeMissions(DefaultOnToggle):
    """
    Include mission objectives.
    """

    display_name = "Rocksmith 2014 Include Missions"
