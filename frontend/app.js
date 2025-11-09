// Configuration
// Use 127.0.0.1 instead of localhost to bypass some extension blockers
const API_BASE = window.location.origin + '/api/v1';

// Global state
let currentUser = null;
let authToken = null;
let currentSection = 'dashboard';

// Place cache for quick lookups in detail modal
let allPlaces = [];
const placeCache = new Map();

function normalizePlaces(places = []) {
    return places.map(item => {
        if (!item) {
            return item;
        }

        if (item.place) {
            return { ...item.place, distance_km: item.distance_km };
        }

        return item;
    });
}

function updatePlaceCache(places = []) {
    places.forEach(place => {
        if (place && place.id) {
            placeCache.set(place.id, place);
        }
    });
}

function getPlaceFromCache(placeId) {
    return placeCache.get(Number(placeId));
}

// Helper function to make API calls using XMLHttpRequest (bypasses some extension blockers)
async function apiCall(url, options = {}) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        const method = options.method || 'GET';
        
        xhr.open(method, url, true);
        
        // Set headers
        if (options.headers) {
            Object.keys(options.headers).forEach(key => {
                xhr.setRequestHeader(key, options.headers[key]);
            });
        }
        
        xhr.onload = function() {
            try {
                const data = xhr.responseText ? JSON.parse(xhr.responseText) : null;
                resolve({
                    ok: xhr.status >= 200 && xhr.status < 300,
                    status: xhr.status,
                    data: data,
                    json: async () => data
                });
            } catch (e) {
                resolve({
                    ok: false,
                    status: xhr.status,
                    data: { detail: xhr.responseText || xhr.statusText },
                    json: async () => ({ detail: xhr.responseText || xhr.statusText })
                });
            }
        };
        
        xhr.onerror = function() {
            reject(new Error('Network request failed. Please check if browser extensions are blocking the request.'));
        };
        
        xhr.ontimeout = function() {
            reject(new Error('Request timeout'));
        };
        
        xhr.send(options.body || null);
    });
}

// DOM Elements
const authSection = document.getElementById('auth-section');
const mainApp = document.getElementById('main-app');
const loading = document.getElementById('loading');
const toast = document.getElementById('toast');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    const token = localStorage.getItem('authToken');
    if (token) {
        authToken = token;
        showMainApp();
        loadUserProfile();
        loadDashboardData();
    } else {
        showAuthSection();
    }
});

// Authentication Functions
function switchAuthTab(tab) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const tabs = document.querySelectorAll('.auth-tab');

    tabs.forEach(t => t.classList.remove('active'));
    
    if (tab === 'login') {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        tabs[0].classList.add('active');
    } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        tabs[1].classList.add('active');
    }
}

