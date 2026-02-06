from __future__ import annotations

from typing import List, Optional
import os
from threading import Lock

from dataclasses import dataclass

from Options import Toggle, DefaultOnToggle, Range, FreeText, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


# Module-level cache that persists across class reloads
_WIKIPEDIA_TRENDING_CACHE = None
_WIKIPEDIA_TRENDING_CACHE_TIME = None
_WIKIPEDIA_TRENDING_CACHE_TTL = 3600  # Cache for 1 hour
_WIKIPEDIA_TRENDING_CACHE_LOCK = Lock()  # Thread-safe lock

_WIKIPEDIA_FEATURED_CACHE = None
_WIKIPEDIA_FEATURED_CACHE_TIME = None
_WIKIPEDIA_FEATURED_CACHE_TTL = 86400  # Cache for 24 hours
_WIKIPEDIA_FEATURED_CACHE_LOCK = Lock()  # Thread-safe lock

_WIKIPEDIA_POPULAR_CACHE = None
_WIKIPEDIA_POPULAR_CACHE_TIME = None
_WIKIPEDIA_POPULAR_CACHE_TTL = 3600  # Cache for 1 hour (pageviews change frequently)
_WIKIPEDIA_POPULAR_CACHE_LOCK = Lock()  # Thread-safe lock

# Track if packs have been initialized to avoid repeated initialization
_WIKIPEDIA_PACKS_INITIALIZED = set()  # Set of initialized pack directories
_WIKIPEDIA_PACKS_INIT_LOCK = Lock()  # Thread-safe lock for initialization

# Cache master articles per pack directory to avoid repeated loading
_WIKIPEDIA_MASTER_ARTICLES_CACHE = {}  # Maps pack_dir -> articles list
_WIKIPEDIA_MASTER_ARTICLES_LOCK = Lock()  # Thread-safe lock


