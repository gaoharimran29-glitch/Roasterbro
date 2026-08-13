<div align="center">

<img src="assets/roasterbro-logo.svg" alt="RoasterBro logo" width="480">
 

### A CLI that scans your codebase — and then roasts it. 🔥

**Version 0.1.0** · Made by [Gaohar Imran](https://github.com/gaoharimran29-glitch)

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Click](https://img.shields.io/badge/built%20with-Click-informational)](https://click.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#license)
[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)](#)

</div>

---

## 📚 Table of Contents
 
- [Overview](#-overview)
- [Features](#-features)
- [Installation](#️-installation)
- [Usage](#-usage)
- [Commands](#-commands)
- [Command Details](#-command-details)
  - [scan](#scan--basic-repo-info)
  - [gitanalyze](#gitanalyze--git-insights)
  - [langs](#langs--language-breakdown)
  - [deps](#deps--dependency-analysis)
  - [filestats](#filestats--file-statistics)
  - [whitespace](#whitespace--whitespace-scanner)
  - [fullscan](#fullscan--everything-at-once)
  - [models](#models--detect-available-llms)
  - [roast](#roast--roast-your-repo-)
- [Examples](#-examples)
- [Project Structure](#️-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 📖 Overview

**RoasterBro** is a command-line tool that inspects a codebase and gives you a full picture of what's going on inside it — languages used, dependencies, file statistics, git history, whitespace hygiene, and more. When you're ready for some tough love, point it at an LLM and let it **roast your repository** based on everything it found.

Think of it as part static-analysis tool, part linter, part stand-up comedian.

---

## ✨ Features

- 🔍 **Repo Scan** — Quick overview of your project structure
- 🌐 **Language Detection** — See every language used across your codebase
- 📦 **Dependency Analysis** — Surface the dependencies your project relies on
- 📊 **File Statistics** — Metrics on files, directories, and test coverage presence
- 🌱 **Git Analysis** — Insights pulled straight from your repository's git history
- 🧹 **Whitespace Scanner** — Hunt down trailing whitespace, file by file, line by line
- 🧠 **Model Discovery** — Detect available local and cloud LLM provider API keys
- 🗂️ **Full Scan** — Run everything at once, with optional JSON export
- 🔥 **AI Roast** — Feed your repo's findings to an LLM and get roasted, powered by your choice of provider and model
- ⚡ **Short Aliases** — Every command has a fast, memorable shortcut

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/gaoharimran29-glitch/Roasterbro.git
cd Roasterbro

# Install dependencies
pip install -e .
```

> Requires **Python 3.10+**.

Once installed, the `roasterbro` command will be available in your terminal.

---

## 🚀 Usage

```bash
roasterbro [COMMAND] [PATH] [OPTIONS]
```

If no `PATH` is provided, RoasterBro defaults to scanning the **current working directory**.

Running `roasterbro` with no arguments displays the banner and a quick pointer to the help menu:

```bash
roasterbro
```

To see all available commands:

```bash
roasterbro --help
# or
roasterbro -h
```

To check the installed version:

```bash
roasterbro --version
# or
roasterbro -v
```

---

## 📋 Commands

| Command | Alias | Description |
|---|---|---|
| `scan` | `-s` | Return basic info about the repo |
| `gitanalyze` | `-g` | Return git info about the repo |
| `langs` | `-l` | Return all the languages used in the repo |
| `deps` | `-d` | Return all the dependencies used in the repo |
| `filestats` | `-fs` | Return stats related to files in the repo |
| `whitespace` | `-w` | Return filename and line number for trailing whitespace |
| `fullscan` | `-f` | Run a combined full scan (with optional JSON export) |
| `models` | `-m` | Detect local repo and cloud provider API keys |
| `roast` | `-r` | Roast the repo using an LLM |

Every command (except `models`) accepts an optional `PATH` argument pointing to the repository you want to analyze. If omitted, it defaults to the current directory.

---

## 🔎 Command Details

### `scan` — Basic Repo Info
```bash
roasterbro scan [PATH]
roasterbro -s
```
Gives you a snapshot summary of the repository: files, directories, and general structure.

### `gitanalyze` — Git Insights
```bash
roasterbro gitanalyze [PATH]
roasterbro -g
```
Analyzes the repository's git history and metadata.

### `langs` — Language Breakdown
```bash
roasterbro langs [PATH]
roasterbro -l
```
Detects and lists every programming language present in the codebase.

### `deps` — Dependency Analysis
```bash
roasterbro deps [PATH]
roasterbro -d
```
Scans the repo and reports the dependencies it relies on.

### `filestats` — File Statistics
```bash
roasterbro filestats [PATH]
roasterbro -fs
```
Reports file- and directory-level metrics, including whether test coverage appears to exist.

### `whitespace` — Whitespace Scanner
```bash
roasterbro whitespace [PATH]
roasterbro -w
```
Flags every file and line number containing trailing whitespace.

### `fullscan` — Everything at Once
```bash
roasterbro fullscan [PATH] [--json OUTPUT.json]
roasterbro -f --json results.json
```
Runs `scan`, `langs`, `deps`, `filestats`, and `gitanalyze` together and prints a combined report. Use `--json` to save the full combined results to a JSON file.

| Option | Description |
|---|---|
| `--json <path>` | Save the combined scan output to a JSON file |

### `models` — Detect Available LLMs
```bash
roasterbro models
roasterbro -m
```
Detects locally configured LLM setups and cloud provider API keys available in your environment.

### `roast` — Roast Your Repo 🔥
```bash
roasterbro roast [PATH] [--provider PROVIDER] [--llm MODEL]
roasterbro -r --provider google --llm gemini-2.5-flash-lite
```
Runs a full scan and hands the results to an LLM, which then proceeds to roast your codebase based on what it finds.

| Option | Default | Description |
|---|---|---|
| `--provider` | `google` | LLM provider company (e.g. `google`) |
| `--llm` | `gemini-2.5-flash-lite` | Specific LLM model to use |

---

## 💡 Examples

```bash
# Scan the current directory
roasterbro scan

# Analyze git history for a specific project
roasterbro gitanalyze ~/projects/my-app

# Get a full report and save it as JSON
roasterbro fullscan . --json report.json

# See which LLM providers you have configured
roasterbro models

# Get roasted using Google's Gemini
roasterbro roast . --provider google --llm gemini-2.5-flash-lite
```

---

## 🗂️ Project Structure

```
roasterbro/
├── roasterbro/                         # Main Python package
│   ├── models/                         # Pydantic models
│   │   └── roast_output_model.py       # Roast output schema
│   │
│   ├── output_formatter/               # Pretty-printers for scan results
│   │   ├── scan_output_formatter.py
│   │   ├── git_output_formatter.py
│   │   ├── lang_output_formatter.py
│   │   ├── dep_output_formatter.py
│   │   ├── filestats_output_formatter.py
│   │   ├── whitespace_output_formatter.py
│   │   └── model_output_formatter.py
│   │
│   ├── prompts/                        # Prompts used by LLMs
│   │   ├── facts_extract_prompt.py
│   │   ├── final_roast_prompt.py
│   │   └── questions_generate_prompt.py
│   │
│   ├── tools/                          # Core repository scanning and analysis
│   │   ├── repo_basic_scan.py          # Basic repository information
│   │   ├── repo_deps_scan.py           # Dependency analysis
│   │   ├── repo_file_scan.py           # File and directory analysis
│   │   ├── repo_git_scan.py            # Git repository analysis
│   │   ├── repo_lang_scan.py           # Programming language detection
│   │   ├── repo_whitespace_scan.py     # Whitespace analysis
│   │   ├── repo_roast_scan.py          # Repository roasting logic
│   │   └── find_llm_models.py          # LLM model discovery
│   │
│   ├── utils/                          # Shared utilities and configuration
│   │   ├── helpers.py                  # Path validation and scanning helpers
│   │   ├── config.py                   # LLM provider/config resolution
│   │   └── constants.py                # Project-wide constants
│   │
│   └── main.py                         # Click-based CLI entry point
│
├── setup.py                             # Package installation configuration
├── requirements.txt                     # Python dependencies
├── .env.example                         # Example environment variables
├── .gitignore                           # Git ignored files and directories
└── LICENSE                              # Project license

```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes
4. Push to the branch and open a Pull Request

If you find a bug or a security vulnerability, please report it directly to the developer.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Gaohar Imran**
- Github: [@gaoharimran29-glitch](https://github.com/gaoharimran29-glitch)
- LinkedIn: [Gaohar Imran](https://www.linkedin.com/in/gaohar-imran-5a4063379/)

---

<div align="center">

*Built for developers who can take a joke — and want their codebase analyzed while they're at it.*

</div>