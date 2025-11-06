# 🎨 Zutreffen Frontend

A beautiful, responsive web interface for the Zutreffen API.

## 🌐 Access the Frontend

**Primary URL (served by FastAPI):**
```
http://localhost:8001/
```

**Alternative (direct file access):**
Open `frontend/index.html` in your browser

## ✨ Features

### 🔐 Authentication
- ✅ Login modal with form validation
- ✅ Registration with optional profile fields
- ✅ JWT token storage in localStorage
- ✅ Automatic session persistence
- ✅ Logout functionality

### 📍 Places
- ✅ Browse all places with images
- ✅ Filter by city and category
- ✅ Responsive grid layout
- ✅ Real-time check-in button
- ✅ Beautiful card design

### ✅ Check-ins
- ✅ View active check-ins
- ✅ Create new check-ins (with message)
- ✅ End your check-ins
- ✅ View your check-in history
- ✅ One active check-in limit

### 🎨 UI/UX
- ✅ Modern, clean design
- ✅ Responsive (mobile-friendly)
- ✅ Toast notifications
- ✅ Modal dialogs
- ✅ Smooth animations
- ✅ Color-coded categories
- ✅ Status badges

## 🖼️ Screenshots

### Login Screen
Beautiful modal with login/register toggle

### Places Grid
Cards with images, categories, and check-in buttons

### Check-ins Feed
Real-time activity from all users

## 🚀 Quick Start

1. **Start the Backend**
   ```bash
   cd /home/ahmad/projects/zutreffen
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

2. **Open Browser**
   ```
   http://localhost:8001/
   ```

3. **Login**
   ```
   Email: max.mueller@example.com
   Password: password123
   ```

4. **Start Exploring!**
   - Browse places
   - Check in
   - See who's where

## 📱 Responsive Design

Works perfectly on:
- 💻 Desktop (1920px+)
- 💼 Laptop (1024px+)
- 📱 Tablet (768px+)
- 📱 Mobile (320px+)

## 🎨 Color Scheme

```css
Primary:   #6366f1 (Indigo)
Secondary: #8b5cf6 (Purple)
Success:   #10b981 (Green)
Danger:    #ef4444 (Red)
```

## 📂 Files

```
frontend/
├── index.html      # Main HTML structure
├── style.css       # All styles and responsive design
└── app.js          # JavaScript logic and API calls
```

## 🔧 Customization

### Change Colors
Edit `style.css` `:root` variables:
```css
:root {
    --primary: #6366f1;
    --secondary: #8b5cf6;
    /* ... */
}
```

### Change API Endpoint
Edit `app.js`:
```javascript
const API_BASE = 'http://localhost:8001/api/v1';
```

### Add New Sections
1. Add HTML in `index.html`
2. Add styles in `style.css`
3. Add logic in `app.js`

## 🐛 Troubleshooting

### "Cannot read property..."
- Make sure the backend is running on port 8001
- Check browser console for errors

### Login doesn't work
- Verify API is accessible at `http://localhost:8001/api/v1`
- Check CORS settings in backend
- Open DevTools Network tab to see requests

### Images not loading
- Check internet connection (images from Unsplash)
- Replace with local images if needed

## 🚧 Next Steps

### Planned Features
- [ ] User profile editing
- [ ] Place search by name
- [ ] Map view with geolocation
- [ ] Real-time updates (WebSocket)
- [ ] Push notifications
- [ ] Dark mode toggle
- [ ] Place ratings and reviews
- [ ] Photo uploads
- [ ] Social features (follow users)
- [ ] Chat between users at same place

### Technical Improvements
- [ ] Service Worker (offline support)
- [ ] PWA manifest
- [ ] Image lazy loading
- [ ] Infinite scroll
- [ ] State management (e.g., Redux)
- [ ] TypeScript migration
- [ ] Build process (Vite/Webpack)
- [ ] Unit tests

## 💡 Usage Tips

### Login Shortcut
The hint below the login form shows test credentials

### Test Different Users
All seeded users have password: `password123`

- max.mueller@example.com
- anna.schmidt@example.com
- lukas.weber@example.com
- ... (see mock_data/users.py)

### Mobile Testing
1. Find your computer's IP: `ip addr show`
2. Access from phone: `http://YOUR_IP:8001`
3. Make sure firewall allows port 8001

## 🎯 Key Features Explained

### Auto Login
- Token stored in localStorage
- Auto-login on page reload
- Session persists across tabs

### Toast Notifications
- Success: Green
- Error: Red
- Auto-dismiss after 3 seconds

### Modal System
- Click outside to close
- ESC key support
- Smooth animations

### Real-time Updates
- Check-ins refresh after actions
- Places update after filtering
- UI updates immediately

## 📖 API Integration

All API calls in `app.js`:

```javascript
// Login
fetch(`${API_BASE}/auth/login/json`, {...})

// Get places
fetch(`${API_BASE}/places/`)

// Create check-in
fetch(`${API_BASE}/checkins/`, {
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
```

## 🎓 Learning Resources

This frontend demonstrates:
- Vanilla JavaScript (no frameworks)
- Modern CSS (Grid, Flexbox)
- Fetch API for REST calls
- JWT authentication
- LocalStorage usage
- Responsive design
- Modal patterns
- Toast notifications

## ✅ Browser Support

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Optimized

## 📝 License

MIT - Same as backend
