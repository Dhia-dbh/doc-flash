"""Abstract interface for pluggable LLM providers."""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Strategy interface for LLM backends."""

    @abstractmethod
    async def document_code(self, code: str) -> str:
        """Return code annotated with docstrings and inline comments."""

    @abstractmethod
    async def describe_behaviour(self, code: str) -> str:
        """Return a markdown summary of the code's behaviour."""
