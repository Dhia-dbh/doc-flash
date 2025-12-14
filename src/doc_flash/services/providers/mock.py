"""Fallback provider that avoids external calls."""

from doc_flash.services.prompts import build_documentation_prompt, build_markdown_prompt
from doc_flash.services.providers.base import LLMProvider


class MockProvider(LLMProvider):
    """Simple provider useful for local testing."""

    async def document_code(self, code: str) -> str:
        prompt = build_documentation_prompt(code)
        return f"# Mocked documentation\n# Prompt would be:\n# {prompt}\n{code}"

    async def describe_behaviour(self, code: str) -> str:
        prompt = build_markdown_prompt(code)
        return "## Mocked summary\n" + prompt
