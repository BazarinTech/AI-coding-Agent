
# GOBIN AI Coding Agent

**GOBIN** is an interactive AI-powered coding assistant designed to help developers manage Python-based projects efficiently. It can read files, write code, execute Python scripts, run shell commands (with approval), and provide intelligent guidance—all from your terminal.

> ⚠️ **Note:** Currently, GOBIN only works for Python-based projects and is designed for local development environments.

---

## 🌟 Features & Capabilities

GOBIN can perform the following tasks for Python projects:

- **Project Exploration**
  - List files and directories in the current working directory.
  - Inspect file contents quickly.

- **Code Execution**
  - Run Python scripts with optional CLI arguments.
  - Execute shell commands safely with user approval.

- **File Management**
  - Create new directories.
  - Write or overwrite files safely, creating parent directories if necessary.

- **Interactive AI Assistance**
  - Generate code snippets or function implementations.
  - Provide guidance and explanations for Python code.
  - Maintain session memory to understand ongoing tasks.

---

## ⚡ Installation

GOBIN is published on PyPI and can be installed globally using `pip`:

```bash
pip install gobin-cli
````

---

## 🔑 Setting Up Your API Key

GOBIN requires a Gemini API key. You can provide it either via an environment variable or a `.env` file.

### Option A: Environment variable

```bash
export GEMINI_API_KEY="your_api_key_here"
```

### Option B: `.env` file

Create a file named `.env` in your project directory with:

```text
GEMINI_API_KEY=your_api_key_here
```

GOBIN will automatically load the API key from this file.

---

## 🚀 Running the CLI

After installation and API key setup, launch the interactive AI agent:

```bash
gobin
```

### CLI Usage Tips

* **Exit the CLI:** Type `exit` or `quit`.
* **Clear the screen:** Type `clear` or `cls`.
* **Multiline input:** Shift+Enter for a new line, Enter to submit.

---

## 🧩 Example Workflow

1. Navigate to your Python project directory:

```bash
cd my-python-project
```

2. Run GOBIN:

```bash
gobin
```

3. Ask GOBIN to create a new Python file:

```
> create a Python file named `utils.py` with a function to calculate factorial
```

4. Inspect, run, or modify your code interactively.

---

## 🔄 Updating GOBIN

To update to the latest version:

```bash
pip install --upgrade gobin-cli
```

---

## 💻 System Requirements

* Python >= 3.8
* Compatible with Linux, macOS, and Windows
* Terminal or shell for CLI usage
* Gemini API key

---

## 📦 Project Structure

```
gobin/
├── __main__.py          # Entry point for CLI
├── cli.py               # CLI runner
├── functions/           # Core function modules (read/write/run files)
├── call_function.py     # Function dispatcher
├── pyproject.toml       # Project metadata & build system
└── README.md            # Project documentation
```

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 📝 Contribution

Feel free to submit issues or pull requests. Contributions to improve Python support, add new functions, or enhance the AI experience are welcome.

---

## 🔗 Links

* [PyPI Package](https://pypi.org/project/gobin-cli/)
* [Gemini AI API](https://developers.google.com/vertex-ai/docs/text-generation/overview)


