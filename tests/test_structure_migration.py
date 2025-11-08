"""
Test to verify the structure migration worked correctly
"""
import pytest
from fastapi.testclient import TestClient


def test_imports():
    """Test that all new imports work correctly"""
    # Test core imports
    from core.config import config
    from core.security import get_password_hash, create_access_token
    from core.deps import get_current_user, authenticate_user
    
    # Test db imports
    from db.session import get_db, Base, engine
    
    # Test model imports
    from models.user import User
    from models.place import Place
    from models.checkin import CheckIn
    
    # Test schema imports
    from schemas.user import User as UserSchema
    from schemas.place import Place as PlaceSchema
    from schemas.checkin import CheckIn as CheckInSchema
    
    # Test routes
    from routes import auth, users, places, checkins, health
    from routes.api import api_router
    
    # Test main app
    from main import app, create_app
    
    assert config is not None
    assert config.PROJECT_NAME == "Zutreffen"
    print("✅ All imports successful")


def test_app_creation():
    """Test that the app can be created"""
    from main import create_app
    app = create_app()
    assert app is not None
    assert app.title == "Zutreffen"
    print("✅ App creation successful")


def test_api_endpoints():
    """Test that API endpoints are accessible"""
    from main import app
    client = TestClient(app)
    
    # Test health endpoint
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health endpoint works")
    
    # Test that routes are properly mounted
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    openapi = response.json()
    assert openapi["info"]["title"] == "Zutreffen"
    print("✅ OpenAPI docs accessible")


def test_authentication_helpers():
    """Test authentication helper functions"""
    from core.security import get_password_hash, verify_password
    
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False
    print("✅ Authentication helpers work")


def test_config_loading():
    """Test that configuration is loaded correctly"""
    from core.config import config
    
    assert hasattr(config, 'PROJECT_NAME')
    assert hasattr(config, 'DATABASE_URL')
    assert hasattr(config, 'SECRET_KEY')
    assert hasattr(config, 'API_V1_STR')
    assert config.API_V1_STR == "/api/v1"
    print("✅ Configuration loaded correctly")


if __name__ == "__main__":
    test_imports()
    test_app_creation()
    test_api_endpoints()
    test_authentication_helpers()
    test_config_loading()
    print("\n🎉 All structure migration tests passed!")