async function login(event) {
    event.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    showLoading();

    try {
        const response = await apiCall(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            authToken = data.access_token;
            localStorage.setItem('authToken', authToken);
            showToast('Login successful!', 'success');
            showMainApp();
            loadUserProfile();
            loadDashboardData();
        } else {
            showToast(data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        document.getElementById('browser-warning').style.display = 'block';
        showToast(error.message || 'Network error. Please check your browser extensions.', 'error');
    }

    hideLoading();
}

async function register(event) {
    event.preventDefault();
    
    const email = document.getElementById('register-email').value;
    const username = document.getElementById('register-username').value;
    const fullName = document.getElementById('register-fullname').value;
    const password = document.getElementById('register-password').value;

    showLoading();

    try {
        const response = await apiCall(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                username: username || null,
                full_name: fullName || null,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            showToast('Registration successful! Please login.', 'success');
            switchAuthTab('login');
            document.getElementById('login-email').value = email;
        } else {
            showToast(data.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        showToast('Network error. Please try again.', 'error');
    }

    hideLoading();
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    showAuthSection();
    showToast('Logged out successfully', 'success');
}

// Navigation Functions
function showSection(sectionName) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.remove('active'));
    
    document.getElementById(sectionName).classList.add('active');
    currentSection = sectionName;

    // Load section-specific data
    if (sectionName === 'dashboard') {
        loadDashboardData();
    } else if (sectionName === 'places') {
        loadPlaces();
    } else if (sectionName === 'checkins') {
        loadCheckins('all');
    } else if (sectionName === 'profile') {
        loadUserProfile();
    }

    // Close mobile menu
    const navMenu = document.querySelector('.nav-menu');
    navMenu.classList.remove('active');
}

function toggleMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.classList.toggle('active');
}

// UI Helper Functions
function showAuthSection() {
    authSection.classList.remove('hidden');
    mainApp.classList.add('hidden');
    document.getElementById('main-navbar').style.display = 'none';
}

function showMainApp() {
    authSection.classList.add('hidden');
    mainApp.classList.remove('hidden');
    document.getElementById('main-navbar').style.display = 'block';
}

function showLoading() {
    loading.classList.remove('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
}

function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// API Helper Functions
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (authToken) {
        headers.Authorization = `Bearer ${authToken}`;
    }

    try {
        const response = await apiCall(url, {
            ...options,
            headers
        });

        if (response.status === 401) {
            logout();
            throw new Error('Unauthorized');
        }

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'API request failed');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Dashboard Functions
async function loadDashboardData() {
    try {
        showLoading();
        
        // Load statistics
        const [places, users, myCheckins, recentCheckins] = await Promise.all([
            apiRequest('/places/'),
            apiRequest('/users/'),
            apiRequest('/checkins/my'),
            apiRequest('/checkins/?limit=5')
        ]);

        // Update stats - Show actual total count
        document.getElementById('total-places').textContent = places.length.toLocaleString();
        document.getElementById('total-users').textContent = users.length;
        document.getElementById('my-checkins').textContent = myCheckins.length;

        // Load place names for recent checkins
        const placeIds = [...new Set(recentCheckins.map(c => c.place_id))];
        const placesMap = {};
        
        for (const placeId of placeIds) {
            try {
                const place = await apiRequest(`/places/${placeId}`);
                placesMap[placeId] = place;
            } catch (error) {
                placesMap[placeId] = { name: `Place ID ${placeId}` };
            }
        }

        // Load people nearby
        await loadPeopleNearby(places);

        // Update recent checkins
        const recentCheckinsContainer = document.getElementById('recent-checkins');
        recentCheckinsContainer.innerHTML = '';

        if (recentCheckins.length === 0) {
            recentCheckinsContainer.innerHTML = '<p class="text-muted">No recent check-ins</p>';
        } else {
            recentCheckins.forEach(checkin => {
                checkin.place_name = placesMap[checkin.place_id]?.name || `Place ID ${checkin.place_id}`;
                recentCheckinsContainer.appendChild(createCheckinCard(checkin));
            });
        }

    } catch (error) {
        showToast('Failed to load dashboard data', 'error');
    }

    hideLoading();
}

async function loadPeopleNearby(places) {
    const container = document.getElementById('people-nearby-list');
    container.innerHTML = '<p style="color: #999;">Loading people nearby...</p>';
    
    try {
        // Get all active checkins
        const checkins = await apiRequest('/checkins/?active_only=true&limit=50');
        
        if (checkins.length === 0) {
            container.innerHTML = '<p style="color: #999;">No one is checked in right now. Be the first! 🎉</p>';
            return;
        }
        
        // Get user and place info for each checkin
        const peopleData = [];
        for (const checkin of checkins.slice(0, 12)) { // Limit to 12 people
            try {
                const [user, place] = await Promise.all([
                    apiRequest(`/users/${checkin.user_id}`),
                    apiRequest(`/places/${checkin.place_id}`)
                ]);
                
                // Calculate time remaining
                const checkinTime = new Date(checkin.check_in_time);
                const endTime = new Date(checkinTime.getTime() + checkin.duration_hours * 60 * 60 * 1000);
                const now = new Date();
                const timeLeft = endTime - now;
                const hoursLeft = Math.max(0, Math.floor(timeLeft / (1000 * 60 * 60)));
                const minutesLeft = Math.max(0, Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60)));
                
                if (timeLeft > 0) {
                    peopleData.push({
                        user,
                        place,
                        checkin,
                        hoursLeft,
                        minutesLeft
                    });
                }
            } catch (error) {
                console.error('Failed to load person data:', error);
            }
        }
        
        if (peopleData.length === 0) {
            container.innerHTML = '<p style="color: #999;">No active users nearby right now.</p>';
            return;
        }
        
        container.innerHTML = peopleData.map(data => {
            const { user, place, checkin, hoursLeft, minutesLeft } = data;
            const timeLeftStr = hoursLeft > 0 ? `${hoursLeft}h ${minutesLeft}m` : `${minutesLeft}m`;
            const languages = user.languages && user.languages.length > 0 
                ? user.languages.join(', ') 
                : '';
            const interests = user.interests && user.interests.length > 0 
                ? user.interests.join(', ') 
                : '';
            
            return `
                <div style="background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;">
                        <div>
                            <h4 style="margin: 0; color: #333; font-size: 1rem;">${user.full_name || user.username || 'Anonymous'}</h4>
                            ${user.why_here ? `<span style="font-size: 0.75rem; color: #888;">📍 ${user.why_here}</span>` : ''}
                        </div>
                        <span style="background: #ff6b6b; color: white; padding: 0.25rem 0.5rem; border-radius: 12px; font-size: 0.75rem; font-weight: 500;">⏱ ${timeLeftStr}</span>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 0.5rem; border-radius: 4px; margin-bottom: 0.75rem;">
                        <div style="font-size: 0.85rem; color: #555;">
                            <strong>📍 ${place.name}</strong>
                        </div>
                        <div style="font-size: 0.75rem; color: #888;">${place.city}</div>
                    </div>
                    
                    ${user.bio ? `<p style="font-size: 0.85rem; color: #666; margin: 0.5rem 0;">${user.bio}</p>` : ''}
                    
                    ${languages ? `<div style="font-size: 0.75rem; color: #888; margin-top: 0.5rem;">🗣️ ${languages}</div>` : ''}
                    ${interests ? `<div style="font-size: 0.75rem; color: #888; margin-top: 0.25rem;">💡 ${interests}</div>` : ''}
                    
                    ${checkin.message ? `<p style="font-size: 0.85rem; color: #4a90e2; margin-top: 0.75rem; padding: 0.5rem; background: #e3f2fd; border-radius: 4px; font-style: italic;">"${checkin.message}"</p>` : ''}
                </div>
            `;
        }).join('');
        
    } catch (error) {
        console.error('Failed to load people nearby:', error);
        container.innerHTML = '<p style="color: #999;">Failed to load people nearby.</p>';
    }
}

