# Google Places API Setup Guide

## Overview

You can scrape German places data using either:
1. **OpenStreetMap** (FREE, no key) - Basic data
2. **Google Places API** (Requires key) - Rich data with photos, ratings, reviews

## Google Places API: What You Get

### ✅ Rich Data Per Place:
- **Name & Address** (formatted, accurate)
- **Real Photos** from Google Maps
- **Ratings** (1-5 stars) + review count
- **Opening Hours** (Mon-Sun with times)
- **Phone Number** (formatted)
- **Website** URL
- **Price Level** (0-4: Free to Very Expensive)
- **Business Status** (Open, Temporarily Closed, etc.)
- **Google Place ID** (unique identifier)

### 💰 Pricing (2024):

| API Call | Cost | What It Does |
|----------|------|--------------|
| Nearby Search | $0.032 | Find places in an area |
| Place Details | $0.017 | Get full info for one place |

**Total per place**: ~$0.05 (1 search + 1 detail call)

### 🎁 Free Tier:
- **$200/month credit** (Google Cloud free tier)
- **~4,000 places per month** for free
- No credit card required initially (but needed for continued use)

## Setup Steps

### 1. Create Google Cloud Account

Go to: https://console.cloud.google.com/

```
1. Sign in with Google account
2. Accept terms
3. Click "Select a project" → "New Project"
4. Name it: "Zutreffen Scraper"
5. Click "Create"
```

### 2. Enable Places API

```
1. Go to: https://console.cloud.google.com/apis/library
2. Search for "Places API"
3. Click "Places API"
4. Click "Enable"
5. Wait ~1 minute for activation
```

### 3. Create API Key

```
1. Go to: https://console.cloud.google.com/apis/credentials
2. Click "Create Credentials" → "API key"
3. Copy the key (looks like: AIzaSyD...)
4. Click "Restrict Key" (important!)
```

### 4. Restrict API Key (Security)

```
1. Under "API restrictions":
   - Select "Restrict key"
   - Check: "Places API"
   - Check: "Places API (New)" (if available)
2. Under "Application restrictions" (optional but recommended):
   - Select "IP addresses"
   - Add your server IP
3. Click "Save"
```

### 5. Add Key to Scraper

Edit `scrape.py`:

```python
# At the top of the file
GOOGLE_API_KEY = "AIzaSyD..."  # Your actual key
USE_GOOGLE_PLACES = True        # Enable Google mode
```

### 6. Test It

```bash
python3 scrape.py
```

Choose "y" when asked to use Google Places API.

## Cost Estimates

### For Complete Germany Scraping:

| Scope | Estimated Places | Estimated Cost |
|-------|-----------------|----------------|
| Major cities only (15) | ~2,000 places | **$100** |
| Large cities (70) | ~8,000 places | **$400** |
| All 600+ cities | ~50,000 places | **$2,500** |

### Recommendation:
Start with **1-3 cities** to test (~100 places = $5)

### Example: Berlin Only
```python
# In scrape.py, modify:
GERMAN_CITIES = {
    'major': ['Berlin'],  # Just one city
    'large': [],
    'medium': [],
    'small': []
}
```

Run it:
- Expected: ~500 places
- Cost: ~$25
- Within free tier: YES ✅

## Monitor Your Usage

### Check current usage:
```
1. Go to: https://console.cloud.google.com/apis/dashboard
2. Click "Places API"
3. View "Metrics" tab
4. See requests and estimated cost
```

### Set budget alerts:
```
1. Go to: https://console.cloud.google.com/billing
2. Click "Budgets & alerts"
3. Create budget: $50
4. Set alert at 50%, 90%, 100%
5. Get email warnings
```

## Free Tier Strategy

To stay within $200/month free tier:

### Option 1: Major Cities Only (~2K places)
- 15 major cities (Berlin, Hamburg, Munich, etc.)
- Cost: ~$100/month
- Best data quality

### Option 2: Mix of Sources
- Google Places for major cities (rich data)
- OpenStreetMap for smaller cities (free)
- Total: 50K+ places, ~$100 cost

### Option 3: Gradual Scraping
- Scrape 1,000 places/week (4K/month)
- Stays within free tier
- Complete Germany in ~3 months

## Comparison: Google vs OpenStreetMap

