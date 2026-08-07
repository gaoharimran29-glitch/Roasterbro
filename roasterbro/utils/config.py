import os
import click
from dotenv import load_dotenv
from pydantic import ValidationError

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain_anthropic import ChatAnthropic

from langchain_core.language_models.chat_models import BaseChatModel

load_dotenv()

PROVIDER_MAP = {
    "ollama":    {"class": ChatOllama, "env": None},
    "openai":    {"class": ChatOpenAI, "env": "OPENAI_API_KEY"},
    "groq":      {"class": ChatGroq, "env": "GROQ_API_KEY"},
    "google":    {"class": ChatGoogleGenerativeAI, "env": "GOOGLE_API_KEY"},
    "mistral":   {"class": ChatMistralAI, "env": "MISTRAL_API_KEY"},
    "anthropic": {"class": ChatAnthropic, "env": "ANTHROPIC_API_KEY"},
}


def _fail(message: str):
    """Print a formatted error and exit once, cleanly."""
    click.secho(f"✖ {message}", fg="red", bold=True)
    click.secho("Run `roasterbro models` to check the configured api key and local LLM", fg="yellow")
    raise click.exceptions.Exit(1)


def get_llm(provider: str, model_name: str) -> BaseChatModel:
    """Create the LLM model instance, safely handling validation exceptions."""

    config = PROVIDER_MAP.get(provider)
    if config is None:
        _fail(f"LLM Provider '{provider}' Not Supported")

    # Validate env var BEFORE the try block — no risk of double-catching Exit
    env_key = config["env"]
    if env_key and not os.getenv(env_key):
        _fail(f"{env_key} Not Found in environment")

    kwargs = {"model": model_name, "temperature": 0.9, "top_p": 0.95}
    if provider == "ollama":
        kwargs["base_url"] = "http://localhost:11434"

    try:
        return config["class"](**kwargs)

    except ValidationError as e:
        click.secho(f"✖ Pydantic Validation Error initializing '{model_name}':", fg="red", bold=True)
        click.secho(f"{e}", fg="red")
        click.secho("Run `roasterbro models` to check the configured api key and local LLM", fg="yellow")
        raise click.exceptions.Exit(1)

    except click.exceptions.Exit:
        raise

    except Exception as e:
        click.secho(f"✖ Unexpected Error initializing '{model_name}': {e}", fg="red", bold=True)
        click.secho("Run `roasterbro models` to check the configured api key and local LLM", fg="yellow")
        raise click.exceptions.Exit(1)