// Places Functions

async function loadPlaces() {
    try {
        showLoading();
        const places = await apiRequest('/places/');
        allPlaces = normalizePlaces(places);
        updatePlaceCache(allPlaces);
        displayPlaces(allPlaces);
    } catch (error) {
        showToast('Failed to load places', 'error');
    }
    hideLoading();
}

function displayPlaces(places = []) {
    const placesGrid = document.getElementById('places-grid');
    placesGrid.innerHTML = '';

    const normalizedPlaces = normalizePlaces(places);
    updatePlaceCache(normalizedPlaces);

    if (normalizedPlaces.length === 0) {
        placesGrid.innerHTML = '<p class="text-muted">No places found</p>';
        return;
    }

    normalizedPlaces.forEach(place => {
        placesGrid.appendChild(createPlaceCard(place));
    });
}

function createPlaceCard(place) {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.addEventListener('click', () => openPlaceDetails(place.id));

    const safePlaceName = JSON.stringify(place.name || 'Place');
    const distanceBadge = typeof place.distance_km === 'number'
        ? `<span class="place-distance">${place.distance_km.toFixed(1)} km away</span>`
        : '';
    
    card.innerHTML = `
        <div class="place-image">
            ${place.image_url ? 
                `<img src="${place.image_url}" alt="${place.name}" onerror="this.style.display='none'">` : 
                '<i class="fas fa-map-marker-alt"></i>'
            }
        </div>
        <div class="place-content">
            <h3>${place.name}</h3>
            <p>${place.description || 'No description available'}</p>
            <div class="place-meta">
                <span class="place-category">${place.category}</span>
                <span class="place-location">${place.city}</span>
            </div>
            ${distanceBadge}
            <div class="place-location">
                <i class="fas fa-map-marker-alt"></i> ${place.address}
            </div>
            <div class="place-actions">
                <button class="btn btn-secondary" type="button" onclick="event.stopPropagation(); openPlaceDetails(${place.id})">
                    <i class="fas fa-eye"></i> View details
                </button>
                <button class="btn btn-primary" type="button" onclick="event.stopPropagation(); showCheckinModal(${place.id}, ${safePlaceName})">
                    <i class="fas fa-check-circle"></i> Check-in
                </button>
            </div>
        </div>
    `;
    
    return card;
}

