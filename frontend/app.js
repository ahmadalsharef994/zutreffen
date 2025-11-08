// Configuration
const API_BASE = 'http://localhost:8001/api/v1';

// Global state
let currentUser = null;
let authToken = null;
let currentSection = 'dashboard';

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
        const response = await fetch(`${API_BASE}/auth/login`, {
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
        showToast('Network error. Please try again.', 'error');
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
        const response = await fetch(`${API_BASE}/auth/register`, {
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
        const response = await fetch(url, {
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

// Places Functions
let allPlaces = []; // Store all places for filtering

async function loadPlaces() {
    try {
        showLoading();
        const places = await apiRequest('/places/');
        allPlaces = places; // Store for filtering
        displayPlaces(places);
        await populateFilters(); // Load cities from API
    } catch (error) {
        showToast('Failed to load places', 'error');
    }
    hideLoading();
}

function displayPlaces(places) {
    const placesGrid = document.getElementById('places-grid');
    placesGrid.innerHTML = '';

    if (places.length === 0) {
        placesGrid.innerHTML = '<p class="text-muted">No places found</p>';
        return;
    }

    places.forEach(place => {
        placesGrid.appendChild(createPlaceCard(place));
    });
}

function createPlaceCard(place) {
    const card = document.createElement('div');
    card.className = 'place-card';
    
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
            <div class="place-location">
                <i class="fas fa-map-marker-alt"></i> ${place.address}
            </div>
            <button class="btn btn-primary" style="margin-top: 1rem; width: 100%;" onclick="showCheckinModal(${place.id}, '${place.name}')">
                <i class="fas fa-check-circle"></i> Check-in
            </button>
        </div>
    `;
    
    return card;
}

async function populateFilters() {
    try {
        // Load cities from the API
        const cities = await apiRequest('/places/cities/all');
        const cityFilter = document.getElementById('city-filter');
        
        // Clear existing options except "All Cities"
        cityFilter.innerHTML = '<option value="">All Cities</option>';
        
        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            cityFilter.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to load cities:', error);
    }
}

async function filterPlaces() {
    const searchTerm = document.getElementById('place-search').value.trim();
    const cityFilter = document.getElementById('city-filter').value;
    const categoryFilter = document.getElementById('category-filter').value;
    
    try {
        showLoading();
        let places;
        
        // Use backend API for filtering
        if (searchTerm) {
            // Text search
            places = await apiRequest(`/places/search/text?query=${encodeURIComponent(searchTerm)}`);
        } else if (cityFilter) {
            // Filter by city
            places = allPlaces.filter(p => p.city === cityFilter);
        } else {
            // Show all places
            places = allPlaces;
        }
        
        // Apply category filter if selected
        if (categoryFilter) {
            places = places.filter(p => p.category === categoryFilter);
        }
        
        displayPlaces(places);
        hideLoading();
    } catch (error) {
        console.error('Filter error:', error);
        // Fallback to client-side filtering
        let filtered = allPlaces;
        
        if (searchTerm) {
            const term = searchTerm.toLowerCase();
            filtered = filtered.filter(p => 
                p.name.toLowerCase().includes(term) || 
                (p.description && p.description.toLowerCase().includes(term))
            );
        }
        
        if (cityFilter) {
            filtered = filtered.filter(p => p.city === cityFilter);
        }
        
        if (categoryFilter) {
            filtered = filtered.filter(p => p.category === categoryFilter);
        }
        
        displayPlaces(filtered);
        hideLoading();
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
                const places = await apiRequest(
                    `/places/nearby/gps?latitude=${latitude}&longitude=${longitude}&radius=${radius}`
                );
                
                if (places.length === 0) {
                    showToast('No places found within 5km', 'info');
                } else {
                    showToast(`Found ${places.length} places nearby!`, 'success');
                    displayPlaces(places);
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
    
    const checkinData = {
        place_id: parseInt(placeId),
        message: message || null
    };

    try {
        showLoading();
        await apiRequest('/checkins', {
            method: 'POST',
            body: JSON.stringify(checkinData)
        });
        
        showToast('Check-in successful!', 'success');
        closeModal('checkin-modal');
        
        // Refresh data if on relevant sections
        if (currentSection === 'checkins') {
            loadCheckins('all');
        } else if (currentSection === 'dashboard') {
            loadDashboardData();
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
async function loadUserProfile() {
    try {
        const user = await apiRequest('/auth/me');
        currentUser = user;
        
        document.getElementById('profile-name').textContent = user.full_name || 'No name set';
        document.getElementById('profile-email').textContent = user.email;
        document.getElementById('profile-username').textContent = user.username || 'No username set';
        document.getElementById('profile-bio').textContent = user.bio || 'No bio set';
    } catch (error) {
        showToast('Failed to load profile', 'error');
    }
}

// Modal Functions
function showCreatePlaceModal() {
    document.getElementById('create-place-modal').classList.add('show');
}

function showCheckinModal(placeId, placeName) {
    document.getElementById('checkin-place-id').value = placeId;
    document.getElementById('checkin-place-name').textContent = placeName;
    document.getElementById('checkin-modal').classList.add('show');
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