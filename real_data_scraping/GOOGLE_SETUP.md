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