| Feature | Google Places | OpenStreetMap |
|---------|--------------|---------------|
| **Cost** | ~$0.05/place | FREE |
| **Photos** | Real Google Maps photos | Placeholder images |
| **Ratings** | Yes (with review count) | No |
| **Phone** | Yes (formatted) | Sometimes |
| **Website** | Yes | Sometimes |
| **Hours** | Detailed (Mon-Sun) | Sometimes (format varies) |
| **Coverage** | Excellent | Good |
| **Accuracy** | Very high | High |
| **Updates** | Real-time | Community-driven |

## Recommended Approach

### For Your Zutreffen App:

**Start**:
1. Use OpenStreetMap to scrape ALL German cities (FREE)
2. Get ~50K places with basic data

**Enhance**:
1. Use Google Places for top 50-100 places per major city
2. Add rich data (photos, ratings, hours) to popular spots
3. Cost: ~$250 for 5,000 enhanced places

**Result**:
- 50K total places (free from OSM)
- 5K premium places (with Google data)
- Total cost: $250 one-time

## FAQ

**Q: Do I need a credit card?**
A: Yes, eventually. You can start with free trial, but need CC for continued use.

**Q: Will I be charged automatically?**
A: Only if you exceed $200/month. Set up billing alerts!

**Q: Can I stop anytime?**
A: Yes. Delete API key or disable Places API to stop charges.

**Q: What if I go over $200?**
A: You'll be charged for overage. Set budget alerts to prevent this.

**Q: Is OSM data enough?**
A: For most places, YES! OSM has good coverage. Use Google only for premium features.

**Q: Can I use both sources?**
A: Yes! Scrape with OSM (free), then enrich top places with Google data.

## Alternative: Mix Both Sources

Best strategy for cost-effectiveness:

```python
# In scrape.py

# First pass: OpenStreetMap (FREE) - All Germany
# Get all places for free
python3 scrape.py
# Choose: No (N) for Google Places

# Second pass: Google Places (PAID) - Major cities only
# Edit GERMAN_CITIES to just: ['Berlin', 'Hamburg', 'Munich']
# Get rich data for top cities
python3 scrape.py
# Choose: Yes (y) for Google Places

# Merge the two JSON files
# Use OSM data as base, overlay Google data for major cities
```

This gives you:
- ✅ Complete coverage (OSM)
- ✅ Rich data for popular cities (Google)
- ✅ Cost: ~$100 (within free tier)

## Support

**Google Cloud Support**:
- Documentation: https://developers.google.com/maps/documentation/places
- Community: https://stackoverflow.com/questions/tagged/google-places-api
- Issues: https://issuetracker.google.com/savedsearches/5013309

**Zutreffen Scraper Issues**:
- Check `data/logs/scraping.log` for errors
- Run with verbose mode: `python3 scrape.py --debug`



# German Places Data Scraper

Scrape comprehensive places data across 600+ German cities for the Zutreffen check-in app.

## 📁 Files (Only 2!)

1. **`scrape.py`** - Complete scraper with images (all-in-one)
2. **`import_to_db.py`** - Optional database importer

That's it! Everything else is consolidated.

## 🚀 Quick Start

### 1. Scrape all German places (with images):

```bash
python3 scrape.py
```

**What it does:**
- ✅ Scrapes 600+ German cities
- ✅ Fetches images (Unsplash/Pixabay or placeholders)
- ✅ Validates coordinates and data quality
- ✅ Outputs to JSON files

**Estimated time**: 2-4 hours for complete coverage

### 2. Import to database (optional):

```bash
python3 import_to_db.py
```

Interactive menu lets you:
- Import all places
- Import specific city
- Import specific category
- View statistics
- Clear database

### 3. Find your data:

**JSON files** (ready to use):
- `data/json_output/all_places.json` - Complete dataset
- `data/json_output/places_by_city.json` - Grouped by city
- `data/json_output/places_by_category.json` - Grouped by category
- `data/json_output/metadata.json` - Statistics and summary

## ⚙️ Configuration

### API Keys (Optional - for better images)

Edit `scrape.py` and add your free API keys:

```python
UNSPLASH_API_KEY = "your_key"  # https://unsplash.com/developers
PIXABAY_API_KEY = "your_key"   # https://pixabay.com/api/docs/
```

**Without keys**: Uses placeholder images (still looks professional!)

### Customize Settings

