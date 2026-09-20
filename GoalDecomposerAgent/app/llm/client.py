class LLMClient:
    """Provider-neutral interface for a future LLM integration.

    The MVP intentionally uses deterministic rules instead of requiring an API key.
    A real provider can implement `generate` later without changing the agent API.
    """

    def generate(self, prompt: str) -> str:
        raise NotImplementedError(
            "No LLM provider is configured. Use the deterministic MVP agent for now."
        )
