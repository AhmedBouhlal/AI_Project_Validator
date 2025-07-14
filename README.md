## 🧠 AI Project Validator

AI-powered CLI tool that reviews your Python project for bugs, concept alignment, and optionally auto-fixes code using LLaMA 3.

---

## 🚀 Features

- ✅ **Bug Detection** using AI
- 🧠 **Concept Checker** — compares code against the project's purpose
- 🤖 **Auto Fixer** — uses LLaMA 3 to refactor or fix buggy code
- 🧪 **Automatic Pytest** — runs test files if available
- 🧹 **Temporary Pytest Generator** — creates minimal tests if none exist
- 📋 **AI Summary** — auto-generated summary of changes & fixes
- 📂 **Saves fixed version** in `fixed_output/` directory

---

## 📦 Installation

```bash
git clone https://github.com/your-username/ai-project-validator.git
cd ai-project-validator
pip install -r requirements.txt
```
## 🧠 Requirements
Python 3.8+

LLaMA model running locally (via Ollama)

Optional: pytest for testing

## ⚙️ Usage
```bash
python cli/validator_cli.py --path /path/to/project --concept "Describe the project purpose here"
```
## 👉 To enable auto-fixing:
```bash
python cli/validator_cli.py --path /path/to/project --concept "..." --fix
```
## 📁 Output
When --fix is used:

fixed_output/fixed_project.py: fixed project code

fixed_output/summary.txt: LLaMA explanation of changes

fixed_output/test_report.txt: result of running Pytest (if any)

Temporary test file is auto-removed after testing

## 📂 Project Structure
```bash
.
├── cli
│   └── validator_cli.py          # Entry point CLI
├── examples                      # Future usage examples
├── main.py                       # Optional main wrapper
├── README.md                     # You're reading this!
├── requirements.txt              # Dependencies
├── tests                         # Real or auto-generated test files
├── utils
│   └── ollama_client.py          # Sends prompt to LLaMA
└── validator
    ├── auto_corrector.py         # Fixes code
    ├── bug_checker.py            # Finds bugs
    ├── concept_checker.py        # Checks concept alignment
    ├── optimizer.py              # Optional code cleaner
```
## 🧪 Example
```bash
python cli/validator_cli.py --path ./my_project --concept "A web scraper that saves headlines into a database." --fix
```
## 🤖 How it Works
Bug Checker sends each .py file to LLaMA to find logic/syntax bugs.

Concept Checker asks LLaMA if code matches the described purpose.

Auto Fixer combines all code and asks LLaMA to fix/refactor it.

If --fix is used:

Saves the fixed project

Generates a summary

Runs tests (real or generated)

## 🔒 Disclaimer
Your code is processed locally through the LLaMA API, so make sure your environment is secure. This is an experimental tool — always review AI-generated code.

## 🛠 Future Improvements
🧪 Automatic full test suite generator (planned)

🔁 Per-file auto-fix mode

📊 Interactive report with scores

## 📫 Contact
Made with 💻 by [Ahmed Bouhlal]
Feel free to contribute or open issues on GitHub!

## 🧠 License
MIT License — free to use, modify, and share.
