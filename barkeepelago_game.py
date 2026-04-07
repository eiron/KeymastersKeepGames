from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import requests

from Options import FreeText, NamedRange, OptionList, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms


VALID_FLAVORS: Tuple[str, ...] = (
    "sweet",
    "fruity",
    "bitter",
    "sour",
    "spicy",
    "creamy",
    "herbal",
    "salty",
    "refreshing",
    "nutty",
    "citrusy",
    "minty",
    "umami",
    "earthy",
    "floral",
    "smoky",
    "savory",
    "tangy",
    "aromatic",
    "dry",
    "bubbly",
    "tart",
    "spiced",
    "rich",
    "chocolatey",
    "smooth",
    "tropical",
    "malty",
)

VALID_GLASS_TYPES: Tuple[str, ...] = (
    "Highball Glass",
    "Collins Glass",
    "Cocktail Glass",
    "Coffee Mug",
    "Margarita Glass",
    "Coupe Glass",
    "Martini Glass",
    "Shot Glass",
    "Wine Glass",
    "Hurricane Glass",
    "Irish Coffee Cup",
    "Balloon Glass",
    "Mason Jar",
    "Champagne Flute",
    "Whiskey Glass",
    "Pint Glass",
    "Punch Bowl",
    "Beer Mug",
    "Beer Pilsner",
    "Pitcher",
    "Copper Mug",
    "Nick And Nora Glass",
    "Brandy Snifter",
    "Cordial Glass",
    "Parfait Glass",
    "Beer Glass",
    "Old-Fashioned Glass",
    "Pousse Cafe Glass",
)

VALID_DIETS: Tuple[str, ...] = (
    "paleo",
    "primal",
    "grain-free",
    "vegan",
    "vegetarian",
)


@dataclass
class BarkeepelagoArchipelagoOptions:
    barkeepelago_api_key: BarkeepelagoAPIKey
    barkeepelago_query: BarkeepelagoQuery
    barkeepelago_flavors: BarkeepelagoFlavors
    barkeepelago_glass_types: BarkeepelagoGlassTypes
    barkeepelago_include_ingredients: BarkeepelagoIncludeIngredients
    barkeepelago_exclude_ingredients: BarkeepelagoExcludeIngredients
    barkeepelago_diet: BarkeepelagoDiet
    barkeepelago_max_alcohol_percent: BarkeepelagoMaxAlcoholPercent
    barkeepelago_max_caffeine: BarkeepelagoMaxCaffeine
    barkeepelago_drink_count: BarkeepelagoDrinkCount
    barkeepelago_prefer_cocktaildb: BarkeepelagoPreferCocktailDb
    barkeepelago_use_random_sort: BarkeepelagoUseRandomSort
    barkeepelago_hard_fail_on_api_errors: BarkeepelagoHardFailOnApiErrors
    barkeepelago_use_cocktaildb_fallback: BarkeepelagoUseCocktailDbFallback
    barkeepelago_ignore_cache: BarkeepelagoIgnoreCache


