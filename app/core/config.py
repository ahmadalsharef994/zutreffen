from pydantic_settings import BaseSettings
from typing import List, Union, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Zutreffen"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    PAYMENT_PROVIDER: str = "stripe"  # placeholder
    API_V1_STR: str = "/api/v1"
    
    # Additional settings
    PLACES_PER_PAGE: int = 20
    MAX_CHECKINS_PER_USER: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()