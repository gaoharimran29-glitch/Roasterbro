import click
from langchain_ollama import ChatOllama

def get_llm(model_name: str):
    """Create the ollama llm model instance"""
    try:
        MODEL = ChatOllama(model=model_name,
            temperature=0.7,
            base_url="http://localhost:11434"
        )

    except Exception as e:
        click.echo(f"Error initializing LLM model '{model_name}': {e}", err=True)
        return

    return MODEL