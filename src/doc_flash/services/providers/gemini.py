"""Gemini implementation of the LLMProvider."""

from __future__ import annotations

import google.generativeai as genai
from fastapi.concurrency import run_in_threadpool

from doc_flash.services.prompts import build_documentation_prompt, build_markdown_prompt
from doc_flash.services.providers.base import LLMProvider


class GeminiProvider(LLMProvider):
    """Google Gemini free tier-backed provider."""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash", temperature: float = 0.2):
        if not api_key:
            raise ValueError("Gemini API key is required for GeminiProvider.")

        self.model_name = model
        self.temperature = temperature
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    async def _generate(self, prompt: str) -> str:
        """Call Gemini on a background thread to keep FastAPI async-friendly."""
        response = await run_in_threadpool(
            self.model.generate_content,
            prompt,
            generation_config={"temperature": self.temperature},
        )
        text = getattr(response, "text", "") or ""
        return text.strip()

    async def document_code(self, code: str) -> str:
        prompt = build_documentation_prompt(code)
        return await self._generate(prompt)

    async def describe_behaviour(self, code: str) -> str:
        prompt = build_markdown_prompt(code)
        return await self._generate(prompt)
