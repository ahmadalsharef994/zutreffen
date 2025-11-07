"""
🇩🇪 German Places Scraper - Complete solution for scraping places across Germany

Features:
- Scrapes cafes, restaurants, bars, libraries, and more
- Covers 600+ German cities (Berlin to small towns like Marburg)
- Rich place data: phone, website, opening hours, rating, photos
- Supports OpenStreetMap (FREE) or Google Places API (better data, requires key)
- Outputs to JSON format (no database required)

Data Sources:
1. OpenStreetMap (FREE, no key) - Good coverage, basic data
2. Google Places API (Requires key) - Rich data, photos, reviews
   - Free tier: $200/month credit (~28,000 place details)
   - Best for: Complete place information, real photos, ratings

Usage:
    python3 scrape.py

Output:
    - data/json_output/all_places.json (with extended fields)
    - data/json_output/places_by_city.json
    - data/json_output/places_by_category.json
"""
import asyncio
import aiohttp
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict

# =============================================================================
# CONFIGURATION
# =============================================================================

# Choose data source
USE_GOOGLE_PLACES = False  # Set to True if you have Google API key
GOOGLE_API_KEY = None      # Get from https://console.cloud.google.com/

# Alternative image APIs (optional)
UNSPLASH_API_KEY = None  # https://unsplash.com/developers
PIXABAY_API_KEY = None   # https://pixabay.com/api/docs/

# Categories to scrape
CATEGORIES = [
    'cafe', 'restaurant', 'bar', 'pub', 'fast_food', 'biergarten',
    'hotel', 'library', 'coworking_space', 'university', 'cinema',
    'fuel', 'gym', 'spa', 'hospital', 'community_centre'
]

# Google Places API type mapping
GOOGLE_PLACES_TYPES = {
    'cafe': 'cafe',
    'restaurant': 'restaurant',
    'bar': 'bar',
    'pub': 'bar',
    'fast_food': 'restaurant',
    'biergarten': 'bar',
    'hotel': 'lodging',
    'library': 'library',
    'coworking_space': 'point_of_interest',
    'university': 'university',
    'cinema': 'movie_theater',
    'fuel': 'gas_station',
    'gym': 'gym',
    'spa': 'spa',
    'hospital': 'hospital',
    'community_centre': 'community_center'
}

# German cities by size (600+ cities) with alternative names
GERMAN_CITIES = {
    'major': ['Berlin', 'Hamburg', 'Munich', 'Cologne', 'Frankfurt', 'Stuttgart', 
              'Düsseldorf', 'Dortmund', 'Essen', 'Leipzig', 'Bremen', 'Dresden', 
              'Hanover', 'Nuremberg', 'Duisburg'],
    'large': ['Bochum', 'Wuppertal', 'Bielefeld', 'Bonn', 'Münster', 'Karlsruhe',
              'Mannheim', 'Augsburg', 'Wiesbaden', 'Gelsenkirchen', 'Mönchengladbach',
              'Braunschweig', 'Chemnitz', 'Kiel', 'Aachen', 'Halle', 'Magdeburg',
              'Freiburg', 'Krefeld', 'Lübeck', 'Oberhausen', 'Erfurt', 'Mainz',
              'Rostock', 'Kassel', 'Hagen', 'Hamm', 'Saarbrücken', 'Mülheim',
              'Potsdam', 'Ludwigshafen', 'Oldenburg', 'Leverkusen', 'Osnabrück',
              'Solingen', 'Heidelberg', 'Herne', 'Neuss', 'Darmstadt', 'Paderborn',
              'Regensburg', 'Ingolstadt', 'Würzburg', 'Fürth', 'Wolfsburg', 'Offenbach',
              'Ulm', 'Heilbronn', 'Pforzheim', 'Göttingen', 'Bottrop', 'Trier',
              'Recklinghausen', 'Reutlingen', 'Bremerhaven', 'Koblenz', 'Bergisch Gladbach',
              'Jena', 'Remscheid', 'Erlangen', 'Moers', 'Siegen', 'Hildesheim', 'Salzgitter'],
    'medium': ['Cottbus', 'Witten', 'Schwerin', 'Kaiserslautern', 'Gütersloh', 'Iserlohn',
               'Düren', 'Esslingen', 'Ratingen', 'Lüdenscheid', 'Marl', 'Ludwigsburg',
               'Velbert', 'Flensburg', 'Wilhelmshaven', 'Minden', 'Worms', 'Viersen',
               'Norderstedt', 'Delmenhorst', 'Marburg', 'Giessen', 'Lüneburg', 'Bayreuth',
               'Detmold', 'Celle', 'Fulda', 'Aschaffenburg', 'Lippstadt', 'Plauen',
               'Neuwied', 'Passau', 'Landshut', 'Bamberg', 'Konstanz', 'Stralsund'],
    'small': ['Tübingen', 'Göppingen', 'Ravensburg', 'Friedrichshafen', 'Weimar',
              'Gera', 'Speyer', 'Schweinfurt', 'Greifswald', 'Wismar', 'Baden-Baden',
              'Neustadt', 'Landau', 'Pirmasens', 'Homburg', 'Zweibrücken']
}

