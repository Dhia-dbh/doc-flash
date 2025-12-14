"""Dependency wiring for FastAPI."""

from functools import lru_cache
from typing import Optional

from fastapi import Depends

from doc_flash.core.config import Settings
from doc_flash.services.documentation_service import DocumentationService
from doc_flash.services.provider_factory import build_provider
from doc_flash.services.providers.base import LLMProvider

_provider_instance: Optional[LLMProvider] = None


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_provider(settings: Settings = Depends(get_settings)) -> LLMProvider:
    global _provider_instance
    if _provider_instance is None:
        _provider_instance = build_provider(settings)
    return _provider_instance


def get_documentation_service(
    provider: LLMProvider = Depends(get_provider),
) -> DocumentationService:
    return DocumentationService(provider)
