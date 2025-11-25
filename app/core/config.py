import http
from proto import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    # JWT Settings
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Google OAuth Settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_OAUTH_REDIRECT_URI: str = "http://localhost:8000/api/v1/google-drive/callback"
    GOOGLE_SCOPES: str = "https://www.googleapis.com/auth/drive.file"

    FERNET_KEY: str
    FRONTEND_URL: str
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Setting()