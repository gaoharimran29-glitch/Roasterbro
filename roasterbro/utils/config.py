from langchain_ollama import ChatOllama

MODEL = ChatOllama(
        model="llama3.2:3b",
        temperature=0.7,
        base_url="http://localhost:11434",
    )