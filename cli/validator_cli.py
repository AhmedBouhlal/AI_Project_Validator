import argparse
import os
import subprocess
from validator.bug_checker import analyze_project_folder
from validator.concept_checker import analyze_project_concept
from validator.auto_corrector import auto_fix_code
from validator.optimizer import optimize_code
from utils.ollama_client import ask_llama


def read_all_code(folder_path):
    """
    Combine all .py file contents from a folder into one string.
    Used for sending full codebase to LLaMA for fixing.
    """
    combined_code = ""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    code = f.read()
                combined_code += f"\n\n# === {file} ===\n{code}"
    return combined_code


def main():
    parser = argparse.ArgumentParser(description="🧠 AI Project Validator CLI")
    parser.add_argument("--path", required=True, help="Path to Python project folder")
    parser.add_argument("--concept", required=True, help="Project concept/description")
    parser.add_argument("--fix", action="store_true", help="Apply LLaMA auto-fix to the project")

    args = parser.parse_args()

    print("🔍 Running Bug Checker...")
    bug_results = analyze_project_folder(args.path)
    for file, result in bug_results.items():
        print(f"\n📄 {file} - Bugs Found:\n{result}")

    print("\n🧠 Running Concept Checker...")
    concept_results = analyze_project_concept(args.path, args.concept)
    for file, result in concept_results.items():
        print(f"\n📄 {file} - Concept Match:\n{result}")

    if args.fix:
        print("\n🤖 Running Auto Fixer (LLaMA 3)...")
        combined_code = read_all_code(args.path)
        fixed_code = auto_fix_code(combined_code)

        # Save fixed code
        os.makedirs("fixed_output", exist_ok=True)
        fixed_path = os.path.join("fixed_output", "fixed_project.py")
        with open(fixed_path, "w") as f:
            f.write(fixed_code)
        print(f"\n✅ Fixed Code Saved: {fixed_path}")

        # Optimize fixed code
        print("\n⚙️ Optimizing Fixed Code...")
        optimized_code = optimize_code(fixed_code)
        optimized_path = os.path.join("fixed_output", "optimized_project.py")
        with open(optimized_path, "w") as f:
            f.write(optimized_code)
        print(f"✅ Optimized Code Saved: {optimized_path}")

        # Generate summary
        print("\n🧠 Generating AI Summary of Fixes...")
        summary_prompt = f"""
        Here is the original Python project followed by the fixed version.

        Explain what changes were made:
        - What bugs were fixed?
        - What optimizations or improvements were done?
        - What parts were unnecessary and removed?
        - What is the overall improvement?

        Be clear, list important points as bullet points.

        ORIGINAL CODE:
        ```python
        {combined_code}
        ```

        FIXED VERSION:
        ```python
        {fixed_code}
        ```

        OPTIMIZED VERSION:
        ```python
        {optimized_code}
        ```
        """
        summary = ask_llama(summary_prompt)
        print("\n📋 AI Summary of Fixes:")
        print(summary)

        with open(os.path.join("fixed_output", "summary.txt"), "w") as f:
            f.write(summary)
        print("📝 Saved summary to: fixed_output/summary.txt")

        # Run pytest if test files exist
        print("\n🔬 Checking for test files...")
        test_files = [f for f in os.listdir(args.path) if f.startswith("test_") and f.endswith(".py")]

        if test_files:
            print(f"🧪 Found test files: {test_files}")
            for test_file in test_files:
                original_path = os.path.join(args.path, test_file)
                destination_path = os.path.join("fixed_output", test_file)
                with open(original_path, "r") as src, open(destination_path, "w") as dst:
                    dst.write(src.read())

            print("🚀 Running pytest on fixed_output/...")

            result = subprocess.run(
                ["pytest", "."],
                cwd="fixed_output",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            print("\n🧪 Pytest Output:\n")
            print(result.stdout)

            with open("fixed_output/test_report.txt", "w") as f:
                f.write(result.stdout)
            print("📝 Saved pytest report to: fixed_output/test_report.txt")

            # 🧹 Cleanup test files
            for test_file in test_files:
                os.remove(os.path.join("fixed_output", test_file))
            print("🧹 Removed temporary test files from fixed_output/")
        else:
            print("❌ No test_*.py files found. Skipping pytest.")


if __name__ == "__main__":
    main()
