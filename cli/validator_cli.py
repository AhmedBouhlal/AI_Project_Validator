import argparse
import os
import subprocess
import shutil

from validator.bug_checker import analyze_project_folder
from validator.concept_checker import analyze_project_concept
from validator.auto_corrector import auto_fix_code
from utils.ollama_client import ask_llama


def read_all_code(folder_path):
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
    parser.add_argument("--concept", help="Project concept/description")
    parser.add_argument("--bugs", action="store_true", help="Run bug checker")
    parser.add_argument("--concept_check", action="store_true", help="Run concept checker")
    parser.add_argument("--fix", action="store_true", help="Auto-fix the project")
    parser.add_argument("--test", action="store_true", help="Run tests using pytest")

    args = parser.parse_args()

    # ✅ Bug Checker
    if args.bugs:
        print("🔍 Running Bug Checker...")
        bug_results = analyze_project_folder(args.path)
        for file, result in bug_results.items():
            print(f"\n📄 {file} - Bugs Found:\n{result}")

    # ✅ Concept Checker
    if args.concept_check:
        if not args.concept:
            print("❌ Concept Checker requires --concept argument.")
        else:
            print("\n🧠 Running Concept Checker...")
            concept_results = analyze_project_concept(args.path, args.concept)
            for file, result in concept_results.items():
                print(f"\n📄 {file} - Concept Match:\n{result}")


if __name__ == "__main__":
    main()
