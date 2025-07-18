import argparse
import os
import sys
import subprocess
import shutil

from validator.bug_checker import analyze_project_folder
from validator.concept_checker import analyze_project_concept
from validator.auto_corrector import auto_fix_code
from utils.ollama_client import ask_llama


def main():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    parser = argparse.ArgumentParser(description="🧠 AI Project Validator CLI")
    parser.add_argument("--path", required=True, help="Path to Python project folder")
    parser.add_argument("--concept", help="Project concept/description")
    parser.add_argument("--bugs", action="store_true", help="Run bug checker")
    parser.add_argument("--concept_check", action="store_true", help="Run concept checker")
    parser.add_argument("--fix", action="store_true", help="Auto-fix project files")
    parser.add_argument("--test", action="store_true", help="Run tests using pytest")

    args = parser.parse_args()

    if args.bugs:
        print("🔍 Running Bug Checker...")
        bug_results = analyze_project_folder(args.path)
        for file, result in bug_results.items():
            print(f"\n📄 {file} - Bugs Found:\n{result}")

    if args.concept_check:
        if not args.concept:
            print("❌ Concept Checker requires --concept argument.")
        else:
            print("\n🧠 Running Concept Checker...")
            concept_results = analyze_project_concept(args.path, args.concept)
            for file, result in concept_results.items():
                print(f"\n📄 {file} - Concept Match:\n{result}")

    if args.fix:
        print("\n🤖 Auto-Fixing Python Files with LLaMA 3...")

        output_dir = "fixed_output"
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        for root, _, files in os.walk(args.path):
            for file in files:
                if file.endswith(".py"):
                    src_path = os.path.join(root, file)
                    with open(src_path, "r") as f:
                        original_code = f.read()

                    print(f"\n🔧 Fixing: {file}")
                    fixed_code = auto_fix_code(original_code)

                    # Save fixed file to same relative path
                    rel_path = os.path.relpath(src_path, args.path)
                    dest_path = os.path.join(output_dir, rel_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                    with open(dest_path, "w") as f:
                        f.write(fixed_code)

        print(f"\n✅ All fixed files saved to: {output_dir}/")

    if args.test:
        test_files = [f for f in os.listdir(args.path) if f.startswith("test_") and f.endswith(".py")]

        if test_files:
            print(f"🧪 Found test files: {test_files}")
            for file in test_files:
                shutil.copy(os.path.join(args.path, file), os.path.join("fixed_output", file))

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
