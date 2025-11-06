# 🎯 Zutreffen

A modern FastAPI application that helps people meet in public places across Germany.

## ✨ Features

- 🔐 **Full Authentication** - JWT-based login/register
- 📍 **Places** - Real German locations with GPS coordinates
- ✅ **Check-ins** - See who's where right now
- 👥 **User Profiles** - Avatars, bios, and more
- 🗺️ **Geographic Search** - Filter by city and category
- 🔒 **Protected Routes** - Secure API endpoints
- 📚 **Interactive Docs** - Swagger UI + ReDoc

## 🚀 Quick Start

```bash
# Start the server

uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**Access the app:**
- API: http://localhost:8001
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 🔑 Test Login

```
Email: max.mueller@example.com
Password: password123
```



## 🧪 Testing

```bash
# Test basic API
python3 test_api.py

# Test authentication
python3 test_auth.py
```

## 📊 Current Database

- **10 Users** - German profiles with avatars
- **21 Places** - Across 7 German cities
- **30 Check-ins** - Real-time activity

### Cities
Berlin • Munich • Hamburg • Frankfurt • Cologne • Stuttgart • Düsseldorf

### Categories
☕ Cafés • 💼 Coworking • 🌳 Parks

## 📡 API Endpoints

### Authentication
```
POST   /api/v1/auth/register     - Register new user
POST   /api/v1/auth/login        - Login (OAuth2)
POST   /api/v1/auth/login/json   - Login (JSON)
GET    /api/v1/auth/me           - Get current user
POST   /api/v1/auth/logout       - Logout
```

### Places
```
GET    /api/v1/places/           - List all places
GET    /api/v1/places/{id}       - Get place
POST   /api/v1/places/           - Create place 🔒
PUT    /api/v1/places/{id}       - Update place 🔒
DELETE /api/v1/places/{id}       - Delete place 🔒
```

### Check-ins
```
GET    /api/v1/checkins/         - List all check-ins
GET    /api/v1/checkins/my       - My check-ins 🔒
POST   /api/v1/checkins/         - Create check-in 🔒
POST   /api/v1/checkins/{id}/end - End check-in 🔒
DELETE /api/v1/checkins/{id}     - Delete check-in 🔒
```

### Users
```
GET    /api/v1/users/            - List users
GET    /api/v1/users/{id}        - Get user
POST   /api/v1/users/            - Create user
```

🔒 = Requires authentication

## 🏗️ Project Structure

```
zutreffen/
├── app/
│   ├── api/
│   │   ├── deps.py              # Auth dependencies
│   │   └── v1/
│   │       ├── routes/
│   │       │   ├── auth.py      # Authentication
│   │       │   ├── users.py     # User management
│   │       │   ├── places.py    # Places CRUD
│   │       │   ├── checkins.py  # Check-ins
│   │       │   └── health.py    # Health check
│   │       └── api.py
│   ├── core/
│   │   ├── config.py            # Settings
│   │   └── security.py          # JWT & passwords
│   ├── db/
│   │   └── session.py           # Database
│   ├── models/                  # SQLAlchemy models
│   ├── schemas/                 # Pydantic schemas
│   └── main.py
├── mock_data/
│   ├── seed_database.py         # Seeding script
│   ├── users.py                 # Mock users
│   ├── places.py                # Mock places
│   └── checkins.py              # Mock check-ins
├── tests/
├── requirements.txt
├── run.sh                       # Helper script
├── test_api.py                  # API tests
├── test_auth.py                 # Auth tests
└── README.md
```

## 💡 Example Usage

### Python
```python
import requests

# Login
response = requests.post("http://localhost:8001/api/v1/auth/login/json", json={
    "email": "max.mueller@example.com",
    "password": "password123"
})
token = response.json()["access_token"]

# Create check-in
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    "http://localhost:8001/api/v1/checkins/",
    headers=headers,
    json={"place_id": 1, "message": "Working here! ☕"}
)
```

### cURL
```bash
# Login
TOKEN=$(curl -X POST http://localhost:8001/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"email":"max.mueller@example.com","password":"password123"}' \
  | jq -r '.access_token')

# Check in
curl -X POST http://localhost:8001/api/v1/checkins/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"place_id":1,"message":"Great place!"}'
```

## 🔧 Technologies

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation
- **JWT** - Token-based authentication
- **Uvicorn** - ASGI server
- **SQLite** - Database (easily switch to PostgreSQL)

## 🎯 Next Steps

- [ ] Add geolocation search (nearby places)
- [ ] Add place ratings and reviews
- [ ] Add user followers/friends
- [ ] Add real-time notifications
- [ ] Add payment integration
- [ ] Build frontend (React/Vue)
- [ ] Mobile app (React Native)
- [ ] Docker containerization
- [ ] PostgreSQL migration
- [ ] CI/CD pipeline

## 📝 License

MIT


### 2. **Database Models**

#### User Model
- `id`, `email`, `username`, `full_name`
- `hashed_password`, `avatar_url`, `bio`
- `is_active`, `created_at`, `updated_at`
- Relationship with check-ins

#### Place Model
- `id`, `name`, `description`, `address`
- `city`, `postal_code`, `country`
- `latitude`, `longitude` (real GPS coordinates)
- `category` (cafe, coworking, park)
- `image_url`, `is_active`
- `created_at`, `updated_at`

#### CheckIn Model
- `id`, `user_id`, `place_id`
- `status` (active, ended)
- `message`, `check_in_time`, `check_out_time`
- Relationships with user and place



## 🔄 Re-seed Database

If you want to reset the database with fresh mock data:

```bash
python3 mock_data/seed_database.py
```

This will:
1. Clear all existing data
2. Create fresh users
3. Create fresh places
4. Generate new check-ins

## 📦 Installed Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` & `pydantic-settings` - Data validation
- `sqlalchemy` - ORM
- `python-dotenv` - Environment variables
- `passlib` & `bcrypt` - Password hashing
- `python-jose` - JWT tokens
- `pytest` & `httpx` - Testing

## 🎯 Current Features

✅ FastAPI application structure  
✅ Database models with relationships  
✅ Pydantic schemas for validation  
✅ Mock data with real German locations  
✅ Real GPS coordinates  
✅ User avatars and place images  
✅ Working API endpoints  
✅ Health check endpoint  
✅ Database seeding script  
✅ API testing script  
✅ SQLite database (easy to use)  
✅ Environment-based configuration  
✅ Password hashing  
✅ CORS middleware  



## 🎉 Success!

Your FastAPI application is fully functional with:
- ✅ Real database with actual data
- ✅ Working API endpoints
- ✅ German locations with GPS coordinates
- ✅ Professional images
- ✅ Comprehensive testing

Access the interactive API docs at: **http://localhost:8001/docs**
