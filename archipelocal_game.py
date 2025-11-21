from __future__ import annotations

import functools
import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover - keep optional for offline option generation
    requests = None  # type: ignore

from os import environ

from Options import FreeText, NamedRange, OptionSet, Range, Toggle  # type: ignore
from ..game import Game  # type: ignore
from ..game_objective_template import GameObjectiveTemplate  # type: ignore
from ..enums import KeymastersKeepGamePlatforms  # type: ignore


# -- Curated default category shortlist (Geoapify taxonomy) --
# Full taxonomy: https://apidocs.geoapify.com/docs/places/#categories
DEFAULT_GEOAPIFY_CATEGORIES: Tuple[str, ...] = (
    
    # Food & drink (catering)
    "catering.restaurant",
    "catering.cafe",
    "catering.fast_food",
    "catering.pub",
    "catering.bar",
    "catering.ice_cream",
    "catering.food_court",
    
    # Food shopping
    "commercial.food_and_drink.bakery",
    "commercial.food_and_drink.ice_cream",
    "commercial.food_and_drink.chocolate",

    # Leisure & parks
    "leisure.park",
    "leisure.park.garden",
    "leisure.playground",
    "leisure.spa",
    "leisure.picnic",

    # Tourism & attractions
    "tourism.attraction",
    "tourism.sights",
    "tourism.attraction.viewpoint",
    "tourism.information",
    
    # Entertainment & culture
    "entertainment.museum",
    "entertainment.cinema",
    "entertainment.culture.theatre",
    "entertainment.culture.gallery",
    "entertainment.zoo",
    "entertainment.theme_park",
    "entertainment.aquarium",
    "entertainment.activity_park",
    "entertainment.bowling_alley",
    
    # NOTE: If you're not finding results for museums or bowling alleys, try these alternatives:
    # - For museums: Try "tourism.museum" or just "tourism.attraction"
    # - For bowling: Try "sport.bowling" or "leisure.bowling_alley"
    # Geoapify's taxonomy can vary by region and data source.

    # Sports & wellness
    "sport.fitness",
    "sport.stadium",
    "sport.swimming_pool",
    "sport.sports_centre",

    # Natural features
    "natural.mountain",
    "natural.forest",
    "natural.water",
    "natural.sand",
    "beach",
    "natural.protected_area",
    "national_park",

    # Man-made structures
    "man_made.bridge",
    "man_made.tower",
    "man_made.lighthouse",
    "man_made.pier",
    "man_made.windmill",
    "man_made.watermill",

    # Shopping & errands
    "commercial.supermarket",
    "commercial.shopping_mall",
    "commercial.convenience",
    "commercial.books",

    # Services & community
    "education.library",

    # Lodging & travel
    "accommodation.hotel",
    "public_transport",
)

# Known category fallbacks for Geoapify taxonomy mismatches
CATEGORY_FALLBACKS: Dict[str, str] = {
    # Legacy fallbacks for old/deprecated category names that users might have in configs
    "sport.gym": "sport.fitness",
    "catering.bakery": "commercial.food_and_drink.bakery",
    "commercial.bakery": "commercial.food_and_drink.bakery",
    "commercial.mall": "commercial.shopping_mall",
    "amenity.library": "education.library",
    "amenity.pharmacy": "healthcare.pharmacy",
    "amenity.post_office": "service.post.office",
    "service.post_office": "service.post.office",
    "transport.public_transport": "public_transport",
    "transport.public_transport_stop": "public_transport",
    "tourism.gallery": "entertainment.culture.gallery",
    "entertainment.theatre": "entertainment.culture.theatre",
    "leisure.garden": "leisure.park.garden",
    "picnic": "leisure.picnic",
}

# Friendly display overrides for specific categories
FRIENDLY_CATEGORY_OVERRIDES: Dict[str, str] = {
    "commercial.convenience": "Convenience store",
    "commercial.shopping_mall": "Shopping mall",
    "commercial.food_and_drink.bakery": "Bakery",
    "commercial.food_and_drink.ice_cream": "Ice cream shop",
    "commercial.food_and_drink.chocolate": "Chocolate shop",
    "commercial.books": "Bookstore",
    "service.post.office": "Post office",
    "service.post": "Post",
    "healthcare.pharmacy": "Pharmacy",
    "education.library": "Library",
    "public_transport": "Public transport",
    "tourism.sights": "Sight",
    "tourism.attraction": "Attraction",
    "tourism.attraction.viewpoint": "Viewpoint",
    "tourism.information": "Tourist information",
    "entertainment.theme_park": "Theme park",
    "entertainment.culture.theatre": "Theatre",
    "entertainment.culture.gallery": "Gallery",
    "entertainment.aquarium": "Aquarium",
    "catering.fast_food": "Fast food",
    "catering.ice_cream": "Ice cream",
    "catering.food_court": "Food court",
    "sport.fitness": "Fitness center",
    "sport.stadium": "Stadium",
    "sport.sports_centre": "Sports centre",
    "sport.swimming_pool": "Swimming pool",
    "natural.mountain": "Mountain",
    "natural.forest": "Forest",
    "natural.water": "Water",
    "natural.sand": "Sand/Beach",
    "natural.protected_area": "Protected area",
    "national_park": "National park",
    "beach": "Beach",
    "man_made.bridge": "Bridge",
    "man_made.tower": "Tower",
    "man_made.lighthouse": "Lighthouse",
    "man_made.pier": "Pier",
    "man_made.windmill": "Windmill",
    "man_made.watermill": "Watermill",
    "leisure.park.garden": "Garden",
    "leisure.picnic": "Picnic area",
}

