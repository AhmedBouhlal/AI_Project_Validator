from utils.ollama_client import ask_llama

def auto_fix_code(code: str, explain: bool = True) -> str:
    """
    Sends the code to LLaMA 3 via Ollama and gets the fixed version.
    
    Args:
        code (str): The original Python code to fix.
        explain (bool): If True, also include explanation of fixes.
        
    Returns:
        str: Fixed code with or without explanation.
    """
    if explain:
        prompt = f"""You are a Python expert. The following code has bugs or poor practices.
Fix it and explain your changes clearly in comments:

```python
{code}
```"""
    else:
        prompt = f"""Fix this Python code and return only the corrected version:

```python
{code}
```"""

    response = ask_llama(prompt)
    return response
