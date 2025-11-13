# Archipelocal Setup Guide

**Archipelocal** is a Keymaster's Keep module that generates real-world place-based objectives using the [Geoapify Places API](https://www.geoapify.com/). Visit nearby cafes, parks, museums, and more based on your actual location!

**Powered by [Geoapify](https://www.geoapify.com/)**

---

## Quick Start

### 1. Get a Free Geoapify API Key

1. Visit [https://www.geoapify.com/](https://www.geoapify.com/)
2. Click **"Get Started for Free"** or **"Sign Up"**
3. Create a free account (email + password)
4. After logging in, go to **"My Projects"** in the dashboard
5. Create a new project or use the default project
6. Click **"API Keys"** and copy your API key
   - Free tier includes **3,000 requests per day** (more than enough for Keymaster's Keep!)

### 2. Configure Your Home Location

Choose **one** of these methods:

#### Option A: Use a Human-Readable Address (Recommended)
```yaml
archipelocal_home_address: "Central Park, New York, NY"
archipelocal_geocode_country_codes: "us"  # Optional: restrict geocoding to specific countries
```

#### Option B: Use Exact Coordinates
```yaml
archipelocal_home_latitude: "40.785091"
archipelocal_home_longitude: "-73.968285"
```

**Privacy Tip:** For privacy, use a nearby public location (park, library, landmark) instead of your exact home address.

### 3. Set Your API Key

Choose **one** of these methods:

#### Option A: In Your YAML (easiest)
```yaml
archipelocal_geoapify_api_key: "your_api_key_here"
```

#### Option B: Environment Variable (more secure)
Set `GEOAPIFY_API_KEY` in your system environment variables.

### 4. Enable Live Suggestions

```yaml
archipelocal_enable_live_suggestions: true
archipelocal_suggestion_strategy: only_concrete  # or prefer_concrete, random_mix
```

---

## Configuration Options

### Distance & Units

```yaml
archipelocal_distance_unit: km  # or mi
archipelocal_global_max_distance: 10  # km or mi, default 5
archipelocal_max_results_per_category: 20  # 1-100, default 20
```

#### Per-Category Distance Overrides
Set custom max distances for specific categories:
```yaml
archipelocal_per_category_max_distance: |
  {
    "catering.cafe": 3,
    "leisure.park": 8,
    "entertainment.museum": 15
  }
```

#### Per-Category Result Limit Overrides
Set custom result limits for specific categories:
```yaml
archipelocal_per_category_max_results: |
  {
    "catering.cafe": 10,
    "leisure.park": 50,
    "entertainment.museum": 15
  }
```

**Note:** Both distance and result limits can be customized per category. This is useful when you want more options for common categories (like cafes) or fewer for rare categories (like museums).

### Category Selection

By default, Archipelocal uses a curated list of 40+ categories including:
- **Food & Drink:** cafes, restaurants, pubs, bakeries, ice cream shops
- **Leisure:** parks, playgrounds, gardens, viewpoints, galleries
- **Entertainment:** museums, cinemas, theaters, zoos, theme parks
- **Natural & Man-Made:** beaches, forests, bridges, towers, lighthouses
- **And more!**

To customize categories:
```yaml
archipelocal_allowed_categories:
  - catering.cafe
  - catering.restaurant
  - leisure.park
  - entertainment.museum
  - tourism.attraction
```

See [Geoapify's full taxonomy](https://apidocs.geoapify.com/docs/places/#categories) for all available categories.

### Conditions (Accessibility & Filters)

Apply optional conditions to filter all place searches. Great for accessibility needs or dietary requirements!

```yaml
archipelocal_named_locations_only: true  # Default: true - only show places with proper names
archipelocal_conditions:
  - wheelchair
  - vegan
```

**Named Locations Only:**
- **`archipelocal_named_locations_only: true`** (default) - Only returns places with proper names, filtering out unnamed or poorly-labeled locations
- **`archipelocal_named_locations_only: false`** - Includes all places, even those without proper names (may include generic addresses or POIs)

**Common conditions:**
- `wheelchair` - Wheelchair accessible places
- `vegan` - Vegan food options available
- `vegan.only` - Only vegan food
- `vegetarian` - Vegetarian options available
- `kosher` - Kosher food options
- `halal` - Halal food options
- `internet_access` - Places with WiFi/internet
- `dogs` - Dog-friendly places
- `no_fee` - Free entry/no admission fee
- `outdoor_seating` - Outdoor seating available

See [Geoapify's full conditions list](https://apidocs.geoapify.com/docs/places/#conditions) for all options.

**Note:** Conditions apply to all categories. The API will only return places matching both the category AND all specified conditions.

### Suggestion Strategies

```yaml
archipelocal_suggestion_strategy: only_concrete
```

- **`only_concrete`**: Only show specific place names (e.g., "Visit Starbucks @ 40.78509, -73.96829 – 0.42 km • Cafe")
  - If no suggestions available, no Archipelocal objectives are generated
- **`prefer_concrete`**: Show specific places plus generic category objectives, biased toward specifics
  - Example: "Visit a Cafe near your home" (with lower weight)
- **`random_mix`**: Balanced mix of specific places and generic categories

---

## Example Configuration

```yaml
# API & Location
archipelocal_geoapify_api_key: "abc123xyz456"
archipelocal_home_address: "Central Park, New York, NY"
archipelocal_geocode_country_codes: "us"

# Distance & Results
archipelocal_distance_unit: km
archipelocal_global_max_distance: 10
archipelocal_max_results_per_category: 20

# Live Suggestions
archipelocal_enable_live_suggestions: true
archipelocal_suggestion_strategy: only_concrete

# Categories (leave empty to use defaults)
archipelocal_allowed_categories: []

# Named Locations & Conditions
archipelocal_named_locations_only: true  # Default: only show places with proper names
archipelocal_conditions:  # Optional: filter places by accessibility/dietary needs
  - wheelchair
  - internet_access

# Per-Category Distances (optional)
archipelocal_per_category_max_distance: |
  {
    "catering.cafe": 3,
    "leisure.park": 5,
    "entertainment.cinema": 15
  }

# Per-Category Result Limits (optional)
archipelocal_per_category_max_results: |
  {
    "catering.cafe": 10,
    "leisure.park": 30,
    "entertainment.cinema": 5
  }
```

---

## How It Works

1. **Template Generation**: When Keymaster's Keep loads your options, Archipelocal registers its objective templates
2. **Lazy Loading**: API calls only happen **when a PLACE objective is selected**, not during initial load
3. **Session Caching**: Locations are fetched once per session and reused for the entire campaign
4. **Geocoding Cache**: Your home location is geocoded once and cached (if using address instead of coordinates)

---

## Sample Objectives

With `only_concrete` and live suggestions enabled:

- ✅ **"Visit Starbucks @ 40.78509, -73.96829 – 0.42 km • Cafe (from live suggestions near your home)"**
- ✅ **"Visit Central Park Zoo @ 40.76775, -73.97189 – 1.23 km • Zoo (from live suggestions near your home)"**
- ✅ **"Visit The Metropolitan Museum of Art @ 40.77934, -73.96337 – 0.87 km • Museum (from live suggestions near your home)"**

With `prefer_concrete` or `random_mix`:

- ✅ **"Visit a Cafe near your home (within your max distance)"**
- ✅ **"Visit your 3rd-closest Park near your home (within your max distance)"**
- ✅ **"Visit a random Museum near your home (within your max distance)"**

---

## Troubleshooting

### "No Archipelocal objectives generated"
- Check that `archipelocal_enable_live_suggestions: true`
- Verify your API key is correct
- Confirm your home location is set (address or coordinates)
- With `only_concrete`, ensure your area has results for your selected categories

### "Geocoding returned no results"
- Double-check your address spelling
- Add `archipelocal_geocode_country_codes` to restrict country (e.g., `"gb"` for UK, `"us"` for USA)
- Try using exact coordinates instead

### "HTTP 400 for category X"
- Some Geoapify categories have changed. Try using the built-in defaults or consult the [current taxonomy](https://www.geoapify.com/places-api)
- The module includes fallback mappings for common mismatches

### "Loading locations every time I generate"
- This should only happen once per session (per unique settings bundle)
- If you're seeing repeated loads, check if your options are changing between runs
- Session cache reuses data as long as home location, categories, distances, and limits stay the same

---

## Privacy & Rate Limits

- **Privacy**: Use a nearby public location instead of your exact address
- **Rate Limits**: Free tier = 3,000 requests/day
  - Each category fetches once per session
  - Example: 20 categories × 1 fetch each = 20 requests per session
  - You can run **150 sessions per day** before hitting limits!
- **Coordinates in Objectives**: All place suggestions include coordinates for accuracy and navigation

---

## Advanced: Manual API Testing

Test your API key and location manually:

```bash
# Test geocoding
curl "https://api.geoapify.com/v1/geocode/search?text=Central%20Park,%20New%20York&format=json&apiKey=YOUR_KEY"

# Test places search
curl "https://api.geoapify.com/v2/places?categories=catering.cafe&filter=circle:-73.968285,40.785091,5000&limit=10&apiKey=YOUR_KEY"
```

---

## Getting Help

If you encounter issues:
1. Check console logs for error messages (look for `[Archipelocal]` prefix)
2. Verify your API key at [Geoapify Dashboard](https://myprojects.geoapify.com/)
3. Test a minimal config (just API key + address)
4. Try using exact coordinates instead of address

---

## Credits

- Uses [Geoapify Places API](https://www.geoapify.com/places-api) for location data
- Module design inspired by the Playnite Library integration pattern
- Built for Keymaster's Keep by eiron