# ----------------------
# Module-level session cache
# ----------------------
# Cache of live suggestions per effective settings bundle so we load once per session
_ARCHIPELOCAL_SESSION_SUGGESTIONS_CACHE: Dict[Tuple[Any, ...], Dict[str, List[Dict[str, Any]]]] = {}
# One-time notice so we don't spam logs when first loading suggestions
_ARCHIPELOCAL_SESSION_PRINTED_LOAD: bool = False
 # Module-level geocode cache to avoid repeated geocoding across instances
_ARCHIPELOCAL_GEOCODE_CACHE: Dict[Tuple[str, str, str, str], Tuple[float, float]] = {}


# =====================
# Options dataclass
# =====================
@dataclass
class ArchipelocalArchipelagoOptions:
    archipelocal_home_address: "ArchipelocalHomeAddress"
    archipelocal_home_latitude: "ArchipelocalHomeLatitude"
    archipelocal_home_longitude: "ArchipelocalHomeLongitude"
    archipelocal_allowed_categories: "ArchipelocalAllowedCategories"
    archipelocal_conditions: "ArchipelocalConditions"
    archipelocal_named_locations_only: "ArchipelocalNamedLocationsOnly"
    archipelocal_distance_unit: "ArchipelocalDistanceUnit"
    archipelocal_global_max_distance: "ArchipelocalGlobalMaxDistance"
    archipelocal_per_category_max_distance: "ArchipelocalPerCategoryMaxDistance"
    archipelocal_geoapify_api_key: "ArchipelocalGeoapifyApiKey"
    archipelocal_max_results_per_category: "ArchipelocalMaxResultsPerCategory"
    archipelocal_per_category_max_results: "ArchipelocalPerCategoryMaxResults"
    archipelocal_enable_live_suggestions: "ArchipelocalEnableLiveSuggestions"
    archipelocal_geocode_country_codes: "ArchipelocalGeocodeCountryCodes"
    archipelocal_suggestion_strategy: "ArchipelocalSuggestionStrategy"