class BarkeepelagoGame(Game):
    name = "Barkeep-elago!"
    platform = KeymastersKeepGamePlatforms.META

    is_adult_only_or_unrated = True

    options_cls = BarkeepelagoArchipelagoOptions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._barkeepelago_skip_api_precheck = True

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        # During pre-filter checks, return a cheap template so no API is hit.
        # The generator may call this method for many games before selecting any.
        if getattr(self, "_barkeepelago_skip_api_precheck", False):
            self._barkeepelago_skip_api_precheck = False
            return [
                GameObjectiveTemplate(
                    label="Mix DRINK",
                    data={
                        "DRINK": (["a drink of your choice"], 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                ),
            ]

        game_objective_templates: List[GameObjectiveTemplate] = list()

        print("[Barkeep-elago] Initializing...")
        if not hasattr(self, "drink_list"):
            print(
                "[Barkeep-elago] Loading drinks...",
                "Query:",
                self.query,
                "Flavors:",
                self.flavors,
                "Glass types:",
                self.glass_types,
                "Count:",
                self.drink_count,
            )
            holder = BarkeepelagoDrinkHolder(
                api_key=self.api_key,
                query=self.query,
                flavors=self.flavors,
                glass_types=self.glass_types,
                include_ingredients=self.include_ingredients,
                exclude_ingredients=self.exclude_ingredients,
                diet=self.diet,
                max_alcohol_percent=self.max_alcohol_percent,
                max_caffeine=self.max_caffeine,
                drink_count=self.drink_count,
                prefer_cocktaildb=self.prefer_cocktaildb,
                use_random_sort=self.use_random_sort,
                hard_fail_on_api_errors=self.hard_fail_on_api_errors,
                use_cocktaildb_fallback=self.use_cocktaildb_fallback,
                ignore_cache=self.ignore_cache,
            )
            drinks_dict = holder.get_drinks()
            print("[Barkeep-elago] Drinks loaded.")
            self.drink_list = list(drinks_dict.values())

        if not getattr(self, "drink_list", []):
            print("[Barkeep-elago] No drinks returned, generating fallback objective")
            game_objective_templates = [
                GameObjectiveTemplate(
                    label="Mix a custom drink with ingredients you already have.",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                ),
            ]
        else:
            print("[Barkeep-elago] Generating objectives...")
            game_objective_templates = [
                GameObjectiveTemplate(
                    label="Mix DRINK",
                    data={
                        "DRINK": (self.drink_list, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                ),
            ]

        print("[Barkeep-elago] Objectives generated.")
        return game_objective_templates

    @property
    def api_key(self) -> str:
        return self.archipelago_options.barkeepelago_api_key.value

    @property
    def query(self) -> str:
        return self.archipelago_options.barkeepelago_query.value

    @property
    def flavors(self) -> List[str]:
        return self.archipelago_options.barkeepelago_flavors.value

    @property
    def glass_types(self) -> List[str]:
        return self.archipelago_options.barkeepelago_glass_types.value

    @property
    def include_ingredients(self) -> List[str]:
        return self.archipelago_options.barkeepelago_include_ingredients.value

    @property
    def exclude_ingredients(self) -> List[str]:
        return self.archipelago_options.barkeepelago_exclude_ingredients.value

    @property
    def diet(self) -> str:
        return self.archipelago_options.barkeepelago_diet.value

    @property
    def max_alcohol_percent(self) -> str:
        return self.archipelago_options.barkeepelago_max_alcohol_percent.value

    @property
    def max_caffeine(self) -> str:
        return self.archipelago_options.barkeepelago_max_caffeine.value

    @property
    def drink_count(self) -> int:
        return self.archipelago_options.barkeepelago_drink_count.value

    @property
    def prefer_cocktaildb(self) -> bool:
        return bool(self.archipelago_options.barkeepelago_prefer_cocktaildb.value)

    @property
    def use_random_sort(self) -> bool:
        return bool(self.archipelago_options.barkeepelago_use_random_sort.value)

    @property
    def hard_fail_on_api_errors(self) -> bool:
        return bool(self.archipelago_options.barkeepelago_hard_fail_on_api_errors.value)

    @property
    def use_cocktaildb_fallback(self) -> bool:
        return bool(self.archipelago_options.barkeepelago_use_cocktaildb_fallback.value)

    @property
    def ignore_cache(self) -> bool:
        return bool(self.archipelago_options.barkeepelago_ignore_cache.value)


class BarkeepelagoAPIKey(FreeText):
    """
    API key used to access the API League Search Drinks endpoint.
    Get a key at https://apileague.com/apis/search-drinks-api/
    """

    display_name = "Barkeep-elago API Key"
    default = ""


class BarkeepelagoQuery(FreeText):
    """
    Search text for drinks, for example: vodka, coffee, mojito, smoothie.
    """

    display_name = "Barkeep-elago Search Query"
    default = ""


class BarkeepelagoFlavors(OptionList):
    """
    Dominant flavors to require. API interprets this as AND.
    Full valid values: sweet, fruity, bitter, sour, spicy, creamy, herbal,
    salty, refreshing, nutty, citrusy, minty, umami, earthy, floral, smoky,
    savory, tangy, aromatic, dry, bubbly, tart, spiced, rich, chocolatey,
    smooth, tropical, malty.
    """

    display_name = "Barkeep-elago Flavors"
    default = []


class BarkeepelagoGlassTypes(OptionList):
    """
    Allowed glass types. API interprets this as OR.
    Full valid values: Highball Glass, Collins Glass, Cocktail Glass,
    Coffee Mug, Margarita Glass, Coupe Glass, Martini Glass, Shot Glass,
    Wine Glass, Hurricane Glass, Irish Coffee Cup, Balloon Glass, Mason Jar,
    Champagne Flute, Whiskey Glass, Pint Glass, Punch Bowl, Beer Mug,
    Beer Pilsner, Pitcher, Copper Mug, Nick And Nora Glass, Brandy Snifter,
    Cordial Glass, Parfait Glass, Beer Glass, Old-Fashioned Glass,
    Pousse Cafe Glass.
    """

    display_name = "Barkeep-elago Glass Types"
    default = []


class BarkeepelagoIncludeIngredients(OptionList):
    """
    Ingredients that should be included.
    """

    display_name = "Barkeep-elago Include Ingredients"
    default = []


class BarkeepelagoExcludeIngredients(OptionList):
    """
    Ingredients that must be excluded.
    """

    display_name = "Barkeep-elago Exclude Ingredients"
    default = []


class BarkeepelagoDiet(FreeText):
    """
    Optional API League diet filter.
    Valid values: paleo, primal, grain-free, vegan, vegetarian.
    Leave blank to disable this filter.
    """

    display_name = "Barkeep-elago Diet"
    default = ""


class BarkeepelagoMaxAlcoholPercent(FreeText):
    """
    Optional API League filter for maximum alcohol percentage.
    This is the primary alcohol-control option.
    Numeric value, for example: 35
    """

    display_name = "Barkeep-elago Max Alcohol Percent"
    default = ""


class BarkeepelagoMaxCaffeine(FreeText):
    """
    Optional API League filter for maximum caffeine in milligrams.
    This is the primary caffeine-control option.
    Numeric value, for example: 80.9
    """

    display_name = "Barkeep-elago Max Caffeine"
    default = ""


class BarkeepelagoDrinkCount(NamedRange):
    """
    Target size of drink pool used for objective selection.
    The module fetches in batches and builds up to this many unique results.
    """

    display_name = "Barkeep-elago Drink Count"
    default = 50
    range_start = 1
    range_end = 50


class BarkeepelagoPreferCocktailDb(Toggle):
    """
    If enabled, use TheCocktailDB as the primary source.
    If CocktailDB returns no drinks or errors, API League can still be used as fallback.
    """

    display_name = "Barkeep-elago Prefer CocktailDB"
    default = False


class BarkeepelagoUseRandomSort(Toggle):
    """
    If enabled, use API sort=random and repeatedly sample to build a varied pool.
    If disabled, use deterministic pagination to minimize API token usage.
    """

    display_name = "Barkeep-elago Use Random API Sort"
    default = False


class BarkeepelagoHardFailOnApiErrors(Toggle):
    """
    If enabled, auth/quota errors from API League (missing key, 401, 402)
    raise an error. If disabled, the module soft-falls back.
    """

    display_name = "Barkeep-elago Hard Fail On API Errors"
    default = False


class BarkeepelagoUseCocktailDbFallback(Toggle):
    """
    If enabled, auth/quota errors from API League (or missing API key) will
    attempt TheCocktailDB fallback. If disabled, soft mode returns no drinks
    and the game uses the generic objective.
    """

    display_name = "Barkeep-elago Use CocktailDB Fallback"
    default = True


class BarkeepelagoIgnoreCache(Toggle):
    """
    If enabled, always fetch fresh drink results instead of using cached data.
    """

    display_name = "Barkeep-elago Ignore Cache"
    default = False


class BarkeepelagoDrinkHolder:
    _drink_cache: Dict[Tuple[object, ...], Dict[int, str]] = {}

    def __init__(
        self,
        api_key: str,
        query: str,
        flavors: List[str],
        glass_types: List[str],
        include_ingredients: List[str],
        exclude_ingredients: List[str],
        diet: str,
        max_alcohol_percent: str,
        max_caffeine: str,
        drink_count: int,
        prefer_cocktaildb: bool,
        use_random_sort: bool,
        hard_fail_on_api_errors: bool,
        use_cocktaildb_fallback: bool,
        ignore_cache: bool,
    ):
        self.api_key = api_key
        self.query = query
        self.flavors = flavors
        self.glass_types = glass_types
        self.include_ingredients = include_ingredients
        self.exclude_ingredients = exclude_ingredients
        self.diet = diet
        self.max_alcohol_percent = max_alcohol_percent
        self.max_caffeine = max_caffeine
        self.drink_count = drink_count
        self.prefer_cocktaildb = prefer_cocktaildb
        self.use_random_sort = use_random_sort
        self.hard_fail_on_api_errors = hard_fail_on_api_errors
        self.use_cocktaildb_fallback = use_cocktaildb_fallback
        self.ignore_cache = ignore_cache

    def get_drinks(self) -> Dict[int, str]:
        normalized_flavors = self._normalize_flavors(self.flavors)
        normalized_glass_types = self._normalize_glass_types(self.glass_types)
        normalized_diet = self._normalize_diet(self.diet)
        normalized_max_alcohol_percent = self._normalize_number(self.max_alcohol_percent, "max-alcohol-percent")
        normalized_max_caffeine = self._normalize_number(self.max_caffeine, "max-caffeine")

        cache_key = (
            self.api_key,
            self.query.strip().lower(),
            tuple(sorted(normalized_flavors)),
            tuple(sorted(normalized_glass_types)),
            tuple(sorted(v.strip().lower() for v in self.include_ingredients if v.strip())),
            tuple(sorted(v.strip().lower() for v in self.exclude_ingredients if v.strip())),
            normalized_diet,
            normalized_max_alcohol_percent,
            normalized_max_caffeine,
            self.drink_count,
            self.prefer_cocktaildb,
            self.use_random_sort,
            self.hard_fail_on_api_errors,
            self.use_cocktaildb_fallback,
        )

        if not self.ignore_cache and cache_key in BarkeepelagoDrinkHolder._drink_cache:
            print("[Barkeep-elago] Using cached drinks...")
            return BarkeepelagoDrinkHolder._drink_cache[cache_key]

        if self.prefer_cocktaildb:
            try:
                drinks_dict = self._get_drinks_from_cocktaildb()
            except Exception as exc:
                print(f"[Barkeep-elago] CocktailDB primary source failed: {exc}")
                drinks_dict = {}

            if drinks_dict:
                BarkeepelagoDrinkHolder._drink_cache[cache_key] = drinks_dict
                return drinks_dict

            print("[Barkeep-elago] CocktailDB returned no drinks, trying API League.")

        if not self.api_key:
            if self.use_cocktaildb_fallback:
                print("[Barkeep-elago] No API key provided, using TheCocktailDB fallback.")
                drinks_dict = self._get_drinks_from_cocktaildb()
                BarkeepelagoDrinkHolder._drink_cache[cache_key] = drinks_dict
                return drinks_dict
            if self.hard_fail_on_api_errors:
                raise RuntimeError("[Barkeep-elago] API key is required. Get one at https://apileague.com/apis/search-drinks-api/")
            print("[Barkeep-elago] No API key provided and fallback is disabled. Returning no drinks.")
            BarkeepelagoDrinkHolder._drink_cache[cache_key] = {}
            return {}

        drinks_dict = self._get_drinks_from_apileague(
            normalized_flavors=normalized_flavors,
            normalized_glass_types=normalized_glass_types,
            normalized_diet=normalized_diet,
            normalized_max_alcohol_percent=normalized_max_alcohol_percent,
            normalized_max_caffeine=normalized_max_caffeine,
        )

        BarkeepelagoDrinkHolder._drink_cache[cache_key] = drinks_dict
        return drinks_dict

    def _get_drinks_from_apileague(
        self,
        normalized_flavors: List[str],
        normalized_glass_types: List[str],
        normalized_diet: str,
        normalized_max_alcohol_percent: str,
        normalized_max_caffeine: str,
    ) -> Dict[int, str]:
        print("[Barkeep-elago] Fetching drinks from API League...")
        params: Dict[str, str | int] = {}

        if self.query.strip():
            params["query"] = self.query.strip()
        if normalized_flavors:
            params["flavors"] = ",".join(normalized_flavors)
        if normalized_glass_types:
            params["glass-types"] = ",".join(normalized_glass_types)

        include_ingredients = self._normalize_list_values(self.include_ingredients)
        exclude_ingredients = self._normalize_list_values(self.exclude_ingredients)
        if include_ingredients:
            params["include-ingredients"] = ",".join(include_ingredients)
        if exclude_ingredients:
            params["exclude-ingredients"] = ",".join(exclude_ingredients)
        if normalized_diet:
            params["diet"] = normalized_diet
        if normalized_max_alcohol_percent:
            params["max-alcohol-percent"] = normalized_max_alcohol_percent
        if normalized_max_caffeine:
            params["max-caffeine"] = normalized_max_caffeine
        params["api-key"] = self.api_key

        target_count = max(1, min(self.drink_count, 50))
        drinks_by_id: Dict[int, str] = {}
        total_available: int | None = None
        if self.use_random_sort:
            random_params = dict(params)
            random_params["sort"] = "random"
            random_params["number"] = 10  # API maximum per request
            random_params["offset"] = 0   # Offset is not meaningful with random sort

            low_yield_streak = 0
            min_new_per_batch = 3  # Fewer than this new drinks in a batch is considered low yield

            for _ in range(10):  # Up to 10 attempts to fill the pool
                if len(drinks_by_id) >= target_count:
                    break
                if total_available is not None and len(drinks_by_id) >= total_available:
                    break
                if low_yield_streak >= 2:
                    break

                response = requests.get(
                    "https://api.apileague.com/search-drinks",
                    params=random_params,
                    timeout=30,
                )
                if response.status_code != 200:
                    if response.status_code in (401, 402):
                        if drinks_by_id:
                            print(
                                f"[Barkeep-elago] API auth/quota error ({response.status_code}). "
                                f"Using {len(drinks_by_id)} drinks collected so far."
                            )
                            break
                        if self.use_cocktaildb_fallback:
                            print(
                                f"[Barkeep-elago] API auth/quota error ({response.status_code}) before any drinks "
                                "were returned. Trying TheCocktailDB fallback."
                            )
                            return self._get_drinks_from_cocktaildb()
                        if self.hard_fail_on_api_errors:
                            raise RuntimeError(f"[Barkeep-elago] API League returned {response.status_code}")
                        print(
                            f"[Barkeep-elago] API auth/quota error ({response.status_code}) before any drinks were returned. "
                            "Falling back to a generic objective."
                        )
                        return {}
                    raise RuntimeError(f"[Barkeep-elago] API League returned {response.status_code}")

                payload = response.json()

                if total_available is None:
                    total_available = int(payload.get("total_results", 0) or 0)
                    if total_available == 0:
                        break

                drinks = payload.get("drinks", [])
                if not drinks:
                    break

                added_this_batch = 0
                for drink in drinks:
                    drink_id = int(drink.get("id", 0) or 0)
                    if drink_id <= 0 or drink_id in drinks_by_id:
                        continue
                    drinks_by_id[drink_id] = (
                        f"{drink.get('title', 'Unknown Drink')}"
                        f" | {drink.get('credits', {}).get('source_url', 'https://apileague.com/apis/search-drinks-api/')}"
                    )
                    added_this_batch += 1
                    if len(drinks_by_id) >= target_count:
                        break

                if added_this_batch < min_new_per_batch:
                    low_yield_streak += 1
                else:
                    low_yield_streak = 0
        else:
            current_offset = 0
            while len(drinks_by_id) < target_count:
                if total_available is not None and current_offset >= total_available:
                    break

                page_params = dict(params)
                page_params["number"] = min(10, target_count - len(drinks_by_id))
                page_params["offset"] = current_offset

                response = requests.get(
                    "https://api.apileague.com/search-drinks",
                    params=page_params,
                    timeout=30,
                )
                if response.status_code != 200:
                    if response.status_code in (401, 402):
                        if drinks_by_id:
                            print(
                                f"[Barkeep-elago] API auth/quota error ({response.status_code}). "
                                f"Using {len(drinks_by_id)} drinks collected so far."
                            )
                            break
                        if self.use_cocktaildb_fallback:
                            print(
                                f"[Barkeep-elago] API auth/quota error ({response.status_code}) before any drinks "
                                "were returned. Trying TheCocktailDB fallback."
                            )
                            return self._get_drinks_from_cocktaildb()
                        if self.hard_fail_on_api_errors:
                            raise RuntimeError(f"[Barkeep-elago] API League returned {response.status_code}")
                        print(
                            f"[Barkeep-elago] API auth/quota error ({response.status_code}) before any drinks were returned. "
                            "Falling back to a generic objective."
                        )
                        return {}
                    raise RuntimeError(f"[Barkeep-elago] API League returned {response.status_code}")

                payload = response.json()

                if total_available is None:
                    total_available = int(payload.get("total_results", 0) or 0)
                    if total_available == 0:
                        break

                drinks = payload.get("drinks", [])
                if not drinks:
                    break

                for drink in drinks:
                    drink_id = int(drink.get("id", 0) or 0)
                    if drink_id <= 0 or drink_id in drinks_by_id:
                        continue
                    drinks_by_id[drink_id] = (
                        f"{drink.get('title', 'Unknown Drink')}"
                        f" | {drink.get('credits', {}).get('source_url', 'https://apileague.com/apis/search-drinks-api/')}"
                    )
                    if len(drinks_by_id) >= target_count:
                        break

                current_offset += 10

        if len(drinks_by_id) < target_count:
            available_str = str(total_available) if total_available is not None else "unknown"
            print(
                f"[Barkeep-elago] Warning: only {len(drinks_by_id)} unique drinks available "
                f"for this query (API total: {available_str}, requested: {target_count})."
            )
        print(f"[Barkeep-elago] Received {len(drinks_by_id)} drinks from API League.")
        return drinks_by_id

    def _get_drinks_from_cocktaildb(self) -> Dict[int, str]:
        print("[Barkeep-elago] Fetching drinks from TheCocktailDB...")
        drinks: List[Dict[str, str]] = []

        if self.query.strip():
            response = requests.get(
                "https://www.thecocktaildb.com/api/json/v1/1/search.php",
                params={"s": self.query.strip()},
                timeout=30,
            )
            if response.status_code != 200:
                raise RuntimeError(f"[Barkeep-elago] TheCocktailDB returned {response.status_code}")
            drinks = (response.json().get("drinks") or [])[: max(1, min(self.drink_count, 50))]
        else:
            seen_ids = set()
            target_count = max(1, min(self.drink_count, 50))
            for _ in range(target_count * 3):
                if len(drinks) >= target_count:
                    break
                response = requests.get(
                    "https://www.thecocktaildb.com/api/json/v1/1/random.php",
                    timeout=30,
                )
                if response.status_code != 200:
                    raise RuntimeError(f"[Barkeep-elago] TheCocktailDB returned {response.status_code}")
                random_drinks = response.json().get("drinks") or []
                if not random_drinks:
                    continue
                drink = random_drinks[0]
                drink_id = drink.get("idDrink")
                if drink_id and drink_id in seen_ids:
                    continue
                if drink_id:
                    seen_ids.add(drink_id)
                drinks.append(drink)

        print(f"[Barkeep-elago] Received {len(drinks)} drinks from TheCocktailDB.")
        return {
            int(drink.get("idDrink") or index): (
                f"{drink.get('strDrink', 'Unknown Drink')}"
                f" | https://www.thecocktaildb.com/drink/{drink.get('idDrink', '')}"
            )
            for index, drink in enumerate(drinks)
        }

    @staticmethod
    def _normalize_flavors(flavors: List[str]) -> List[str]:
        valid = set(VALID_FLAVORS)
        seen = set()
        normalized = []
        for flavor in flavors:
            value = flavor.strip().lower()
            if value in valid and value not in seen:
                seen.add(value)
                normalized.append(value)
            elif value:
                print(f"[Barkeep-elago] Ignoring unknown flavor '{flavor}'.")
        return normalized

    @staticmethod
    def _normalize_glass_types(glass_types: List[str]) -> List[str]:
        canonical = {value.lower(): value for value in VALID_GLASS_TYPES}
        seen = set()
        normalized = []
        for glass_type in glass_types:
            lookup = glass_type.strip().lower()
            if lookup in canonical:
                value = canonical[lookup]
                if value not in seen:
                    seen.add(value)
                    normalized.append(value)
            elif lookup:
                print(f"[Barkeep-elago] Ignoring unknown glass type '{glass_type}'.")
        return normalized

    @staticmethod
    def _normalize_diet(diet: str) -> str:
        value = diet.strip().lower()
        if not value:
            return ""
        if value not in VALID_DIETS:
            print(f"[Barkeep-elago] Ignoring unknown diet '{diet}'.")
            return ""
        return value

    @staticmethod
    def _normalize_number(value: str, parameter_name: str) -> str:
        text = value.strip()
        if not text:
            return ""
        try:
            number = float(text)
        except ValueError:
            print(f"[Barkeep-elago] Ignoring invalid numeric value '{value}' for {parameter_name}.")
            return ""
        if number.is_integer():
            return str(int(number))
        return str(number)

    @staticmethod
    def _normalize_list_values(values: List[str]) -> List[str]:
        seen = set()
        normalized = []
        for value in values:
            item = value.strip()
            if not item:
                continue
            key = item.lower()
            if key in seen:
                continue
            seen.add(key)
            normalized.append(item)
        return normalized
