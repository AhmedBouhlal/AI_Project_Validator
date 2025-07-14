from utils.ollama_client import ask_llama
import os

def check_file_concept_alignment(code: str, concept: str) -> str:
    """
    Use LLaMA to evaluate if a file matches the project concept.

    Args:
        code (str): The source code of the file.
        concept (str): The project description/concept.

    Returns:
        str: AI feedback on alignment and suggestions.
    """
    prompt = f"""
You are an expert Python reviewer.

Project Concept:
\"\"\"{concept}\"\"\"

Here is a Python file from the project:
```python
{code}
```
Analyze if the code matches the concept.

Does it fulfill the goal?

Is anything missing?

Is anything irrelevant or unnecessary?

What should be added or changed?

Be precise and explain clearly.
"""

    return ask_llama(prompt)

def analyze_project_concept(folder_path: str, concept: str) -> dict:
    """
    Run concept matching check for each file in the project folder.
    Args:
    folder_path (str): Root folder of the Python project.
    concept (str): Description of what the project is supposed to do.

    Returns:
    dict: Each file path mapped to LLaMA's evaluation result.
    """
    report = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r") as f:
                        code = f.read()
                    print(f"🔍 Analyzing concept match for: {file_path}")
                    result = check_file_concept_alignment(code, concept)
                    report[file_path] = result
                except Exception as e:
                    report[file_path] = f"[ERROR] Could not read/analyze file: {e}"
    return report
