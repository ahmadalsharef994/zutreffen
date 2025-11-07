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
