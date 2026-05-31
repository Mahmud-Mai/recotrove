"""
Configuration Management for RecoTrove
"""
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class DatabaseSettings(BaseSettings):
    """Database-specific configuration"""

    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://recotrove_user:recotrove_password@localhost:5462/recotrove_db",
        description="PostgreSQL connection string"
    )

    DATABASE_POOL_SIZE: int = Field(default=20)
    DATABASE_MAX_OVERFLOW: int = Field(default=40)

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if "postgresql" in v and "asyncpg" not in v:
            v = v.replace("postgresql://", "postgresql+asyncpg://")
        return v


class SecuritySettings(BaseSettings):
    """Security and authentication configuration"""

    SECRET_KEY: str = Field(
        default="CHANGE_THIS_IN_PRODUCTION_USE_OPENSSL_TO_GENERATE_32_BYTES",
        min_length=32,
        description="JWT signing key - KEEP SECRET!"
    )

    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    PASSWORD_MIN_LENGTH: int = Field(default=8)
    PASSWORD_REQUIRE_UPPER: bool = Field(default=True)
    PASSWORD_REQUIRE_DIGIT: bool = Field(default=True)
    PASSWORD_REQUIRE_SPECIAL: bool = Field(default=True)


class AppSettings(BaseSettings):
    """Main application configuration"""

    # App metadata
    APP_NAME: str = Field(default="RecoTrove")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=True)

    ALLOWED_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:8030",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:8030"
        ]
    )

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100)

    # Admin user
    FIRST_ADMIN_EMAIL: str = Field(default="admin@recotrove.com")
    FIRST_ADMIN_PASSWORD: str = Field(default="Admin123!")
    FIRST_ADMIN_NAME: str = Field(default="System Administrator")

    # Nested settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = False
        extra = "ignore"  # This ignores extra fields like 'secret_key' from env

    @field_validator("FIRST_ADMIN_PASSWORD")
    @classmethod
    def validate_admin_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Admin password must be at least 8 characters")
        return v


# Create singleton instance
settings = AppSettings()

logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
logger.info(f"Debug mode: {settings.DEBUG}")