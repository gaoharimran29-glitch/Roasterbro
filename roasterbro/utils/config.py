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

def get_llm(provider: str, model_name: str) -> BaseChatModel | None:
    """Create the LLM model instance safely handling validation exceptions."""
    
    kwargs = {
        "model": model_name,
        "temperature": 0.9,
        "top_p": 0.95
    }

    try:
        if provider == "ollama":
            return ChatOllama(**kwargs, base_url="http://localhost:11434")

        elif provider == "openai":
            if not os.getenv("OPENAI_API_KEY"):
                click.secho("✖ OPENAI_API_KEY Not Found in environment", fg="red")
                return None
            
            return ChatOpenAI(**kwargs)

        elif provider == "groq":
            if not os.getenv("GROQ_API_KEY"):
                click.secho("✖ GROQ_API_KEY Not Found in environment", fg="red")
                return None
            
            return ChatGroq(**kwargs)

        elif provider == "google":
            if not os.getenv("GOOGLE_API_KEY"):
                click.secho("✖ GOOGLE_API_KEY Not Found in environment", fg="red")
                return None
            
            return ChatGoogleGenerativeAI(**kwargs)

        elif provider == "mistral":
            if not os.getenv("MISTRAL_API_KEY"):
                click.secho("✖ MISTRAL_API_KEY Not Found in environment", fg="red")
                return None
            
            return ChatMistralAI(**kwargs)

        elif provider == "anthropic":
            if not os.getenv("ANTHROPIC_API_KEY"):
                click.secho("✖ ANTHROPIC_API_KEY Not Found in environment", fg="red")
                return None
            
            return ChatAnthropic(**kwargs)

        else:
            click.secho("✖ LLM Provider Not Supported", fg="red")
            return None

    except ValidationError as e:
        click.secho(f"✖ Pydantic Validation Error initializing '{model_name}':\n{e}", fg="red")
        return None

    except Exception as e:
        click.secho(f"✖ Unexpected Error initializing '{model_name}': {e}", fg="red")
        return None