function formatOpeningHours(openingHours) {
    if (!openingHours) {
        return null;
    }

    if (Array.isArray(openingHours)) {
        return openingHours.join('<br>');
    }

    if (typeof openingHours === 'object') {
        return Object.entries(openingHours)
            .map(([day, hours]) => `${day}: ${hours}`)
            .join('<br>');
    }

    return openingHours;
}

async function openPlaceDetails(placeId) {
    try {
        let place = getPlaceFromCache(placeId);

        if (!place) {
            const response = await apiRequest(`/places/${placeId}`);
            const [normalized] = normalizePlaces([response]);
            place = normalized;
            updatePlaceCache([place]);
        }

        renderPlaceDetails(place);
        document.getElementById('place-details-modal').classList.add('show');
    } catch (error) {
        console.error('Failed to open place details:', error);
        showToast('Failed to load place details', 'error');
    }
}

function renderPlaceDetails(place) {
    const nameEl = document.getElementById('place-details-name');
    const descriptionEl = document.getElementById('place-details-description');
    const addressEl = document.getElementById('place-details-address');
    const metaEl = document.getElementById('place-details-meta');
    const contactEl = document.getElementById('place-details-contact');
    const hoursEl = document.getElementById('place-details-hours');
    const ratingEl = document.getElementById('place-details-rating');
    const distanceEl = document.getElementById('place-details-distance');
    const checkinBtn = document.getElementById('place-details-checkin-btn');

    nameEl.textContent = place.name || 'Place';
    descriptionEl.innerHTML = place.description || 'No description yet.';
    addressEl.innerHTML = `
        <strong><i class="fas fa-map-marker-alt"></i> Address:</strong>
        <span>${place.address || 'n/a'}, ${place.postal_code || ''} ${place.city || ''}</span>
    `;

    metaEl.innerHTML = `
        <span class="details-pill">${place.category || 'Uncategorized'}</span>
        ${place.country ? `<span class="details-pill">${place.country}</span>` : ''}
    `;

    if (typeof place.distance_km === 'number') {
        distanceEl.innerHTML = `<i class="fas fa-location-arrow"></i> ${place.distance_km.toFixed(1)} km away from you`;
        distanceEl.style.display = 'block';
    } else {
        distanceEl.style.display = 'none';
    }

    if (place.phone || place.website) {
        const phoneHtml = place.phone ? `<div><i class="fas fa-phone"></i> <a href="tel:${place.phone}">${place.phone}</a></div>` : '';
        const websiteHtml = place.website ? `<div><i class="fas fa-globe"></i> <a href="${place.website}" target="_blank" rel="noopener">Website</a></div>` : '';
        contactEl.innerHTML = `<strong>Contact</strong>${phoneHtml}${websiteHtml}`;
        contactEl.style.display = 'block';
    } else {
        contactEl.style.display = 'none';
    }

    const formattedHours = formatOpeningHours(place.opening_hours);
    if (formattedHours) {
        hoursEl.innerHTML = `<strong>Opening hours</strong><p>${formattedHours}</p>`;
        hoursEl.style.display = 'block';
    } else {
        hoursEl.style.display = 'none';
    }

    if (place.rating) {
        const reviews = place.user_ratings_total ? ` (${place.user_ratings_total} reviews)` : '';
        ratingEl.innerHTML = `<strong>Rating</strong><p>⭐ ${place.rating}${reviews}</p>`;
        ratingEl.style.display = 'block';
    } else {
        ratingEl.style.display = 'none';
    }

    checkinBtn.onclick = () => {
        closeModal('place-details-modal');
        showCheckinModal(place.id, place.name || '');
    };
}

