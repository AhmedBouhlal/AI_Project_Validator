import argparse
import os
import subprocess
from validator.bug_checker import analyze_project_folder
from validator.concept_checker import analyze_project_concept
from validator.auto_corrector import auto_fix_project_separately
from utils.ollama_client import ask_llama


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
        fixed_files = auto_fix_project_separately(args.path)

        print("\n✅ All fixed files saved in 'fixed_output/'")

        # 🧠 Generate AI summary
        print("\n🧠 Generating AI Summary of Fixes...")
        summary_prompt = "Explain the improvements and fixes made to each file:\n"
        for file_path, fixed_code in fixed_files.items():
            summary_prompt += f"\n\n📄 File: {file_path}\n```python\n{fixed_code}\n```"

        summary = ask_llama(summary_prompt)

        print("\n📋 AI Summary of Fixes:")
        print(summary)

        with open("fixed_output/summary.txt", "w") as f:
            f.write(summary)
        print("📝 Saved summary to: fixed_output/summary.txt")

        # 🔬 Check for test files and run pytest
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
        else:
            print("❌ No test_*.py files found. Skipping pytest.")


if __name__ == "__main__":
    main()