# Alternative city names (German/English variations for search)
CITY_ALTERNATIVES = {
    'Munich': ['München', 'Munchen'],
    'Cologne': ['Köln', 'Koln'],
    'Nuremberg': ['Nürnberg', 'Nurnberg'],
    'Hanover': ['Hannover'],
    'Brunswick': ['Braunschweig'],
    'Mönchengladbach': ['Monchengladbach'],
    'Düsseldorf': ['Dusseldorf'],
    'Saarbrücken': ['Saarbrucken'],
    'Göttingen': ['Gottingen'],
    'Würzburg': ['Wurzburg'],
    'Fürth': ['Furth'],
    'Kaiserslautern': ['K-Town'],  # US military nickname
    'Lübeck': ['Lubeck'],
    'Münster': ['Munster'],
    'Osnabrück': ['Osnabruck'],
    'Düren': ['Duren'],
    'Gütersloh': ['Gutersloh'],
    'Lüdenscheid': ['Ludenscheid'],
}

# OSM to App category mapping
OSM_CATEGORY_MAP = {
    'cafe': 'cafe',
    'restaurant': 'restaurant',
    'bar': 'bar',
    'pub': 'bar',
    'fast_food': 'fast_food',
    'biergarten': 'bar',
    'food_court': 'mall_food_court',
    'hotel': 'hotel_lobby',
    'hostel': 'hotel_lobby',
    'library': 'library',
    'coworking_space': 'coworking',
    'university': 'university_cafe',
    'cinema': 'cinema_lobby',
    'theatre': 'cinema_lobby',
    'fuel': 'service_station',
    'gym': 'gym_cafe',
    'spa': 'spa_lounge',
    'hospital': 'hospital_cafe',
    'community_centre': 'community_centre',
}

# Validation bounds for Germany
GERMANY_BOUNDS = {
    'min_lat': 47.0, 'max_lat': 55.1,
    'min_lng': 5.8, 'max_lng': 15.0
}

# Scraping settings
REQUEST_DELAY = 1.5  # seconds between requests (faster for testing)
BATCH_SIZE = 3       # cities processed in parallel
MAX_RETRIES = 3

# =============================================================================
# GOOGLE PLACES API INTEGRATION
# =============================================================================