class ArchipelocalGame(Game):
    name = "Archipelocal"
    platform = KeymastersKeepGamePlatforms.META

    is_adult_only_or_unrated = False

    options_cls = ArchipelocalArchipelagoOptions

    # --------- Public choice providers used by templates ---------
    def allowed_categories(self) -> List[str]:
        opts = getattr(self, "archipelago_options", None)
        if not opts:
            return list(DEFAULT_GEOAPIFY_CATEGORIES)
        try:
            values = list(opts.archipelocal_allowed_categories.value or [])
            return values or list(DEFAULT_GEOAPIFY_CATEGORIES)
        except Exception:
            return list(DEFAULT_GEOAPIFY_CATEGORIES)

    def allowed_categories_friendly(self) -> List[str]:
        """Return friendly human-readable category labels for display in generic objectives.

        This does not affect API queries, which continue to use the raw taxonomy codes
        via allowed_categories().
        """
        codes = self.allowed_categories()
        out: List[str] = []
        seen = set()
        for c in codes:
            label = self._friendly_category_label(c)
            if label not in seen:
                seen.add(label)
                out.append(label)
        return out

    def nth_choices(self) -> List[str]:
        return [self._ordinal(n) for n in range(1, 11)]

    def _normalize_category(self, category: str) -> str:
        mapped = CATEGORY_FALLBACKS.get(category, category)
        if mapped != category:
            print(f"[Archipelocal] Using fallback category '{mapped}' for '{category}'.")
        return mapped

    def _friendly_category_label(self, category: str) -> str:
        """Return a human-friendly label for a Geoapify category string.

        Examples:
        - 'tourism.attraction' -> 'Attraction'
        - 'catering.fast_food' -> 'Fast food'
        - 'transport.public_transport' -> 'Public transport'
        """
        # Specific overrides first
        if category in FRIENDLY_CATEGORY_OVERRIDES:
            return FRIENDLY_CATEGORY_OVERRIDES[category]
        last = category.split(".")[-1] if category else ""
        last = last.replace("_", " ")
        if not last:
            return "Place"
        return last.capitalize()

    # --------- Objective generation ---------
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        """
        Generate objectives about visiting real-world places near the configured home location.

        We avoid mandatory network calls when generating objectives; actual place lookup is left to the player
        (or can be surfaced by enabling live suggestions). The configured max distances constrain what "near" means.
        """
        cats = self.allowed_categories()
        if not cats:
            return []

        # One-time helpful summary (not spammed) if live suggestions are enabled but API key is missing
        if self._suggestions_enabled() and not self._get_api_key():
            print("[Archipelocal] Live suggestions enabled but no Geoapify API key was found. Set Archipelocal option or GEOAPIFY_API_KEY.")

        templates: List[GameObjectiveTemplate] = []

        # Helper to build generic category-based objectives with adjustable weights
        def add_generic_objectives(cat_w: int = 2, nth_w: int = 3, rand_w: int = 1) -> None:
            templates.append(
                GameObjectiveTemplate(
                    label="Visit a CATEGORY near your home (within your max distance)",
                    data={"CATEGORY": (lambda: self.allowed_categories_friendly(), 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=cat_w,
                )
            )
            templates.append(
                GameObjectiveTemplate(
                    label="Visit your NTH-closest CATEGORY near your home (within your max distance)",
                    data={
                        "CATEGORY": (lambda: self.allowed_categories_friendly(), 1),
                        "NTH": (lambda: self.nth_choices(), 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=nth_w,
                )
            )
            if len(cats) >= 2:
                templates.append(
                    GameObjectiveTemplate(
                        label="Visit a random CATEGORY near your home (within your max distance)",
                        data={"CATEGORY": (lambda: self.allowed_categories_friendly(), 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=rand_w,
                    )
                )

        # Strategy handling (lazy-load suggestions only when the PLACE token is actually used)
        strategy = self._suggestion_strategy()
        
        # If only_concrete is selected, never emit generic objectives regardless of suggestions being enabled
        if strategy == "only_concrete":
            if self._suggestions_enabled():
                # Add PLACE objective only
                templates.append(
                    GameObjectiveTemplate(
                        label="Visit PLACE",
                        data={"PLACE": (lambda: self._place_name_choices(), 1)},
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=3,
                    )
                )
            # Return templates (could be empty if suggestions disabled, or just PLACE if enabled)
            return templates
        
        # For prefer_concrete and random_mix strategies, add PLACE if suggestions enabled
        if self._suggestions_enabled():
            place_weight = 4 if strategy == "prefer_concrete" else 2
            templates.append(
                GameObjectiveTemplate(
                    label="Visit PLACE",
                    data={"PLACE": (lambda: self._place_name_choices(), 1)},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=place_weight,
                )
            )
            
            if strategy == "prefer_concrete":
                # Include generic with lower weights to bias towards PLACE
                add_generic_objectives(cat_w=1, nth_w=2, rand_w=1)
            else:  # random_mix
                # Include generic with normal weights to get a balanced mix
                add_generic_objectives(cat_w=2, nth_w=3, rand_w=1)
            return templates

        # Generic fallback when suggestions are disabled and strategy is not only_concrete
        add_generic_objectives(cat_w=2, nth_w=3, rand_w=1)
        return templates

    def _place_name_choices(self) -> List[str]:
        """Lazily compute PLACE token choices using cached live suggestions.

        This is invoked only when an objective concretely needs PLACE options,
        avoiding API calls during template generation for unused games.
        """
        examples = self._live_suggestions()
        if not examples:
            return []
        seen: Dict[str, bool] = {}
        out_list: List[str] = []
        for _, entries in examples.items():
            for e in entries:
                disp = (e.get("display_name") or "").strip()
                if not disp or disp in seen:
                    continue
                seen[disp] = True
                out_list.append(disp)
        return out_list

    # --------- Helpers ---------
    def _ordinal(self, n: int) -> str:
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

    def _get_api_key(self) -> str:
        opts = getattr(self, "archipelago_options", None)
        key = ""
        if opts is not None:
            try:
                key = str(getattr(opts.archipelocal_geoapify_api_key, "value", "") or "").strip()
            except Exception:
                key = ""
        if not key:
            key = (environ.get("GEOAPIFY_API_KEY") or "").strip()
        return key

    def _get_geocode_country_codes(self) -> str:
        """Return pipe-separated ISO country codes (e.g., 'gb|ie'), or empty for no filter."""
        opts = getattr(self, "archipelago_options", None)
        if not opts:
            return ""
        try:
            raw = str(getattr(opts.archipelocal_geocode_country_codes, "value", "") or "").strip()
        except Exception:
            raw = ""
        # sanitize: keep letters and pipes, lowercase
        cleaned = "|".join([seg.strip().lower() for seg in raw.split("|") if seg.strip()])
        return cleaned

    def _get_unit(self) -> str:
        opts = getattr(self, "archipelago_options", None)
        unit = "km"
        if opts is not None:
            try:
                chosen = str(getattr(opts.archipelocal_distance_unit, "value", "km") or "km").lower()
                if chosen in ("km", "mi"):
                    unit = chosen
            except Exception:
                pass
        return unit

    def _get_conditions(self) -> List[str]:
        """Return list of Geoapify conditions to apply to place searches.
        
        The 'named' condition is included by default (when archipelocal_named_locations_only is True)
        to ensure all results have proper names.
        
        Examples: wheelchair, vegan, kosher, internet_access, dogs, no_fee
        Full list: https://apidocs.geoapify.com/docs/places/#conditions
        """
        opts = getattr(self, "archipelago_options", None)
        conditions = []
        
        # Check if 'named' condition should be included (default: True)
        require_named = True
        if opts:
            try:
                require_named = bool(getattr(opts.archipelocal_named_locations_only, "value", True))
            except Exception:
                require_named = True
        
        if require_named:
            conditions.append("named")
        
        if opts:
            try:
                conditions_set = getattr(opts.archipelocal_conditions, "value", set())
                if isinstance(conditions_set, set):
                    user_conditions = [str(c).strip() for c in conditions_set if str(c).strip()]
                    # Add user conditions, avoiding duplicates
                    for cond in user_conditions:
                        if cond not in conditions:
                            conditions.append(cond)
            except Exception:
                pass
        
        return sorted(conditions)

    def _suggestion_strategy(self) -> str:
        opts = getattr(self, "archipelago_options", None)
        val = "prefer_concrete"
        if opts is not None:
            try:
                # OptionSet.value is a set, not a string - take first element if available
                raw_set = getattr(opts.archipelocal_suggestion_strategy, "value", set())
                if isinstance(raw_set, set) and raw_set:
                    raw = str(next(iter(raw_set))).strip()
                    if raw in ("only_concrete", "prefer_concrete", "random_mix"):
                        val = raw
                elif isinstance(raw_set, str):
                    # Fallback if it's somehow a string
                    raw = raw_set.strip()
                    if raw in ("only_concrete", "prefer_concrete", "random_mix"):
                        val = raw
            except Exception:
                pass
        return val

    @functools.lru_cache(maxsize=None)
    def _get_home_coords(self) -> Optional[Tuple[float, float]]:
        opts = getattr(self, "archipelago_options", None)
        lat_txt = lon_txt = ""
        if opts is not None:
            try:
                lat_txt = str(getattr(opts.archipelocal_home_latitude, "value", "") or "").strip()
                lon_txt = str(getattr(opts.archipelocal_home_longitude, "value", "") or "").strip()
            except Exception:
                lat_txt = lon_txt = ""

        if lat_txt and lon_txt:
            try:
                return float(lat_txt), float(lon_txt)
            except Exception:
                pass

        # Attempt geocoding if address is provided
        addr = ""
        if opts is not None:
            try:
                addr = str(getattr(opts.archipelocal_home_address, "value", "") or "").strip()
            except Exception:
                addr = ""
        if not addr:
            return None
        key = self._get_api_key()
        if not key or requests is None:
            return None
        # Use module-level cache to avoid repeated geocoding across instances
        cc = self._get_geocode_country_codes()
        cache_key = (lat_txt, lon_txt, addr, cc)
        global _ARCHIPELOCAL_GEOCODE_CACHE
        if cache_key in _ARCHIPELOCAL_GEOCODE_CACHE:
            return _ARCHIPELOCAL_GEOCODE_CACHE[cache_key]
        
        print(f"[Archipelocal] Geocoding address: '{addr}' ...")
        params = {"text": addr, "format": "json", "apiKey": key}
        if cc:
            params["filter"] = f"countrycode:{cc}"
        
        # Retry logic with exponential backoff for timeouts
        max_retries = 3
        base_timeout = 30  # Increased from 15s since queries consistently need more time
        import time
        
        for attempt in range(max_retries):
            try:
                timeout = base_timeout + (base_timeout * attempt)  # 30s, 60s, 90s
                if attempt > 0:
                    print(f"[Archipelocal] Geocoding retry {attempt}/{max_retries - 1} with {timeout}s timeout...")
                
                resp = requests.get(
                    "https://api.geoapify.com/v1/geocode/search",
                    params=params,
                    timeout=timeout,
                )
                
                if resp.status_code != 200:
                    print(f"[Archipelocal] Geocoding failed with HTTP {resp.status_code}.")
                    try:
                        error_body = resp.text[:500]  # First 500 chars of error response
                        print(f"[Archipelocal] Response body: {error_body}")
                    except Exception:
                        pass
                    return None
                
                # Success - break out of retry loop
                break
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    wait_time = 0.5 * (2 ** attempt)  # 0.5s, 1s, 2s
                    print(f"[Archipelocal] Geocoding timeout, waiting {wait_time:.1f}s before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"[Archipelocal] Geocoding timeout after {max_retries} attempts, skipping.")
                    return None
            except Exception as e:
                print(f"[Archipelocal] Geocoding error occurred: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
                return None
        
        # Parse the successful response
        try:
            js = resp.json()
            results = js.get("results") or []
            if not results:
                print("[Archipelocal] Geocoding returned no results.")
                return None
            best = results[0]
            lat_val = float(best.get("lat"))
            lon_val = float(best.get("lon"))
            country = best.get("country_code") or best.get("country") or "?"
            print(f"[Archipelocal] Geocoded to lat={lat_val:.5f}, lon={lon_val:.5f} (country={country}).")
            _ARCHIPELOCAL_GEOCODE_CACHE[cache_key] = (lat_val, lon_val)
            return lat_val, lon_val
        except Exception as e:
            print(f"[Archipelocal] Geocoding parse error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _get_global_max_distance_m(self) -> Optional[int]:
        opts = getattr(self, "archipelago_options", None)
        if opts is None:
            # default 5 km
            return 5000
        try:
            raw = int(getattr(opts.archipelocal_global_max_distance, "value", 5))
        except Exception:
            raw = 5
        if raw < 0:
            # no_limit -> cap to 50 km to keep queries reasonable
            raw = 50
        unit = self._get_unit()
        meters_per_unit = 1000 if unit == "km" else 1609
        return raw * meters_per_unit

    def _get_per_category_overrides(self) -> Mapping[str, int]:
        """Return per-category max distance in meters."""
        opts = getattr(self, "archipelago_options", None)
        txt = ""
        if opts is not None:
            try:
                txt = str(getattr(opts.archipelocal_per_category_max_distance, "value", "") or "").strip()
            except Exception:
                txt = ""
        if not txt:
            return {}
        # Expect JSON object {"category": distance_number}
        try:
            data = json.loads(txt)
            if not isinstance(data, dict):
                return {}
            unit = self._get_unit()
            meters_per_unit = 1000 if unit == "km" else 1609
            out: Dict[str, int] = {}
            for k, v in data.items():
                try:
                    d = int(v)
                except Exception:
                    continue
                if d < 0:
                    # Treat negative like no_limit -> cap 50
                    d = 50
                out[str(k)] = d * meters_per_unit
            return out
        except Exception:
            return {}

    def _get_per_category_result_overrides(self) -> Mapping[str, int]:
        """Return per-category max result count (1-100)."""
        opts = getattr(self, "archipelago_options", None)
        txt = ""
        if opts is not None:
            try:
                txt = str(getattr(opts.archipelocal_per_category_max_results, "value", "") or "").strip()
            except Exception:
                txt = ""
        if not txt:
            return {}
        # Expect JSON object {"category": result_count}
        try:
            data = json.loads(txt)
            if not isinstance(data, dict):
                return {}
            out: Dict[str, int] = {}
            for k, v in data.items():
                try:
                    count = int(v)
                    # Clamp to API limits [1, 100]
                    count = max(1, min(100, count))
                    out[str(k)] = count
                except Exception:
                    continue
            return out
        except Exception:
            return {}

    def _radius_for_category_m(self, category: str) -> int:
        overrides = self._get_per_category_overrides()
        if category in overrides:
            return overrides[category]
        global_m = self._get_global_max_distance_m() or 5000
        return global_m

    def _limit_for_category(self, category: str) -> int:
        """Get the result limit for a specific category, respecting per-category overrides."""
        overrides = self._get_per_category_result_overrides()
        if category in overrides:
            return overrides[category]
        # Fall back to global max_results_per_category
        try:
            cfg_limit = int(getattr(self.archipelago_options, "archipelocal_max_results_per_category", 25).value or 25)
        except Exception:
            cfg_limit = 25
        return max(1, min(100, cfg_limit))

    def _suggestions_enabled(self) -> bool:
        opts = getattr(self, "archipelago_options", None)
        enabled = False
        if opts is not None:
            try:
                enabled = bool(getattr(opts.archipelocal_enable_live_suggestions, "value", False))
            except Exception:
                enabled = False
        return enabled

    # ------- Live suggestions (optional) -------
    def _fetch_places(self, lat: float, lon: float, category: str, radius_m: int, limit: int) -> List[Dict[str, Any]]:
        """Fetch places from Geoapify API. Results are cached only if successful."""
        # Check cache first (manual caching to avoid caching failures)
        cache_key = (lat, lon, category, radius_m, limit)
        global _ARCHIPELOCAL_SESSION_SUGGESTIONS_CACHE
        
        # Use a separate cache for individual place fetches
        if not hasattr(self.__class__, '_place_fetch_cache'):
            self.__class__._place_fetch_cache = {}
        
        if cache_key in self.__class__._place_fetch_cache:
            return self.__class__._place_fetch_cache[cache_key]
        
        key = self._get_api_key()
        if not key or requests is None:
            return []
        
        # Console feedback before the call
        unit = self._get_unit()
        radius_disp = (radius_m / 1000.0) if unit == "km" else (radius_m / 1609.344)
        query_cat = self._normalize_category(category)
        conditions = self._get_conditions()
        conditions_str = f" with conditions [{', '.join(conditions)}]" if conditions else ""
        print(f"[Archipelocal] Fetching '{query_cat}'{conditions_str} within {radius_disp:.2f} {unit} around ({lat:.5f}, {lon:.5f}) ...")
        
        # Build request parameters
        params = {
            "categories": query_cat,
            "filter": f"circle:{lon},{lat},{radius_m}",
            "bias": f"proximity:{lon},{lat}",
            "limit": max(1, min(100, int(limit))),
            "apiKey": key,
        }
        
        # Add conditions if specified
        if conditions:
            params["conditions"] = ",".join(conditions)
        
        # Retry logic with exponential backoff for timeouts
        max_retries = 3
        base_timeout = 30  # Increased from 15s since queries consistently need more time
        import time
        
        for attempt in range(max_retries):
            try:
                timeout = base_timeout + (base_timeout * attempt)  # 30s, 60s, 90s
                if attempt > 0:
                    print(f"[Archipelocal] Retry {attempt}/{max_retries - 1} for '{query_cat}' with {timeout}s timeout...")
                
                resp = requests.get(
                    "https://api.geoapify.com/v2/places",
                    params=params,
                    timeout=timeout,
                )
                
                if resp.status_code != 200:
                    print(f"[Archipelocal] Places API HTTP {resp.status_code} for category '{query_cat}'.")
                    try:
                        error_body = resp.text[:500]  # First 500 chars of error response
                        print(f"[Archipelocal] Response body: {error_body}")
                    except Exception:
                        pass
                    return []
                
                # Success - break out of retry loop
                break
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    wait_time = 0.5 * (2 ** attempt)  # 0.5s, 1s, 2s
                    print(f"[Archipelocal] Timeout for '{query_cat}', waiting {wait_time:.1f}s before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"[Archipelocal] Timeout for '{query_cat}' after {max_retries} attempts, skipping.")
                    return []
            except Exception as e:
                print(f"[Archipelocal] Error fetching places for '{query_cat}': {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
                return []
        
        # Parse the successful response
        try:
            js = resp.json() or {}
            feats = (js.get("features") or [])
            
            out: List[Dict[str, Any]] = []
            for f in feats:
                props = f.get("properties") or {}
                geom = f.get("geometry") or {}
                coords = geom.get("coordinates") or []
                feat_lon = None
                feat_lat = None
                try:
                    if isinstance(coords, (list, tuple)) and len(coords) >= 2:
                        feat_lon = float(coords[0])
                        feat_lat = float(coords[1])
                except Exception:
                    feat_lon = feat_lat = None
                name = props.get("name") or props.get("address_line2") or props.get("address_line1")
                dist_m = props.get("distance")  # if present
                addr = props.get("formatted") or props.get("address_line2") or props.get("address_line1")
                out.append({
                    "name": name,
                    "distance_m": dist_m,
                    "address": addr,
                    "lat": feat_lat,
                    "lon": feat_lon,
                    "display_name": self._format_place_display(name, dist_m, query_cat, feat_lat, feat_lon, addr),
                })
            if len(out) == 0:
                print(f"[Archipelocal] ⚠️  Received 0 places for '{query_cat}'.")
                print(f"[Archipelocal] Search parameters: radius={radius_m}m ({radius_disp:.2f} {unit}), limit={limit}")
                if conditions:
                    print(f"[Archipelocal] Active conditions: {', '.join(conditions)}")
                print(f"[Archipelocal] If you verified this category returns results in the API playground with the same")
                print(f"[Archipelocal] coordinates and radius, check if you have restrictive conditions enabled.")
                # Don't cache empty results - might be a transient error
            else:
                print(f"[Archipelocal] Received {len(out)} places for '{query_cat}'.")
                # Cache successful results only
                self.__class__._place_fetch_cache[cache_key] = out
            return out
        except Exception as e:
            print(f"[Archipelocal] Error parsing response for '{query_cat}': {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return []

    def _format_place_display(self, name: Optional[str], distance_m: Optional[float], category: str, lat: Optional[float] = None, lon: Optional[float] = None, address: Optional[str] = None) -> str:
        # Prefer explicit name; else fall back to address; else Unnamed
        base_raw = (name or "").strip()
        addr_raw = (address or "").strip()
        base = base_raw or addr_raw or "Unnamed place"
        unit = self._get_unit()
        cat_label = self._friendly_category_label(category)
        dist_part = ""
        if distance_m is not None:
            if unit == "km":
                d = max(0.0, float(distance_m)) / 1000.0
                dist_part = f"{d:.2f} km"
            else:
                d = max(0.0, float(distance_m)) / 1609.344
                dist_part = f"{d:.2f} mi"
        # Always append coordinates when available for precision
        if lat is not None and lon is not None:
            base = f"{base} @ {lat:.5f}, {lon:.5f}"
        if dist_part:
            return f"{base} – {dist_part} • {cat_label}"
        return f"{base} • {cat_label}"

    def _example_places_all_categories(self, max_per_cat: Optional[int] = None) -> Dict[str, List[Dict[str, Any]]]:
        if not self._get_api_key():
            print("[Archipelocal] No API key set; skipping live suggestions.")
            return {}
        if not self._get_home_coords():
            print("[Archipelocal] No home location configured; skipping live suggestions.")
            return {}
        latlon = self._get_home_coords()
        if not latlon:
            return {}
        lat, lon = latlon
        out: Dict[str, List[Dict[str, Any]]] = {}
        cats = self.allowed_categories()
        # Print a one-time session message when we actually go to fetch
        global _ARCHIPELOCAL_SESSION_PRINTED_LOAD
        if not _ARCHIPELOCAL_SESSION_PRINTED_LOAD:
            print(f"[Archipelocal] Loading live suggestions for {len(cats)} categories...")
            print("[Archipelocal] Powered by Geoapify (https://www.geoapify.com/)")
            _ARCHIPELOCAL_SESSION_PRINTED_LOAD = True
        for cat in cats:
            r = self._radius_for_category_m(cat)
            # Use per-category limit if available, else global, potentially capped by max_per_cat
            cat_limit = self._limit_for_category(cat)
            if max_per_cat is not None:
                cat_limit = min(cat_limit, int(max_per_cat))
            results = self._fetch_places(lat, lon, cat, r, cat_limit)
            if results:
                out[cat] = results
        # One-time session completion message (only if we printed the start message here)
        if _ARCHIPELOCAL_SESSION_PRINTED_LOAD:
            print(f"[Archipelocal] Loaded suggestions for {len(out)} categories.")
        return out

    def _live_suggestions(self, max_per_cat: Optional[int] = None) -> Dict[str, List[Dict[str, Any]]]:
        latlon = self._get_home_coords()
        if not latlon:
            return {}
        cats = tuple(sorted(self.allowed_categories()))
        conditions = tuple(self._get_conditions())
        # Include unit, distance settings, result limits, and conditions in key
        key: Tuple[Any, ...] = (
            latlon,
            cats,
            conditions,
            max_per_cat,
            self._get_unit(),
            self._get_global_max_distance_m(),
            tuple(sorted(self._get_per_category_overrides().items())),
            tuple(sorted(self._get_per_category_result_overrides().items())),
        )
        # Module-level session cache: load once per settings bundle
        global _ARCHIPELOCAL_SESSION_SUGGESTIONS_CACHE
        cached = _ARCHIPELOCAL_SESSION_SUGGESTIONS_CACHE.get(key)
        if isinstance(cached, dict):
            return cached
        data = self._example_places_all_categories(max_per_cat=max_per_cat)
        _ARCHIPELOCAL_SESSION_SUGGESTIONS_CACHE[key] = data
        return data


# =====================
# Options
# =====================
class ArchipelocalHomeAddress(FreeText):
    """
    A human-readable home/base address. Used to geocode coordinates if latitude/longitude are not provided.

    Tip: For privacy, provide a nearby public location (e.g., a park) rather than your exact address.
    """
    display_name = "Archipelocal Home Address (optional)"


class ArchipelocalHomeLatitude(FreeText):
    """
    Home latitude as a decimal number. If set together with longitude, geocoding is skipped.
    """
    display_name = "Archipelocal Home Latitude"


class ArchipelocalHomeLongitude(FreeText):
    """
    Home longitude as a decimal number. If set together with latitude, geocoding is skipped.
    """
    display_name = "Archipelocal Home Longitude"


class ArchipelocalAllowedCategories(OptionSet):
    """
    Geoapify category codes you want to allow. Leave empty to use a curated default shortlist.

    Examples: catering.cafe, leisure.park, entertainment.museum
    """
    display_name = "Archipelocal Allowed Categories"


class ArchipelocalConditions(OptionSet):
    """
    Optional Geoapify conditions to filter places (applies to all categories).
    
    Common examples:
    - wheelchair: Places with wheelchair accessibility
    - vegan: Vegan food options
    - vegan.only: Only vegan food
    - kosher: Kosher food options
    - halal: Halal food options
    - internet_access: Places with internet/WiFi
    - dogs: Dog-friendly places
    - no_fee: Free entry/no fees
    - outdoor_seating: Outdoor seating available
    
    Full list: https://apidocs.geoapify.com/docs/places/#conditions
    """
    display_name = "Archipelocal Conditions (filters)"


class ArchipelocalNamedLocationsOnly(Toggle):
    """
    When enabled, only places with proper names will be returned (using the 'named' condition).
    This filters out unnamed or poorly-labeled locations.
    
    Enabled by default to ensure better quality results.
    """
    display_name = "Archipelocal Named Locations Only"
    default = True


class ArchipelocalDistanceUnit(OptionSet):
    """
    Unit for distances in options and labels (km/mi).
    """
    display_name = "Archipelocal Distance Unit"
    valid_keys = {"km", "mi"}
    default = "km"


class ArchipelocalGlobalMaxDistance(NamedRange):
    """
    Maximum distance for places when no per-category override is set. Use -1 or "no_limit" for an open search
    (internally capped to a reasonable radius of 50 km / 31 mi).
    """
    display_name = "Archipelocal Global Max Distance"
    default = 5
    range_start = -1
    range_end = 200
    special_range_names = {
        "no_limit": -1,
    }


class ArchipelocalPerCategoryMaxDistance(FreeText):
    """
    Optional JSON mapping of per-category max distances overriding the global setting.

    Example:
    {"catering.cafe": 3, "leisure.park": 8}

    Distances use your selected distance unit (km/mi). Negative values are treated as "no_limit" and capped.
    """
    display_name = "Archipelocal Per-Category Max Distance (JSON)"


class ArchipelocalGeoapifyApiKey(FreeText):
    """
    Geoapify API key. If empty, the GEOAPIFY_API_KEY environment variable will be used.
    """
    display_name = "Archipelocal Geoapify API Key"


class ArchipelocalMaxResultsPerCategory(Range):
    """
    Limit the number of results fetched per category when live suggestions are enabled (1-100).
    """
    display_name = "Archipelocal Max Results Per Category"
    default = 20
    range_start = 1
    range_end = 100


class ArchipelocalPerCategoryMaxResults(FreeText):
    """
    Optional JSON mapping of per-category max result counts overriding the global setting.

    Example:
    {"catering.cafe": 10, "leisure.park": 50, "entertainment.museum": 15}

    Result counts are clamped to API limits (1-100).
    """
    display_name = "Archipelocal Per-Category Max Results (JSON)"


class ArchipelocalEnableLiveSuggestions(Toggle):
    """
    When enabled, the module may fetch nearby places from Geoapify to include concrete PLACE suggestions.

    This requires a Geoapify API key and a home location (lat/lon or an address to geocode).
    """
    display_name = "Archipelocal Enable Live Suggestions"


class ArchipelocalSuggestionStrategy(OptionSet):
    """
    How to construct objectives when live suggestions are available:

    - only_concrete: Only emit PLACE objectives (fallback to generic if no suggestions available)
    - prefer_concrete: Emit PLACE and generic objectives, with a bias towards PLACE
    - random_mix: Emit PLACE and generic objectives with a balanced mix
    """
    display_name = "Archipelocal Suggestion Strategy"
    valid_keys = {"only_concrete", "prefer_concrete", "random_mix"}
    default = "prefer_concrete"


class ArchipelocalGeocodeCountryCodes(FreeText):
    """
    Optional ISO country codes to restrict geocoding, pipe-separated (e.g., "gb|ie|us").
    Leave empty for no country filter.
    """
    display_name = "Archipelocal Geocoding Country Codes (ISO)"
