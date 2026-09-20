"""LLM abstraction layer. The MVP does not require an external provider."""

from app.llm.client import LLMClient

__all__ = ["LLMClient"]