async function filterPlaces() {
    const searchTerm = document.getElementById('place-search').value.trim();
    const categoryFilter = document.getElementById('category-filter').value;
    
    try {
        let filtered = [...allPlaces];

        if (searchTerm) {
            const term = searchTerm.toLowerCase();
            filtered = filtered.filter(place => {
                const nameMatch = place.name && place.name.toLowerCase().includes(term);
                const cityMatch = place.city && place.city.toLowerCase().includes(term);
                const postalCode = place.postal_code ? String(place.postal_code).toLowerCase() : '';
                const postalMatch = postalCode.includes(term);
                const addressMatch = place.address && place.address.toLowerCase().includes(term);
                return nameMatch || cityMatch || postalMatch || addressMatch;
            });
        }

        if (categoryFilter) {
            filtered = filtered.filter(place => place.category === categoryFilter);
        }

        displayPlaces(filtered);
    } catch (error) {
        console.error('Filter error:', error);
        displayPlaces(allPlaces);
    }
}

// GPS Location Function
async function useMyLocation() {
    if (!navigator.geolocation) {
        showToast('Geolocation is not supported by your browser', 'error');
        return;
    }

    showLoading();
    showToast('Getting your location...', 'info');

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            const radius = 5; // 5 km default radius

            try {
                const nearbyResponse = await apiRequest(
                    `/places/nearby/gps?lat=${latitude}&lng=${longitude}&radius=${radius}`
                );
                const nearbyPlaces = normalizePlaces(nearbyResponse);
                
                if (nearbyPlaces.length === 0) {
                    showToast('No places found within 5km', 'info');
                } else {
                    showToast(`Found ${nearbyPlaces.length} places nearby!`, 'success');
                    displayPlaces(nearbyPlaces);
                }
            } catch (error) {
                showToast('Failed to load nearby places', 'error');
            }
            hideLoading();
        },
        (error) => {
            hideLoading();
            let errorMsg = 'Unable to get your location';
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    errorMsg = 'Location permission denied. Please enable location access.';
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMsg = 'Location information unavailable.';
                    break;
                case error.TIMEOUT:
                    errorMsg = 'Location request timed out.';
                    break;
            }
            showToast(errorMsg, 'error');
        }
    );
}

async function createPlace(event) {
    event.preventDefault();
    
    const placeData = {
        name: document.getElementById('place-name').value,
        description: document.getElementById('place-description').value || null,
        address: document.getElementById('place-address').value,
        city: document.getElementById('place-city').value,
        postal_code: document.getElementById('place-postal').value,
        latitude: parseFloat(document.getElementById('place-latitude').value),
        longitude: parseFloat(document.getElementById('place-longitude').value),
        category: document.getElementById('place-category').value,
        image_url: document.getElementById('place-image').value || null
    };

    try {
        showLoading();
        await apiRequest('/places/', {
            method: 'POST',
            body: JSON.stringify(placeData)
        });
        
        showToast('Place created successfully!', 'success');
        closeModal('create-place-modal');
        loadPlaces();
        
        // Reset form
        event.target.reset();
    } catch (error) {
        showToast(error.message || 'Failed to create place', 'error');
    }
    
    hideLoading();
}

