from utils.ollama_client import ask_llama

def generate_project_feedback(bug_results, concept_results, concept_text):
    """
    Use LLaMA to generate a project-level quality report.
    
    Args:
        bug_results (dict): File => bug summary
        concept_results (dict): File => concept match feedback
        concept_text (str): Original concept provided

    Returns:
        str: AI-generated feedback summary
    """
    bug_report = "\n".join([f"{file}:\n{msg}" for file, msg in bug_results.items()])
    concept_report = "\n".join([f"{file}:\n{msg}" for file, msg in concept_results.items()])

    prompt = f"""
You are an expert software reviewer.

The following Python project was analyzed using AI tools:

=== Project Concept ===
\"\"\"{concept_text}\"\"\"

=== Bug Report (file by file) ===
{bug_report}

=== Concept Match Analysis (file by file) ===
{concept_report}

Please now provide a full project review:
- Overall quality of the code
- Design, maintainability, and clarity
- Do files match the concept well?
- What are the most critical problems?
- What are suggestions for improvement?
Respond with clear bullet points and overall project advice.
"""

    return ask_llama(prompt)
