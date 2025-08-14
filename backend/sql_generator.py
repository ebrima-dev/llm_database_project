# SQL generation with LLaMa
import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"


def handle_sql_query(question: str) -> str:
    prompt = f"""
    You are a SQL generator.
    Convert the following natrual language question into valid SQL query.
    Do NOT include explanations - only output SQL.
    Question: {question}
    """
    
    response = requests.post(
        OLLAMA_API_URL,
        json ={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        raise Exception(f"Ollama API error: {response.text}")
    
    data = response.json()
    return data.get("response", "").strip()

