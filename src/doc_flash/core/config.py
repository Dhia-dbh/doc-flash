"""Application settings."""

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralised runtime configuration."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="DOCFLASH_", extra="ignore")

    app_name: str = "DocFlash"
    llm_provider: str = "gemini"
    gemini_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("DOCFLASH_GEMINI_API_KEY", "GEMINI_API_KEY"),
    )
    gemini_model: str = "gemini-2.5-flash"
    temperature: float = 0.2