In `scrape.py`, adjust these at the top:

```python
# What to scrape
CATEGORIES = ['cafe', 'restaurant', 'bar', 'library', ...]

# Performance
REQUEST_DELAY = 2.0  # Seconds between API requests
BATCH_SIZE = 5       # Cities processed in parallel

# Geography (default: all of Germany)
GERMAN_CITIES = {
    'major': [...],   # Berlin, Hamburg, etc.
    'large': [...],   # Bonn, Münster, etc.
    'medium': [...],  # Marburg, Giessen, etc.
    'small': [...]    # Small towns
}
```

## 📊 What Gets Scraped

**Categories** (17 types):
- Cafes, restaurants, bars, pubs, fast food, beer gardens
- Libraries, coworking spaces
- Hotels, gyms, spas
- Cinemas, community centers
- Universities, hospitals
- Fuel stations

**Cities** (600+ total):
- **Major** (15): Berlin, Hamburg, Munich, Cologne, Frankfurt...
- **Large** (70): Bonn, Münster, Karlsruhe, Heidelberg...
- **Medium** (120+): Marburg, Giessen, Lüneburg, Bayreuth...
- **Small** (400+): Towns across Germany

**Data per place**:
- Name, address, postal code
- Latitude, longitude (validated for Germany)
- Category
- Image URL
- City
- OpenStreetMap ID
- Timestamp

## 💡 Usage Examples

### Use JSON directly in your app:

```python
import json

# Load all places
with open('data/json_output/all_places.json', 'r') as f:
    places = json.load(f)

# Load by city
with open('data/json_output/places_by_city.json', 'r') as f:
    berlin_places = json.load(f)['Berlin']

# Use with pandas
import pandas as pd
df = pd.read_json('data/json_output/all_places.json')
```

### Import to database:

```bash
python3 import_to_db.py

# Options:
# 1 - Import everything
# 2 - Import only Berlin
# 3 - Import only cafes
# 4 - View stats
```

## 🛠️ Technical Details

**Data Source**: OpenStreetMap Overpass API (free, no API key needed)
- Rate limited: 2 seconds between requests
- Coverage: Complete Germany
- Quality: Validated coordinates, required fields

**Image Sources**:
1. Unsplash API (if key provided) - High quality
2. Pixabay API (if key provided) - Good variety
3. Placeholder images (fallback) - Category-specific

**Output Format**:
```json
{
  "name": "Café Einstein",
  "address": "Kurfürstenstraße 58",
  "city": "Berlin",
  "postal_code": "10785",
  "latitude": 52.5065,
  "longitude": 13.3635,
  "category": "cafe",
  "description": "Café Einstein in Berlin",
  "image_url": "https://...",
  "osm_id": 123456789,
  "scraped_at": "2025-11-07T..."
}
```

## 📈 Expected Results

**Realistic estimates**:
- **Cafes**: ~15,000-25,000 places
- **Restaurants**: ~20,000-35,000 places
- **Bars**: ~8,000-15,000 places
- **Libraries**: ~2,000-4,000 places
- **Total**: ~50,000-100,000 places

**Processing time**:
- API requests: ~8,000-10,000 total
- With 2s delay: ~4-6 hours
- Faster with higher BATCH_SIZE (but respect rate limits!)

## 🚨 Important Notes

1. **Rate Limiting**: Default 2s delay is respectful. Don't decrease below 1s.
2. **API Keys**: Optional but recommended for better images
3. **Storage**: Expect ~50-100MB for complete JSON dataset
4. **Interruption**: Safe to stop and restart - progress is saved
5. **Quality**: Data is validated (coordinates, names, categories)

## 🔧 Troubleshooting

**Slow scraping?**
- Increase `BATCH_SIZE` (but stay reasonable: 5-10)
- Reduce `REQUEST_DELAY` to 1.5s minimum
- Limit to specific cities/categories

**Missing images?**
- Add API keys for better quality
- Placeholder images always work as fallback

**Database import fails?**
- Make sure Zutreffen app is set up
- Check: `app/models/place.py` exists
- Run from project root: `cd /home/ahmad/projects/zutreffen`

**Out of memory?**
- Process fewer cities at once
- Reduce `BATCH_SIZE`
- Import to database in chunks

## 📝 License

Uses OpenStreetMap data (© OpenStreetMap contributors, ODbL license)