@dataclass
class WikipediaGameArchipelagoOptions:
    wikipedia_game_include_specific_paths: WikipediaGameIncludeSpecificPaths
    wikipedia_game_include_random_paths: WikipediaGameIncludeRandomPaths
    wikipedia_game_max_clicks: WikipediaGameMaxClicks
    wikipedia_game_difficulties: WikipediaGameDifficulties
    wikipedia_game_trending_articles_limit: WikipediaGameTrendingArticlesLimit
    wikipedia_game_generate_default_packs: WikipediaGameGenerateDefaultPacks
    wikipedia_game_update_trending_articles_pack: WikipediaGameUpdateTrendingArticlesPack
    wikipedia_game_update_featured_articles_pack: WikipediaGameUpdateFeaturedArticlesPack
    wikipedia_game_update_popular_articles_pack: WikipediaGameUpdatePopularArticlesPack
    wikipedia_game_packs_subfolder: WikipediaGamePacksSubfolder


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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure pack directories exist on game initialization (once per directory)
        global _WIKIPEDIA_PACKS_INITIALIZED, _WIKIPEDIA_PACKS_INIT_LOCK
        
        packs_dir = self.packs_dir()
        
        with _WIKIPEDIA_PACKS_INIT_LOCK:
            if packs_dir not in _WIKIPEDIA_PACKS_INITIALIZED:
                print(f"[Wikipedia Game] Initializing packs directory: {packs_dir}")
                self.ensure_packs_dir()
                
                # Check if pack files exist
                pack_files_exist = any(f.lower().endswith('.txt') for f in os.listdir(packs_dir))
                
                # Generate/update based on toggles or if no files exist
                if self.generate_default_packs or not pack_files_exist:
                    if not pack_files_exist:
                        print(f"[Wikipedia Game] No pack files found. Auto-generating defaults...")
                    else:
                        print(f"[Wikipedia Game] Generate default packs enabled. Regenerating...")
                    self.generate_or_update_default_packs()
                else:
                    print(f"[Wikipedia Game] Pack files found, skipping auto-generation")
                
                if self.update_trending_articles_pack:
                    print(f"[Wikipedia Game] Update trending articles enabled. Updating...")
                    self.update_trending_articles_pack_file()
                
                if self.update_featured_articles_pack:
                    print(f"[Wikipedia Game] Update featured articles enabled. Updating...")
                    self.update_featured_articles_pack_file()
                
                if self.update_popular_articles_pack:
                    print(f"[Wikipedia Game] Update popular articles enabled. Updating...")
                    self.update_popular_articles_pack_file()
                
                print(f"[Wikipedia Game] Packs directory ready")
                _WIKIPEDIA_PACKS_INITIALIZED.add(packs_dir)

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
        
        if self.include_random_paths:
            objectives += self.random_path_objectives()
        
        return objectives
    
    def easy_clicks_for_easy(self) -> range:
        base = self.get_effective_max_clicks("easy")
        return range(max(6, base - 8), base + 1)
    
    def easy_clicks_for_standard(self) -> range:
        base = self.get_effective_max_clicks("standard")
        return range(max(6, base - 8), base + 1)
    
    def easy_clicks_for_hard(self) -> range:
        base = self.get_effective_max_clicks("hard")
        return range(max(6, base - 8), base + 1)
    
    def easy_clicks_for_expert(self) -> range:
        base = self.get_effective_max_clicks("expert")
        return range(max(6, base - 8), base + 1)

    def standard_clicks_for_easy(self) -> range:
        base = self.get_effective_max_clicks("easy")
        return range(max(6, base - 5), base + 1)
    
    def standard_clicks_for_standard(self) -> range:
        base = self.get_effective_max_clicks("standard")
        return range(max(6, base - 5), base + 1)
    
    def standard_clicks_for_hard(self) -> range:
        base = self.get_effective_max_clicks("hard")
        return range(max(6, base - 5), base + 1)
    
    def standard_clicks_for_expert(self) -> range:
        base = self.get_effective_max_clicks("expert")
        return range(max(6, base - 5), base + 1)

    def hard_clicks_for_easy(self) -> range:
        base = self.get_effective_max_clicks("easy")
        return range(max(6, base - 3), base + 1)
    
    def hard_clicks_for_standard(self) -> range:
        base = self.get_effective_max_clicks("standard")
        return range(max(6, base - 3), base + 1)
    
    def hard_clicks_for_hard(self) -> range:
        base = self.get_effective_max_clicks("hard")
        return range(max(6, base - 3), base + 1)
    
    def hard_clicks_for_expert(self) -> range:
        base = self.get_effective_max_clicks("expert")
        return range(max(6, base - 3), base + 1)

    def expert_clicks_for_easy(self) -> range:
        base = self.get_effective_max_clicks("easy")
        return range(max(6, base - 1), base + 1)
    
    def expert_clicks_for_standard(self) -> range:
        base = self.get_effective_max_clicks("standard")
        return range(max(6, base - 1), base + 1)
    
    def expert_clicks_for_hard(self) -> range:
        base = self.get_effective_max_clicks("hard")
        return range(max(6, base - 1), base + 1)
    
    def expert_clicks_for_expert(self) -> range:
        base = self.get_effective_max_clicks("expert")
        return range(max(6, base - 1), base + 1)

    def base_objectives(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = []
        
        # Easy difficulty objectives
        if self.include_easy_objectives:
            objectives.extend([
                # Pair selection (easier)
                GameObjectiveTemplate(
                    label="Connect the following articles (in order) in EASY_CLICKS clicks or fewer: ARTICLES1",
                    data={
                        "ARTICLES1": (self.master_articles, 2),
                        "EASY_CLICKS": (self.easy_clicks_for_easy, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
                # Three-article challenge with generous limit
                GameObjectiveTemplate(
                    label="Find a path between these 3 articles (in order) in GENEROUS_CLICKS clicks or fewer: ARTICLES3",
                    data={
                        "ARTICLES3": (self.master_articles, 3),
                        "GENEROUS_CLICKS": (self.easy_clicks_for_easy, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
            ])
        
        # Standard difficulty objectives
        if self.include_standard_objectives:
            objectives.extend([
                # Single article pair (standard)
                GameObjectiveTemplate(
                    label="Connect the following articles (in order) in STANDARD_CLICKS clicks or fewer: ARTICLE1, ARTICLE2",
                    data={
                        "ARTICLE1": (self.master_articles, 1),
                        "ARTICLE2": (self.master_articles, 1),
                        "STANDARD_CLICKS": (self.standard_clicks_for_standard, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
                # Another pair (standard)
                GameObjectiveTemplate(
                    label="Connect the following articles (in order) in STANDARD_CLICKS clicks or fewer: ARTICLE3, ARTICLE4",
                    data={
                        "ARTICLE3": (self.master_articles, 1),
                        "ARTICLE4": (self.master_articles, 1),
                        "STANDARD_CLICKS": (self.standard_clicks_for_standard, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=4,
                ),
            ])
        
        # Hard difficulty objectives
        if self.include_hard_objectives:
            objectives.extend([
                # Third pair (hard)
                GameObjectiveTemplate(
                    label="Connect the following articles (in order) in HARD_CLICKS clicks or fewer: ARTICLE5, ARTICLE6",
                    data={
                        "ARTICLE5": (self.master_articles, 1),
                        "ARTICLE6": (self.master_articles, 1),
                        "HARD_CLICKS": (self.hard_clicks_for_hard, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
                # Fourth pair (hard)
                GameObjectiveTemplate(
                    label="Connect the following articles (in order) in HARD_CLICKS clicks or fewer: ARTICLE7, ARTICLE8",
                    data={
                        "ARTICLE7": (self.master_articles, 1),
                        "ARTICLE8": (self.master_articles, 1),
                        "HARD_CLICKS": (self.hard_clicks_for_hard, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
                # Fifth pair (harder)
                GameObjectiveTemplate(
                    label="Connect the following articles (in order) in HARD_CLICKS clicks or fewer: ARTICLE9, ARTICLE10",
                    data={
                        "ARTICLE9": (self.master_articles, 1),
                        "ARTICLE10": (self.master_articles, 1),
                        "HARD_CLICKS": (self.hard_clicks_for_hard, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                ),
            ])
        
        # Expert difficulty objectives
        if self.include_expert_objectives:
            objectives.extend([
                # Starter to finisher (expert, tight clicks)
                GameObjectiveTemplate(
                    label="Connect the following articles (in order) in EXPERT_CLICKS clicks or fewer: ARTICLES2",
                    data={
                        "ARTICLES2": (self.master_articles, 2),
                        "EXPERT_CLICKS": (self.expert_clicks_for_expert, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=8,
                ),
                # Three-article challenge with no click limit
                GameObjectiveTemplate(
                    label="Find a path between these 3 articles (in order): ARTICLES4",
                    data={
                        "ARTICLES4": (self.master_articles, 3),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=6,
                ),
            ])
        
        return objectives

    def random_path_objectives(self) -> List[GameObjectiveTemplate]:
        objectives = [
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
                    "END_ARTICLE": (self.master_articles, 1),
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
        
        return objectives
    
    @property
    def include_random_paths(self) -> bool:
        return self.archipelago_options.wikipedia_game_include_random_paths.value
    
    @property
    def trending_articles_limit(self) -> int:
        return self.archipelago_options.wikipedia_game_trending_articles_limit.value

    @property
    def generate_default_packs(self) -> bool:
        return self.archipelago_options.wikipedia_game_generate_default_packs.value
    
    @property
    def update_trending_articles_pack(self) -> bool:
        return self.archipelago_options.wikipedia_game_update_trending_articles_pack.value
    
    @property
    def update_featured_articles_pack(self) -> bool:
        return self.archipelago_options.wikipedia_game_update_featured_articles_pack.value
    
    @property
    def update_popular_articles_pack(self) -> bool:
        return self.archipelago_options.wikipedia_game_update_popular_articles_pack.value
    
    @property
    def difficulties(self) -> List[str]:
        return sorted(self.archipelago_options.wikipedia_game_difficulties.value)
    
    @property
    def include_easy_objectives(self) -> bool:
        return "Easy" in self.difficulties
    
    @property
    def include_standard_objectives(self) -> bool:
        return "Standard" in self.difficulties
    
    @property
    def include_hard_objectives(self) -> bool:
        return "Hard" in self.difficulties
    
    @property
    def include_expert_objectives(self) -> bool:
        return "Expert" in self.difficulties
    
    def get_effective_max_clicks(self, difficulty: str) -> int:
        """Get max_clicks adjusted by difficulty level."""
        base = self.max_clicks
        
        # Apply difficulty multipliers to reduce clicks
        difficulty_multipliers = {
            "easy": 1.0,      # No reduction
            "standard": 0.75,  # 25% reduction
            "hard": 0.5,       # 50% reduction
            "expert": 0.3,     # 70% reduction
        }
        
        multiplier = difficulty_multipliers.get(difficulty.lower(), 1.0)
        return max(4, int(base * multiplier))  # Never go below 4 clicks
    
    @property
    def packs_subfolder(self) -> str:
        folder = self.archipelago_options.wikipedia_game_packs_subfolder.value.strip()
        # Remove invalid characters for folder names
        invalid_chars = '<>:"|?*\\/'
        for char in invalid_chars:
            folder = folder.replace(char, '')
        return folder
    
    @property
    def max_clicks(self) -> int:
        return self.archipelago_options.wikipedia_game_max_clicks.value
    
    @property
    def max_clicks_range(self) -> range:
        """Returns a range centered around the max_clicks setting"""
        base = self.max_clicks
        return range(max(3, base - 2), base + 3)
    
    @property
    def easy_clicks_range(self, difficulty: str) -> range:
        """Most lenient range for easier objectives - large downward variance."""
        base = self.get_effective_max_clicks(difficulty)
        return range(max(6, base - 8), base + 1)

    def standard_clicks_range(self, difficulty: str) -> range:
        """Default range for standard difficulty objectives - medium downward variance."""
        base = self.get_effective_max_clicks(difficulty)
        return range(max(6, base - 5), base + 1)

    def hard_clicks_range(self, difficulty: str) -> range:
        """More challenging range for harder objectives - small downward variance."""
        base = self.get_effective_max_clicks(difficulty)
        return range(max(6, base - 3), base + 1)

    def expert_clicks_range(self, difficulty: str) -> range:
        """Most challenging range for expert-level objectives - minimal downward variance."""
        base = self.get_effective_max_clicks(difficulty)
        return range(max(6, base - 1), base + 1)

    def fetch_trending_articles(self, limit: Optional[int] = None) -> List[str]:
        """Fetch recently changed Wikipedia articles using the MediaWiki API.
        Returns a list of article titles, or empty list if API fails.
        """
        import requests
        
        # Use configured limit if not specified
        if limit is None:
            limit = self.trending_articles_limit
        
        try:
            print(f"[Wikipedia Game] Fetching trending articles...")
            
            # Use MediaWiki API to get recent changes
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "recentchanges",
                "rcnamespace": "0",  # Main namespace only
                "rclimit": min(limit, 500),  # API max is 500
                "rctype": "new|edit",  # New articles and edits
                "format": "json"
            }
            headers = {
                "User-Agent": "KeymastersKeep/1.0 (Wikipedia Game objectives)"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                changes = data.get("query", {}).get("recentchanges", [])
                
                # Extract unique article titles, filtering out meta pages
                articles = []
                seen = set()
                for change in changes:
                    title = change.get("title", "")
                    if (title and 
                        title not in seen and
                        not title.startswith(("Special:", "Wikipedia:", "User:", "User talk:", "Template:", "File:")) and
                        title not in ["Main Page"]):
                        articles.append(title)
                        seen.add(title)
                        if len(articles) >= limit:
                            break
                
                print(f"[Wikipedia Game] Successfully fetched {len(articles)} trending articles")
                return articles
            else:
                print(f"[Wikipedia Game] API returned status code {response.status_code}")
            
        except requests.exceptions.Timeout:
            print("[Wikipedia Game] WARNING: API request timed out (trending articles unavailable)")
        except requests.exceptions.RequestException as e:
            print(f"[Wikipedia Game] WARNING: Network error fetching trending articles: {e}")
        except Exception as e:
            print(f"[Wikipedia Game] WARNING: Error fetching trending articles: {e}")
        
        return []
    
    def get_trending_articles_cached(self, limit: Optional[int] = None) -> List[str]:
        """Get trending articles with caching to avoid repeated API calls.
        Returns cached results if available and fresh, otherwise fetches new ones.
        Thread-safe implementation prevents multiple simultaneous fetches.
        Uses module-level cache to persist across class reloads.
        """
        global _WIKIPEDIA_TRENDING_CACHE, _WIKIPEDIA_TRENDING_CACHE_TIME, _WIKIPEDIA_TRENDING_CACHE_LOCK
        
        import time
        
        current_time = time.time()
        
        # Fast path: check cache without lock first
        if (_WIKIPEDIA_TRENDING_CACHE is not None and 
            _WIKIPEDIA_TRENDING_CACHE_TIME is not None and
            current_time - _WIKIPEDIA_TRENDING_CACHE_TIME < _WIKIPEDIA_TRENDING_CACHE_TTL):
            return _WIKIPEDIA_TRENDING_CACHE
        
        # Use stale cache if available (better than multiple fetches)
        if _WIKIPEDIA_TRENDING_CACHE is not None and len(_WIKIPEDIA_TRENDING_CACHE) > 0:
            return _WIKIPEDIA_TRENDING_CACHE
        
        # Acquire lock for fetch operation
        with _WIKIPEDIA_TRENDING_CACHE_LOCK:
            # Double-check: another thread may have just populated the cache
            if _WIKIPEDIA_TRENDING_CACHE is not None and len(_WIKIPEDIA_TRENDING_CACHE) > 0:
                return _WIKIPEDIA_TRENDING_CACHE
            
            # Cache is empty, fetch new articles
            articles = self.fetch_trending_articles(limit=limit)
            
            # Only update cache if fetch was successful (non-empty)
            if articles:
                _WIKIPEDIA_TRENDING_CACHE = articles
                _WIKIPEDIA_TRENDING_CACHE_TIME = current_time
            elif _WIKIPEDIA_TRENDING_CACHE:
                # API failed but we have old cache - keep using it
                return _WIKIPEDIA_TRENDING_CACHE
            
            return articles

    @staticmethod
    def fetch_featured_articles(limit: Optional[int] = None) -> List[str]:
        """Fetch featured Wikipedia articles using the MediaWiki API.
        Returns a list of article titles, or empty list if API fails.
        """
        import requests

        try:
            print(f"[Wikipedia Game] Fetching featured articles...")

            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "categorymembers",
                "cmtitle": "Category:Featured articles",
                "cmnamespace": "0",  # Main namespace only
                "cmlimit": 500,
                "format": "json",
            }
            headers = {
                "User-Agent": "KeymastersKeep/1.0 (Wikipedia Game objectives)"
            }

            articles: List[str] = []
            seen = set()
            cmcontinue = None

            while True:
                if cmcontinue:
                    params["cmcontinue"] = cmcontinue

                response = requests.get(url, params=params, headers=headers, timeout=10)

                if response.status_code != 200:
                    print(f"[Wikipedia Game] API returned status code {response.status_code}")
                    break

                data = response.json()
                members = data.get("query", {}).get("categorymembers", [])

                for member in members:
                    title = member.get("title", "")
                    if title and title not in seen:
                        articles.append(title)
                        seen.add(title)
                        if limit is not None and len(articles) >= limit:
                            print(f"[Wikipedia Game] Reached featured article limit ({limit})")
                            return articles

                cmcontinue = data.get("continue", {}).get("cmcontinue")
                if not cmcontinue:
                    break

            print(f"[Wikipedia Game] Successfully fetched {len(articles)} featured articles")
            return articles

        except requests.exceptions.Timeout:
            print("[Wikipedia Game] Featured articles API request timed out")
        except requests.exceptions.RequestException as e:
            print(f"[Wikipedia Game] Network error fetching featured articles: {e}")
        except Exception as e:
            print(f"[Wikipedia Game] Error fetching featured articles: {e}")

        print("[Wikipedia Game] Featured articles disabled - API unavailable")
        return []

    def get_featured_articles_cached(self, limit: Optional[int] = None) -> List[str]:
        """Get featured articles with caching to avoid repeated API calls.
        Returns cached results if available and fresh, otherwise fetches new ones.
        Thread-safe implementation prevents multiple simultaneous fetches.
        Uses module-level cache to persist across class reloads.
        """
        global _WIKIPEDIA_FEATURED_CACHE, _WIKIPEDIA_FEATURED_CACHE_TIME, _WIKIPEDIA_FEATURED_CACHE_LOCK

        import time

        current_time = time.time()

        if (_WIKIPEDIA_FEATURED_CACHE is not None and
            _WIKIPEDIA_FEATURED_CACHE_TIME is not None and
            current_time - _WIKIPEDIA_FEATURED_CACHE_TIME < _WIKIPEDIA_FEATURED_CACHE_TTL):
            return _WIKIPEDIA_FEATURED_CACHE

        if _WIKIPEDIA_FEATURED_CACHE is not None and len(_WIKIPEDIA_FEATURED_CACHE) > 0:
            return _WIKIPEDIA_FEATURED_CACHE

        with _WIKIPEDIA_FEATURED_CACHE_LOCK:
            if _WIKIPEDIA_FEATURED_CACHE is not None and len(_WIKIPEDIA_FEATURED_CACHE) > 0:
                return _WIKIPEDIA_FEATURED_CACHE

            articles = self.fetch_featured_articles(limit=limit)

            if articles:
                _WIKIPEDIA_FEATURED_CACHE = articles
                _WIKIPEDIA_FEATURED_CACHE_TIME = current_time
            elif _WIKIPEDIA_FEATURED_CACHE:
                return _WIKIPEDIA_FEATURED_CACHE

            return articles
    
    def get_trending_articles_cached(self, limit: Optional[int] = None) -> List[str]:
        """Get trending articles with caching to avoid repeated API calls.
        Returns cached results if available and fresh, otherwise fetches new ones.
        Thread-safe implementation prevents multiple simultaneous fetches.
        Uses module-level cache to persist across class reloads.
        Cache TTL: 1 hour for trending articles.
        """
        global _WIKIPEDIA_TRENDING_CACHE, _WIKIPEDIA_TRENDING_CACHE_TIME, _WIKIPEDIA_TRENDING_CACHE_LOCK

        import time

        current_time = time.time()

        if (_WIKIPEDIA_TRENDING_CACHE is not None and
            _WIKIPEDIA_TRENDING_CACHE_TIME is not None and
            current_time - _WIKIPEDIA_TRENDING_CACHE_TIME < _WIKIPEDIA_TRENDING_CACHE_TTL):
            return _WIKIPEDIA_TRENDING_CACHE

        if _WIKIPEDIA_TRENDING_CACHE is not None and len(_WIKIPEDIA_TRENDING_CACHE) > 0:
            return _WIKIPEDIA_TRENDING_CACHE

        with _WIKIPEDIA_TRENDING_CACHE_LOCK:
            if _WIKIPEDIA_TRENDING_CACHE is not None and len(_WIKIPEDIA_TRENDING_CACHE) > 0:
                return _WIKIPEDIA_TRENDING_CACHE

            articles = self.fetch_trending_articles(limit=limit)

            if articles:
                _WIKIPEDIA_TRENDING_CACHE = articles
                _WIKIPEDIA_TRENDING_CACHE_TIME = current_time
            elif _WIKIPEDIA_TRENDING_CACHE:
                return _WIKIPEDIA_TRENDING_CACHE

            return articles

    @staticmethod
    def fetch_popular_articles(limit: Optional[int] = None) -> List[str]:
        """Fetch most popular Wikipedia articles using the Wikimedia Pageviews API.
        Returns a list of article titles sorted by view count (most viewed first).
        Returns empty list if API fails.
        """
        import requests
        from datetime import datetime, timedelta
        
        if limit is None:
            limit = 100
        
        try:
            print(f"[Wikipedia Game] Fetching popular articles...")
            
            # Get yesterday's date for pageviews (API updates with 1-day lag)
            yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y/%m/%d")
            
            # Use Wikimedia Pageviews API for most viewed articles
            url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{yesterday}"
            headers = {
                "User-Agent": "KeymastersKeep/1.0 (Wikipedia Game objectives)"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles_data = data.get("items", [{}])[0].get("articles", [])
                
                # Extract unique article titles, filtering out meta pages
                articles = []
                for item in articles_data:
                    title = item.get("article", "")
                    if (title and
                        not title.startswith(("Special:", "Wikipedia:", "User:", "User talk:", "Template:", "File:", "Main_Page")) and
                        title != "Main Page" and
                        title.replace("_", " ") not in ["Main Page"]):  # Handle underscore variant
                        articles.append(title.replace("_", " "))
                        if len(articles) >= limit:
                            break
                
                print(f"[Wikipedia Game] Successfully fetched {len(articles)} popular articles")
                return articles
            else:
                print(f"[Wikipedia Game] API returned status code {response.status_code}")
            
        except requests.exceptions.Timeout:
            print("[Wikipedia Game] WARNING: Pageviews API request timed out (popular articles unavailable)")
        except requests.exceptions.RequestException as e:
            print(f"[Wikipedia Game] WARNING: Network error fetching popular articles: {e}")
        except Exception as e:
            print(f"[Wikipedia Game] WARNING: Error fetching popular articles: {e}")
        
        return []
    
    def get_popular_articles_cached(self, limit: Optional[int] = None) -> List[str]:
        """Get popular articles with caching to avoid repeated API calls.
        Returns cached results if available and fresh, otherwise fetches new ones.
        Thread-safe implementation prevents multiple simultaneous fetches.
        Uses module-level cache to persist across class reloads.
        Cache TTL: 1 hour for popular articles (pageviews update daily but we cache shorter).
        """
        global _WIKIPEDIA_POPULAR_CACHE, _WIKIPEDIA_POPULAR_CACHE_TIME, _WIKIPEDIA_POPULAR_CACHE_LOCK

        import time

        current_time = time.time()

        if (_WIKIPEDIA_POPULAR_CACHE is not None and
            _WIKIPEDIA_POPULAR_CACHE_TIME is not None and
            current_time - _WIKIPEDIA_POPULAR_CACHE_TIME < _WIKIPEDIA_POPULAR_CACHE_TTL):
            return _WIKIPEDIA_POPULAR_CACHE

        if _WIKIPEDIA_POPULAR_CACHE is not None and len(_WIKIPEDIA_POPULAR_CACHE) > 0:
            return _WIKIPEDIA_POPULAR_CACHE

        with _WIKIPEDIA_POPULAR_CACHE_LOCK:
            if _WIKIPEDIA_POPULAR_CACHE is not None and len(_WIKIPEDIA_POPULAR_CACHE) > 0:
                return _WIKIPEDIA_POPULAR_CACHE

            articles = self.fetch_popular_articles(limit=limit)

            if articles:
                _WIKIPEDIA_POPULAR_CACHE = articles
                _WIKIPEDIA_POPULAR_CACHE_TIME = current_time
            elif _WIKIPEDIA_POPULAR_CACHE:
                return _WIKIPEDIA_POPULAR_CACHE

            return articles

    def master_articles(self) -> List[str]:
        """Master list of articles derived entirely from packs.
        Automatically generates defaults if no packs exist.
        Updates trending and featured packs based on toggles.
        """
        global _WIKIPEDIA_MASTER_ARTICLES_CACHE, _WIKIPEDIA_MASTER_ARTICLES_LOCK
        
        # Auto-generate defaults if packs directory is empty
        packs_dir = self.packs_dir()
        
        # Check if we've already loaded this pack directory
        with _WIKIPEDIA_MASTER_ARTICLES_LOCK:
            if packs_dir in _WIKIPEDIA_MASTER_ARTICLES_CACHE:
                return _WIKIPEDIA_MASTER_ARTICLES_CACHE[packs_dir]
        
        # First load for this pack directory - do all the setup
        print(f"[Wikipedia Game] Using packs directory: {packs_dir}")
        
        if not os.path.isdir(packs_dir) or not any(f.lower().endswith('.txt') for f in os.listdir(packs_dir)):
            print(f"[Wikipedia Game] Pack directory empty at {packs_dir}. Auto-generating defaults...")
            self.generate_or_update_default_packs()
        
        if self.generate_default_packs:
            print(f"[Wikipedia Game] Generating default packs...")
            self.generate_or_update_default_packs()
        
        if self.update_trending_articles_pack:
            print(f"[Wikipedia Game] Updating trending articles pack...")
            self.update_trending_articles_pack_file()
        
        if self.update_featured_articles_pack:
            print(f"[Wikipedia Game] Updating featured articles pack...")
            self.update_featured_articles_pack_file()

        articles = self.load_pack_articles()
        print(f"[Wikipedia Game] Loaded {len(articles)} total articles from packs in {packs_dir}")
        
        # Cache for future calls
        with _WIKIPEDIA_MASTER_ARTICLES_LOCK:
            _WIKIPEDIA_MASTER_ARTICLES_CACHE[packs_dir] = articles
        
        return articles

    def packs_dir(self) -> str:
        base_dir = os.path.join(os.path.dirname(__file__), "wikipedia_game_packs")
        subfolder = self.packs_subfolder
        if subfolder:
            return os.path.join(base_dir, subfolder)
        return base_dir

    def ensure_packs_dir(self) -> str:
        packs_dir = self.packs_dir()
        os.makedirs(packs_dir, exist_ok=True)
        return packs_dir

    def load_pack_articles(self) -> List[str]:
        packs_dir = self.packs_dir()
        if not os.path.isdir(packs_dir):
            return []

        articles: List[str] = []
        for filename in sorted(os.listdir(packs_dir)):
            if not filename.lower().endswith(".txt"):
                continue
            file_path = os.path.join(packs_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as pack_file:
                    for line in pack_file:
                        entry = line.strip()
                        if not entry or entry.startswith("##"):
                            continue
                        # Filter out meta pages that don't work as destinations
                        if (entry.startswith(("Special:", "Wikipedia:", "User:", "User talk:", "Template:", "File:")) or
                            entry == "Main Page"):
                            continue
                        articles.append(entry)
            except Exception as e:
                print(f"[Wikipedia Game] Failed to read pack file {filename}: {e}")

        return self._dedupe_preserve_order(articles)
    
    def load_pack_file(self, pack_name: str) -> List[str]:
        """Load articles from a specific pack file."""
        packs_dir = self.packs_dir()
        file_path = os.path.join(packs_dir, pack_name)
        
        if not os.path.isfile(file_path):
            print(f"[Wikipedia Game] Pack file not found: {pack_name}")
            return []
        
        articles: List[str] = []
        try:
            with open(file_path, "r", encoding="utf-8") as pack_file:
                for line in pack_file:
                    entry = line.strip()
                    if not entry or entry.startswith("##"):
                        continue
                    articles.append(entry)
        except Exception as e:
            print(f"[Wikipedia Game] Failed to read pack file {pack_name}: {e}")
        
        return articles
    
    def animals_from_packs(self) -> List[str]:
        """Load animals from curated_animals.txt pack."""
        return self.load_pack_file("curated_animals.txt")
    
    def countries_from_packs(self) -> List[str]:
        """Load countries from curated_countries.txt pack."""
        return self.load_pack_file("curated_countries.txt")
    
    def foods_from_packs(self) -> List[str]:
        """Load foods from curated_foods.txt pack."""
        return self.load_pack_file("curated_foods.txt")
    
    def technologies_from_packs(self) -> List[str]:
        """Load technologies from curated_technologies.txt pack."""
        return self.load_pack_file("curated_technologies.txt")
    
    def historical_events_from_packs(self) -> List[str]:
        """Load historical events from curated_historical_events.txt pack."""
        return self.load_pack_file("curated_historical_events.txt")
    
    def video_games_from_packs(self) -> List[str]:
        """Load video games from curated_video_games.txt pack."""
        return self.load_pack_file("curated_video_games.txt")
    
    def memes_from_packs(self) -> List[str]:
        """Load memes from curated_memes.txt pack."""
        return self.load_pack_file("curated_memes.txt")

    def generate_or_update_default_packs(self) -> None:
        """Generate or overwrite default category packs and curated articles."""
        packs_dir = self.ensure_packs_dir()
        print(f"[Wikipedia Game] Generating default packs to {packs_dir}")

        # Extract articles from start/end lists for categorization
        start = self.start_articles()
        end = self.end_articles()
        
        pack_definitions = {
            "curated_animals.txt": self.animals(),
            "curated_countries.txt": self.countries(),
            "curated_foods.txt": self.foods(),
            "curated_technologies.txt": self.technologies(),
            "curated_historical_events.txt": self.historical_events(),
            "curated_video_games.txt": self.video_games(),
            "curated_memes.txt": self.memes(),
            "curated_chemistry.txt": [
                "Vitamin C", "Water", "Carbon", "Oxygen", "Hydrogen", "Iron", "Gold", "Salt", "DNA"
            ],
            "curated_locations.txt": [
                "Texas", "California", "New York City", "London", "Paris", "Tokyo", "Antarctica",
                "Mount Everest", "Eiffel Tower", "Great Wall of China", "Pyramids of Giza", "Stonehenge", "Atlantis"
            ],
            "curated_philosophy.txt": [
                "Philosophy", "Real life", "Time", "Space", "Love", "Death", "Consciousness", 
                "Free will", "Infinity", "Democracy", "Existentialism", "Truth", "Reality", "Existence"
            ],
            "curated_disambiguation.txt": [
                "Pyramid (disambiguation)", "Orange (disambiguation)", "Turkey (disambiguation)",
                "Java (disambiguation)", "Mercury (disambiguation)", "Apple (disambiguation)",
                "Amazon (disambiguation)", "Bank (disambiguation)", "Bat (disambiguation)", "Crane (disambiguation)"
            ],
            "curated_soundtracks.txt": [
                "Footloose (2011 soundtrack)", "Shrek 2 (soundtrack)", "Frozen (soundtrack)",
                "The Social Network (soundtrack)", "Guardians of the Galaxy (soundtrack)",
                "Tron: Legacy (soundtrack)", "The Lion King (soundtrack)"
            ],
            "curated_languages.txt": [
                "Klingon language", "Elvish languages", "Dothraki language", "Na'vi language",
                "Newspeak", "Pig Latin", "Esperanto", "Language", "Communication"
            ],
            "curated_gaming_hardware.txt": [
                "PlayStation Vita", "Sega Dreamcast", "Nintendo Virtual Boy", "Ouya", "Steam Deck",
                "Game Boy Color", "Nintendo 64", "PlayStation 2", "Xbox"
            ],
            "curated_historical_figures.txt": [
                "Napoleon", "Albert Einstein", "Cleopatra", "Leonardo da Vinci", "Marie Curie",
                "Genghis Khan", "Abraham Lincoln", "Nikola Tesla", "Galileo Galilei", "Isaac Newton",
                "Charles Darwin", "Joan of Arc", "Queen Victoria", "Julius Caesar"
            ],
            "curated_companies.txt": [
                "Wikipedia", "Apple Inc.", "Microsoft", "Tesla, Inc.", "Google", "Amazon (company)",
                "Facebook", "Twitter"
            ],
            "curated_music.txt": [
                "The Beatles", "Queen (band)", "Beethoven", "Mozart", "Bach", "Elvis Presley",
                "Michael Jackson", "Guitar", "Piano", "Drums", "Violin", "Jazz", "Rock music",
                "Hip hop music", "K-pop", "Vocaloid", "Dubstep", "Music"
            ],
            "curated_sports.txt": [
                "Basketball", "Baseball", "Soccer", "American football", "Tennis", "Golf",
                "Cricket", "Rugby", "Swimming"
            ],
            "curated_athletes.txt": [
                "Michael Jordan", "Serena Williams", "Muhammad Ali", "Usain Bolt",
                "Lionel Messi", "Cristiano Ronaldo"
            ],
            "curated_science.txt": [
                "Periodic table", "Evolution", "Photosynthesis", "Global warming", "Dinosaur",
                "Bacteria", "Mitochondria", "Gravity", "Electricity", "Magnetism", "Atom", "Cell (biology)"
            ],
            "curated_franchises.txt": [
                "Shakespeare", "Star Wars", "Harry Potter", "The Lord of the Rings",
                "Marvel Cinematic Universe", "DC Comics", "Anime", "Manga", "James Bond",
                "Doctor Who", "Star Trek"
            ],
            "curated_art.txt": [
                "Mona Lisa", "The Scream", "The Starry Night", "Guernica", "The Persistence of Memory"
            ],
            "curated_conspiracies.txt": [
                "42 (number)", "Area 51", "Bermuda Triangle", "Flat Earth",
                "Moon landing conspiracy theories", "Illuminati", "Roswell incident", "Crop circle"
            ],
            "curated_film_tv.txt": [
                "The Room (film)", "Citizen Kane", "The Godfather", "Pulp Fiction",
                "Breaking Bad", "Game of Thrones", "The Simpsons", "Friends"
            ],
            "curated_concepts.txt": [
                "Chess", "Mathematics", "Color", "Number", "Information", "Knowledge", "Memory", "Perception"
            ],
            "curated_internet_culture.txt": [
                "Selfie", "Banana for scale", "Murphy's law", "Rubber duck debugging",
                "The cake is a lie", "Easter egg (media)", "Wilhelm scream", "Red herring",
                "MacGuffin", "Deus ex machina", "Fourth wall", "Trope", "Internet"
            ],
            "curated_world_civilizations.txt": [
                "Ancient Greece", "Ancient Rome", "Ancient Egypt", "Byzantine Empire",
                "Ottoman Empire", "Holy Roman Empire", "Roman Empire"
            ],
        }

        for filename, items in pack_definitions.items():
            file_path = os.path.join(packs_dir, filename)
            self._write_pack_file(file_path, items)
            print(f"[Wikipedia Game] Generated {filename} with {len(items)} articles")
    
    def update_featured_articles_pack_file(self) -> None:
        """Update the featured_articles.txt pack with current Wikipedia featured articles."""
        packs_dir = self.ensure_packs_dir()
        featured = self.get_featured_articles_cached(limit=None)
        if featured:
            file_path = os.path.join(packs_dir, "featured_articles.txt")
            self._write_pack_file(file_path, featured)
            print(f"[Wikipedia Game] Updated featured_articles.txt with {len(featured)} articles")
        else:
            print(f"[Wikipedia Game] No featured articles fetched from API")
    
    def update_trending_articles_pack_file(self) -> None:
        """Update the trending_articles.txt pack with current Wikipedia trending articles."""
        packs_dir = self.ensure_packs_dir()
        trending = self.get_trending_articles_cached(limit=None)
        if trending:
            file_path = os.path.join(packs_dir, "trending_articles.txt")
            self._write_pack_file(file_path, trending)
            print(f"[Wikipedia Game] Updated trending_articles.txt with {len(trending)} articles")

    def update_popular_articles_pack_file(self) -> None:
        """Update the popular_articles.txt pack with most-viewed Wikipedia articles."""
        packs_dir = self.ensure_packs_dir()
        popular = self.get_popular_articles_cached(limit=None)
        if popular:
            file_path = os.path.join(packs_dir, "popular_articles.txt")
            self._write_pack_file(file_path, popular)
            print(f"[Wikipedia Game] Updated popular_articles.txt with {len(popular)} articles")

    def _write_pack_file(self, file_path: str, items: List[str]) -> None:
        deduped = self._dedupe_preserve_order([item.strip() for item in items if item and item.strip()])
        try:
            with open(file_path, "w", encoding="utf-8") as pack_file:
                pack_file.write("# Wikipedia Game pack file\n")
                pack_file.write("# One article title per line. Lines starting with # are ignored.\n\n")
                for item in deduped:
                    pack_file.write(f"{item}\n")
            print(f"[Wikipedia Game] Wrote {os.path.basename(file_path)} with {len(deduped)} articles")
        except Exception as e:
            print(f"[Wikipedia Game] ERROR: Failed to write pack file {os.path.basename(file_path)}: {e}")

    @staticmethod
    def _dedupe_preserve_order(items: List[str]) -> List[str]:
        seen = set()
        deduped = []
        for item in items:
            if item not in seen:
                deduped.append(item)
                seen.add(item)
        return deduped
    
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
            "Winston Churchill",
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


class WikipediaGameIncludeRandomPaths(Toggle):
    """
    Indicates whether to include objectives using Wikipedia's Random Article feature.
    These are more challenging as the start/end articles are unknown.
    """
    display_name = "Wikipedia Game: Include Random Paths"


class WikipediaGameMaxClicks(Range):
    """
    Maximum number of clicks allowed for Wikipedia path objectives (before difficulty adjustment).
    The actual click limits will be reduced based on the chosen difficulty levels.
    Higher values allow more generous click budgets. Difficulty will apply a multiplier.
    """
    display_name = "Wikipedia Game: Maximum Clicks"
    range_start = 10
    range_end = 50
    default = 20


class WikipediaGameDifficulties(OptionSet):
    """
    Select which difficulty levels to include in objectives.
    Difficulty adjusts click limits:
    - Easy: 100% of max clicks
    - Standard: 75% of max clicks
    - Hard: 50% of max clicks
    - Expert: 30% of max clicks
    """
    display_name = "Wikipedia Game: Difficulties"
    valid_keys = [
        "Easy",
        "Standard",
        "Hard",
        "Expert",
    ]
    default = valid_keys


class WikipediaGameTrendingArticlesLimit(Range):
    """
    Maximum number of trending articles to fetch from Wikipedia's recent changes.
    Higher values give more variety but take longer to fetch.
    """
    display_name = "Wikipedia Game: Trending Articles Limit"
    range_start = 10
    range_end = 500
    default = 100


class WikipediaGameGenerateDefaultPacks(Toggle):
    """
    When enabled, generates or overwrites the default category packs
    (animals.txt, countries.txt, foods.txt, etc.) and curated_articles.txt
    from the built-in lists.
    """
    display_name = "Wikipedia Game: Generate Default Packs"
    default = 0


class WikipediaGameUpdateTrendingArticlesPack(Toggle):
    """
    When enabled, updates trending_articles.txt with currently trending
    Wikipedia articles fetched from the MediaWiki API (cache TTL: 1 hour).
    """
    display_name = "Wikipedia Game: Update Trending Articles Pack"
    default = 0


class WikipediaGameUpdateFeaturedArticlesPack(Toggle):
    """
    When enabled, updates featured_articles.txt with Wikipedia's featured
    articles fetched from the MediaWiki API (cache TTL: 24 hours).
    """
    display_name = "Wikipedia Game: Update Featured Articles Pack"
    default = 0


class WikipediaGameUpdatePopularArticlesPack(Toggle):
    """
    When enabled, updates popular_articles.txt with Wikipedia's most-viewed
    articles fetched from the Wikimedia Pageviews API (cache TTL: 1 hour).
    Uses pageview statistics from the previous day for accuracy.
    """
    display_name = "Wikipedia Game: Update Popular Articles Pack"
    default = 0


class WikipediaGamePacksSubfolder(FreeText):
    """
    The name of the subfolder to use within wikipedia_game_packs/ for storing this player's article packs.
    Leave empty to use the root packs directory (shared across all players).
    Only provide the subfolder name (e.g., "eiron", "player2", "family") - do not include path separators.
    Invalid characters will be automatically removed.
    """
    display_name = "Wikipedia Game: Packs Subfolder"
    default = ""
