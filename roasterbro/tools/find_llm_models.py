import os
from dotenv import load_dotenv

import ollama

load_dotenv()

def find_models() -> dict[str, dict]:
    """To list the local models and cloud providers api key"""
    response = ollama.list()
    ollama_models = {}

    cloud_providers = {
        "OPENAI" : False,
        "GROQ" : False,
        "GOOGLE" : False,
        "MISTRAL" : False,
        "ANTHROPIC" : False,   
    }

    for models in response.get('models', []):
        model = models['model']
        size = round(models['size'] / (1024**3), 2) ## IN GB
        ollama_models[model] = size

    if os.getenv("OPENAI_API_KEY"):
        cloud_providers["OPENAI"] = True

    if os.getenv("GROQ_API_KEY"):
        cloud_providers["GROQ"] = True

    if os.getenv("GOOGLE_API_KEY"):
        cloud_providers["GOOGLE"] = True

    if os.getenv("MISTRAL_API_KEY"):
        cloud_providers["MISTRAL"] = True

    if os.getenv("ANTHROPIC_API_KEY"):
        cloud_providers["ANTHROPIC"] = True

    return {
        "ollama_models": ollama_models,
        "cloud_providers": cloud_providers
    }