// Check-ins Functions
async function loadCheckins(type = 'all') {
    try {
        showLoading();
        const endpoint = type === 'my' ? '/checkins/my' : '/checkins';
        const checkins = await apiRequest(endpoint);
        
        // Load place names for all checkins
        const placeIds = [...new Set(checkins.map(c => c.place_id))];
        const placesMap = {};
        
        for (const placeId of placeIds) {
            try {
                const place = await apiRequest(`/places/${placeId}`);
                placesMap[placeId] = place;
            } catch (error) {
                placesMap[placeId] = { name: `Place ID ${placeId}` };
            }
        }
        
        // Add place names to checkins
        checkins.forEach(checkin => {
            checkin.place_name = placesMap[checkin.place_id]?.name || `Place ID ${checkin.place_id}`;
        });
        
        displayCheckins(checkins);
    } catch (error) {
        showToast('Failed to load check-ins', 'error');
    }
    hideLoading();
}

function displayCheckins(checkins) {
    const checkinsList = document.getElementById('checkins-list');
    checkinsList.innerHTML = '';

    if (checkins.length === 0) {
        checkinsList.innerHTML = '<p class="text-muted">No check-ins found</p>';
        return;
    }

    checkins.forEach(checkin => {
        checkinsList.appendChild(createCheckinCard(checkin));
    });
}

function createCheckinCard(checkin) {
    const card = document.createElement('div');
    card.className = 'checkin-card';
    
    // Use place name if available, otherwise fall back to place ID
    const placeName = checkin.place_name || `Place ID: ${checkin.place_id}`;
    const isMyCheckin = currentUser && checkin.user_id === currentUser.id;
    const canEnd = isMyCheckin && checkin.status === 'active';
    const canDelete = isMyCheckin;
    
    card.innerHTML = `
        <div class="checkin-header">
            <div class="checkin-info">
                <h4>${placeName}</h4>
                <p>User ID: ${checkin.user_id}</p>
                ${checkin.check_out_time ? 
                    `<p>Checked out: ${new Date(checkin.check_out_time).toLocaleString()}</p>` : 
                    ''
                }
            </div>
            <div class="checkin-time">
                <div>${new Date(checkin.check_in_time).toLocaleDateString()}</div>
                <div>${new Date(checkin.check_in_time).toLocaleTimeString()}</div>
            </div>
        </div>
        ${checkin.message ? `<div class="checkin-message">"${checkin.message}"</div>` : ''}
        <div class="checkin-actions">
            <span class="checkin-status ${checkin.status}">${checkin.status}</span>
            <div>
                ${canEnd ? `<button class="btn btn-primary btn-sm" onclick="endCheckin(${checkin.id})">End Check-in</button>` : ''}
                ${canDelete ? `<button class="btn btn-danger btn-sm" onclick="deleteCheckin(${checkin.id})">Delete</button>` : ''}
            </div>
        </div>
    `;
    
    return card;
}

function switchCheckinsTab(type) {
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    if (type === 'my') {
        tabs[1].classList.add('active');
    } else {
        tabs[0].classList.add('active');
    }
    
    loadCheckins(type);
}

async function checkinToPlace(event) {
    event.preventDefault();
    
    const placeId = document.getElementById('checkin-place-id').value;
    const message = document.getElementById('checkin-message').value;
    const duration = parseInt(document.getElementById('checkin-duration').value);
    
    const checkinData = {
        place_id: parseInt(placeId),
        message: message || null,
        duration_hours: duration
    };

    try {
        showLoading();
        await apiRequest('/checkins/', {
            method: 'POST',
            body: JSON.stringify(checkinData)
        });
        
        showToast(`Check-in successful! You're here for ${duration} hour${duration > 1 ? 's' : ''} 🎉`, 'success');
        closeModal('checkin-modal');
        
        // Refresh data if on relevant sections
        if (currentSection === 'checkins') {
            loadCheckins('all');
        } else if (currentSection === 'dashboard') {
            loadDashboardData();
        } else if (currentSection === 'places') {
            loadPlaces();
        }
        
        // Reset form
        event.target.reset();
    } catch (error) {
        showToast(error.message || 'Failed to check-in', 'error');
    }
    
    hideLoading();
}

