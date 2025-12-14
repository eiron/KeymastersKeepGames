from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class JustDanceArchipelagoOptions:
    just_dance_games_owned: JustDanceGamesOwned
    just_dance_include_unlimited_songs: JustDanceIncludeUnlimitedSongs
    just_dance_dlc_content: JustDanceDLCContent
    just_dance_exclusive_content: JustDanceExclusiveContent
    just_dance_plus_content: JustDancePlusContent


class JustDanceGame(Game):
    name = "Just Dance"
    platform = KeymastersKeepGamePlatforms.SW

    platforms_other = [
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
        KeymastersKeepGamePlatforms.WII,
        KeymastersKeepGamePlatforms.WIIU,
        KeymastersKeepGamePlatforms.X360,
        KeymastersKeepGamePlatforms.PS3,
    ]

    is_adult_only_or_unrated = False

    options_cls = JustDanceArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Only dance to songs from DECADE",
                data={
                    "DECADE": (self.decades, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Only dance to songs by ARTIST",
                data={
                    "ARTIST": (self.artists, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Only dance to GENRE songs",
                data={
                    "GENRE": (self.genres, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Dance to SONG",
                data={
                    "SONG": (self.songs, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Get at least 3 stars on SONG",
                data={
                    "SONG": (self.songs, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get 4 stars on SONG",
                data={
                    "SONG": (self.songs, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get a Megastar on SONG",
                data={
                    "SONG": (self.songs, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    # Property accessors for owned content
    @property
    def games_owned(self) -> List[str]:
        return sorted(self.archipelago_options.just_dance_games_owned.value)

    @property
    def include_unlimited_songs(self) -> bool:
        return bool(self.archipelago_options.just_dance_include_unlimited_songs.value)

    @property
    def dlc_content(self) -> List[str]:
        return sorted(self.archipelago_options.just_dance_dlc_content.value)

    @property
    def exclusive_content(self) -> List[str]:
        return sorted(self.archipelago_options.just_dance_exclusive_content.value)

    @property
    def just_dance_plus_content(self) -> List[str]:
        return sorted(self.archipelago_options.just_dance_plus_content.value)

    # Game ownership checks
    @property
    def has_just_dance_1(self) -> bool:
        return "Just Dance" in self.games_owned

    @property
    def has_just_dance_2(self) -> bool:
        return "Just Dance 2" in self.games_owned

    @property
    def has_just_dance_3(self) -> bool:
        return "Just Dance 3" in self.games_owned

    @property
    def has_just_dance_4(self) -> bool:
        return "Just Dance 4" in self.games_owned

    @property
    def has_just_dance_2014(self) -> bool:
        return "Just Dance 2014" in self.games_owned

    @property
    def has_just_dance_2015(self) -> bool:
        return "Just Dance 2015" in self.games_owned

    @property
    def has_just_dance_2016(self) -> bool:
        return "Just Dance 2016" in self.games_owned

    @property
    def has_just_dance_2017(self) -> bool:
        return "Just Dance 2017" in self.games_owned

    @property
    def has_just_dance_2018(self) -> bool:
        return "Just Dance 2018" in self.games_owned

    @property
    def has_just_dance_2019(self) -> bool:
        return "Just Dance 2019" in self.games_owned

    @property
    def has_just_dance_2020(self) -> bool:
        return "Just Dance 2020" in self.games_owned

    @property
    def has_just_dance_2021(self) -> bool:
        return "Just Dance 2021" in self.games_owned

    @property
    def has_just_dance_2022(self) -> bool:
        return "Just Dance 2022" in self.games_owned

    @property
    def has_just_dance_2023(self) -> bool:
        return "Just Dance 2023 Edition" in self.games_owned

    @property
    def has_just_dance_2024(self) -> bool:
        return "Just Dance 2024 Edition" in self.games_owned

    @property
    def has_just_dance_2025(self) -> bool:
        return "Just Dance 2025 Edition" in self.games_owned

    @property
    def has_just_dance_2026(self) -> bool:
        return "Just Dance 2026 Edition" in self.games_owned

    # Utility properties
    def artists(self) -> List[str]:
        artists = set()
        for song in self.songs():
            # Extract artist from song format "Artist - Song"
            if " - " in song:
                artist = song.split(" - ")[0]
                artists.add(artist)
        return sorted(list(artists))

    def genres(self) -> List[str]:
        return sorted([
            "Pop", "Rock", "Hip-Hop", "Electronic", "Latin", "Country", 
            "R&B", "Classical", "Jazz", "Alternative", "Indie", "Funk"
        ])

    def decades(self) -> List[str]:
        return sorted([
            "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"
        ])

    # Base game song collections
    @functools.cached_property
    def songs_just_dance_1(self) -> List[str]:
        return [
            "Cyndi Lauper - Girls Just Want to Have Fun [JD1]",
            "Anita Ward - Ring My Bell [JD1]",
            "Elvis Presley vs. JXL - A Little Less Conversation (JXL Radio Edit Remix) [JD1]",
            "Rednex - Cotton Eye Joe [JD1]",
            "The Trashmen - Surfin' Bird [JD1]",
            "Blondie - Heart of Glass [JD1]",
            "The Gym All-Stars - Womanizer (Britney Spears) [JD1]",
            "Deee-Lite - Groove Is in the Heart [JD1]",
            "Caesars - Jerk It Out [JD1]",
            "Reel 2 Real feat. The Mad Stuntman - I Like to Move It (Radio Mix) [JD1]",
            "Katy Perry - Hot N Cold [JD1]",
            "Dee Dee Sharp - Mashed Potato Time [JD1]",
            "Blur - Girls & Boys [JD1]",
            "In The Style of Irene Cara - Fame (Irene Cara) [JD1]",
            "The Presidents of the United States of America - Lump [JD1]",
            "Kim Wilde - Kids in America [JD1]",
            "Technotronic - Pump Up the Jam [JD1]",
            "The Beach Boys - I Get Around [JD1]",
            "Chic - Le Freak [JD1]",
            "KC and the Sunshine Band - That's the Way (I Like It) [JD1]",
            "Iggy Pop - Louie Louie [JD1]",
            "The B-52's - Funplex (CSS Remix) [JD1]",
            "Fatboy Slim - Jin Go Lo Ba [JD1]",
            "Gorillaz - Dare [JD1]",
            "Divine Brown - Bebe [JD1]",
            "Survivor - Eye of the Tiger [JD1]",
            "Kylie Minogue - Can't Get You Out of My Head [JD1]",
            "Calvin Harris - Acceptable in the 80s [JD1]",
            "Baha Men - Who Let the Dogs Out? [JD1]",
            "Spice Girls - Wannabe [JD1]",
            "New Kids on the Block - Step by Step [JD1]",
            "MC Hammer - U Can't Touch This [JD1]",
        ]

    @functools.cached_property
    def songs_just_dance_2(self) -> List[str]:
        return [
            "The Weather Girls - It's Raining Men [JD2]",
            "Kesha - TiK ToK [JD2]",
            "Vampire Weekend - A-Punk [JD2]",
            "James Brown - I Got You (I Feel Good) [JD2]",
            "The Pussycat Dolls - When I Grow Up [JD2]",
            "The Hit Crew - Toxic (Britney Spears) [JD2]",
            "Digitalism - Idealistic [JD2]",
            "Avril Lavigne - Girlfriend [JD2]",
            "Rihanna - S.O.S. [JD2]",
            "Sorcerer - Dagomba [JD2]",
            "Junior Senior - Move Your Feet [JD2]",
            "Ike & Tina Turner - Proud Mary [JD2]",
            "Donna Summer - Hot Stuff [JD2]",
            "MIKA - Big Girl (You Are Beautiful) [JD2]",
            "The Jackson 5 - I Want You Back [JD2]",
            "Mardi Gras - Iko Iko [JD2]",
            "Bollywood - Katti Kalandal [JD2]",
            "The Hit Crew - Holiday (Madonna) [JD2]",
            "Blondie - Call Me [JD2]",
            "Marine Band - Sway (Quién Será) (Michael Bublé) [JD2]",
            "Benny Benassi presents \"The Biz\" - Satisfaction (Isak Original Extended) [JD2]",
            "Outkast - Hey Ya! [JD2]",
            "Gert Wilden (Charleston) - Mugsy Baloney [JD2]",
            "Carsten Lindberg & Joachim Svare (Reggaeton) - Baby Girl [JD2]",
            "Studio Musicians - Jungle Boogie (Kool & the Gang) [JD2]",
            "Studio Musicians - Crazy in Love (Beyoncé ft. Jay-Z) [JD2]",
            "Quincy Jones and His Orchestra - Soul Bossa Nova [JD2]",
            "Justice - D.A.N.C.E. [JD2]",
            "The Rolling Stones - Sympathy for the Devil (Fatboy Slim Remix) [JD2]",
            "Boney M. - Rasputin [JD2]",
            "Harry Belafonte - Jump in the Line [JD2]",
            "Wham! - Wake Me Up Before You Go-Go [JD2]",
            "The Bangles - Walk Like an Egyptian [JD2]",
            "Snap! - The Power [JD2]",
            "Studio Allstars - Jump (Kris Kross) [JD2]",
            "The Frighteners - Monster Mash (Boris Pickett and The Crypt Kickers) [JD2]",
            "Franz Ferdinand - Take Me Out [JD2]",
            "The Ting Tings - That's Not My Name [JD2]",
            "Cher - The Shoop Shoop Song (It's in His Kiss) [JD2]",
            "Jamiroquai - Cosmic Girl [JD2]",
            "Beastie Boys - Body Movin' (Fatboy Slim Remix) [JD2]",
            "Elvis Presley - Viva Las Vegas [JD2]",
            "Supergrass - Alright [JD2]",
            "Fatboy Slim - Rockafeller Skank [JD2]",
        ]

    @functools.cached_property
    def songs_just_dance_3(self) -> List[str]:
        return [
            "Katy Perry featuring Snoop Dogg - California Gurls [JD3]",
            "a-ha - Take On Me [JD3]",
            "The Black Eyed Peas - Pump It [JD3]",
            "MIKA - Lollipop [JD3]",
            "Nelly Furtado featuring Timbaland - Promiscuous [JD3]",
            "The Girly Team - Baby One More Time (Britney Spears) [JD3]",
            "Jessie J featuring B.o.B. - Price Tag [JD3]",
            "Scissor Sisters - I Don't Feel Like Dancin' [JD3]",
            "Duck Sauce - Barbra Streisand [JD3]",
            "Bananarama - Venus [JD3]",
            "2 Unlimited - No Limit [JD3]",
            "Taio Cruz - Dynamite [JD3]",
            "CeeLo Green - Forget You [JD3]",
            "Girls Aloud - Jump (For My Love) [JD3]",
            "Sweat Invaders - Gonna Make You Sweat (Everybody Dance Now) (C+C Music Factory feat. Freedom Williams) [JD3]",
            "Gwen Stefani - What You Waiting For? [JD3]",
            "Queen - Crazy Little Thing Called Love [JD3]",
            "The London Theatre Orchestra & Cast - Think (Aretha Franklin) [JD3]",
            "Groove Century - Boogie Wonderland (Earth, Wind & Fire feat. The Emotions) [JD3]",
            "The Chemical Brothers - Hey Boy Hey Girl [JD3]",
            "Reggaeton Storm - Boom [JD3]",
            "Daft Punk - Da Funk [JD3]",
            "Donna Summer - I Feel Love [JD3]",
            "Anja - Dance All Nite [JD3]",
            "Sentai Express - Spectronizer [JD3]",
            "LMFAO featuring Lauren Bennett and GoonRock - Party Rock Anthem [JD3]",
            "Lenny Kravitz - Are You Gonna Go My Way [JD3]",
            "Wilson Pickett - Land Of 1000 Dances [JD3]",
            "Tommy Sparks - She's Got Me Dancing [JD3]",
            "Konshens - Jamaican Dance [JD3]",
            "Cobie Smulders (as Robin Sparkles) - Let's Go To The Mall [JD3]",
            "Madness - Night Boat To Cairo [JD3]",
            "The Pointer Sisters - I'm So Excited [JD3]",
            "The Buggles - Video Killed the Radio Star [JD3]",
            "Bollywood Rainbow - Kurio ko uddah le jana (Lata Mangeshkar and S. P. Balasubrahmanyam) [JD3]",
            "Laura Bell Bundy - Giddy on Up (Giddy on Out) [JD3]",
            "Kiss - I Was Made For Lovin' You [JD3]",
            "Janelle Monae - Tightrope (Solo Version) [JD3]",
            "Countdown Mix Masters - Beautiful Liar (Beyoncé and Shakira) [JD3]",
            "The Sugarhill Gang - Apache (Jump On It) [JD3]",
            "African Ladies - Pata Pata (Miriam Makeba) [JD3]",
            "Robbie Williams and Nicole Kidman - Somethin' Stupid [JD3]",
            "Danny Elfman - This is Halloween [JD3]",
            "Ole Orquesta - Jambo Mambo [JD3]",
            "Anja - Baby Don't Stop Now [JD3]",
            "The Girly Team - Twist and Shake It (Ben Wheeler and Tara Chinn) [JD3]",
            "Groove Century - Soul Searchin' [JD3]",
        ]

    @functools.cached_property
    def songs_just_dance_4(self) -> List[str]:
        return [
            "Carly Rae Jepsen - Call Me Maybe [JD4]",
            "Flo Rida - Good Feeling [JD4]",
            "The B-52's - Rock Lobster [JD4]",
            "Rihanna - Disturbia [JD4]",
            "One Direction - What Makes You Beautiful [JD4]",
            "A.K.A - Hot For Me [JD4]",
            "Las Ketchup - Aserejé (The Ketchup Song) [JD4]",
            "Blu Cantrell - Hit 'Em Up Style (Oops!) [JD4]",
            "Hit The Electro Beat - We No Speak Americano (Yolanda Be Cool and DCUP) [JD4]",
            "The Girly Team - Oops!... I Did It Again (Britney Spears) [JD4]",
            "Justin Bieber ft. Nicki Minaj - Beauty And A Beat [JD4]",
            "Dancing Bros - Everybody Needs Somebody To Love (The Blues Brothers) [JD4]",
            "Anja - Crazy Little Thing [JD4]",
            "Nicki Minaj - Super Bass [JD4]",
            "2 Unlimited - Tribal Dance [JD4]",
            "Jennifer Lopez ft. Pitbull - On the Floor [JD4]",
            "Panjabi MC - Beware of the Boys (Mundian To Bach Ke) [JD4]",
            "Rick Astley - Never Gonna Give You Up [JD4]",
            "Nelly Furtado - Maneater [JD4]",
            "Kat DeLuna ft. Busta Rhymes - Run The Show [JD4]",
            "Ricky Martin - Livin' La Vida Loca [JD4]",
            "Barry White - You're the First, the Last, My Everything [JD4]",
            "Marina and the Diamonds - Oh No! [JD4]",
            "The Blackout Allstars - I Like It [JD4]",
            "Selena Gomez and the Scene - Love You Like A Love Song [JD4]",
            "Army of Lovers - Crucified [JD4]",
            "Sergio Mendes ft. The Black Eyed Peas - Mas Que Nada [JD4]",
            "Sammy - Some Catchin' Up To Do [JD4]",
            "Europe - The Final Countdown [JD4]",
            "Alexandra Stan - Mr. Saxobeat [JD4]",
            "Elvis Presley - Jailhouse Rock [JD4]",
            "Maroon 5 ft. Christina Aguilera - Moves Like Jagger [JD4]",
            "Boys Town Gang - Can't Take My Eyes Off You (Frankie Valli) [JD4]",
            "Will Smith - Wild Wild West [JD4]",
            "P!nk - So What [JD4]",
            "They Might Be Giants - Istanbul (Not Constantinople) [JD4]",
            "Stevie Wonder - Superstition [JD4]",
            "Bill Medley and Jennifer Warnes - (I've Had) The Time Of My Life [JD4]",
            "Skrillex - Rock n' Roll (Will Take You to the Mountain) [JD4]",
            "Halloween Thrills - Time Warp (The Rocky Horror Picture Show Cast) [JD4]",
        ]

    @functools.cached_property
    def songs_just_dance_2014(self) -> List[str]:
        return [
            "One Direction - Kiss You [JD2014]",
            "Lady Gaga feat. Colby O'Donis - Just Dance [JD2014]",
            "George Michael - Careless Whisper [JD2014]",
            "Ke$ha - C'mon [JD2014]",
            "David Guetta feat. Sia - She Wolf (Falling to Pieces) [JD2014]",
            "The Girly Team - Flashdance... What A Feeling (Irene Cara) [JD2014]",
            "Disney's Aladdin - Prince Ali (Robin Williams) [JD2014]",
            "Daft Punk feat. Pharrell Williams - Get Lucky [JD2014]",
            "Jessie J feat. Big Sean - Wild [JD2014]",
            "PSY - Gentleman [JD2014]",
            "Robin Thicke feat. Pharrell Williams - Blurred Lines [JD2014]",
            "Ray Parker Jr. - Ghostbusters [JD2014]",
            "Gloria Gaynor - I Will Survive [JD2014]",
            "will.i.am feat. Justin Bieber - #thatPOWER [JD2014]",
            "Daddy Yankee - Limbo [JD2014]",
            "Ariana Grande feat. Mac Miller - The Way [JD2014]",
            "Nicki Minaj - Pound The Alarm [JD2014]",
            "Frankie Bostello - Love Boat (Jack Jones) [JD2014]",
            "Olly Murs feat. Flo Rida - Troublemaker [JD2014]",
            "Lady Gaga - Applause [JD2014]",
            "Mick Jackson - Blame It on the Boogie [JD2014]",
            "Imposs feat. Konshens - Feel So Right [JD2014]",
            "Mungo Jerry - In the Summertime [JD2014]",
            "Chris Brown - Fine China [JD2014]",
            "Louis Prima - Just A Gigolo [JD2014]",
            "Rihanna - Where Have You Been [JD2014]",
            "Ricky Martin - María [JD2014]",
            "ABBA - Gimme! Gimme! Gimme! (A Man After Midnight) [JD2014]",
            "Dancing Bros. - Moskau (Dschinghis Khan) [JD2014]",
            "Pitbull feat. Christina Aguilera - Feel This Moment [JD2014]",
            "Wisin & Yandel feat. Jennifer Lopez - Follow the Leader [JD2014]",
            "Village People - Y.M.C.A. [JD2014]",
            "Far East Movement feat. Cover Drive - Turn Up the Love [JD2014]",
            "Bob Marley - Could You Be Loved [JD2014]",
            "Nicki Minaj - Starships [JD2014]",
            "Rutschen Planeten - 99 Luftballons (NENA) [JD2014]",
            "Robbie Williams - Candy [JD2014]",
            "Katy Perry - I Kissed a Girl [JD2014]",
            "Bog Bog Orkestar - Isidora [JD2014]",
            "Gwen Stefani feat. Eve - Rich Girl [JD2014]",
            "Duck Sauce - It's You [JD2014]",
            "The Sunlight Shakers - Aquarius/Let the Sunshine In (The 5th Dimension) [JD2014]",
            "Sammie - Miss Understood [JD2014]",
            "Sentai Express - Nitro Bot [JD2014]",
        ]

    @functools.cached_property
    def songs_just_dance_2015(self) -> List[str]:
        return [
            "Ariana Grande feat. Iggy Azalea & Big Sean - Problem [JD2015]",
            "Pharrell Williams - Happy [JD2015]",
            "Ylvis - The Fox (What Does The Fox Say?) [JD2015]",
            "John Newman - Love Me Again [JD2015]",
            "Katy Perry - Dark Horse [JD2015]",
            "The Sunlight Shakers - Love Is All (Roger Glover & the Butterfly Ball) [JD2015]",
            "Rixton - Me And My Broken Heart [JD2015]",
            "Icona Pop feat. Charli XCX - I Love It [JD2015]",
            "Dancing Bros. - Tetris (Hirokazu Tanaka) [JD2015]",
            "Run DMC & Aerosmith - Walk This Way [JD2015]",
            "Disney's Frozen - Let It Go (Idina Menzel) [JD2015]",
            "Becky G - Built For This [JD2015]",
            "Enrique Iglesias feat. Descemer Bueno and Gente de Zona - Bailando [JD2015]",
            "Calvin Harris - Summer [JD2015]",
            "The Bench Men - Don't Worry Be Happy (Bobby McFerrin) [JD2015]",
            "The Girly Team - Macarena (Los Del Rio) [JD2015]",
            "Iggy Azalea feat. Rita Ora - Black Widow [JD2015]",
            "Marvin Gaye & Tammi Terrell - Ain't No Mountain High Enough [JD2015]",
            "Dillon Francis feat. DJ Snake - Get Low [JD2015]",
            "Jessie J feat. Ariana Grande & Nicki Minaj - Bang Bang [JD2015]",
            "Cheb Salama - Fatima (Sylvain Lux & llan Abou) [JD2015]",
            "Bonnie Tyler - Holding Out for a Hero [JD2015]",
            "Katy Perry - Birthday [JD2015]",
            "Love Letter - Only You (And You Alone) (The Platters) [JD2015]",
            "Rihanna - Diamonds [JD2015]",
            "5 Seconds Of Summer - She Looks So Perfect [JD2015]",
            "Bollywood Santa - XMas Tree [JD2015]",
            "One Direction - Best Song Ever [JD2015]",
            "Lady Gaga - Bad Romance [JD2015]",
            "Gloria Gaynor - Never Can Say Goodbye [JD2015]",
            "Dead or Alive - You Spin Me Round (Like a Record) [JD2015]",
            "Miley Cyrus - 4x4 [JD2015]",
            "The Bouzouki's - Epic Sirtaki [JD2015]",
            "will.i.am feat. Cody Wise - It's My Birthday [JD2015]",
            "Ellie Goulding - Burn [JD2015]",
            "Frankie Bostello - Mahna Mahna (Piero Umiliani) [JD2015]",
            "Los Pimientos Locos - Speedy Gonzalez (David Dante) [JD2015]",
            "Maroon 5 - Maps [JD2015]",
            "Imposs feat. J. Perry - You're On My Mind [JD2015]",
            "Avicii - Addicted To You [JD2015]",
            # Special unlockable content
            "Avishay Goren & Yossi Cohen - Movement is Happiness (Find Your Thing) [JD2015]",  # 60min unlock
        ]

    @functools.cached_property
    def songs_just_dance_2015_exclusives(self) -> List[str]:
        """Just Dance 2015 exclusive content."""
        exclusives = []
        
        if "JD2015 - Ubisoft Connect Unlockables" in self.exclusive_content:
            exclusives.extend([
                "Sentai Express - Nitro Bot [JD2015 Ubisoft Connect]",
            ])
        
        return exclusives

    @functools.cached_property
    def songs_just_dance_2016(self) -> List[str]:
        """Base track list for Just Dance 2016 (44 songs)."""
        return [
            "Meghan Trainor - All About That Bass [JD2016]",
            "One Direction - No Control [JD2016]",
            "The Black Eyed Peas - I Gotta Feeling [JD2016]",
            "Iggy Azalea ft. Charli XCX - Fancy [JD2016]",
            "The Girly Team - These Boots Are Made For Walking (Nancy Sinatra)* [JD2016]",
            "Martin Garrix - Animals [JD2016]",
            "Mark Ronson ft. Bruno Mars - Uptown Funk [JD2016]",
            "Angry Birds - Balkan Blast Remix [JD2016]",
            "Kelly Clarkson - Heartbeat Song [JD2016]",
            "David Guetta ft. Nicki Minaj, Bebe Rexha & Afrojack - Hey Mama [JD2016]",
            "Hatsune Miku - Ievan Polkka [JD2016]",
            "Darius Dante Van Dijk - The Choice Is Yours [JD2016]",
            "Pitbull ft. Chris Brown - Fun [JD2016]",
            "Rossini - William Tell Overture [JD2016]",
            "Ellie Goulding - Lights [JD2016]",
            "Wanko Ni Mero Mero - Chiwawa [JD2016]",
            "A. Caveman & The Backseats - You Never Can Tell (Chuck Berry)* [JD2016]",
            "Lady Gaga - Born This Way [JD2016]",
            "Nikki Yanofsky - Kaboom Pow [JD2016]",
            "Sky Trucking - When The Rain Begins To Fall (Jermaine Jackson and Pia Zadora)* [JD2016]",
            "Selena Gomez - Same Old Love [JD2016]",
            "Demi Lovato - Cool For The Summer [JD2016]",
            "Jason Derulo - Want To Want Me [JD2016]",
            "Disney's \"The Little Mermaid\" - Under the Sea (Samuel E. Wright)* [JD2016]",
            "Katy Perry - This Is How We Do [JD2016]",
            "Charles Percy - Hit The Road Jack (Ray Charles)* [JD2016]",
            "Disney's \"Violetta\" - Junto a Ti (Martina Stoessel & Lodovica Comello) [JD2016]",
            "Calvin Harris ft. John Newman - Blame [JD2016]",
            "O'Callaghan's Orchestra - Irish Meadow Dance [JD2016]",
            "Shakira ft. El Cata - Rabiosa [JD2016]",
            "Britney Spears - Circus [JD2016]",
            "From The Movie Grease - You're The One That I Want (John Travolta & Olivia Newton-John)* [JD2016]",
            "Buraka Som Sistema - Hangover (BaBaBa) [JD2016]",
            "AronChupa - I'm An Albatraoz [JD2016]",
            "Glorious Black Belts - Kool Kontact [JD2016]",
            "Nick Jonas - Teacher [JD2016]",
            "Prince Royce - Stuck On A Feeling [JD2016]",
            "The Lemon Cubes - Boys (Summertime Love) (Sabrina Salerno)* [JD2016]",
            "Diva Carmina - Drop the Mambo [JD2016]",
            "MAX - Gibberish [JD2016]",
            "Frankie Bostello - Copacabana (Barry Manilow)* [JD2016]",
            "Equinox Stars - Let's Groove (Earth, Wind & Fire)* [JD2016]",
            "Imposs - Stadium Flow [JD2016]",
        ]

    @functools.cached_property
    def songs_just_dance_2016_exclusives(self) -> List[str]:
        """Just Dance 2016 exclusive content."""
        exclusives = []
        
        if "JD2016 - Ubisoft Connect Unlockables" in self.exclusive_content:
            exclusives.extend([
                "Sorcerer - Dagomba [JD2016 Ubisoft Connect]",
                "Sentai Express - Spectronizer [JD2016 Ubisoft Connect]",
                "Imposs ft. Konshens - Feel So Right [JD2016 Ubisoft Connect]",
                "Bog Bog Orkestar - Isidora [JD2016 Ubisoft Connect]",
                "The Bouzouki's - Epic Sirtaki [JD2016 Ubisoft Connect]",
                "Bollywood Santa - XMas Tree [JD2016 Ubisoft Connect]",
                "Imposs ft. J.Perry - You're On My Mind [JD2016 Ubisoft Connect]",
            ])
        
        if "JD2016 - Russia Exclusive" in self.exclusive_content:
            exclusives.extend([
                "IOWA - Smile (Улыбайся) [JD2016 Russia Exclusive]",
            ])
        
        return exclusives

    @functools.cached_property
    def songs_just_dance_2016_just_dance_unlimited(self) -> List[str]:
        """Just Dance 2016 DLC content (Just Dance Unlimited)."""
        dlc_songs = []
        
        if "JD2016 - Just Dance Unlimited" in self.dlc_content:
            dlc_songs.extend([
                "OMI - Cheerleader (Felix Jaehn Remix) [JD2016 DLC]",
                "IOWA - Улыбайся (Smile) [JD2016 DLC]",  # Also available as DLC
                "Meghan Trainor - Better When I'm Dancin' [JD2016 DLC]",
                "Walk the Moon - Shut Up and Dance [JD2016 DLC]",
                "Jason Derulo - Get Ugly [JD2016 DLC]",
                "Avicii vs. Conrad Sewell - Taste The Feeling [JD2016 DLC]",
                "Nico & Vinz - Am I Wrong [JD2016 DLC]",
                "Jess Glynne - Hold My Hand [JD2016 DLC]",
                "Imposs - Stadium Flow (Fanmade) [JD2016 DLC]",
                "Avicii vs. Conrad Sewell - Taste The Feeling (Alternate) [JD2016 DLC]",
                "Katy Perry - This Is How We Do (Fanmade) [JD2016 DLC]",
            ])
        
        return dlc_songs

    @functools.cached_property
    def songs_just_dance_2017(self) -> List[str]:
        return [
            "DNCE - Cake By The Ocean [JD2017]",
            "Sia ft. Sean Paul - Cheap Thrills [JD2017]", 
            "PSY ft. CL of 2NE1 - DADDY [JD2017]",
            "Justin Bieber - Sorry [JD2017]",
            "Shakira ft. Wyclef Jean - Hips Don't Lie [JD2017]",
            "Earth, Wind & Fire - September [JD2017]",
            "Beyoncé - Single Ladies (Put a Ring on It) [JD2017]",
            "Queen - Don't Stop Me Now [JD2017]",
            "Major Lazer & DJ Snake ft. MØ - Lean On [JD2017]",
            "The Weeknd - Can't Feel My Face [JD2017]",
            "Hatsune Miku - PoPiPo [JD2017]",
            "Ariana Grande - Into You [JD2017]",
            "Maroon 5 - Don't Wanna Know [JD2017]",
            "Anitta - Bang [JD2017]",
            "Halloween Thrills - Ghost In The Keys [JD2017]",
            "Dyro & Dannic - RADICAL [JD2017]",
            "Carlos Vives & Shakira - La Bicicleta [JD2017]",
            "OneRepublic - Wherever I Go [JD2017]",
            "Silentó - Watch Me (Whip/Nae Nae) [JD2017]",
            "Joan Jett & The Blackhearts - I Love Rock 'N' Roll [JD2017]",
            "Era Istrefi - Bonbon [JD2017]",
            "Jack & Jack - Groove [JD2017]",
            "Wanko Ni Mero Mero - Oishii Oishii [JD2017]",
            "Fifth Harmony ft. Kid Ink - Worth It [JD2017]",
            "Latino Sunset - Carnaval Boom [JD2017]",
            "Jordan Fisher - All About Us [JD2017]",
            "Cheb Salama - Leila [JD2017]",
            "INNA ft. J Balvin - Cola Song [JD2017]",
            "AronChupa ft. Little Sis Nora - Little Swing [JD2017]",
            "Gigi Rowe - Run The Night [JD2017]",
            "O-Zone - Dragostea Din Tei [JD2017]",
            "will.i.am ft. Britney Spears - Scream & Shout [JD2017]",
            "Zequinha de Abreu - Tico-Tico No Fubá [JD2017]",
            "Deorro ft. Elvis Crespo - Bailar [JD2017]",
            "David Guetta ft. Sia - Titanium [JD2017]",
            "Daya Luz - Te Dominar [JD2017]",
            "Haddaway - What Is Love [JD2017]",
            "Maluma - El Tiki [JD2017]",
            # Nintendo Switch version specific songs (replacing Like I Would and Last Christmas)
            "Wanko Ni Mero Mero - Chiwawa [JD2017]",  # Switch exclusive
            "Rossini - William Tell Overture [JD2017]",  # Switch exclusive
        ]

    @functools.cached_property
    def songs_just_dance_2017_exclusives(self) -> List[str]:
        exclusive_songs = []
        
        # Ubisoft Connect Exclusives
        if "JD2017 - Ubisoft Connect Unlockables" in self.exclusive_content:
            exclusive_songs.extend([
                "Diva Carmina - Drop the Mambo [JD2017 Ubisoft Connect]",
                "Glorious Black Belts - Kool Kontact [JD2017 Ubisoft Connect]",
                "DJ Snake feat. Justin Bieber - Let Me Love You [JD2017 Ubisoft Connect]",
                "Rossini - William Tell Overture [JD2017 Ubisoft Connect]",
            ])
        
        # Russia Exclusive
        if "JD2017 - Russia Exclusive" in self.exclusive_content:
            exclusive_songs.extend([
                "Vremya i Steklo - Imya 505 [JD2017 Russia Exclusive]",
            ])
        
        return exclusive_songs

    @functools.cached_property
    def songs_just_dance_2017_platform_exclusives(self) -> List[str]:
        """Platform exclusive content for Just Dance 2017 (Nintendo Switch exclusives)"""
        return [
            "Wanko Ni Mero Mero - Chiwawa [JD2017 Switch Exclusive]",
            "Rossini - William Tell Overture [JD2017 Switch Exclusive]",
        ]

    @functools.cached_property
    def songs_just_dance_2017_just_dance_unlimited(self) -> List[str]:
        if "JD2017 - Just Dance Unlimited" in self.dlc_content:
            return [
                "Troye Sivan - YOUTH [JD2017 DLC]",
                "Vremya i Steklo - Imya 505 [JD2017 DLC]",
                "Weekend - Ona tańczy dla mnie [JD2017 DLC]",
                "Natoo - Je sais pas danser [JD2017 DLC]",
                "DNCE - Cake By The Ocean (VIP) [JD2017 DLC]",
                "Sia - The Greatest [JD2017 DLC]",
                "Wanko Ni Mero Mero - Oishii Oishii (VIP) [JD2017 DLC]",
                "Shakira ft. Wyclef Jean - Hips Don't Lie (VIP) [JD2017 DLC]",
                "Zay Hilfigerrr & Zayion McCall - Juju On That Beat [JD2017 DLC]",
                "Madcon ft. Ray Dalton - Don't Worry [JD2017 DLC]",
                "Wanko Ni Mero Mero - Chiwawa (Remastered Version, by Barbie) [JD2017 DLC]",
                "Meghan Trainor - Me Too [JD2017 DLC]",
                "Calvin Harris & Disciples - How Deep Is Your Love [JD2017 DLC]",
                "Fitz & the Tantrums - HandClap [JD2017 DLC]",
                "The Chainsmokers ft. Daya - Don't Let Me Down [JD2017 DLC]",
                "Zara Larsson - Ain't My Fault [JD2017 DLC]",
                "Wham! - Wake Me Up Before You Go-Go (From The Emoji Movie) [JD2017 DLC]",
                "Fitz and the Tantrums - HandClap (World Cup Champion Version) [JD2017 DLC]",
                "DJ Snake ft. Justin Bieber - Let Me Love You [JD2017 DLC]",
                # Nintendo Switch Unlimited exclusives
                "Zayn - Like I Would [JD2017 DLC]",
                "Wham! - Last Christmas [JD2017 DLC]",
            ]
        return []

    @functools.cached_property
    def songs_just_dance_2018(self) -> List[str]:
        """Base disc songs for Just Dance 2018"""
        return [
            "Bruno Mars - 24K Magic [JD2018]",
            "HyunA - Bubble Pop! [JD2018]", 
            "Big Freedia - Make It Jingle [JD2018]",
            "Luis Fonsi & Daddy Yankee - Despacito [JD2018]",
            "Jax Jones ft. Demi Lovato and Stefflon Don - Instruction [JD2018]",
            "Auli'i Cravalho - How Far I'll Go (Disney's Moana) [JD2018]",
            "Ariana Grande ft. Nicki Minaj - Side to Side [JD2018]",
            "Hatsune Miku - Love Ward [JD2018]",
            "Ed Sheeran - Shape of You [JD2018]",
            "Shakira ft. Maluma - Chantaje [JD2018]",
            "Shakira - Waka Waka (This Time for Africa) [JD2018]",
            "Boney M. - Daddy Cool (Groove Century) [JD2018]",
            "Clean Bandit ft. Sean Paul & Anne-Marie - Rockabye [JD2018]",
            "Headhunterz & KSHMR - Dharma [JD2018]",
            "Brian Hyland - Itsy Bitsy Teenie Weenie Yellow Polka Dot Bikini (The Sunlight Shakers) [JD2018]",
            "Jamiroquai - Automaton [JD2018]",
            "Yemi Alade - Tumbum [JD2018]",
            "Dancing Bros. - In the Hall of the Pixel King [JD2018]",
            "Katy Perry ft. Nicki Minaj - Swish Swish [JD2018]",
            "The Just Dance Band - All You Gotta Do (Is Just Dance) [JD2018]",
            "DNCE ft. Nicki Minaj - Kissing Strangers [JD2018]",
            "Lady Gaga - John Wayne [JD2018]",
            "Jorge Blanco - Risky Business [JD2018]",
            "Queen - Another One Bites the Dust [JD2018]",
            "Beyoncé - Naughty Girl [JD2018]",
            "LilDeuceDeuce ft. BlackGryph0n & TomSka - Beep Beep I'm A Sheep [JD2018]",
            "Lights - Fight Club [JD2018]",
            "Dua Lipa - Blow Your Mind (Mwah) [JD2018]",
            "Georges Bizet - Carmen (Ouverture) (The Just Dance Orchestra) [JD2018]",
            "Michelle Delamor - Keep on Moving [JD2018]",
            "Psy - New Face [JD2018]",
            "Kenny Loggins - Footloose (Top Culture) [JD2018]",
            "Bebe Rexha ft. Lil Wayne - The Way I Are (Dance With Somebody) [JD2018]",
            "Iggy Azalea ft. Zedd - Boom Boom [JD2018]",
            "Wanko Ni Mero Mero - Sayonara [JD2018]",
            "Spencer Ludwig - Diggy [JD2018]",
            "Britney Spears ft. Tinashe - Slumber Party [JD2018]",
            "Selena Gomez - Bad Liar [JD2018]",
            "Gigi Rowe - Got That [JD2018]",
            "Eiffel 65 - Blue (Da Ba Dee) (Hit The Electro Beat) [JD2018]",
        ]

    @functools.cached_property
    def songs_just_dance_2018_exclusives(self) -> List[str]:
        """Ubisoft Connect exclusive and regional exclusive songs for Just Dance 2018"""
        exclusives = []
        
        if "JD2018 - Ubisoft Connect Unlockables" in self.exclusive_content:
            exclusives.extend([
                "Sabrina Carpenter - Thumbs [JD2018 Ubisoft Connect]",
                "The Just Dance Band - Sugar Dance [JD2018 Code Unlock]",
            ])
            
        if "JD2018 - Russia Exclusive" in self.exclusive_content:
            exclusives.extend([
                "Demo - Sun (Солнышко) [JD2018 Russia Exclusive]",
            ])
            
        return exclusives

    @functools.cached_property
    def songs_just_dance_2018_platform_exclusives(self) -> List[str]:
        """Platform exclusive content for Just Dance 2018 (Nintendo Switch Double Rumble)"""
        return [
            "Just Vibes - Better Call The Handyman [JD2018 Switch Double Rumble]",
            "Artistas Varios - El Sabor Del Ritmo [JD2018 Switch Double Rumble]",
            "Artistas Varios - Food Paradise [JD2018 Switch Double Rumble]",
            "Artistas Varios - Sports 'Til I Drop [JD2018 Switch Double Rumble]",
            "Artistas Varios - Tales Of The Cauldron [JD2018 Switch Double Rumble]",
        ]

    @functools.cached_property
    def songs_just_dance_2018_just_dance_unlimited(self) -> List[str]:
        """Just Dance Unlimited tracks available for Just Dance 2018"""
        return [
            "Andy Raconte - J'suis pas jalouse [JD2018 DLC]",
            "Natalia Nykiel - Error [JD2018 DLC]",
            "The Just Dance Band - All You Gotta Do (Is Just Dance) (VIPMADE) [JD2018 DLC]",
            "Portugal. The Man - Feel It Still [JD2018 DLC]",
            "J Balvin & Willy William - Mi Gente [JD2018 DLC]",
            "Beyoncé - Naughty Girl (Rabbid Peach Version) [JD2018 DLC]",
            "Fleur East - Sax [JD2018 DLC]",
            "Maroon 5 ft. SZA - What Lovers Do [JD2018 DLC]",
            "El Chombo ft. Cutty Ranks - Dame Tu Cosita [JD2018 DLC]",
            "ABBA - Dancing Queen [JD2018 DLC]",
            "Sean Paul ft. Dua Lipa - No Lie [JD2018 DLC]",
        ]

    @functools.cached_property
    def songs_just_dance_2019(self) -> List[str]:
        """Base disc songs for Just Dance 2019"""
        return [
            "Daddy Yankee - Shaky Shaky [JD2019]",
            "SEREBRO - Mi Mi Mi (Hit The Electro Beat) [JD2019]",
            "Lady Leshurr ft. Wiley - Where Are You Now? [JD2019]",
            "BIGBANG - Bang Bang Bang [JD2019]",
            "Glorious Black Belts - Shinobi Cat [JD2019]",
            "Halloween Thrills - Friendly Phantom [JD2019]",
            "Britney Spears - Work Work [JD2019]",
            "Corona - Rhythm of the Night (Ultraclub 90) [JD2019]",
            "A. Caveman and the Backseats - Boogiesaurus [JD2019]",
            "Groove Century - Monsters of Jazz [JD2019]",
            "Mayra Verónica - Mama Mia [JD2019]",
            "LLP ft. Mike Diamondz - Fire [JD2019]",
            "Elton John - I'm Still Standing (Top Culture) [JD2019]",
            "Santa Clones - Jingle Bells [JD2019]",
            "Plastic Bertrand - Ça Plane Pour Moi (Bob Platine) [JD2019]",
            "O'Callagan's Orchestra - Irish Meadow Dance [JD2019]",
            "Blasterjaxx & Timmy Trumpet - Narco [JD2019]",
            "The Weeknd ft. Daft Punk - I Feel It Coming [JD2019]",
            "MC Fioti, Future, J Balvin, Stefflon Don, Juan Magan - Bum Bum Tam Tam [JD2019]",
            "Persian Nights - Tales of the Desert [JD2019]",
            "Equinox Stars - Cosmic Party [JD2019]",
            "Ece Seçkin - Adeyyo [JD2019]",
            "Bruno Mars ft. Cardi B - Finesse (Remix) [JD2019]",
            "Dua Lipa - New Rules [JD2019]",
            "Camila Cabello - Havana [JD2019]",
            "Gigi Rowe - New Reality [JD2019]",
            "Krewella, Yellow Claw ft. Vava - New World [JD2019]",
            "Sean Paul, David Guetta ft. Becky G - Mad Love [JD2019]",
            "Fergie ft. Q-Tip, GoonRock - A Little Party Never Killed Nobody (All We Got) [JD2019]",
            "Arash ft. Snoop Dogg - OMG [JD2019]",
            "Toshio Kai - Pac-Man (Dancing Bros.) [JD2019]",
            "Lizzo - Water Me [JD2019]",
            "Stella Mwangi - Not Your Ordinary [JD2019]",
            "Maroon 5 - Sugar [JD2019]",
            "Slawomir - Milosc W Zakopanem [JD2019]",
            "Flo Rida - Sweet Sensation [JD2019]",
            "Bea Miller - Sweet Little Unforgettable Thing [JD2019]",
            "Gael García Bernal & Anthony Gonzalez - Un Poco Loco (Disney's Coco) [JD2019]",
            "Netta - TOY [JD2019]",
            "Ariana Grande - No Tears Left To Cry [JD2019]",
            "Liam Payne & J Balvin - Familiar [JD2019]",
            "Calvin Harris & Dua Lipa - One Kiss [JD2019]",
            "AronChupa ft. Little Sis Nora - Rave in the Grave [JD2019]",
            "Pharrell Williams x Camila Cabello - Sangria Wine [JD2019]",
            "Luis Fonsi ft. Stefflon Don - Calypso [JD2019]",
            "BLACKPINK - DDU-DU DDU-DU [JD2019]",
            "Aventura - Obsesión [JD2019]",
            "Janelle Monáe - Make Me Feel [JD2019]",
        ]

    @functools.cached_property
    def songs_just_dance_2019_code_unlock(self) -> List[str]:
        """Code exclusive songs for Just Dance 2019"""
        return [
            "Michelle Delamor - Fire On The Dancefloor [JD2019 Code Unlock]",
        ]

    @functools.cached_property
    def songs_just_dance_2019_middle_east_exclusive(self) -> List[str]:
        """Middle East exclusive songs for Just Dance 2019"""
        return [
            "Maan Barghouth - Hala Bel Khamis [JD2019 Middle East Exclusive]",
        ]

    @functools.cached_property
    def songs_just_dance_2019_france_canada_exclusive(self) -> List[str]:
        """France/Canada exclusive songs for Just Dance 2019"""
        return [
            "McFly & Carlito - On Ne Porte Pas De Sous-Vêtements [JD2019 France/Canada Exclusive]",
        ]

    @functools.cached_property
    def songs_just_dance_2019_russia_exclusive(self) -> List[str]:
        """Russia exclusive songs for Just Dance 2019"""
        return [
            "Bremenskiye Muzykanty - There Is Nothing Better In The World (Ничего на свете лучше нету) [JD2019 Russia Exclusive]",
        ]

    @functools.cached_property
    def songs_just_dance_2019_just_dance_unlimited(self) -> List[str]:
        """Just Dance Unlimited tracks available for Just Dance 2019"""
        return [
            "Charlie Puth ft. Kehlani - Done For Me [JD2019 DLC]",
            "BIGBANG - Bang Bang Bang (VIPMADE) [JD2019 DLC]",
            "Gigi Rowe - New Reality (VIPMADE) [JD2019 DLC]",
            "Katy Perry ft. Nicki Minaj - Swish Swish (VIPMADE) [JD2019 DLC]",
            "LULU - Leg Song [JD2019 DLC]",
            "Alan Tam - Karaoke Forever - Future Underworld Mix [JD2019 DLC]",
            "Anitta - Medicina [JD2019 DLC]",
            "Zara Larsson - Lush Life [JD2019 DLC]",
            "Natti Natasha and Ozuna - Criminal [JD2019 DLC]",
            "Anitta - Medicina (Extreme Version) [JD2019 DLC]",
            "Major Lazer ft. Busy Signal - Jump [JD2019 DLC]",
            "Galantis - Peanut Butter Jelly [JD2019 DLC]",
            "Jax Jones ft. RAYE - You Don't Know Me [JD2019 DLC]",
            "Lizzo - Boys [JD2019 DLC]",
            "Becky G ft. Bad Bunny - Mayores [JD2019 DLC]",
        ]

    @functools.cached_property
    def songs_just_dance_2020(self) -> List[str]:
        """Base disc tracks for Just Dance 2020"""
        return [
            "Ariana Grande - 7 rings [JD2020]",
            "Lil Nas X ft. Billy Ray Cyrus - Old Town Road (Remix) [JD2020]",
            "Little Big - Skibidi [JD2020]",
            "Stella Mwangi - MA ITŪ [JD2020]",
            "Daddy Yankee ft. Snow - Con Calma [JD2020]",
            "Merk & Kremont - Sushi [JD2020]",
            "BLACKPINK - Kill This Love [JD2020]",
            "Pinkfong - Baby Shark [JD2020]",
            "DJ Snake ft. Selena Gomez, Ozuna, Cardi B - Taki Taki [JD2020]",
            "Pitbull ft. Marc Anthony - Rain Over Me [JD2020]",
            "Omer Adam ft. Arisa - Tel Aviv [JD2020]",
            "Jolin Tsai - Ugly Beauty (​怪美的​) [JD2020]",
            "Billie Eilish - bad guy [JD2020]",
            "Panic! At the Disco - High Hopes [JD2020]",
            "Imagination (Equinox Stars) - Just An Illusion [JD2020]",
            "Ariana Grande - God Is A Woman [JD2020]",
            "Cardi B, Bad Bunny & J Balvin - I Like It [JD2020]",
            "XS Project - Vodovorot [JD2020]",
            "2NE1 - I Am the Best [JD2020]",
            "The Streets - Fit But You Know It [JD2020]",
            "Eva Simons ft. Konshens - Policeman [JD2020]",
            "Backstreet Boys (Millennium Alert) - Everybody (Backstreet's Back) [JD2020]",
            "Skrillex ft. Sirah - Bangarang [JD2020]",
            "TWICE - FANCY [JD2020]",
            "Bomba Estéreo - Soy Yo [JD2020]",
            "La Compagnie Créole (Dr. Creole) - Le Bal Masqué [JD2020]",
            "The Black Eyed Peas - The Time (Dirty Bit) [JD2020]",
            "VAVA ft. Ty & Nina Wang - My New Swag (我的新衣) [JD2020]",
            "Jacques Offenbach (The Just Dance Orchestra) - Infernal Galop (Can-Can) [JD2020]",
            "ROSALÍA & J Balvin ft. El Guincho - Con Altura [JD2020]",
            "Royal Republic - Stop Movin' [JD2020]",
            "Lexa - Só Depois do Carnaval [JD2020]",
            "Khalid - Talk [JD2020]",
            "Riton & Kah-Lo - Bad Boy [JD2020]",
            "JD McCrary - Keep in Touch [JD2020]",
            "Zedd & Katy Perry - 365 [JD2020]",
            "KOYOTIE - Get Busy [JD2020]",
            "Netta - Bassa Sababa [JD2020]",
            "Chromeo - Fancy Footwork [JD2020]",
            "Ed Sheeran & Justin Bieber - I Don't Care [JD2020]",
        ]

    @functools.cached_property
    def songs_just_dance_2020_japan_exclusive(self) -> List[str]:
        return [
            "NiziU - Make you happy [JD2020 Japan Exclusive]",
            "NiziU - Step and a step [JD2020 Japan Exclusive]", 
            "NiziU - Poppin' Shakin' [JD2020 Japan Exclusive]",
            "NiziU - Take a picture [JD2020 Japan Exclusive]",
            "The Black Eyed Peas - Boom Boom Pow (Japan Ver.) [JD2020 Japan Exclusive]",
            "The Black Eyed Peas - I Gotta Feeling (Japan Ver.) [JD2020 Japan Exclusive]",
            "The Black Eyed Peas - My Humps (Japan Ver.) [JD2020 Japan Exclusive]",
            "The Black Eyed Peas - Where Is the Love? (Japan Ver.) [JD2020 Japan Exclusive]",
            "The Black Eyed Peas - Let's Go (Japan Ver.) [JD2020 Japan Exclusive]",
            "TRF - EZ DO DANCE [JD2020 Japan Exclusive]",
        ]

    @functools.cached_property
    def songs_just_dance_2020_france_exclusive(self) -> List[str]:
        return [
            "Tal - Le sens de la vie [JD2020 France Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2020_benelux_exclusive(self) -> List[str]:
        return [
            "K3 - Roller Disco [JD2020 Benelux Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2020_russia_exclusive(self) -> List[str]:
        return [
            "LOBODA - SuperStar [JD2020 Russia Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2020_just_dance_unlimited(self) -> List[str]:
        """Just Dance Unlimited tracks available for Just Dance 2020"""
        return [
            "Aya Nakamura - Djadja [JD2020 DLC]",
            "Lil Nas X - Panini [JD2020 DLC]",
            "Monatik - Spinning (Кружит) [JD2020 DLC]",
            "K3 - 10.000 luchtballonnen [JD2020 DLC]",
            "Jonas Brothers - Sucker [JD2020 DLC]",
            "Mabel - Don't Call Me Up [JD2020 DLC]",
            "Charli XCX & Troye Sivan - 1999 [JD2020 DLC]",
            "Little Mix ft. Nicki Minaj - Woman Like Me [JD2020 DLC]",
            "Nicky Jam ft. J Balvin - X [JD2020 DLC]",
            "Lizzo - Boys (Voguing Version) [JD2020 DLC]",
            "Krewella, Yellow Claw ft. Vava - New World (World Cup Champion Version) [JD2020 DLC]",
            "Dizzee Rascal & Calvin Harris - Hype [JD2020 DLC]",
            "Becky G and Maluma - La Respuesta [JD2020 DLC]",
            "G-Dragon - Crayon (크레용) [JD2020 DLC]",
            "Disclosure ft. AlunaGeorge - White Noise [JD2020 DLC]",
        ]

    @functools.cached_property
    def songs_just_dance_2021(self) -> List[str]:
        """Base disc tracks for Just Dance 2021"""
        return [
            "Harry Styles - Adore You [JD2021]",
            "Claude François (Jérôme Francis) - Alexandrie Alexandra [JD2021]",
            "Billie Eilish - all the good girls go to hell [JD2021]",
            "Paradisio ft. DJ Patrick Samoy - Bailando [JD2021]",
            "The Weeknd - Blinding Lights [JD2021]",
            "Alex Newell - Boy, You Can Keep It [JD2021]",
            "GTA & Jenn Morel - Buscando [JD2021]",
            "Tones And I - Dance Monkey [JD2021]",
            "DJ Fresh & Jay Fay ft. Ms. Dynamite - Dibby Dibby Sound [JD2021]",
            "Dua Lipa - Don't Start Now [JD2021]",
            "Twice - Feel Special [JD2021]",
            "Tiggs Da Author - Georgia [JD2021]",
            "Paul Johnson - Get Get Down [JD2021]",
            "Dreamers - Heat Seeker [JD2021]",
            "BLACKPINK & Selena Gomez - Ice Cream [JD2021]",
            "Village People (The Sunlight Shakers) - In The Navy [JD2021]",
            "Black Cats - Joone Khodet [JD2021]",
            "Lizzo - Juice [JD2021]",
            "NCT 127 - Kick It [JD2021]",
            "Toño Rosario - Kulikitaka [JD2021]",
            "Apashe - Lacrimosa [JD2021]",
            "DJ Snake - Magenta Riddim [JD2021]",
            "The Just Dance Band - Paca Dance [JD2021]",
            "Daddy Yankee - Que Tire Pa Lante [JD2021]",
            "Lady Gaga & Ariana Grande - Rain On Me [JD2021]",
            "Selena Gomez - Rare [JD2021]",
            "Galantis - Runaway (U & I) [JD2021]",
            "Bellini (Ultraclub 90) - Samba de Janeiro [JD2021]",
            "Doja Cat - Say So [JD2021]",
            "Shawn Mendes & Camila Cabello - Señorita [JD2021]",
            "Sean Paul - Temperature [JD2021]",
            "SZA & Justin Timberlake - The Other Side [JD2021]",
            "Michael Gray - The Weekend [JD2021]",
            "Britney Spears (The Girly Team) - Till The World Ends [JD2021]",
            "Little Big - UNO [JD2021]",
            "Lele Pons ft. Susan Diaz & Victor Cardenas - Volar [JD2021]",
            "Eminem - Without Me [JD2021]",
            "DJ Absi - Yameen Yasar [JD2021]",
            "J Balvin & Bad Bunny - YO LE LLEGO [JD2021]",
            "Randy Newman (Disney•Pixar's Toy Story) - You've Got a Friend In Me [JD2021]",
            "ONUKA - Zenit [JD2021]",
        ]

    @functools.cached_property
    def songs_just_dance_2021_just_dance_unlimited(self) -> List[str]:
        """Just Dance Unlimited tracks available for Just Dance 2021"""
        return [
            "K/DA ft. Aluna, Wolftyla, and Bekuh BOOM - DRUM GO DUM [JD2021 DLC]",
            "K3 - Dans van de Farao [JD2021 DLC]",
            "Bilal Hassani ft. Sundy Jules, Paola Locatelli, and Sulivan Gwed - Flash (Just Dance Version) [JD2021 DLC]",
            "Lizzo - Juice (VIPMADE) [JD2021 DLC]",
            "KAROL G and Nicki Minaj - Tusa [JD2021 DLC]",
            "Lady Gaga - Stupid Love [JD2021 DLC]",
            "Tinie Tempah ft. Zara Larsson - Girls Like [JD2021 DLC]",
            "Luis Fonsi ft. Stefflon Don - Calypso (Community Remix) [JD2021 DLC]",
            "EXO - Monster [JD2021 DLC]",
            "Timbaland ft. Keri Hilson, D.O.E. & Sebastian - The Way I Are [JD2021 DLC]",
            "2NE1 - Come Back Home [JD2021 DLC]",
            "Joel Corry ft. MNEK - Head & Heart [JD2021 DLC]",
            "Martin Solveig & GTA - Intoxicated [JD2021 DLC]",
            "Sho Madjozi - John Cena [JD2021 DLC]",
            "Kendrick Lamar & SZA - All The Stars [JD2021 DLC]",
            "Yi Yan/Zhao Fang Jing/Suika Kune/Feizaojun - Rainbow Beats [JD2021 DLC]",
        ]

    @functools.cached_property
    def songs_just_dance_2021_japan_exclusive(self) -> List[str]:
        return [
            "Da Pump - U.S.A. [JD2021 Japan Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2021_france_exclusive(self) -> List[str]:
        return [
            "Bilal Hassani ft. Sundy Jules, Paola Locatelli & Sulivan Gwed - Flash (Just Dance Version) [JD2021 France Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2021_benelux_exclusive(self) -> List[str]:
        return [
            "K3 - Dans van de Farao [JD2021 Benelux Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2022(self) -> List[str]:
        return [
            "Bakermat - Baianá [JD2022]",
            "Imagine Dragons - Believer [JD2022]",
            "aespa - Black Mamba [JD2022]",
            "BLACKPINK - BOOMBAYAH [JD2022]",
            "Doja Cat - Boss Witch [JD2022]",
            "Bella Poarch - Build A B**** [JD2022]",
            "The Pussycat Dolls ft. Snoop Dogg - Buttons [JD2022]",
            "El Chombo - Chacarron [JD2022]",
            "Sia - Chandelier [JD2022]",
            "Camila Cabello - Don't Go Yet [JD2022]",
            "Pabllo Vittar ft. Charli XCX - Flash Pose [JD2022]",
            "Gala - Freed from Desire [JD2022]",
            "Meghan Trainor - Funk [JD2022]",
            "Black Eyed Peas & Shakira - GIRL LIKE ME [JD2022]",
            "Olivia Rodrigo - good 4 u [JD2022]",
            "Billie Eilish - Happier Than Ever [JD2022]",
            "Sevdaliza - Human [JD2022]",
            "Anastacia - I'm Outta Love [JD2022]",
            "Master KG ft. Nomcebo Zikode - Jerusalema [JD2022]",
            "SuperM - Jopping [JD2022]",
            "Lady Gaga - Judas [JD2022]",
            "Katy Perry - Last Friday Night (T.G.I.F.) [JD2022]",
            "Ciara - Level Up [JD2022]",
            "Dua Lipa - Levitating [JD2022]",
            "Taylor Swift - Love Story (Taylor's Version) [JD2022]",
            "24kGoldn ft. Iann Dior - Mood [JD2022]",
            "Electric Light Orchestra - Mr. Blue Sky [JD2022]",
            "Domino Saints - My Way [JD2022]",
            "Todrick Hall - Nails, Hair, Hips, Heels [JD2022]",
            "K/DA - POP/STARS [JD2022]",
            "Zara Larsson - Poster Girl [JD2022]",
            "Justin Timberlake - Rock Your Body [JD2022]",
            "Beyoncé - Run the World (Girls) [JD2022]",
            "The Weeknd & Ariana Grande - Save Your Tears (Remix) [JD2022]",
            "Bronski Beat - Smalltown Boy [JD2022]",
            "Ayo & Teo - Stop Drop Roll [JD2022]",
            "Major Lazer ft. Anitta & Pabllo Vittar - Sua Cara [JD2022]",
            "Daði Freyr - Think About Things [JD2022]",
            "Chilly Gonzales - You Can Dance [JD2022]",
            "Sylvester - You Make Me Feel (Mighty Real) [JD2022]",
        ]

    @functools.cached_property
    def songs_just_dance_2022_china_exclusive(self) -> List[str]:
        return [
            "阿里郎 - 作为你的兄弟 (As Your Brother) [JD2022 China Exclusive]",
            "音阙诗听/赵方婧 - 芒种 (Grain in Ear) [JD2022 China Exclusive]",
            "梦然 - 少年 (Teenager) [JD2022 China Exclusive]",
            "韩红 - 飞云之下 (Under Flying Clouds) [JD2022 China Exclusive]",
            "胡维纳 - 冰雪奇缘 (Let It Go Chinese Ver.) [JD2022 China Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2022_france_exclusive(self) -> List[str]:
        return [
            "Julien Granel & Lena Situations - À la Folie [JD2022 France Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2022_france_canada_exclusive(self) -> List[str]:
        return [
            "Julien Granel & Lena Situations - À la Folie [JD2022 France/Canada Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2022_japan_exclusive(self) -> List[str]:
        return [
            "Gen Hoshino - Koi [JD2022 Japan Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2022_benelux_exclusive(self) -> List[str]:
        return [
            "K3 - Waterval [JD2022 Benelux Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2022_germany_exclusive(self) -> List[str]:
        return [
            "Lisa Pac - Shoutout [JD2022 Germany Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2022_southeast_asia_exclusive(self) -> List[str]:
        return [
            "Jam Hsiao - Princess (王妃) [JD2022 Southeast Asia Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2022_just_dance_unlimited(self) -> List[str]:
        return [
            "Gen Hoshino - Koi [JD2022 JDU]",
            "Ciara - Level Up (VIPMADE) [JD2022 JDU]",
            "Lisa Pac - Shoutout [JD2022 JDU]",
            "Julien Granel & Lena Situations - À la Folie [JD2022 JDU]",
            "K3 - Waterval [JD2022 JDU]",
            "Jam Hsiao - Princess (王妃) [JD2022 JDU]",
            "Ariana Grande - Positions [JD2022 JDU]",
            "Lil Nas X - MONTERO (Call Me By Your Name) [JD2022 JDU]",
            "Doja Cat & SZA - Kiss Me More [JD2022 JDU]",
            "Madison Beer - Follow the White Rabbit [JD2022 JDU]",
            "Ed Sheeran - Bad Habits [JD2022 JDU]",
            "Ashnikko - Daisy [JD2022 JDU]",
            "Kim Petras - Malibu [JD2022 JDU]",
            "Dua Lipa - Break My Heart [JD2022 JDU]"
        ]

    @functools.cached_property
    def songs_just_dance_2022_just_dance_plus(self) -> List[str]:
        return [
            "Stromae - L'enfer [JD2022 JD+]",
            "Tones and I - Cloudy Day [JD2022 JD+]",
            "Jason Derulo - Acapulco [JD2022 JD+]",
            "Daddy Yankee - X Última Vez [JD2022 JD+]",
        ]

    @functools.cached_property
    def songs_just_dance_2023(self) -> List[str]:
        return [
            "CLiQ feat. Ms Banks and Alika - Anything I Do [JD2023]",
            "Harry Styles - As It Was [JD2023]",
            "BTS feat. Halsey - Boy With Luv [JD2023]",
            "Evanescence - Bring Me to Life [JD2023]",
            "Justin Timberlake - Can't Stop the Feeling! [JD2023]",
            "Electric Six - Danger! High Voltage [JD2023]",
            "The Trammps - Disco Inferno [JD2023]",
            "Olivia Rodrigo - Drivers License [JD2023]",
            "BTS - Dynamite [JD2023]",
            "Charli XCX - Good Ones [JD2023]",
            "Glass Animals - Heat Waves [JD2023]",
            "Taylor Swift - I Knew You Were Trouble (Taylor's Version) [JD2023]",
            "The Just Dancers - If You Wanna Party [JD2023]",
            "Bruno Mars - Locked Out of Heaven [JD2023]",
            "Zara Larsson - Love Me Land [JD2023]",
            "Kylie Minogue - Magic [JD2023]",
            "Apashe feat. Wasiu - Majesty [JD2023]",
            "Ava Max - Million Dollar Baby [JD2023]",
            "K/DA feat. Madison Beer, (G)-IDLE, Lexie Liu, Seraphine, Jaira Burns - More [JD2023]",
            "Linkin Park - Numb [JD2023]",
            "Dua Lipa - Physical [JD2023]",
            "Bea Miller - Playground [JD2023]",
            "Red Velvet - Psycho [JD2023]",
            "Imagine Dragons - Radioactive [JD2023]",
            "Clean Bandit feat. Jess Glynne - Rather Be [JD2023]",
            "RuPaul - Sissy That Walk [JD2023]",
            "The Kid Laroi and Justin Bieber - Stay [JD2023]",
            "Ava Max - Sweet but Psycho [JD2023]",
            "Lady Gaga feat. Beyoncé - Telephone [JD2023]",
            "Billie Eilish - Therefore I Am [JD2023]",
            "Shawn Mendes - Top of the World [JD2023]",
            "Britney Spears - Toxic (Just Dance 2) [JD2023]",
            "Britney Spears - Toxic [JD2023]",
            "Katrina and the Waves - Walking on Sunshine [JD2023]",
            "Itzy - Wannabe [JD2023]",
            "Major Lazer feat. Busy Signal, The Flexican and FS Green - Watch Out for This (Bumaye) [JD2023]",
            "Cast from Encanto - We Don't Talk About Bruno [JD2023]",
            "Apashe feat. Alina Pash - Witch [JD2023]",
            "Doja Cat - Woman [JD2023]",
            "The Beach Boys - Wouldn't It Be Nice [JD2023]",
            "Tigermonkey - Zooby Doo [JD2023]",
        ]

    @functools.cached_property
    def songs_just_dance_2023_france_exclusive(self) -> List[str]:
        return [
            "Michou - Jamais Lâcher [JD2023 France Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2023_italy_exclusive(self) -> List[str]:
        return [
            "Sangiovanni - Farfalle [JD2023 Italy Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2023_japan_exclusive(self) -> List[str]:
        return [
            "Naniwa Danshi - Ubu Love [JD2023 Japan Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2023_benelux_exclusive(self) -> List[str]:
        return [
            "K3 - Vleugels [JD2023 Benelux Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2023_just_dance_unlimited(self) -> List[str]:
        return [
            "Purple Disco Machine & Sophie and the Giants - In The Dark [JD2023 JDU]",
            "Harry Styles - Music For a Sushi Restaurant [JD2023 JDU]",
            "Nicki Minaj - Super Freaky Girl [JD2023 JDU]",
            "Maroon 5 - Moves Like Jagger [JD2023 JDU]",
            "Måneskin - Beggin' [JD2023 JDU]",
            "Olivia Rodrigo - good 4 u [JD2023 JDU]",
            "Dua Lipa - Physical [JD2023 JDU]",
            "The Kid LAROI & Justin Bieber - Stay [JD2023 JDU]",
            "Glass Animals - Heat Waves [JD2023 JDU]",
            "Billie Eilish - bad guy [JD2023 JDU]",
        ]

    @functools.cached_property
    def songs_just_dance_2023_just_dance_plus(self) -> List[str]:
        return [
            "Stray Kids - CIRCUS [JD2023 JD+]",
            "Ava Max - Maybe You're The Problem [JD2023 JD+]",
            "Natti Natasha x Ozuna - Las Nenas [JD2023 JD+]",
            "Camila Cabello - Bam Bam [JD2023 JD+]",
        ]

    @functools.cached_property
    def songs_just_dance_2024(self) -> List[str]:
        """Just Dance 2024 Edition songs."""
        return [
            "The Just Dance Orchestra - A Night in the Château de Versailles [JD2024]",
            "Gloria Groove - A QUEDA [JD2024]",
            "Banx & Ranx ft. Zach Zoya - After Party [JD2024]",
            "BTS - Butter [JD2024]",
            "Rema - Calm Down [JD2024]",
            "Zara Larsson - Can't Tame Her [JD2024]",
            "Jamiroquai - Canned Heat [JD2024]",
            "Wet Leg - Chaise Longue [JD2024]",
            "Sub Urban - Cradles [JD2024]",
            "AURORA - Cure For Me [JD2024]",
            "ROSALÍA - DESPECHÁ [JD2024]",
            "The Pussycat Dolls ft. Busta Rhymes - Don't Cha [JD2024]",
            "Miley Cyrus - Flowers [JD2024]",
            "Britney Spears - Gimme More [JD2024]",
            "BLACKPINK - How You Like That [JD2024]",
            "Fall Out Boy - I Am My Own Muse [JD2024]",
            "Whitney Houston - I Wanna Dance with Somebody (Who Loves Me) [JD2024]",
            "David Guetta & Bebe Rexha - I'm Good (Blue) [JD2024]",
            "Sam Smith - I'm Not Here to Make Friends [JD2024]",
            "Andy Williams - It's the Most Wonderful Time of the Year [JD2024]",
            "SZA - Kill Bill [JD2024]",
            "Jain - Makeba [JD2024]",
            "D Billions - My Name Is [JD2024]",
            "Flume ft. Kai - Never Be Like You [JD2024]",
            "Atarashii Gakko! - OTONABLUE [JD2024]",
            "The Sugarhill Gang (Groove Century) - Rapper's Delight [JD2024]",
            "AWOLNATION - Sail [JD2024]",
            "ATEEZ - Say My Name [JD2024]",
            "Jung Kook ft. Latto - Seven [JD2024]",
            "Electric Light Orchestra (The Sunlight Shakers) - Shine a Little Love [JD2024]",
            "Kelly Clarkson - Stronger (What Doesn't Kill You) [JD2024]",
            "Destiny's Child - Survivor [JD2024]",
            "Pyotr Ilyich Tchaikovsky (The Just Dance Orchestra) - Swan Lake [JD2024]",
            "Gloria Jones (The Just Dancers) - Tainted Love [JD2024]",
            "Ariana DeBose - This Wish [JD2024]",
            "Bad Bunny - Tití Me Preguntó [JD2024]",
            "Bruno Mars - Treasure [JD2024]",
            "Olivia Rodrigo - vampire [JD2024]",
            "Little Mix - Wasabi [JD2024]",
            "Rêve - Whitney [JD2024]",
            "Sofi Tukker ft. Kah-Lo - Woof [JD2024]",
            "Billie Eilish - you should see me in a crown [JD2024]"
        ]

    @functools.cached_property
    def songs_just_dance_2024_japan_exclusive(self) -> List[str]:
        """Just Dance 2024 Edition Japan exclusive songs."""
        return [
            "Atarashii Gakko! - OTONABLUE [Japan Exclusive]"
        ]

    @functools.cached_property
    def songs_just_dance_2024_just_dance_unlimited(self) -> List[str]:
        return [
            "Miley Cyrus - Flowers [JD2024 JDU]",
            "Taylor Swift - Anti-Hero [JD2024 JDU]",
            "Doja Cat - Woman [JD2024 JDU]",
            "Ed Sheeran - Shivers [JD2024 JDU]",
            "Lizzo - About Damn Time [JD2024 JDU]",
            "Bad Bunny - Tití Me Preguntó [JD2024 JDU]",
            "Nicki Minaj - Anaconda [JD2024 JDU]",
            "Olivia Rodrigo - vampire [JD2024 JDU]",
            "Sam Smith - Unholy [JD2024 JDU]",
            "Beyoncé - Crazy in Love [JD2024 JDU]",
        ]

    @functools.cached_property
    def songs_just_dance_2024_just_dance_plus(self) -> List[str]:
        return [
            "NewJeans - Get Up [JD2024 JD+]",
            "Måneskin - Supermodel [JD2024 JD+]",
            "Karol G - TQG [JD2024 JD+]",
            "David Guetta & Bebe Rexha - I'm Good (Blue) [JD2024 JD+]",
        ]

    @functools.cached_property
    def songs_just_dance_2026(self) -> List[str]:
        """Base tracklist for Just Dance 2026 Edition."""
        return [
            "Lady Gaga - Abracadabra [JD2026]",
            "Smash Mouth - All Star [JD2026]",
            "Doechii - Anxiety [JD2026]",
            "ROSÉ & Bruno Mars - APT. [JD2026]",
            "Ed Sheeran - Azizam [JD2026]",
            "Austin & Colin - Big Bad Frog [JD2026]",
            "Bluey - Bluey Medley [JD2026]",
            "Patrick Hernandez - Born to Be Alive (Reborn Version) [JD2026]",
            "MariaDennis ft. METAMAMI - Chichika [JD2026]",
            "OneRepublic - Counting Stars [JD2026]",
            "Melanie Martinez - Cry Baby [JD2026]",
            "Su Real & DISTORT - Don Raja [JD2026]",
            "Elton John & Kiki Dee - Don't Go Breaking My Heart [JD2026]",
            "BABYMONSTER - DRIP [JD2026]",
            "Sabrina Carpenter - Feather [JD2026]",
            "Cyndi Lauper - Girls Just Want to Have Fun [JD2026]",
            "Humphrey Dennis ft. Zanillya - Good Girls [JD2026]",
            "Chappell Roan - Good Luck, Babe! [JD2026]",
            "Dua Lipa - Houdini [JD2026]",
            "Madonna - Hung Up [JD2026]",
            "Post Malone ft. Morgan Wallen - I Had Some Help [JD2026]",
            "Tate McRae - It's ok I'm ok [JD2026]",
            "Dixson Waz, La Tukiti & Amenazandel - Kitipo [JD2026]",
            "Los Lobos - La Bamba [JD2026]",
            "Don Elektron & Derek - Louder [JD2026]",
            "Dua Lipa - Love Again [JD2026]",
            "Lola Young - Messy [JD2026]",
            "Aileen-O - Moonlight [JD2026]",
            "M / Robin Scott - Pop Muzik [JD2026]",
            "Ricky Stone - Prehistorock [JD2026]",
            "Brenda Lee - Rockin' Around the Christmas Tree [JD2026]",
            "Paul Russell - Say Cheese [JD2026]",
            "Boomborg - Show Me What You Got [JD2026]",
            "Wanko Ni Mero Mero - Sokusu [JD2026]",
            "Kevin J Simon - Spin Your Love [JD2026]",
            "Sigrid - Strangers [JD2026]",
            "Macklemore & Ryan Lewis ft. Wanz - Thrift Shop [JD2026]",
            "Coldplay - Viva la Vida [JD2026]",
            "Stush & WOST - We Just Begun [JD2026]",
            "Lady Gaga - Zombieboy [JD2026]"
        ]

    @functools.cached_property
    def songs_just_dance_2025(self) -> List[str]:
        """Base tracklist for Just Dance 2025 Edition."""
        return [
            "Galantis - BANG BANG! (My Neurodivergent Anthem) [JD2025]",
            "Green Day - Basket Case [JD2025]",
            "Ariana Grande - break up with your girlfriend, i'm bored [JD2025]",
            "Enur ft. Natasja - Calabria 2007 [JD2025]",
            "Alan Jackson - Chattahoochee [JD2025]",
            "Hyper - Control Response [JD2025]",
            "Christell - Dubidubidu (Chipi Chipi Chapa Chapa) [JD2025]",
            "Sabrina Carpenter - Espresso [JD2025]",
            "Tate McRae - exes [JD2025]",
            "The Just Dance Band - Halloween's Here [JD2025]",
            "The Rasmus - In the Shadows [JD2025]",
            "The Weeknd ft. Doja Cat - In Your Eyes (Remix) [JD2025]",
            "Jack Harlow - Lovin On Me [JD2025]",
            "Billie Eilish - LUNCH [JD2025]",
            "Gotopo & Don Elektron - Mi Gente lo Siente [JD2025]",
            "The Sunlight Shakers - Move Your Body [JD2025]",
            "Céline Dion - My Heart Will Go On [JD2025]",
            "Ariana Grande - One Last Time [JD2025]",
            "Kylie Minogue - Padam Padam [JD2025]",
            "Doja Cat - Paint The Town Red [JD2025]",
            "Miley Cyrus - Party in the U.S.A. [JD2025]",
            "Maroon 5 ft. Wiz Khalifa - Payphone [JD2025]",
            "BLACKPINK - Pink Venom [JD2025]",
            "Melanie Martinez - Play Date [JD2025]",
            "Lady Gaga - Poker Face [JD2025]",
            "Mrs. Claus and the Elves - Sleigh Ride [JD2025]",
            "Mandy Harvey - Something I Can Feel [JD2025]",
            "Groove Century - SpongeBob's Birthday [JD2025]",
            "Nius - Stop This Fire [JD2025]",
            "The Just Dance Band - Sunlight [JD2025]",
            "Little Mix - Sweet Melody [JD2025]",
            "Ariana Grande - the boy is mine [JD2025]",
            "The Tokens - The Lion Sleeps Tonight (Wimoweh) [JD2025]",
            "Dua Lipa - Training Season [JD2025]",
            "Sia - Unstoppable [JD2025]",
            "Madonna - Vogue [JD2025]",
            "Ariana Grande - we can't be friends (wait for your love) [JD2025]",
            "Shakira - Whenever, Wherever [JD2025]",
            "Usher ft. Lil Jon - Yeah! [JD2025]",
            "Ariana Grande - yes, and? [JD2025]",
            "Zara Larsson - You Love Who You Love [JD2025]"
        ]

    @functools.cached_property
    def songs_just_dance_2026_just_dance_unlimited(self) -> List[str]:
        """Just Dance Unlimited exclusive songs for JD2026 Edition."""
        return []  # No confirmed Unlimited songs at launch

    @functools.cached_property
    def songs_just_dance_2025_just_dance_unlimited(self) -> List[str]:
        return [
            "Olivia Rodrigo - bad idea right? [JD2025 JDU]",
            "Tyla - Water [JD2025 JDU]",
            "Jungkook - Standing Next to You [JD2025 JDU]",
            "Camila Cabello - I LUV IT [JD2025 JDU]",
            "Charli xcx - 360 [JD2025 JDU]",
            "Chappell Roan - Good Luck, Babe! [JD2025 JDU]",
            "Benson Boone - Beautiful Things [JD2025 JDU]",
            "Taylor Swift - Fortnight [JD2025 JDU]",
            "Shaboozey - A Bar Song (Tipsy) [JD2025 JDU]",
            "Teddy Swims - Lose Control [JD2025 JDU]",
        ]

    @functools.cached_property
    def songs_just_dance_2025_just_dance_plus(self) -> List[str]:
        return [
            "ITZY - CAKE [JD2025 JD+]",
            "Laufey - From The Dining Table [JD2025 JD+]",
            "Bad Bunny & Feid - PERRO NEGRO [JD2025 JD+]",
            "Anitta - Funk Rave [JD2025 JD+]",
        ]

    @functools.cached_property
    def songs_just_dance_2026_just_dance_plus(self) -> List[str]:
        """Just Dance+ exclusive songs for JD2026 Edition (scheduled early 2026)."""
        return [
            "Blaiz Fayah, Maureen & DJ Glad - Money Pull Up [JD2026 JD+]",
        ]

    # Main songs method that aggregates all available songs
    def songs(self) -> List[str]:
        song_collection: List[str] = []

        if self.has_just_dance_1:
            song_collection.extend(self.songs_just_dance_1)
        if self.has_just_dance_2:
            song_collection.extend(self.songs_just_dance_2)
        if self.has_just_dance_3:
            song_collection.extend(self.songs_just_dance_3)
        if self.has_just_dance_4:
            song_collection.extend(self.songs_just_dance_4)
        if self.has_just_dance_2014:
            song_collection.extend(self.songs_just_dance_2014)
        if self.has_just_dance_2015:
            song_collection.extend(self.songs_just_dance_2015)
        if self.has_just_dance_2016:
            song_collection.extend(self.songs_just_dance_2016)
        if self.has_just_dance_2017:
            song_collection.extend(self.songs_just_dance_2017)
        if self.has_just_dance_2018:
            song_collection.extend(self.songs_just_dance_2018)
        if self.has_just_dance_2019:
            song_collection.extend(self.songs_just_dance_2019)
        if self.has_just_dance_2020:
            song_collection.extend(self.songs_just_dance_2020)
        if self.has_just_dance_2021:
            song_collection.extend(self.songs_just_dance_2021)
        if self.has_just_dance_2022:
            song_collection.extend(self.songs_just_dance_2022)
        if self.has_just_dance_2023:
            song_collection.extend(self.songs_just_dance_2023)
        if self.has_just_dance_2024:
            song_collection.extend(self.songs_just_dance_2024)
        if self.has_just_dance_2025:
            song_collection.extend(self.songs_just_dance_2025)
        if self.has_just_dance_2026:
            song_collection.extend(self.songs_just_dance_2026)

        # Add Unlimited songs if owned
        if self.include_unlimited_songs:
            song_collection.extend(self.songs_unlimited)

        # Add DLC content
        for dlc in self.dlc_content:
            if dlc == "JD2 - DLC Pack 1 (Launch)":
                song_collection.extend(self.songs_jd2_dlc_pack_1_launch)
            elif dlc == "JD2 - DLC Pack 2 (October 2010)":
                song_collection.extend(self.songs_jd2_dlc_pack_2_october_2010)
            elif dlc == "JD2 - DLC Pack 3 (November 2010)":
                song_collection.extend(self.songs_jd2_dlc_pack_3_november_2010)
            elif dlc == "JD2 - DLC Pack 4 (December 2010)":
                song_collection.extend(self.songs_jd2_dlc_pack_4_december_2010)
            elif dlc == "JD2 - DLC Pack 5 (January 2011)":
                song_collection.extend(self.songs_jd2_dlc_pack_5_january_2011)
            elif dlc == "JD2 - DLC Pack 6 (February 2011)":
                song_collection.extend(self.songs_jd2_dlc_pack_6_february_2011)
            elif dlc == "JD2 - DLC Pack 7 (March 2011)":
                song_collection.extend(self.songs_jd2_dlc_pack_7_march_2011)
            elif dlc == "JD2 - DLC Pack 8 (April-June 2011)":
                song_collection.extend(self.songs_jd2_dlc_pack_8_april_june_2011)
            elif dlc == "JD3 - Sweat Pack #1":
                song_collection.extend(self.songs_jd3_sweat_pack_1)
            elif dlc == "JD3 - Sweat Pack #2":
                song_collection.extend(self.songs_jd3_sweat_pack_2)
            elif dlc == "JD3 - Valentine Pack":
                song_collection.extend(self.songs_jd3_valentine_pack)
            elif dlc == "JD3 - Christmas Pack":
                song_collection.extend(self.songs_jd3_christmas_pack)
            elif dlc == "JD3 - Spring Break Pack #1":
                song_collection.extend(self.songs_jd3_spring_break_pack_1)
            elif dlc == "JD3 - Spring Break Pack #2":
                song_collection.extend(self.songs_jd3_spring_break_pack_2)
            elif dlc == "JD3 - Individual DLC Songs":
                song_collection.extend(self.songs_jd3_individual_dlc)
            elif dlc == "JD4 - DLC Pack 1 (October 2012)":
                song_collection.extend(self.songs_jd4_dlc_pack_1_october_2012)
            elif dlc == "JD4 - DLC Pack 2 (November 2012)":
                song_collection.extend(self.songs_jd4_dlc_pack_2_november_2012)
            elif dlc == "JD4 - DLC Pack 3 (December 2012)":
                song_collection.extend(self.songs_jd4_dlc_pack_3_december_2012)
            elif dlc == "JD4 - DLC Pack 4 (January 2013)":
                song_collection.extend(self.songs_jd4_dlc_pack_4_january_2013)
            elif dlc == "JD4 - DLC Pack 5 (March 2013)":
                song_collection.extend(self.songs_jd4_dlc_pack_5_march_2013)
            elif dlc == "JD4 - DLC Pack 6 (April 2013)":
                song_collection.extend(self.songs_jd4_dlc_pack_6_april_2013)
            elif dlc == "JD2014 - Launch DLC":
                song_collection.extend(self.songs_jd2014_dlc_launch)
            elif dlc == "JD2014 - November 2013 DLC":
                song_collection.extend(self.songs_jd2014_dlc_november_2013)
            elif dlc == "JD2014 - December 2013 DLC":
                song_collection.extend(self.songs_jd2014_dlc_december_2013)
            elif dlc == "JD2014 - February 2014 DLC":
                song_collection.extend(self.songs_jd2014_dlc_february_2014)
            elif dlc == "JD2014 - March 2014 DLC":
                song_collection.extend(self.songs_jd2014_dlc_march_2014)
            elif dlc == "JD2014 - April 2014 DLC":
                song_collection.extend(self.songs_jd2014_dlc_april_2014)
            elif dlc == "JD2014 - May 2014 DLC":
                song_collection.extend(self.songs_jd2014_dlc_may_2014)
            elif dlc == "JD2015 - Day One DLC":
                song_collection.extend(self.songs_jd2015_dlc_day_one)
            elif dlc == "JD2015 - November 2014 DLC":
                song_collection.extend(self.songs_jd2015_dlc_november_2014)
            elif dlc == "JD2015 - January 2015 DLC":
                song_collection.extend(self.songs_jd2015_dlc_january_2015)
            elif dlc == "JD2016 - Just Dance Unlimited":
                song_collection.extend(self.songs_just_dance_2016_just_dance_unlimited)
            elif dlc == "JD2017 - Just Dance Unlimited":
                song_collection.extend(self.songs_just_dance_2017_just_dance_unlimited)
            elif dlc == "JD2018 - Just Dance Unlimited":
                song_collection.extend(self.songs_just_dance_2018_just_dance_unlimited)
            elif dlc == "JD2019 - Just Dance Unlimited":
                song_collection.extend(self.songs_just_dance_2019_just_dance_unlimited)
            elif dlc == "JD2020 - Just Dance Unlimited":
                song_collection.extend(self.songs_just_dance_2020_just_dance_unlimited)
            elif dlc == "JD2021 - Just Dance Unlimited":
                song_collection.extend(self.songs_just_dance_2021_just_dance_unlimited)
            elif dlc == "JD2022 - Just Dance Unlimited":
                song_collection.extend(self.songs_just_dance_2022_just_dance_unlimited)
            elif dlc == "JD2023 - Just Dance Unlimited":
                song_collection.extend(self.songs_just_dance_2023_just_dance_unlimited)
            elif dlc == "JD2024 - Just Dance Unlimited":
                song_collection.extend(self.songs_just_dance_2024_just_dance_unlimited)
            elif dlc == "JD2025 - Just Dance Unlimited":
                song_collection.extend(self.songs_just_dance_2025_just_dance_unlimited)

        # Add Just Dance+ content
        for plus_content in self.just_dance_plus_content:
            if plus_content == "JD2022 - Just Dance+":
                song_collection.extend(self.songs_just_dance_2022_just_dance_plus)
            elif plus_content == "JD2023 - Just Dance+":
                song_collection.extend(self.songs_just_dance_2023_just_dance_plus)
            elif plus_content == "JD2024 - Just Dance+":
                song_collection.extend(self.songs_just_dance_2024_just_dance_plus)
            elif plus_content == "JD2025 - Just Dance+":
                song_collection.extend(self.songs_just_dance_2025_just_dance_plus)
            elif plus_content == "JD2026 - Just Dance+":
                song_collection.extend(self.songs_just_dance_2026_just_dance_plus)

        # Add exclusive content
        for exclusive in self.exclusive_content:
            if exclusive == "JD1 - PAL Exclusive":
                song_collection.extend(self.songs_jd1_pal_exclusive)
            elif exclusive == "JD2 - Best Buy/Walmart Exclusive":
                song_collection.extend(self.songs_jd2_best_buy_walmart_exclusive)
            elif exclusive == "JD3 - Target/Zellers Exclusive":
                song_collection.extend(self.songs_jd3_target_zellers_exclusive)
            elif exclusive == "JD3 - Best Buy Exclusive":
                song_collection.extend(self.songs_jd3_best_buy_exclusive)
            elif exclusive == "JD3 - PAL Exclusive":
                song_collection.extend(self.songs_jd3_pal_exclusive)
            elif exclusive == "JD3 - PS3 Exclusive":
                song_collection.extend(self.songs_jd3_ps3_exclusive)
            elif exclusive == "JD4 - Target Exclusive":
                song_collection.extend(self.songs_jd4_target_exclusive)
            elif exclusive == "JD4 - Best Buy Exclusive":
                song_collection.extend(self.songs_jd4_best_buy_exclusive)
            elif exclusive == "JD4 - PAL Exclusive":
                song_collection.extend(self.songs_jd4_pal_exclusive)
            elif exclusive == "JD4 - Wii U Exclusive":
                song_collection.extend(self.songs_jd4_wii_u_exclusive)
            elif exclusive == "JD4 - NTSC Exclusive":
                song_collection.extend(self.songs_jd4_ntsc_exclusive)
            elif exclusive == "JD4 - Excluded from NTSC Wii":
                song_collection.extend(self.songs_jd4_excluded_from_ntsc_wii)
            elif exclusive == "JD4 - Cheetos Promo":
                song_collection.extend(self.songs_jd4_cheetos_promo)
            elif exclusive == "JD2014 - NTSC Exclusive":
                song_collection.extend(self.songs_jd2014_ntsc_exclusive)
            elif exclusive == "JD2014 - PAL Exclusive":
                song_collection.extend(self.songs_jd2014_pal_exclusive)
            elif exclusive == "JD2014 - Popchips Promo":
                song_collection.extend(self.songs_jd2014_popchips_promo)
            elif exclusive == "JD2015 - NTSC Exclusive":
                song_collection.extend(self.songs_jd2015_ntsc_exclusive)
            elif exclusive == "JD2015 - PAL Exclusive":
                song_collection.extend(self.songs_jd2015_pal_exclusive)
            elif exclusive == "JD2015 - Ubisoft Connect Unlockables":
                song_collection.extend(self.songs_just_dance_2015_exclusives)
            elif exclusive in ["JD2016 - Ubisoft Connect Unlockables", "JD2016 - Russia Exclusive"]:
                song_collection.extend(self.songs_just_dance_2016_exclusives)
            elif exclusive in ["JD2017 - Ubisoft Connect Unlockables", "JD2017 - Russia Exclusive"]:
                song_collection.extend(self.songs_just_dance_2017_exclusives)
            elif exclusive == "JD2017 - Switch Exclusive":
                song_collection.extend(self.songs_just_dance_2017_platform_exclusives)
            elif exclusive in ["JD2018 - Ubisoft Connect Unlockables", "JD2018 - Russia Exclusive"]:
                song_collection.extend(self.songs_just_dance_2018_exclusives)
            elif exclusive == "JD2018 - Switch Exclusive":
                song_collection.extend(self.songs_just_dance_2018_platform_exclusives)
            elif exclusive == "JD2019 - Code Unlock":
                song_collection.extend(self.songs_just_dance_2019_code_unlock)
            elif exclusive == "JD2019 - Middle East Exclusive":
                song_collection.extend(self.songs_just_dance_2019_middle_east_exclusive)
            elif exclusive == "JD2019 - France/Canada Exclusive":
                song_collection.extend(self.songs_just_dance_2019_france_canada_exclusive)
            elif exclusive == "JD2019 - Russia Exclusive":
                song_collection.extend(self.songs_just_dance_2019_russia_exclusive)
            elif exclusive == "JD2020 - Japan Exclusive":
                song_collection.extend(self.songs_just_dance_2020_japan_exclusive)
            elif exclusive == "JD2020 - France Exclusive":
                song_collection.extend(self.songs_just_dance_2020_france_exclusive)
            elif exclusive == "JD2020 - Benelux Exclusive":
                song_collection.extend(self.songs_just_dance_2020_benelux_exclusive)
            elif exclusive == "JD2020 - Russia Exclusive":
                song_collection.extend(self.songs_just_dance_2020_russia_exclusive)
            elif exclusive == "JD2021 - Japan Exclusive":
                song_collection.extend(self.songs_just_dance_2021_japan_exclusive)
            elif exclusive == "JD2021 - France Exclusive":
                song_collection.extend(self.songs_just_dance_2021_france_exclusive)
            elif exclusive == "JD2021 - Benelux Exclusive":
                song_collection.extend(self.songs_just_dance_2021_benelux_exclusive)
            elif exclusive == "JD2022 - China Exclusive":
                song_collection.extend(self.songs_just_dance_2022_china_exclusive)
            elif exclusive == "JD2022 - France Exclusive":
                song_collection.extend(self.songs_just_dance_2022_france_exclusive)
            elif exclusive == "JD2022 - France/Canada Exclusive":
                song_collection.extend(self.songs_just_dance_2022_france_canada_exclusive)
            elif exclusive == "JD2022 - Japan Exclusive":
                song_collection.extend(self.songs_just_dance_2022_japan_exclusive)
            elif exclusive == "JD2022 - Benelux Exclusive":
                song_collection.extend(self.songs_just_dance_2022_benelux_exclusive)
            elif exclusive == "JD2022 - Germany Exclusive":
                song_collection.extend(self.songs_just_dance_2022_germany_exclusive)
            elif exclusive == "JD2022 - Southeast Asia Exclusive":
                song_collection.extend(self.songs_just_dance_2022_southeast_asia_exclusive)
            elif exclusive == "JD2023 - France Exclusive":
                song_collection.extend(self.songs_just_dance_2023_france_exclusive)
            elif exclusive == "JD2023 - Italy Exclusive":
                song_collection.extend(self.songs_just_dance_2023_italy_exclusive)
            elif exclusive == "JD2023 - Japan Exclusive":
                song_collection.extend(self.songs_just_dance_2023_japan_exclusive)
            elif exclusive == "JD2023 - Benelux Exclusive":
                song_collection.extend(self.songs_just_dance_2023_benelux_exclusive)
            elif exclusive == "JD2024 - Japan Exclusive":
                song_collection.extend(self.songs_just_dance_2024_japan_exclusive)

        return sorted(list(set(song_collection)))  # Remove duplicates and sort

    # Unlimited songs (available via subscription)
    @functools.cached_property
    def songs_unlimited(self) -> List[str]:
        return [
            "Cheap Thrills - Sia [JD Unlimited]",
            "Work from Home - Fifth Harmony feat. Ty Dolla $ign [JD Unlimited]",
            "Can't Stop the Feeling! - Justin Timberlake [JD Unlimited]",
            "Sorry - Justin Bieber [JD Unlimited]",
            "Cake by the Ocean - DNCE [JD Unlimited]",
            "Don't Let Me Down - The Chainsmokers feat. Daya",
            "Stressed Out - Twenty One Pilots",
            "Ride - Twenty One Pilots",
            "Heathens - Twenty One Pilots",
            "Closer - The Chainsmokers feat. Halsey",
            "Let Me Love You - DJ Snake feat. Justin Bieber",
            "Cold Water - Major Lazer feat. Justin Bieber & MØ",
            "Treat You Better - Shawn Mendes",
            "We Don't Talk Anymore - Charlie Puth feat. Selena Gomez",
            "24K Magic - Bruno Mars",
            "Starboy - The Weeknd feat. Daft Punk",
            "Black Beatles - Rae Sremmurd feat. Gucci Mane",
            "Side to Side - Ariana Grande feat. Nicki Minaj",
            "Into You - Ariana Grande",
            "Dangerous Woman - Ariana Grande",
            "This Is What You Came For - Calvin Harris feat. Rihanna",
            "One Dance - Drake feat. WizKid & Kyla",
            "Work - Rihanna feat. Drake",
            "Formation - Beyoncé",
            "Sorry - Beyoncé",
            "Lemonade - Beyoncé",
            "Freedom - Beyoncé feat. Kendrick Lamar",
            "Hold Up - Beyoncé",
            "6 Inch - Beyoncé feat. The Weeknd",
            "Daddy Lessons - Beyoncé",
            "Love Drought - Beyoncé",
            "Sandcastles - Beyoncé",
            "Forward - Beyoncé feat. James Blake",
            "All Night - Beyoncé",
            "Formation - Beyoncé",
            "Crazy in Love - Beyoncé feat. Jay-Z",
            "Single Ladies (Put a Ring on It) - Beyoncé",
            "Halo - Beyoncé",
            "If I Were a Boy - Beyoncé",
            "Love on Top - Beyoncé",
            "Drunk in Love - Beyoncé feat. Jay-Z",
            "Partition - Beyoncé",
            "XO - Beyoncé",
            "Flawless - Beyoncé feat. Nicki Minaj",
            "7/11 - Beyoncé",
            "Pretty Hurts - Beyoncé",
            "Blow - Beyoncé",
            "Haunted - Beyoncé",
        ]

    # DLC song collections
    @functools.cached_property
    def songs_jd2_dlc_pack_1_launch(self) -> List[str]:
        return [
            "Katy Perry - Firework [JD2 DLC - Pack 1]",
            "Rihanna - Pon de Replay [JD2 DLC - Pack 1]",
            "Countdown Dee's Hit Explosion - Barbie Girl (Aqua) [JD2 DLC - Pack 1]",
            "M/A/R/R/S - Pump Up the Volume [JD2 DLC - Pack 1]",
        ]

    @functools.cached_property
    def songs_jd2_dlc_pack_2_october_2010(self) -> List[str]:
        return [
            "Studio Allstars - Maniac (Michael Sembello) [JD2 DLC - Pack 2]",
            "Steppenwolf - Born To Be Wild [JD2 DLC - Pack 2]",
            "Nick Phoenix and Thomas J. Bergersen - Professor Pumplestickle [JD2 DLC - Pack 2]",
            "V V Brown - Crying Blood [JD2 DLC - Pack 2]",
        ]

    @functools.cached_property
    def songs_jd2_dlc_pack_3_november_2010(self) -> List[str]:
        return [
            "The Reverend Horatio Duncan and Amos Sweets - Down By The Riverside",
            "The World Cup Girls - Futebol Crazy (Paul J. Borg)",
        ]

    @functools.cached_property
    def songs_jd2_dlc_pack_4_december_2010(self) -> List[str]:
        return [
            "Carl Douglas - Kung Fu Fighting (Dave Ruffy/Mark Wallis Remix)",
            "Lou Bega - Mambo No. 5 (A Little Bit of Monika)",
            "Panic! At The Disco - Nine in the Afternoon",
            "Tom Jones - It's Not Unusual",
            "A Band of Bees - Chicken Payback",
            "Santa Clones - Crazy Christmas",
        ]

    @functools.cached_property
    def songs_jd2_dlc_pack_5_january_2011(self) -> List[str]:
        return [
            "Sweat Invaders - Skin-To-Skin",
        ]

    @functools.cached_property
    def songs_jd2_dlc_pack_6_february_2011(self) -> List[str]:
        return [
            "The Supremes - You Can't Hurry Love",
            "Love Letter - Why Oh Why",
            "Estelle feat. Kanye West - American Boy",
        ]

    @functools.cached_property
    def songs_jd2_dlc_pack_7_march_2011(self) -> List[str]:
        return [
            "Dexy's Midnight Runners - Come On Eileen",
            "Blur - Song 2",
            "Spice Girls - Spice Up Your Life",
            "The Hit Crew - Here Comes the Hotstepper (Ini Kamoze)",
        ]

    @functools.cached_property
    def songs_jd2_dlc_pack_8_april_june_2011(self) -> List[str]:
        return [
            "M People - Moving on Up",
        ]

    @functools.cached_property
    def songs_jd3_sweat_pack_1(self) -> List[str]:
        return [
            "Alan Hawkshaw and Andrew Kingslow - Beat Match Until I'm Blue (Sweat Invaders) [JD3 DLC - Sweat Pack #1]",
            "Sweat Invaders - Dun N' Dusted [JD3 DLC - Sweat Pack #1]",
            "Sweat Invaders - Touch Me Want Me [JD3 DLC - Sweat Pack #1]",
        ]

    @functools.cached_property
    def songs_jd3_sweat_pack_2(self) -> List[str]:
        return [
            "Sweat Invaders - Cardiac Caress",
            "Sweat Invaders - Boomsday",
            "Sweat Invaders - Merengue",
        ]

    @functools.cached_property
    def songs_jd3_valentine_pack(self) -> List[str]:
        return [
            "Bollywood - Katti Kalandal",
            "Sweat Invaders - Skin-To-Skin",
            "Love Letter - Why Oh Why",
        ]

    @functools.cached_property
    def songs_jd3_christmas_pack(self) -> List[str]:
        return [
            "The Bangles - Walk Like an Egyptian",
            "Mardi Gras - Iko Iko",
            "Reggaeton - Baby Girl",
            "Dee Dee Sharp - Mashed Potato Time",
        ]

    @functools.cached_property
    def songs_jd3_spring_break_pack_1(self) -> List[str]:
        return [
            "Kim Wilde - Kids in America",
            "The Reverend Horatio Duncan and Amos Sweets - Down By The Riverside",
            "Nick Phoenix and Thomas J. Bergersen - Professor Pumplestickle",
            "Gorillaz - Dare",
        ]

    @functools.cached_property
    def songs_jd3_spring_break_pack_2(self) -> List[str]:
        return [
            "The World Cup Girls - Futebol Crazy (Paul J. Borg)",
            "Supergrass - Alright",
            "Sorcerer - Dagomba",
        ]

    @functools.cached_property
    def songs_jd3_individual_dlc(self) -> List[str]:
        return [
            "In the Style of Irene Cara - Fame (Irene Cara)",
            "Blondie - Heart of Glass",
            "Groove Century - U Can't Touch This (MC Hammer)",
            "Anja - Baby Don't Stop Now",
            "Olé Orquesta - Jambo Mambo",
            "Groove Century - Soul Searchin'",
            "The Girly Team - Twist and Shake It (Ben Wheeler and Tara Chinn)",
            "Fatboy Slim - Jin Go Lo Ba",
            "Jamiroquai - Cosmic Girl",
            "The Sunlight Shakers - Jump in the Line (Harry Belafonte)",
            "Benny Benassi presents \"The Biz\" - Satisfaction (Isak Original Extended)",
            "Calvin Harris - Acceptable in the 80s",
            "Studio Allstars - Jump (Kris Kross)",
            "Ike & Tina Turner - Proud Mary",
            "The Hit Crew - Toxic (Britney Spears)",
            "Ubisoft Meets Nintendo - Just Mario",
            "The B-52's - Funplex (CSS Remix)",
            "Iggy Pop - Louie Louie",
            "New Kids on The Block - Step by Step",
            "Santa Clones - Crazy Christmas",
            "Groove Century - I Like to Move It (Radio Mix) (Reel 2 Real feat. The Mad Stuntman)",
            "The Sunlight Shakers - Who Let the Dogs Out? (Baha Men)",
            "Snap! - The Power",
            "KC and the Sunshine Band - That's the Way (I Like It)",
            "Charleston - Mugsy Baloney",
            "Boney M. - Rasputin",
            "The Weather Girls - It's Raining Men",
        ]

    @functools.cached_property
    def songs_jd4_dlc_pack_1_october_2012(self) -> List[str]:
        return [
            "Katy Perry - Part Of Me [JD4 DLC - Pack 1]",
            "Cobra Starship ft. Sabi - You Make Me Feel... [JD4 DLC - Pack 1]",
        ]

    @functools.cached_property
    def songs_jd4_dlc_pack_2_november_2012(self) -> List[str]:
        return [
            "PSY - Gangnam Style",
            "P!nk - Funhouse",
            "Bunny Beatz ft. Liquid - Make The Party (Don't Stop)",
            "Sorcerer - Dagomba",
        ]

    @functools.cached_property
    def songs_jd4_dlc_pack_3_december_2012(self) -> List[str]:
        return [
            "One Direction - One Thing",
            "Gossip - Heavy Cross",
            "The Girly Team - So Glamorous",
            "Selena Gomez and the Scene - Hit The Lights",
            "Carrie Underwood - Good Girl",
            "Cher Lloyd ft. Astro - Want U Back",
        ]

    @functools.cached_property
    def songs_jd4_dlc_pack_4_january_2013(self) -> List[str]:
        return [
            "Cher Lloyd ft. Becky G - Oath",
            "Ke$ha - We R Who We R",
            "Reggaeton Storm - Boom",
        ]

    @functools.cached_property
    def songs_jd4_dlc_pack_5_march_2013(self) -> List[str]:
        return [
            "Nick Phoenix and Thomas J. Bergersen - Professor Pumplestickle",
            "Bruno Mars - The Lazy Song",
            "DJ Fresh - Gold Dust",
        ]

    @functools.cached_property
    def songs_jd4_dlc_pack_6_april_2013(self) -> List[str]:
        return [
            "Ke$ha - Die Young",
            "Marina and the Diamonds - Primadonna",
            "Reggaeton - Baby Girl",
        ]

    # Just Dance 2014 DLC Collections
    @functools.cached_property
    def songs_jd2014_dlc_launch(self) -> List[str]:
        return [
            "Katy Perry - Roar [JD2014 DLC - Launch]",
            "Macklemore & Ryan Lewis feat. Ray Dalton - Can't Hold Us [JD2014 DLC - Launch]",
            "Avicii feat. Aloe Blacc - Wake Me Up [JD2014 DLC - Launch]",
        ]

    @functools.cached_property
    def songs_jd2014_dlc_november_2013(self) -> List[str]:
        return [
            "Miley Cyrus - We Can't Stop [JD2014 DLC - November 2013]",
            "Austin Mahone - What About Love [JD2014 DLC - November 2013]",
            "One Direction - One Way Or Another (Teenage Kicks) [JD2014 DLC - November 2013]",
            "LMFAO - Sexy And I Know It [JD2014 DLC - November 2013]",
            "Bonnie McKee - American Girl [JD2014 DLC - November 2013]",
        ]

    @functools.cached_property
    def songs_jd2014_dlc_december_2013(self) -> List[str]:
        return [
            "Mainstreet - My Main Girl [JD2014 DLC - December 2013]",
            "Calvin Harris feat. Ellie Goulding - I Need Your Love [JD2014 DLC - December 2013]",
            "Becky G feat. Pitbull - Can't Get Enough [JD2014 DLC - December 2013]",
            "Swedish House Mafia feat. John Martin - Don't You Worry Child [JD2014 DLC - December 2013]",
            "PSY - Gangnam Style [JD2014 DLC - December 2013]",
        ]

    @functools.cached_property
    def songs_jd2014_dlc_february_2014(self) -> List[str]:
        return [
            "Pitbull feat. Ke$ha - Timber [JD2014 DLC - February 2014]",
            "Avril Lavigne - Rock n Roll [JD2014 DLC - February 2014]",
        ]

    @functools.cached_property
    def songs_jd2014_dlc_march_2014(self) -> List[str]:
        return [
            "P!nk - Funhouse [JD2014 DLC - March 2014]",
            "Katy Perry - Part of Me [JD2014 DLC - March 2014]",
        ]

    @functools.cached_property
    def songs_jd2014_dlc_april_2014(self) -> List[str]:
        return [
            "Justin Bieber feat. Nicki Minaj - Beauty And A Beat [JD2014 DLC - April 2014]",
            "Maroon 5 feat. Christina Aguilera - Moves Like Jagger [JD2014 DLC - April 2014]",
            "One Direction - One Thing [JD2014 DLC - April 2014]",
            "Ke$ha - We R Who We R [JD2014 DLC - April 2014]",
        ]

    @functools.cached_property
    def songs_jd2014_dlc_may_2014(self) -> List[str]:
        return [
            "David Correy feat. Monobloco - The World is Ours [JD2014 DLC - May 2014]",
        ]

    # Just Dance 2015 DLC Collections
    @functools.cached_property
    def songs_jd2015_dlc_day_one(self) -> List[str]:
        return [
            "Ariana Grande feat. Zedd - Break Free [JD2015 DLC - Day One]",  # Free
            "Jennifer Lopez feat. French Montana - I Luh Ya Papi [JD2015 DLC - Day One]",
            # Plus various recycled tracks from previous games
            "One Direction - One Way Or Another (Teenage Kicks) [JD2015 DLC - Day One]",
            "Swedish House Mafia feat. John Martin - Don't You Worry Child [JD2015 DLC - Day One]",
            "Avicii feat. Aloe Blacc - Wake Me Up [JD2015 DLC - Day One]",
            "LMFAO - Sexy And I Know It [JD2015 DLC - Day One]",
            "PSY - Gangnam Style [JD2015 DLC - Day One]",
            "Ke$ha - Die Young [JD2015 DLC - Day One]",
            "Katy Perry - Roar [JD2015 DLC - Day One]",
            "Lady Gaga feat. Colby O'Donis - Just Dance [JD2015 DLC - Day One]",
            "Calvin Harris feat. Ellie Goulding - I Need Your Love [JD2015 DLC - Day One]",
            "Maroon 5 feat. Christina Aguilera - Moves Like Jagger [JD2015 DLC - Day One]",
            "Justin Bieber feat. Nicki Minaj - Beauty And A Beat [JD2015 DLC - Day One]",
        ]

    @functools.cached_property
    def songs_jd2015_dlc_november_2014(self) -> List[str]:
        return [
            "Miley Cyrus - We Can't Stop [JD2015 DLC - November 2014]",
            "Cher Lloyd feat. Astro - Want U Back [JD2015 DLC - November 2014]",
            "Ke$ha - C'Mon [JD2015 DLC - November 2014]",
            "One Direction - Kiss You [JD2015 DLC - November 2014]",
            "P!nk - Funhouse [JD2015 DLC - November 2014]",
        ]

    @functools.cached_property
    def songs_jd2015_dlc_january_2015(self) -> List[str]:
        return [
            "Charli XCX - Boom Clap [JD2015 DLC - January 2015]",
            "Prince Royce - Kiss Kiss [JD2015 DLC - January 2015]",
            "Disney's Frozen - Let It Go (Sing Along) (Idina Menzel) [JD2015 DLC - January 2015]",
            "From The Movie Happy New Year - India Waale [JD2015 DLC - January 2015]",
            "Avril Lavigne - Rock n Roll [JD2015 DLC - January 2015]",
        ]

    # Exclusive content collections
    @functools.cached_property
    def songs_jd1_pal_exclusive(self) -> List[str]:
        return [
            # PAL region had some different songs, but JD1 was fairly consistent
            # Most exclusives were in later games
        ]

    @functools.cached_property
    def songs_jd2_best_buy_walmart_exclusive(self) -> List[str]:
        return [
            "The Clash - Should I Stay or Should I Go [JD2 - Best Buy/Walmart Exclusive]",
            "Sweat Invaders - Funkytown (Lipps Inc.) [JD2 - Best Buy/Walmart Exclusive]",
            "A. R. Rahman and The Pussycat Dolls ft. Nicole Scherzinger - Jai Ho! (You Are My Destiny) [JD2 - Best Buy/Walmart Exclusive]",
        ]

    @functools.cached_property
    def songs_jd3_target_zellers_exclusive(self) -> List[str]:
        return [
            "Rihanna - Only Girl (In The World) [JD3 - Target/Zellers Exclusive]",
            "B.o.B. ft. Hayley Williams of Paramore - Airplanes [JD3 - Target/Zellers Exclusive]",
        ]

    @functools.cached_property
    def songs_jd3_best_buy_exclusive(self) -> List[str]:
        return [
            "Katy Perry - Teenage Dream [JD3 - Best Buy Exclusive]",
            "Katy Perry - E.T. [JD3 - Best Buy Exclusive]",
        ]

    @functools.cached_property
    def songs_jd3_pal_exclusive(self) -> List[str]:
        return [
            "Les Rita Mitsouko - Marcia Baila [JD3 - PAL Exclusive]",
            "Lena Meyer-Landrut - Satellite [JD3 - PAL Exclusive]",
        ]

    @functools.cached_property
    def songs_jd3_ps3_exclusive(self) -> List[str]:
        return [
            "Ole Orquesta - Jambo Mambo [JD3 - PS3 Exclusive]",
            "Anja - Baby Don't Stop Now [JD3 - PS3 Exclusive]",
            "The Girly Team - Twist and Shake It (Ben Wheeler and Tara Chinn) [JD3 - PS3 Exclusive]",
            "Groove Century - Soul Searchin' [JD3 - PS3 Exclusive]",
        ]

    @functools.cached_property
    def songs_jd4_target_exclusive(self) -> List[str]:
        return [
            "Cobra Starship ft. Sabi - You Make Me Feel...",
        ]

    @functools.cached_property
    def songs_jd4_best_buy_exclusive(self) -> List[str]:
        return [
            "Anja - Brand New Start",
            "Carrie Underwood - Good Girl",
        ]

    @functools.cached_property
    def songs_jd4_pal_exclusive(self) -> List[str]:
        return [
            "Cercavo Amore - Emma",
            "Diggin' in the Dirt - Stefanie Heinzmann",
            "Rihanna ft. Jay-Z - Umbrella",  # PAL Special Edition only
        ]

    @functools.cached_property
    def songs_jd4_wii_u_exclusive(self) -> List[str]:
        return [
            "The Girly Team - Ain't No Other Man (Christina Aguilera)",
            "Jessie J - Domino",
            "Cher Lloyd ft. Astro - Want U Back",
        ]

    @functools.cached_property
    def songs_jd4_ntsc_exclusive(self) -> List[str]:
        return [
            "Carrie Underwood - Good Girl",
        ]

    @functools.cached_property
    def songs_jd4_excluded_from_ntsc_wii(self) -> List[str]:
        return [
            "Bunny Beatz ft. Liquid - Make The Party (Don't Stop)",  # Available on other platforms but not NTSC Wii
        ]

    @functools.cached_property
    def songs_jd4_cheetos_promo(self) -> List[str]:
        return [
            "Anja - Brand New Start [JD4 - Cheetos Promo]",
        ]

    @functools.cached_property
    def songs_jd2014_ntsc_exclusive(self) -> List[str]:
        return [
            "Jason Derulo - The Other Side [JD2014 - NTSC Exclusive]",
        ]

    @functools.cached_property
    def songs_jd2014_pal_exclusive(self) -> List[str]:
        return [
            "Ivete Sangalo - Dançando [JD2014 - PAL Exclusive]",
            "Tal - Danse (Pop Version) [JD2014 - PAL Exclusive]",
            "Fedez - Alfonso Signorini (Eroe Nazionale) [JD2014 - PAL Exclusive]",
        ]

    @functools.cached_property
    def songs_jd2014_popchips_promo(self) -> List[str]:
        return [
            "Capital Cities - Safe And Sound [JD2014 - Popchips Promo]",
            "Katy Perry - Waking Up in Vegas [JD2014 - Popchips Promo]",
        ]

    @functools.cached_property
    def songs_jd2015_ntsc_exclusive(self) -> List[str]:
        return [
            "Austin Mahone - Till I Find You [JD2015 - NTSC Exclusive]",
        ]

    @functools.cached_property
    def songs_jd2015_pal_exclusive(self) -> List[str]:
        return [
            "Stromae - Papaoutai [JD2015 - PAL Exclusive]",
        ]
class JustDanceGamesOwned(OptionSet):
    """
    Indicates which Just Dance games the player owns.
    """
    display_name = "Just Dance Games Owned"
    valid_keys = [
        "Just Dance",
        "Just Dance 2", 
        "Just Dance 3",
        "Just Dance 4",
        "Just Dance 2014",
        "Just Dance 2015",
        "Just Dance 2016", 
        "Just Dance 2017",
        "Just Dance 2018",
        "Just Dance 2019",
        "Just Dance 2020",
        "Just Dance 2021",
        "Just Dance 2022",
        "Just Dance 2023 Edition",
        "Just Dance 2024 Edition",
        "Just Dance 2025 Edition",
        "Just Dance 2026 Edition",
    ]
    default = [
        "Just Dance",
        "Just Dance 2", 
        "Just Dance 3",
        "Just Dance 4",
        "Just Dance 2014",
        "Just Dance 2015",
        "Just Dance 2016", 
        "Just Dance 2017",
        "Just Dance 2018",
        "Just Dance 2019",
        "Just Dance 2020",
        "Just Dance 2021",
        "Just Dance 2022",
        "Just Dance 2023 Edition",
        "Just Dance 2024 Edition",
        "Just Dance 2025 Edition",
        "Just Dance 2026 Edition",
    ]


class JustDanceIncludeUnlimitedSongs(DefaultOnToggle):
    """
    Include songs from Just Dance Unlimited subscription service.
    """
    display_name = "Include Just Dance Unlimited Songs"


class JustDanceDLCContent(OptionSet):
    """
    Official DLC packs for Just Dance games.
    """
    display_name = "Just Dance DLC Content"
    valid_keys = [
        "JD2 - DLC Pack 1 (Launch)",
        "JD2 - DLC Pack 2 (October 2010)",
        "JD2 - DLC Pack 3 (November 2010)",
        "JD2 - DLC Pack 4 (December 2010)",
        "JD2 - DLC Pack 5 (January 2011)",
        "JD2 - DLC Pack 6 (February 2011)",
        "JD2 - DLC Pack 7 (March 2011)",
        "JD2 - DLC Pack 8 (April-June 2011)",
        "JD3 - Sweat Pack #1",
        "JD3 - Sweat Pack #2", 
        "JD3 - Valentine Pack",
        "JD3 - Christmas Pack",
        "JD3 - Spring Break Pack #1",
        "JD3 - Spring Break Pack #2",
        "JD3 - Individual DLC Songs",
        "JD4 - DLC Pack 1 (October 2012)",
        "JD4 - DLC Pack 2 (November 2012)",
        "JD4 - DLC Pack 3 (December 2012)",
        "JD4 - DLC Pack 4 (January 2013)",
        "JD4 - DLC Pack 5 (March 2013)",
        "JD4 - DLC Pack 6 (April 2013)",
        "JD2014 - Launch DLC",
        "JD2014 - November 2013 DLC",
        "JD2014 - December 2013 DLC",
        "JD2014 - February 2014 DLC",
        "JD2014 - March 2014 DLC",
        "JD2014 - April 2014 DLC",
        "JD2014 - May 2014 DLC",
        "JD2015 - Day One DLC",
        "JD2015 - November 2014 DLC",
        "JD2015 - January 2015 DLC",
        "JD2016 - Just Dance Unlimited",
        "JD2017 - Just Dance Unlimited",
        "JD2018 - Just Dance Unlimited",
        "JD2019 - Just Dance Unlimited",
        "JD2020 - Just Dance Unlimited",
        "JD2021 - Just Dance Unlimited",
        "JD2022 - Just Dance Unlimited",
        "JD2023 - Just Dance Unlimited",
        "JD2024 - Just Dance Unlimited",
        "JD2025 - Just Dance Unlimited",
    ]
    default = [
        "JD2 - DLC Pack 1 (Launch)",
        "JD2 - DLC Pack 2 (October 2010)",
        "JD2 - DLC Pack 3 (November 2010)",
        "JD2 - DLC Pack 4 (December 2010)",
        "JD2 - DLC Pack 5 (January 2011)",
        "JD2 - DLC Pack 6 (February 2011)",
        "JD2 - DLC Pack 7 (March 2011)",
        "JD2 - DLC Pack 8 (April-June 2011)",
        "JD3 - Sweat Pack #1",
        "JD3 - Sweat Pack #2", 
        "JD3 - Valentine Pack",
        "JD3 - Christmas Pack",
        "JD3 - Spring Break Pack #1",
        "JD3 - Spring Break Pack #2",
        "JD3 - Individual DLC Songs",
        "JD4 - DLC Pack 1 (October 2012)",
        "JD4 - DLC Pack 2 (November 2012)",
        "JD4 - DLC Pack 3 (December 2012)",
        "JD4 - DLC Pack 4 (January 2013)",
        "JD4 - DLC Pack 5 (March 2013)",
        "JD4 - DLC Pack 6 (April 2013)",
        "JD2014 - Launch DLC",
        "JD2014 - November 2013 DLC",
        "JD2014 - December 2013 DLC",
        "JD2014 - February 2014 DLC",
        "JD2014 - March 2014 DLC",
        "JD2014 - April 2014 DLC",
        "JD2014 - May 2014 DLC",
        "JD2015 - Day One DLC",
        "JD2015 - November 2014 DLC",
        "JD2015 - January 2015 DLC",
        "JD2016 - Just Dance Unlimited",
        "JD2017 - Just Dance Unlimited",
        "JD2018 - Just Dance Unlimited",
        "JD2019 - Just Dance Unlimited",
        "JD2020 - Just Dance Unlimited",
        "JD2021 - Just Dance Unlimited",
        "JD2022 - Just Dance Unlimited",
        "JD2023 - Just Dance Unlimited",
        "JD2024 - Just Dance Unlimited",
        "JD2025 - Just Dance Unlimited",
    ]


class JustDanceExclusiveContent(OptionSet):
    """
    Regional exclusive content and special editions.
    """
    display_name = "Just Dance Exclusive Content"
    valid_keys = [
        "JD1 - PAL Exclusive",
        "JD2 - Best Buy/Walmart Exclusive",
        "JD3 - Target/Zellers Exclusive",
        "JD3 - Best Buy Exclusive",
        "JD3 - PAL Exclusive",
        "JD3 - PS3 Exclusive",
        "JD4 - Target Exclusive",
        "JD4 - Best Buy Exclusive",
        "JD4 - PAL Exclusive",
        "JD4 - Wii U Exclusive",
        "JD4 - NTSC Exclusive",
        "JD4 - Excluded from NTSC Wii",
        "JD4 - Cheetos Promo",
        "JD2014 - NTSC Exclusive",
        "JD2014 - PAL Exclusive",
        "JD2014 - Popchips Promo",
        "JD2015 - NTSC Exclusive",
        "JD2015 - PAL Exclusive",
        "JD2015 - Ubisoft Connect Unlockables",
        "JD2016 - Ubisoft Connect Unlockables",
        "JD2016 - Russia Exclusive",
        "JD2017 - Ubisoft Connect Unlockables",
        "JD2017 - Russia Exclusive",
        "JD2017 - Switch Exclusive",
        "JD2018 - Ubisoft Connect Unlockables",
        "JD2018 - Russia Exclusive",
        "JD2018 - Switch Exclusive",
        "JD2019 - Code Unlock",
        "JD2019 - Middle East Exclusive",
        "JD2019 - France/Canada Exclusive",
        "JD2019 - Russia Exclusive",
        "JD2020 - Japan Exclusive",
        "JD2020 - France Exclusive",
        "JD2020 - Benelux Exclusive", 
        "JD2020 - Russia Exclusive",
        "JD2021 - Japan Exclusive",
        "JD2021 - France Exclusive",
        "JD2021 - Benelux Exclusive",
        "JD2022 - China Exclusive",
        "JD2022 - France Exclusive",
        "JD2022 - France/Canada Exclusive",
        "JD2022 - Japan Exclusive",
        "JD2022 - Benelux Exclusive",
        "JD2022 - Germany Exclusive",
        "JD2022 - Southeast Asia Exclusive",
        "JD2023 - France Exclusive",
        "JD2023 - Italy Exclusive",
        "JD2023 - Japan Exclusive",
        "JD2023 - Benelux Exclusive",
        "JD2024 - Japan Exclusive",
    ]
    default = [
        "JD1 - PAL Exclusive",
        "JD2 - Best Buy/Walmart Exclusive",
        "JD3 - Target/Zellers Exclusive",
        "JD3 - Best Buy Exclusive",
        "JD3 - PAL Exclusive",
        "JD3 - PS3 Exclusive",
        "JD4 - Target Exclusive",
        "JD4 - Best Buy Exclusive",
        "JD4 - PAL Exclusive",
        "JD4 - Wii U Exclusive",
        "JD4 - NTSC Exclusive",
        "JD4 - Excluded from NTSC Wii",
        "JD4 - Cheetos Promo",
        "JD2014 - NTSC Exclusive",
        "JD2014 - PAL Exclusive",
        "JD2014 - Popchips Promo",
        "JD2015 - NTSC Exclusive",
        "JD2015 - PAL Exclusive",
        "JD2015 - Ubisoft Connect Unlockables",
        "JD2016 - Ubisoft Connect Unlockables",
        "JD2016 - Russia Exclusive",
        "JD2017 - Ubisoft Connect Unlockables",
        "JD2017 - Russia Exclusive",
        "JD2017 - Switch Exclusive",
        "JD2018 - Ubisoft Connect Unlockables",
        "JD2018 - Russia Exclusive",
        "JD2018 - Switch Exclusive",
        "JD2019 - Code Unlock",
        "JD2019 - Middle East Exclusive",
        "JD2019 - France/Canada Exclusive",
        "JD2019 - Russia Exclusive",
        "JD2020 - Japan Exclusive",
        "JD2020 - France Exclusive",
        "JD2020 - Benelux Exclusive",
        "JD2020 - Russia Exclusive",
        "JD2021 - Japan Exclusive",
        "JD2021 - France Exclusive",
        "JD2021 - Benelux Exclusive",
        "JD2022 - China Exclusive",
        "JD2022 - France Exclusive",
        "JD2022 - France/Canada Exclusive",
        "JD2022 - Japan Exclusive",
        "JD2022 - Benelux Exclusive",
        "JD2022 - Germany Exclusive",
        "JD2022 - Southeast Asia Exclusive",
        "JD2023 - France Exclusive",
        "JD2023 - Italy Exclusive",
        "JD2023 - Japan Exclusive",
        "JD2023 - Benelux Exclusive",
        "JD2024 - Japan Exclusive",
    ]


class JustDancePlusContent(OptionSet):
    """
    Just Dance+ subscription service tracks.
    """
    display_name = "Just Dance+ Content"
    valid_keys = [
        "JD2022 - Just Dance+",
        "JD2023 - Just Dance+",
        "JD2024 - Just Dance+",
        "JD2025 - Just Dance+",
        "JD2026 - Just Dance+",
    ]
    default = [
        "JD2022 - Just Dance+",
        "JD2023 - Just Dance+",
        "JD2024 - Just Dance+",
        "JD2025 - Just Dance+",
        "JD2026 - Just Dance+",
    ]
