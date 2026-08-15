import os
from dotenv import load_dotenv

import ollama

load_dotenv()


def find_models() -> dict[str, dict]:
    """List local Ollama models and available cloud providers."""

    ollama_models = {}

    try:
        response = ollama.list()

        for model_data in response.get("models", []):
            model = model_data["model"]
            size = round(model_data["size"] / (1024**3), 2)  # IN GB
            ollama_models[model] = size

    except Exception:
        # Ollama is optional and may not be running.
        ollama_models = {}

    cloud_providers = {
        "OPENAI": bool(os.getenv("OPENAI_API_KEY")),
        "GROQ": bool(os.getenv("GROQ_API_KEY")),
        "GOOGLE": bool(os.getenv("GOOGLE_API_KEY")),
        "MISTRAL": bool(os.getenv("MISTRAL_API_KEY")),
        "ANTHROPIC": bool(os.getenv("ANTHROPIC_API_KEY")),
    }

    return {
        "ollama_models": ollama_models,
        "cloud_providers": cloud_providers,
    }
