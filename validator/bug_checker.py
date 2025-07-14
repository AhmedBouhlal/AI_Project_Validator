import subprocess
import os

def run_pylint_on_file(file_path: str) -> str:
    """
    Run pylint on a single Python file and return the output as a string.
    
    Args:
        file_path (str): Path to the Python file.
        
    Returns:
        str: Pylint output (score, warnings, errors).
    """
    try:
        result = subprocess.run(
            ['pylint', file_path, '--disable=R,C'],  # Disable refactor & convention for simplicity
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"[ERROR] Failed to run pylint: {e}"

def analyze_project_folder(folder_path: str) -> dict:
    """
    Walk through all Python files in a folder and analyze them using pylint.
    
    Args:
        folder_path (str): Path to the root of the Python project.
        
    Returns:
        dict: Mapping of file path to its pylint analysis result.
    """
    report = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                print(f"Checking: {full_path}")
                report[full_path] = run_pylint_on_file(full_path)
    return report