async function endCheckin(checkinId) {
    if (!confirm('Are you sure you want to end this check-in?')) {
        return;
    }

    try {
        showLoading();
        await apiRequest(`/checkins/${checkinId}/end`, {
            method: 'POST'
        });
        
        showToast('Check-in ended successfully!', 'success');
        
        // Refresh current view
        if (currentSection === 'checkins') {
            const activeTab = document.querySelector('.tab-btn.active');
            const tabType = activeTab.textContent.includes('My') ? 'my' : 'all';
            loadCheckins(tabType);
        } else if (currentSection === 'dashboard') {
            loadDashboardData();
        }
    } catch (error) {
        showToast(error.message || 'Failed to end check-in', 'error');
    }
    
    hideLoading();
}

async function deleteCheckin(checkinId) {
    if (!confirm('Are you sure you want to delete this check-in? This action cannot be undone.')) {
        return;
    }

    try {
        showLoading();
        await apiRequest(`/checkins/${checkinId}`, {
            method: 'DELETE'
        });
        
        showToast('Check-in deleted successfully!', 'success');
        
        // Refresh current view
        if (currentSection === 'checkins') {
            const activeTab = document.querySelector('.tab-btn.active');
            const tabType = activeTab.textContent.includes('My') ? 'my' : 'all';
            loadCheckins(tabType);
        } else if (currentSection === 'dashboard') {
            loadDashboardData();
        }
    } catch (error) {
        showToast(error.message || 'Failed to delete check-in', 'error');
    }
    
    hideLoading();
}

// Profile Functions
let userLanguages = [];
let userInterests = [];

async function loadUserProfile() {
    try {
        const user = await apiRequest('/auth/me');
        currentUser = user;
        
        // Display name and email
        document.getElementById('profile-name').textContent = user.full_name || user.username || 'No name set';
        document.getElementById('profile-email').textContent = user.email;
        
        // Fill form fields
        document.getElementById('profile-username').value = user.username || '';
        document.getElementById('profile-fullname').value = user.full_name || '';
        document.getElementById('profile-bio').value = user.bio || '';
        document.getElementById('profile-why-here').value = user.why_here || '';
        
        // Load languages and interests
        userLanguages = user.languages || [];
        userInterests = user.interests || [];
        renderLanguageTags();
        renderInterestTags();
    } catch (error) {
        showToast('Failed to load profile', 'error');
    }
}

function renderLanguageTags() {
    const container = document.getElementById('profile-languages-tags');
    container.innerHTML = userLanguages.map(lang => `
        <span style="background: #4a90e2; color: white; padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.5rem;">
            ${lang}
            <button type="button" onclick="removeLanguage('${lang}')" style="background: none; border: none; color: white; cursor: pointer; padding: 0; font-size: 1rem; line-height: 1;">×</button>
        </span>
    `).join('');
}

function renderInterestTags() {
    const container = document.getElementById('profile-interests-tags');
    container.innerHTML = userInterests.map(interest => `
        <span style="background: #2ecc71; color: white; padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.5rem;">
            ${interest}
            <button type="button" onclick="removeInterest('${interest}')" style="background: none; border: none; color: white; cursor: pointer; padding: 0; font-size: 1rem; line-height: 1;">×</button>
        </span>
    `).join('');
}

function addLanguage() {
    const input = document.getElementById('new-language');
    const language = input.value.trim();
    
    if (language && !userLanguages.includes(language)) {
        userLanguages.push(language);
        renderLanguageTags();
        input.value = '';
    }
}

function removeLanguage(language) {
    userLanguages = userLanguages.filter(l => l !== language);
    renderLanguageTags();
}

