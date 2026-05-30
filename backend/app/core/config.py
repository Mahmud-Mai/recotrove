"""
Configuration Management for RecoTrove

This module handles all environment-specific configuration using Pydantic's
BaseSettings. It reads from .env file and environment variables, validates
all required settings, and provides typed access throughout the application.

Why Pydantic Settings?
- Automatic validation: App crashes on startup if required config missing
- Type conversion: "true" string becomes boolean True automatically
- Nested settings: Can group related config into subclasses
- Environment variable mapping: Can override any setting with UPPER_CASE vars
"""
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class DatabaseSettings(BaseSettings):
    """Database-specific configuration"""

    # PostgreSQL connection URL format:
    # postgresql+asyncpg://user:password@host:port/database
    # +asyncpg indicates we're using the async PostgreSQL driver
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://recotrove_user:recotrove_password@localhost:5432/recotrove_db",
        description="PostgreSQL connection string"
    )

    # Connection pool settings (for production scaling)
    DATABASE_POOL_SIZE: int = Field(default=20, description="Max database connections")
    DATABASE_MAX_OVERFLOW: int = Field(default=40, description="Extra connections when pool is full")

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure the database URL uses asyncpg driver"""
        if "postgresql" in v and "asyncpg" not in v:
            logger.warning(f"Converting database URL to use asyncpg: {v}")
            v = v.replace("postgresql://", "postgresql+asyncpg://")
        return v


class SecuritySettings(BaseSettings):
    """Security and authentication configuration"""

    # JWT Secret - MUST be at least 32 characters in production
    # Generate with: openssl rand -hex 32
    SECRET_KEY: str = Field(
        default="CHANGE_THIS_IN_PRODUCTION_USE_OPENSSL_TO_GENERATE_32_BYTES",
        min_length=32,
        description="JWT signing key - KEEP SECRET!"
    )

    ALGORITHM: str = Field(default="HS256", description="JWT signing algorithm")

    # Token lifetimes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Short-lived access tokens (minutes)"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Longer-lived refresh tokens (days)"
    )

    # Password requirements
    PASSWORD_MIN_LENGTH: int = Field(default=8)
    PASSWORD_REQUIRE_UPPER: bool = Field(default=True)
    PASSWORD_REQUIRE_DIGIT: bool = Field(default=True)
    PASSWORD_REQUIRE_SPECIAL: bool = Field(default=True)


class StorageSettings(BaseSettings):
    """File/object storage configuration (MinIO/S3)"""

    MINIO_ENDPOINT: str = Field(default="localhost:9000")
    MINIO_ACCESS_KEY: str = Field(default="minioadmin")
    MINIO_SECRET_KEY: str = Field(default="minioadmin123")
    MINIO_BUCKET: str = Field(default="recotrove-thumbnails")
    MINIO_SECURE: bool = Field(default=False)  # False for local development

    # URL for accessing thumbnails (MinIO web UI or CDN)
    THUMBNAIL_URL_PREFIX: str = Field(default="http://localhost:9000")

    @field_validator("THUMBNAIL_URL_PREFIX")
    @classmethod
    def ensure_trailing_slash(cls, v: str) -> str:
        """Ensure URL prefix ends with slash for proper concatenation"""
        if not v.endswith("/"):
            v = v + "/"
        return v


class EmailSettings(BaseSettings):
    """Email configuration (MailHog for development)"""

    SMTP_HOST: str = Field(default="mailhog")
    SMTP_PORT: int = Field(default=1025)
    SMTP_USER: Optional[str] = Field(default=None)
    SMTP_PASSWORD: Optional[str] = Field(default=None)
    SMTP_USE_TLS: bool = Field(default=False)

    FROM_EMAIL: str = Field(default="noreply@recotrove.com")
    FROM_NAME: str = Field(default="RecoTrove")

    # Email verification
    EMAIL_VERIFICATION_REQUIRED: bool = Field(default=True)
    VERIFICATION_TOKEN_EXPIRE_HOURS: int = Field(default=24)


class AppSettings(BaseSettings):
    """Main application configuration - aggregates all sub-settings"""

    # App metadata
    APP_NAME: str = Field(default="RecoTrove")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=True)

    # CORS (Cross-Origin Resource Sharing) - which frontend origins can call API
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173", "http://localhost:8030"]
    )

    # API rate limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Max requests per minute")

    # Admin user (created on first startup)
    FIRST_ADMIN_EMAIL: str = Field(default="admin@recotrove.com")
    FIRST_ADMIN_PASSWORD: str = Field(default="Admin123!", description="CHANGE IN PRODUCTION")
    FIRST_ADMIN_NAME: str = Field(default="System Administrator")

    # Sub-configurations
    database: DatabaseSettings = DatabaseSettings()
    security: SecuritySettings = SecuritySettings()
    storage: StorageSettings = StorageSettings()
    email: EmailSettings = EmailSettings()

    class Config:
        # Tell Pydantic to read from .env file
        env_file = ".env"
        # Allow environment variables to override nested settings
        # e.g., SECURITY_SECRET_KEY=xyz will set security.SECRET_KEY
        env_nested_delimiter = "__"
        # Case-sensitive mapping
        case_sensitive = False

    @field_validator("FIRST_ADMIN_PASSWORD")
    @classmethod
    def validate_admin_password(cls, v: str) -> str:
        """Ensure admin password meets security requirements"""
        if len(v) < 8:
            raise ValueError("Admin password must be at least 8 characters")
        return v


# Create singleton instance that all modules import
# This ensures configuration is loaded once at startup
settings = AppSettings()

# Log configuration on startup (without exposing secrets)
logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
logger.info(f"Debug mode: {settings.DEBUG}")
logger.info(f"Database: {settings.database.DATABASE_URL.split('@')[1] if '@' in settings.database.DATABASE_URL else 'configured'}")
logger.info(f"Storage: {settings.storage.MINIO_ENDPOINT}")