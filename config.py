"""Configuration management for Gitinsky Support Bot."""

import os
from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Telegram Bot Configuration
    telegram_bot_token: str = Field(..., description="Telegram bot token from BotFather")
    
    # DeepSeek API Configuration
    openrouter_api_key: str = Field(..., description="DeepSeek API key")
    deepseek_api_url: str = Field(
        default="https://api.deepseek.com/v1",
        description="DeepSeek API endpoint URL"
    )
    
    # Database Configuration
    database_url: str = Field(
        default="sqlite:///./gitinsky_bot.db",
        description="Database connection string"
    )
    
    # Email Configuration (SMTP)
    smtp_host: str = Field(..., description="SMTP server host")
    smtp_port: int = Field(default=587, description="SMTP server port")
    smtp_user: str = Field(..., description="SMTP username")
    smtp_password: str = Field(..., description="SMTP password")
    smtp_from_email: str = Field(..., description="From email address")
    smtp_from_name: str = Field(
        default="Gitinsky Support Bot",
        description="From name for emails"
    )
    
    # Company Email Domain (for verification)
    company_email_domain: str = Field(..., description="Allowed email domain for verification")
    
    # Verification Settings
    verification_code_ttl: int = Field(
        default=15,
        description="Verification code time to live in minutes"
    )
    session_ttl_days: int = Field(
        default=30,
        description="User session duration in days"
    )
    
    # Performance Settings
    max_concurrent_users: int = Field(
        default=100,
        description="Maximum concurrent users"
    )
    max_response_tokens: int = Field(
        default=2000,
        description="Maximum tokens for AI response"
    )
    api_timeout_seconds: int = Field(
        default=30,
        description="API request timeout in seconds"
    )
    
    # Feature Flags
    enable_email_verification: bool = Field(
        default=True,
        description="Enable email verification requirement"
    )
    enable_feedback_collection: bool = Field(
        default=True,
        description="Enable user feedback feature"
    )
    enable_admin_commands: bool = Field(
        default=True,
        description="Enable administrative commands"
    )
    enable_response_streaming: bool = Field(
        default=False,
        description="Enable streaming for long responses"
    )
    
    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    
    # Admin Configuration
    admin_telegram_ids: str = Field(
        default="",
        description="Comma-separated list of admin Telegram IDs"
    )
    
    @field_validator("admin_telegram_ids")
    @classmethod
    def parse_admin_ids(cls, v: str) -> List[int]:
        """Parse comma-separated admin IDs into list of integers."""
        if not v:
            return []
        try:
            return [int(id_.strip()) for id_ in v.split(",") if id_.strip()]
        except ValueError:
            raise ValueError("ADMIN_TELEGRAM_IDS must be comma-separated integers")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings: Settings = None


def load_settings() -> Settings:
    """Load and validate settings from environment."""
    global settings
    if settings is None:
        settings = Settings()
    return settings


def get_settings() -> Settings:
    """Get current settings instance."""
    if settings is None:
        return load_settings()
    return settings
