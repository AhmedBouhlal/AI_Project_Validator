import os
import ast
import shutil
import subprocess

TEMP_TEST_DIR = "temp_tests"

TEMPLATE = '''import pytest
from {module} import {function}


def test_{function}():
    # TODO: Replace with real test logic
    result = {function}()
    assert result is not None
'''


def extract_functions(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def generate_test_file(src_path, dst_path):
    functions = extract_functions(src_path)
    if not functions:
        return None

    module_name = os.path.splitext(os.path.basename(src_path))[0]
    test_file_name = f"test_{module_name}.py"
    test_code = "\n\n".join(
        TEMPLATE.format(module=module_name, function=fn) for fn in functions
    )

    with open(os.path.join(dst_path, test_file_name), "w") as f:
        f.write(test_code)

    return test_file_name


def generate_all_tests(project_path):
    os.makedirs(TEMP_TEST_DIR, exist_ok=True)
    generated = []

    for root, _, files in os.walk(project_path):
        if 'tests' in root or '__pycache__' in root:
            continue

        for file in files:
            if file.endswith(".py") and not file.startswith("test_"):
                src_path = os.path.join(root, file)
                generated_name = generate_test_file(src_path, TEMP_TEST_DIR)
                if generated_name:
                    generated.append(generated_name)

    print(f"\n✅ Generated {len(generated)} temporary test files in '{TEMP_TEST_DIR}/'")
    return generated


def run_pytest():
    print("\n🚀 Running pytest on temporary test files...\n")
    result = subprocess.run(
        ["pytest", "."],
        cwd=TEMP_TEST_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    print(result.stdout)

    with open(os.path.join(TEMP_TEST_DIR, "test_report.txt"), "w") as f:
        f.write(result.stdout)

    print("\n📋 Pytest report saved to: temp_tests/test_report.txt")


def cleanup():
    if os.path.exists(TEMP_TEST_DIR):
        shutil.rmtree(TEMP_TEST_DIR)
        print("\n🧹 Removed temporary test folder.")


if __name__ == "__main__":
    try:
        generate_all_tests("validator")  # Or "." to scan entire project
        run_pytest()
    finally:
        cleanup()