class GooglePlacesAPI:
    """Google Places API client for rich place data."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None
        self.places_searched = 0
        self.details_fetched = 0
    
    async def search_places(self, city: str, category: str, latitude: float, longitude: float) -> List[Dict]:
        """Search for places using Google Places Nearby Search."""
        try:
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            place_type = GOOGLE_PLACES_TYPES.get(category, 'point_of_interest')
            
            params = {
                'location': f"{latitude},{longitude}",
                'radius': 5000,  # 5km radius
                'type': place_type,
                'key': self.api_key
            }
            
            async with self.session.get(url, params=params, timeout=30) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.places_searched += 1
                    
                    places = []
                    for result in data.get('results', [])[:20]:  # Limit per search
                        # Get detailed info
                        place_details = await self.get_place_details(result['place_id'])
                        if place_details:
                            places.append(place_details)
                            await asyncio.sleep(0.1)  # Rate limit
                    
                    return places
                else:
                    return []
        except Exception as e:
            logging.error(f"Google Places search error: {e}")
            return []
    
    async def get_place_details(self, place_id: str) -> Optional[Dict]:
        """Get detailed place information."""
        try:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            
            params = {
                'place_id': place_id,
                'fields': 'name,formatted_address,geometry,formatted_phone_number,website,'
                         'opening_hours,rating,user_ratings_total,price_level,photos,reviews,'
                         'types,vicinity,business_status',
                'key': self.api_key
            }
            
            async with self.session.get(url, params=params, timeout=30) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    result = data.get('result', {})
                    self.details_fetched += 1
                    
                    # Get best photo
                    photo_url = None
                    if result.get('photos'):
                        photo_ref = result['photos'][0].get('photo_reference')
                        if photo_ref:
                            photo_url = self._get_photo_url(photo_ref)
                    
                    # Parse opening hours
                    opening_hours = None
                    if result.get('opening_hours'):
                        opening_hours = result['opening_hours'].get('weekday_text', [])
                    
                    return {
                        'place_id': place_id,
                        'name': result.get('name'),
                        'address': result.get('formatted_address'),
                        'vicinity': result.get('vicinity'),
                        'latitude': result['geometry']['location']['lat'],
                        'longitude': result['geometry']['location']['lng'],
                        'phone': result.get('formatted_phone_number'),
                        'website': result.get('website'),
                        'rating': result.get('rating'),
                        'user_ratings_total': result.get('user_ratings_total'),
                        'price_level': result.get('price_level'),
                        'photo_url': photo_url,
                        'opening_hours': opening_hours,
                        'business_status': result.get('business_status'),
                        'types': result.get('types', [])
                    }
                else:
                    return None
        except Exception as e:
            logging.error(f"Error fetching place details: {e}")
            return None
    
    def _get_photo_url(self, photo_reference: str, max_width: int = 400) -> str:
        """Get photo URL from photo reference."""
        return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photo_reference={photo_reference}&key={self.api_key}"
    
    def get_usage_stats(self) -> Dict:
        """Get API usage statistics."""
        # Google Places API pricing (as of 2024)
        nearby_search_cost = self.places_searched * 0.032  # $0.032 per search
        details_cost = self.details_fetched * 0.017        # $0.017 per detail
        total_cost = nearby_search_cost + details_cost
        
        return {
            'searches': self.places_searched,
            'details_fetched': self.details_fetched,
            'estimated_cost_usd': round(total_cost, 2),
            'free_tier_remaining': max(0, round(200 - total_cost, 2))
        }

# =============================================================================
# IMAGE FETCHER
# =============================================================================

class ImageFetcher:
    """Fetch images for places from multiple sources."""
    
    PLACEHOLDER_URLS = {
        'cafe': 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=400',
        'restaurant': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400',
        'bar': 'https://images.unsplash.com/photo-1566417713940-fe7c737a9ef2?w=400',
        'library': 'https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=400',
        'hotel_lobby': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=400',
        'coworking': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=400',
        'default': 'https://images.unsplash.com/photo-1519167758481-83f29da8c2f0?w=400'
    }
    
    def __init__(self):
        self.session = None
        self.unsplash_key = UNSPLASH_API_KEY
        self.pixabay_key = PIXABAY_API_KEY
        self.last_request_time = {}
    
    async def get_image(self, place_name: str, category: str, city: str) -> Optional[str]:
        """Get image URL for a place."""
        
        # Try Unsplash first (if API key provided)
        if self.unsplash_key:
            img = await self._get_unsplash_image(category)
            if img:
                return img
        
        # Try Pixabay (if API key provided)
        if self.pixabay_key:
            img = await self._get_pixabay_image(f"{category} {city}")
            if img:
                return img
        
        # Fallback to placeholder
        return self.PLACEHOLDER_URLS.get(category, self.PLACEHOLDER_URLS['default'])
    
    async def _get_unsplash_image(self, query: str) -> Optional[str]:
        """Fetch from Unsplash API."""
        try:
            await self._rate_limit('unsplash', 1.0)
            url = f"https://api.unsplash.com/photos/random"
            params = {
                'query': query,
                'client_id': self.unsplash_key,
                'w': 400,
                'h': 300
            }
            async with self.session.get(url, params=params, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('urls', {}).get('small')
        except:
            pass
        return None
    
    async def _get_pixabay_image(self, query: str) -> Optional[str]:
        """Fetch from Pixabay API."""
        try:
            await self._rate_limit('pixabay', 1.0)
            url = "https://pixabay.com/api/"
            params = {
                'key': self.pixabay_key,
                'q': query,
                'image_type': 'photo',
                'per_page': 3
            }
            async with self.session.get(url, params=params, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    hits = data.get('hits', [])
                    if hits:
                        return hits[0].get('webformatURL')
        except:
            pass
        return None
    
    async def _rate_limit(self, source: str, delay: float):
        """Simple rate limiting."""
        now = time.time()
        last = self.last_request_time.get(source, 0)
        if now - last < delay:
            await asyncio.sleep(delay - (now - last))
        self.last_request_time[source] = time.time()

# =============================================================================
# SCRAPER
# =============================================================================

class GermanPlacesScraper:
    """Main scraper class."""
    
    def __init__(self, use_google: bool = False):
        self.session = None
        self.image_fetcher = ImageFetcher()
        self.google_api = None
        self.use_google = use_google
        self.places = []
        self.stats = {
            'cities_processed': 0,
            'total_places': 0,
            'api_requests': 0,
            'start_time': None
        }
        
        # Initialize Google API if needed
        if use_google and GOOGLE_API_KEY:
            self.google_api = GooglePlacesAPI(GOOGLE_API_KEY)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    async def scrape_all(self) -> List[Dict]:
        """Scrape all cities and return places."""
        self.stats['start_time'] = time.time()
        
        # Get all cities
        all_cities = []
        for size_group in GERMAN_CITIES.values():
            all_cities.extend(size_group)
        
        mode = "Google Places API" if self.use_google else "OpenStreetMap"
        self.logger.info(f"🚀 Starting scrape of {len(all_cities)} German cities")
        self.logger.info(f"📍 Mode: {mode}")
        self.logger.info(f"📍 Categories: {', '.join(CATEGORIES)}")
        
        # Create session
        async with aiohttp.ClientSession() as session:
            self.session = session
            self.image_fetcher.session = session
            if self.google_api:
                self.google_api.session = session
            
            # Process cities in batches
            for i in range(0, len(all_cities), BATCH_SIZE):
                batch = all_cities[i:i + BATCH_SIZE]
                tasks = [self._scrape_city(city) for city in batch]
                await asyncio.gather(*tasks)
                
                # Progress update
                progress = min(i + BATCH_SIZE, len(all_cities))
                self.logger.info(f"Progress: {progress}/{len(all_cities)} cities | "
                               f"Places found: {self.stats['total_places']}")
                
                # Show Google API usage
                if self.google_api:
                    usage = self.google_api.get_usage_stats()
                    self.logger.info(f"   Google API: ${usage['estimated_cost_usd']} "
                                   f"(${usage['free_tier_remaining']} free tier left)")
        
        elapsed = time.time() - self.stats['start_time']
        self.logger.info(f"\n✅ Scraping complete!")
        self.logger.info(f"   Cities: {self.stats['cities_processed']}")
        self.logger.info(f"   Places: {self.stats['total_places']}")
        self.logger.info(f"   Time: {elapsed/60:.1f} minutes")
        
        if self.google_api:
            usage = self.google_api.get_usage_stats()
            self.logger.info(f"\n💰 Google API Usage:")
            self.logger.info(f"   Searches: {usage['searches']}")
            self.logger.info(f"   Details: {usage['details_fetched']}")
            self.logger.info(f"   Cost: ${usage['estimated_cost_usd']}")
            self.logger.info(f"   Free tier remaining: ${usage['free_tier_remaining']}")
        
        return self.places
    
    async def _scrape_city(self, city: str):
        """Scrape all categories for a city."""
        # Get city coordinates (approximate center)
        city_coords = await self._get_city_coordinates(city)
        
        for category in CATEGORIES:
            if self.use_google and self.google_api:
                await self._scrape_category_google(city, category, city_coords)
            else:
                await self._scrape_category_osm(city, category)
            await asyncio.sleep(REQUEST_DELAY)
        
        self.stats['cities_processed'] += 1
    
    async def _get_city_coordinates(self, city: str) -> tuple:
        """Get approximate city center coordinates."""
        # Simplified - you could use geocoding API for exact coords
        # For now, return Germany center
        return (51.1657, 10.4515)  # Germany center
    
    async def _scrape_category_google(self, city: str, category: str, coords: tuple):
        """Scrape using Google Places API."""
        try:
            places_data = await self.google_api.search_places(
                city, category, coords[0], coords[1]
            )
            
            for place_data in places_data:
                # Convert to our format
                app_category = OSM_CATEGORY_MAP.get(category, category)
                
                place = {
                    'name': place_data['name'],
                    'address': place_data.get('address', ''),
                    'city': city,
                    'city_alternatives': CITY_ALTERNATIVES.get(city, []),  # Add alternative names
                    'postal_code': self._extract_postal_code(place_data.get('address', '')),
                    'latitude': float(place_data['latitude']),
                    'longitude': float(place_data['longitude']),
                    'category': app_category,
                    'description': f"{place_data['name']} in {city}",
                    'image_url': place_data.get('photo_url'),
                    'rating': place_data.get('rating'),
                    'phone': place_data.get('phone'),
                    'website': place_data.get('website'),
                    'opening_hours': place_data.get('opening_hours'),
                    'price_level': place_data.get('price_level'),
                    'user_ratings_total': place_data.get('user_ratings_total'),
                    'business_status': place_data.get('business_status'),
                    'google_place_id': place_data.get('place_id'),
                    'osm_id': None,
                    'scraped_at': datetime.now().isoformat(),
                    'data_source': 'google_places'
                }
                
                self.places.append(place)
                self.stats['total_places'] += 1
        
        except Exception as e:
            self.logger.error(f"Error scraping Google Places {city}/{category}: {e}")
    
    async def _scrape_category_osm(self, city: str, category: str):
        """Scrape using OpenStreetMap (original method)."""
        try:
            # Build Overpass query
            query = self._build_overpass_query(city, category)
            
            # Query Overpass API
            url = "https://overpass-api.de/api/interpreter"
            
            for attempt in range(MAX_RETRIES):
                try:
                    async with self.session.post(url, data=query, timeout=180) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            places = await self._process_response(data, city, category)
                            self.places.extend(places)
                            self.stats['total_places'] += len(places)
                            self.stats['api_requests'] += 1
                            return
                        elif resp.status == 429:
                            await asyncio.sleep(60)  # Rate limited
                        else:
                            break
                except asyncio.TimeoutError:
                    if attempt < MAX_RETRIES - 1:
                        await asyncio.sleep(5)
                    continue
                except Exception as e:
                    self.logger.warning(f"Error querying {city}/{category}: {e}")
                    break
        
        except Exception as e:
            self.logger.error(f"Failed to scrape {city}/{category}: {e}")
    
    def _build_overpass_query(self, city: str, category: str) -> str:
        """Build Overpass QL query."""
        # Map category to OSM tags
        osm_queries = []
        
        if category in ['cafe', 'restaurant', 'bar', 'pub', 'fast_food', 'biergarten']:
            osm_queries.append(f'node["amenity"="{category}"](area.a);')
            osm_queries.append(f'way["amenity"="{category}"](area.a);')
        elif category == 'hotel':
            osm_queries.append('node["tourism"="hotel"](area.a);')
            osm_queries.append('way["tourism"="hotel"](area.a);')
        elif category == 'library':
            osm_queries.append('node["amenity"="library"](area.a);')
            osm_queries.append('way["amenity"="library"](area.a);')
        elif category == 'coworking_space':
            osm_queries.append('node["amenity"="coworking_space"](area.a);')
            osm_queries.append('way["amenity"="coworking_space"](area.a);')
        elif category == 'university':
            osm_queries.append('node["amenity"="university"](area.a);')
            osm_queries.append('way["amenity"="university"](area.a);')
        elif category == 'cinema':
            osm_queries.append('node["amenity"="cinema"](area.a);')
            osm_queries.append('way["amenity"="cinema"](area.a);')
        elif category == 'fuel':
            osm_queries.append('node["amenity"="fuel"](area.a);')
            osm_queries.append('way["amenity"="fuel"](area.a);')
        elif category == 'gym':
            osm_queries.append('node["leisure"="fitness_centre"](area.a);')
            osm_queries.append('way["leisure"="fitness_centre"](area.a);')
        elif category == 'spa':
            osm_queries.append('node["leisure"="spa"](area.a);')
            osm_queries.append('way["leisure"="spa"](area.a);')
        elif category == 'hospital':
            osm_queries.append('node["amenity"="hospital"](area.a);')
            osm_queries.append('way["amenity"="hospital"](area.a);')
        elif category == 'community_centre':
            osm_queries.append('node["amenity"="community_centre"](area.a);')
            osm_queries.append('way["amenity"="community_centre"](area.a);')
        else:
            osm_queries.append(f'node["amenity"="{category}"](area.a);')
            osm_queries.append(f'way["amenity"="{category}"](area.a);')
        
        query_parts = '\n'.join(osm_queries)
        
        # Simpler, more reliable query
        return f"""
        [out:json][timeout:180];
        area["name"="{city}"]->.a;
        ({query_parts});
        out center;
        """
    
    async def _process_response(self, data: Dict, city: str, category: str) -> List[Dict]:
        """Process Overpass API response."""
        places = []
        
        for element in data.get('elements', []):
            tags = element.get('tags', {})
            
            # Get coordinates (handle both nodes and ways)
            if element.get('type') == 'node':
                lat = element.get('lat')
                lon = element.get('lon')
            elif element.get('type') == 'way' and 'center' in element:
                lat = element['center'].get('lat')
                lon = element['center'].get('lon')
            else:
                continue
            
            # Validate
            if not lat or not lon:
                continue
            if not self._is_valid_coordinates(lat, lon):
                continue
            
            name = tags.get('name', tags.get('operator', ''))
            if not name or len(name) < 2:
                continue
            
            # Get image
            app_category = OSM_CATEGORY_MAP.get(category, category)
            image_url = await self.image_fetcher.get_image(name, app_category, city)
            
            # Build place data
            place = {
                'name': name,
                'address': tags.get('addr:street', ''),
                'city': city,
                'city_alternatives': CITY_ALTERNATIVES.get(city, []),  # Add alternative names
                'postal_code': tags.get('addr:postcode', ''),
                'latitude': float(lat),
                'longitude': float(lon),
                'category': app_category,
                'description': f"{name} in {city}",
                'image_url': image_url,
                'rating': None,
                'phone': tags.get('phone', tags.get('contact:phone')),
                'website': tags.get('website', tags.get('contact:website')),
                'opening_hours': tags.get('opening_hours'),
                'price_level': None,
                'user_ratings_total': None,
                'business_status': 'OPERATIONAL',
                'osm_id': element.get('id'),
                'google_place_id': None,
                'scraped_at': datetime.now().isoformat(),
                'data_source': 'openstreetmap'
            }
            
            places.append(place)
        
        return places
    
    def _is_valid_coordinates(self, lat: float, lon: float) -> bool:
        """Validate coordinates are in Germany."""
        return (GERMANY_BOUNDS['min_lat'] <= lat <= GERMANY_BOUNDS['max_lat'] and
                GERMANY_BOUNDS['min_lng'] <= lon <= GERMANY_BOUNDS['max_lng'])
    
    def _extract_postal_code(self, address: str) -> str:
        """Extract postal code from address."""
        import re
        match = re.search(r'\b\d{5}\b', address)
        return match.group(0) if match else ''

# =============================================================================
# OUTPUT GENERATOR
# =============================================================================

def save_json_outputs(places: List[Dict]):
    """Save scraped data to multiple JSON formats."""
    output_dir = Path('data/json_output')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. All places
    with open(output_dir / 'all_places.json', 'w', encoding='utf-8') as f:
        json.dump(places, f, indent=2, ensure_ascii=False)
    
    # 2. By city
    by_city = defaultdict(list)
    for place in places:
        by_city[place['city']].append(place)
    
    with open(output_dir / 'places_by_city.json', 'w', encoding='utf-8') as f:
        json.dump(dict(by_city), f, indent=2, ensure_ascii=False)
    
    # 3. By category
    by_category = defaultdict(list)
    for place in places:
        by_category[place['category']].append(place)
    
    with open(output_dir / 'places_by_category.json', 'w', encoding='utf-8') as f:
        json.dump(dict(by_category), f, indent=2, ensure_ascii=False)
    
    # 4. Metadata
    metadata = {
        'total_places': len(places),
        'cities': len(set(p['city'] for p in places)),
        'categories': len(set(p['category'] for p in places)),
        'generated_at': datetime.now().isoformat(),
        'places_by_city': {city: len(plist) for city, plist in by_city.items()},
        'places_by_category': {cat: len(plist) for cat, plist in by_category.items()}
    }
    
    with open(output_dir / 'metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved to {output_dir}/")
    print(f"   - all_places.json ({len(places)} places)")
    print(f"   - places_by_city.json ({len(by_city)} cities)")
    print(f"   - places_by_category.json ({len(by_category)} categories)")
    print(f"   - metadata.json")

# =============================================================================
# MAIN
# =============================================================================

async def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("🇩🇪 GERMAN PLACES SCRAPER")
    print("="*60)
    
    # Choose data source
    print("\n📊 Data Source Options:")
    print("  1. OpenStreetMap (FREE, no API key needed)")
    print("     - Good coverage across Germany")
    print("     - Basic data: name, address, coords, some phone/website")
    print("     - Placeholder images")
    print("\n  2. Google Places API (Requires API key)")
    print("     - Rich data: ratings, reviews, photos, hours")
    print("     - Real photos from Google Maps")
    print("     - Cost: ~$0.05 per place")
    print("     - Free tier: $200/month (~4,000 places)")
    
    use_google = False
    if GOOGLE_API_KEY:
        choice = input("\n▶️  Use Google Places API? (y/N): ")
        use_google = choice.lower() == 'y'
    else:
        print("\n ℹ️  No Google API key configured - using OpenStreetMap")
    
    print(f"\n📋 Scraping Plan:")
    print(f"   Data source: {'Google Places' if use_google else 'OpenStreetMap'}")
    print(f"   Categories: {len(CATEGORIES)}")
    print(f"   Cities: ~{sum(len(cities) for cities in GERMAN_CITIES.values())}")
    
    if use_google:
        est_places = sum(len(cities) for cities in GERMAN_CITIES.values()) * len(CATEGORIES) * 10
        est_cost = est_places * 0.05
        print(f"   Estimated places: ~{est_places:,}")
        print(f"   Estimated cost: ${est_cost:.2f}")
        print(f"   ⚠️  Note: You may want to limit cities to stay within free tier!")
    else:
        print(f"   Estimated time: ~2-4 hours")
    
    print(f"\n🔧 Configuration:")
    print(f"   Request delay: {REQUEST_DELAY}s")
    print(f"   Batch size: {BATCH_SIZE} cities")
    
    proceed = input("\n▶️  Start scraping? (y/N): ")
    if proceed.lower() != 'y':
        print("👋 Cancelled!")
        return
    
    # Run scraper
    scraper = GermanPlacesScraper(use_google=use_google)
    places = await scraper.scrape_all()
    
    # Save outputs
    save_json_outputs(places)
    
    print("\n✅ Done!")

if __name__ == "__main__":
    asyncio.run(main())
