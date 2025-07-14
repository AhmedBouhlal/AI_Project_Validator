# validator/optimizer.py

def optimize_code(code: str) -> str:
    """
    Perform basic optimizations on the Python code.
    This can be extended to include linting, formatting, or refactoring.

    Args:
        code (str): Python source code

    Returns:
        str: Optimized code
    """
    # Example: remove extra blank lines (very basic)
    lines = code.split("\n")
    cleaned = []
    blank = False
    for line in lines:
        if line.strip() == "":
            if not blank:
                cleaned.append("")
                blank = True
        else:
            cleaned.append(line)
            blank = False
    return "\n".join(cleaned)
