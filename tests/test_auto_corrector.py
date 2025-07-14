import os
from utils.ollama_client import ask_llama


def auto_fix_single_file(code: str, filename: str) -> str:
    """
    Fix bugs in a single Python file using LLaMA 3.

    Args:
        code (str): Code to be fixed.
        filename (str): Name of the file (for context).

    Returns:
        str: Fixed version of the code.
    """
    prompt = f"""
You are an expert Python code fixer.

This is the file: {filename}

Fix all bugs, clean the code, and optimize where possible.

ONLY return the corrected code.

```python
{code}
```"""
    return ask_llama(prompt)


def auto_fix_project_separately(project_path: str) -> dict:
    """
    Auto-fix each Python file in the project folder separately.

    Args:
        project_path (str): Path to the project folder.

    Returns:
        dict: Mapping of file path to fixed code.
    """
    fixed_files = {}
    os.makedirs("fixed_output", exist_ok=True)

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    code = f.read()

                print(f"🤖 Fixing: {file_path}")
                fixed_code = auto_fix_single_file(code, file)
                fixed_files[file_path] = fixed_code

                # Preserve folder structure in fixed_output/
                relative_path = os.path.relpath(file_path, project_path)
                save_path = os.path.join("fixed_output", relative_path)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                with open(save_path, "w") as out_file:
                    out_file.write(fixed_code)
                print(f"✅ Saved fixed file: {save_path}")

    return fixed_files
