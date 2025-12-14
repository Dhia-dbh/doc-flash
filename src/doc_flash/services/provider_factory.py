"""Factory for selecting the configured LLM provider."""

from doc_flash.core.config import Settings
from doc_flash.services.providers.base import LLMProvider
from doc_flash.services.providers.gemini import GeminiProvider
from doc_flash.services.providers.mock import MockProvider


def build_provider(settings: Settings) -> LLMProvider:
    """Construct the provider based on settings."""
    provider_name = settings.llm_provider.lower()

    if provider_name == "gemini":
        if not settings.gemini_api_key:
            raise RuntimeError("Gemini provider selected but GEMINI_API_KEY is not set.")
        return GeminiProvider(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
            temperature=settings.temperature,
        )

    if provider_name == "mock":
        return MockProvider()

    raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
