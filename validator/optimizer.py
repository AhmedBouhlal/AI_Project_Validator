from utils.ollama_client import ask_llama

def optimize_code(code: str, goal: str = "Make this code cleaner, more readable, and optimized.") -> str:
    """
    Use LLaMA to intelligently refactor and optimize the given Python code.
    """
    prompt = f"""
    You are an expert Python architect and code optimizer.

    GOAL:
    {goal}

    Code to optimize:
    ```python
    {code}
    ```

    Return only the optimized Python code.
    """
    optimized_code = ask_llama(prompt)
    return optimized_code
