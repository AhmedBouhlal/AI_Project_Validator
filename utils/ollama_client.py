import requests

def ask_llama(prompt: str, model: str = "llama3", stream: bool = False) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": stream
            }
        )
        return response.json()["response"]
    except Exception as e:
        return f"Error: {e}"
