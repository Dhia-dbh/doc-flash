"""Application-facing documentation service."""

from doc_flash.services.providers.base import LLMProvider


class DocumentationService:
    """Coordinates documentation tasks using the configured provider."""

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def document_code(self, code: str) -> str:
        return await self.provider.document_code(code)

    async def generate_markdown(self, code: str) -> str:
        return await self.provider.describe_behaviour(code)

    async def generate_tests(self, code: str) -> str:
        return await self.provider.generate_tests(code)