function addInterest() {
    const input = document.getElementById('new-interest');
    const interest = input.value.trim();
    
    if (interest && !userInterests.includes(interest)) {
        userInterests.push(interest);
        renderInterestTags();
        input.value = '';
    }
}

function removeInterest(interest) {
    userInterests = userInterests.filter(i => i !== interest);
    renderInterestTags();
}

async function updateProfile(event) {
    event.preventDefault();
    
    const profileData = {
        username: document.getElementById('profile-username').value || null,
        full_name: document.getElementById('profile-fullname').value || null,
        bio: document.getElementById('profile-bio').value || null,
        languages: userLanguages.length > 0 ? userLanguages : null,
        interests: userInterests.length > 0 ? userInterests : null,
        why_here: document.getElementById('profile-why-here').value || null
    };
    
    try {
        showLoading();
        await apiRequest(`/users/${currentUser.id}`, {
            method: 'PUT',
            body: JSON.stringify(profileData)
        });
        
        showToast('Profile updated successfully! 🎉', 'success');
        await loadUserProfile();
    } catch (error) {
        showToast(error.message || 'Failed to update profile', 'error');
    }
    
    hideLoading();
}

// Modal Functions
function showCreatePlaceModal() {
    document.getElementById('create-place-modal').classList.add('show');
}

async function showCheckinModal(placeId, placeName) {
    document.getElementById('checkin-place-id').value = placeId;
    document.getElementById('checkin-place-name').textContent = placeName;
    
    // Load active users at this place
    await loadActiveUsersAtPlace(placeId);
    
    document.getElementById('checkin-modal').classList.add('show');
}

async function loadActiveUsersAtPlace(placeId) {
    const listContainer = document.getElementById('active-users-list');
    
    try {
        const activeUsers = await apiRequest(`/checkins/place/${placeId}/active`);
        
        if (activeUsers.length === 0) {
            listContainer.innerHTML = '<p style="color: #999; font-size: 0.85rem; margin: 0;">No one here yet. Be the first! 🎉</p>';
        } else {
            listContainer.innerHTML = activeUsers.map(user => {
                const languages = user.languages && user.languages.length > 0 
                    ? user.languages.join(', ') 
                    : 'No languages listed';
                const interests = user.interests && user.interests.length > 0 
                    ? user.interests.join(', ') 
                    : 'No interests listed';
                
                const timeLeft = user.hours_left > 0 
                    ? `${user.hours_left}h ${user.minutes_left}m left`
                    : `${user.minutes_left}m left`;
                
                return `
                    <div style="padding: 0.75rem; margin-bottom: 0.5rem; background: white; border-radius: 4px; border: 1px solid #e0e0e0;">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.25rem;">
                            <strong style="color: #333; font-size: 0.9rem;">${user.username || user.full_name || 'Anonymous'}</strong>
                            <span style="font-size: 0.75rem; color: #ff6b6b; font-weight: 500;">⏱ ${timeLeft}</span>
                        </div>
                        ${user.bio ? `<p style="font-size: 0.8rem; color: #666; margin: 0.25rem 0;">${user.bio}</p>` : ''}
                        <div style="font-size: 0.75rem; color: #888; margin-top: 0.25rem;">
                            <div>🗣️ ${languages}</div>
                            <div>💡 ${interests}</div>
                            ${user.why_here ? `<div>📍 ${user.why_here}</div>` : ''}
                        </div>
                        ${user.message ? `<p style="font-size: 0.8rem; color: #4a90e2; margin-top: 0.5rem; font-style: italic;">"${user.message}"</p>` : ''}
                    </div>
                `;
            }).join('');
        }
    } catch (error) {
        console.error('Failed to load active users:', error);
        listContainer.innerHTML = '<p style="color: #999; font-size: 0.85rem;">Unable to load active users</p>';
    }
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

// Close modals when clicking outside
window.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('show');
    }
});

// Close modals with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.remove('show');
        });
    }
});