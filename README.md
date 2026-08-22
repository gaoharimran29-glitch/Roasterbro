<div align="center">

<img src="assets/roasterbro-logo.svg" alt="RoasterBro logo" width="480">
 

### A CLI that scans your codebase, interrogates you and then roasts it.

**Version 0.1.0** · Made by [Gaohar Imran](https://github.com/gaoharimran29-glitch)

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Click](https://img.shields.io/badge/built%20with-Click-informational)](https://click.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#license)
[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)](#)

</div>

---

## 📚 Table of Contents
 
- [Overview](#-overview)
- [Features](#-features)
- [Supported Languages & Ecosystems](#-supported-languages--ecosystems)
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
- [LLM Support](#-llm-support)
- [Examples](#-examples)
- [Known Limitations](#-known-limitations)
- [Project Structure](#️-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 📖 Overview

**RoasterBro** is a command-line tool that inspects a codebase and gives you a full picture of what's going on inside it — languages used, dependencies, file statistics, git history, whitespace hygiene, and more. When you're ready for some tough love, point it at an LLM and let it **roast your repository** based on everything it found.

Think of it as part static-analysis tool, part linter, part stand-up comedian.

> **Scope note:** RoasterBro's language detection works on virtually any codebase (it's extension-based). Its *dependency* and *framework* detection is currently scoped to **Python, JavaScript/TypeScript (Node.js), Rust, and Go** — see [Supported Languages & Ecosystems](#-supported-languages--ecosystems) below for exactly what that covers today.

---

## ✨ Features

* 🔍 **Repo Scan** — Quick overview of your project structure and project maturity signals
* 🌐 **Language Detection** — Recognizes 90+ file extensions across most mainstream languages
* 📦 **Dependency Analysis** — Parses `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, and `go.mod` for dependencies, package managers, and frameworks
* 📊 **File Statistics** — Inspect LOC, file sizes, largest files, empty files, and test files
* 🌱 **Git Analysis** — Insights pulled straight from your repository's Git history
* 🧹 **Whitespace Scanner** — Hunt down trailing whitespace, file by file, line by line
* 🏗️ **Project Maturity Analysis** — Detect testing, CI/CD, documentation, security, contribution, and other repository signals
* 🔐 **Suspicious File Detection** — Identify files that may require additional attention
* 🧠 **Model Discovery** — Detect available local LLM setups and configured cloud providers
* 🤖 **Multi-Provider LLM Support** — Use local models through Ollama or supported online LLM providers
* 🗂️ **Full Scan** — Run repository analysis together, with optional JSON export
* 🔥 **AI Interrogation & Roast** — Answer 3 repository-based ragebait questions before receiving a personalized final roast
* 🎯 **Evidence-Based Roasting** — Generate jokes and questions from actual repository signals instead of predefined jokes
* ⚡ **Short Aliases** — Every command has a fast, memorable shortcut

---

## 🧬 Supported Languages & Ecosystems

**Language detection** (`langs`) is extension-based and works on any codebase — it recognizes 90+ file extensions spanning most mainstream languages (Python, JavaScript/TypeScript, Go, Rust, Java, C/C++, Ruby, PHP, and many more). This part has no dependency-file requirement and works everywhere.

**Dependency and framework detection** (`deps`, and the dependency section of `fullscan`/`roast`) is more targeted. RoasterBro currently reads these manifest files:

| Ecosystem | Manifest file(s) read | Package managers detected |
|---|---|---|
| Python | `pyproject.toml`, `requirements.txt` | pip, pip/pyproject, poetry, pipenv |
| JavaScript / TypeScript (Node.js) | `package.json` | npm, yarn, pnpm |
| Rust | `Cargo.toml` | cargo |
| Go | `go.mod` | go modules |

Within those ecosystems, these frameworks are currently recognized from your dependency list:

- **Python:** Django, FastAPI, Flask
- **JavaScript/TypeScript:** Next.js, NestJS, Express, React

**Not yet supported:** manifests for other ecosystems (e.g. `composer.json` for PHP, `Gemfile` for Ruby, `pom.xml`/`build.gradle` for Java) aren't parsed yet, so `deps` won't report dependencies for those repos even though `langs` will still correctly detect the source files. If your project uses one of these, `deps`/`fullscan` will simply show no dependency file found — that's an expected current limitation, not a bug. Contributions adding new ecosystem parsers are very welcome (see [Contributing](#-contributing)).

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/gaoharimran29-glitch/Roasterbro.git
cd Roasterbro

# Install dependencies
pip install -e .
```

> Requires **Python 3.11+** (RoasterBro's TOML parsing uses the `tomllib` standard-library module, added in 3.11).

Once installed, the `roasterbro` command will be available in your terminal.

---

## 🚀 Usage

```bash
roasterbro COMMAND PATH [OPTIONS]
```

> `PATH` is **required** for every command except `models` — point it at the repository you want to analyze. Use `.` to scan the current directory.

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
| `models` | `-m` | Detect local LLM models and cloud LLM provider API keys |
| `roast` | `-r` | Interrogate the developer with 3 repository-based ragebait questions and generate a final AI roast |

Every command (except `models`) accepts a required `PATH` argument pointing to the repository you want to analyze.

---

## 🔎 Command Details

### `scan` — Basic Repo Info
```bash
roasterbro scan PATH
roasterbro -s .
```
Gives you a snapshot summary of the repository: files, directories, and general structure.

### `gitanalyze` — Git Insights
```bash
roasterbro gitanalyze PATH
roasterbro -g .
```
Analyzes the repository's git history and metadata. `PATH` must itself be the root of a git repository (RoasterBro does not search parent directories for one).

### `langs` — Language Breakdown
```bash
roasterbro langs PATH
roasterbro -l .
```
Detects and lists every recognized programming language present in the codebase, by file extension.

### `deps` — Dependency Analysis
```bash
roasterbro deps PATH
roasterbro -d .
```
Scans the repo and reports the dependencies it relies on. See [Supported Languages & Ecosystems](#-supported-languages--ecosystems) for which manifest files are currently parsed.

### `filestats` — File Statistics
```bash
roasterbro filestats PATH
roasterbro -fs .
```
Reports file- and directory-level metrics, including whether test coverage appears to exist.

### `whitespace` — Whitespace Scanner
```bash
roasterbro whitespace PATH
roasterbro -w .
```
Flags every file and line number containing trailing whitespace.

### `fullscan` — Everything at Once
```bash
roasterbro fullscan PATH [--json OUTPUT.json]
roasterbro -f . --json results.json
```
Runs `scan`, `langs`, `deps`, `filestats`, and `gitanalyze` together and prints a combined report. Use `--json` to save the full combined results to a JSON file.

| Option | Description |
|---|---|
| `--json <path>` | Save the combined scan output to a JSON file. Resolved relative to your **current shell location**, not the scanned repo. |

### `models` — Detect Available LLMs
```bash
roasterbro models
roasterbro -m
```
Detects locally configured LLM setups and cloud provider API keys available in your environment. This is the only command that doesn't take a `PATH`.

### `roast` — Roast Your Repo 🔥
```bash
roasterbro roast PATH [--provider PROVIDER] [--llm MODEL]
roasterbro -r . --provider google --llm gemini-2.5-flash-lite
```
Runs a full scan and hands the results to an LLM, which then proceeds to roast your codebase based on what it finds. Requires a usable LLM — either a running Ollama instance or a configured cloud provider API key. Run `roasterbro models` first if you're not sure what's available.

| Option | Default | Description |
|---|---|---|
| `--provider` | `google` | LLM provider company (e.g. `google`) |
| `--llm` | `gemini-2.5-flash-lite` | Specific LLM model to use |

---

## 🤖 LLM Support

RoasterBro's AI features are designed to work with different LLM providers.

### Local Models with Ollama

RoasterBro supports locally running models through Ollama.

Example:

```bash
roasterbro roast . --provider ollama --llm llama3.2:3b
```

You can use any model available through your Ollama installation.
The model does not need to be hardcoded into RoasterBro.

### Online Models

RoasterBro can also use configured online LLM providers.

Example:

```bash
roasterbro roast . --provider google --llm gemini-2.5-flash-lite
```

Provider API keys should be configured through environment variables.

Check Available Models
```bash
roasterbro models

or:

roasterbro -m
```

This command helps identify available local LLM configurations and configured online providers.

---

## 💡 Examples

```bash
# Scan the current directory (the "." is required)
roasterbro scan .

# Analyze git history for a specific project
roasterbro gitanalyze ~/projects/my-app

# Get a full report and save it as JSON (saved relative to where you run this, not to my-app)
roasterbro fullscan ~/projects/my-app --json report.json

# See which LLM providers you have configured
roasterbro models

# Get roasted using Google's Gemini
roasterbro roast . --provider google --llm gemini-2.5-flash-lite

# Get roasted using a local Ollama model instead
roasterbro roast . --provider ollama --llm llama3.2:3b
```

---

## ⚠️ Known Limitations

Being upfront about what RoasterBro doesn't do yet:

- **Dependency/framework detection is scoped to Python, JS/TS, Rust, and Go.** See [Supported Languages & Ecosystems](#-supported-languages--ecosystems). Other ecosystems (PHP, Ruby, Java, .NET, etc.) are correctly language-detected by `langs` but won't show up in `deps`.
- **`gitanalyze` looks for a `.git` directory at the exact `PATH` you give it** — it doesn't walk up through parent directories. Point it at your repo root.
- **`roast` needs a working LLM.** Either Ollama running locally, or an API key for one of the supported cloud providers (OpenAI, Groq, Google, Mistral, Anthropic) set in your environment. Run `roasterbro models` to check what's available before running `roast`.
- **`--json` on `fullscan` resolves relative to your current shell directory**, not the repository you're scanning — so `roasterbro fullscan ~/other-repo --json out.json` writes `out.json` where you ran the command, not inside `~/other-repo`.
- **"Total Size" in `scan`/`fullscan` reflects the full directory size on disk**, including files RoasterBro otherwise excludes from its file/dependency analysis (e.g. `.git` history, `node_modules` if present). File and directory *counts* are filtered; the size figure currently is not.
- **"Created At" is exact on macOS but approximate on Linux.** macOS exposes a true file-creation timestamp (`st_birthtime`), which RoasterBro uses when available. Most Linux filesystems don't track creation time at all, so on Linux this field falls back to `st_ctime` — the last time the directory's *metadata* changed (permissions, ownership, a rename, etc.), not when it was actually created. RoasterBro detects this automatically and labels the field `Created At (approx.*)` with an inline note whenever it's using the fallback, so you'll always know which one you're looking at.

Found something else? Please open an issue — see [Contributing](#-contributing).

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
├── CONTRIBUTING.md                      # Contribution guide
└── LICENSE                              # Project license

```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for the development setup, project structure, and a guide to adding support for a new ecosystem or language — that's currently the highest-value place to contribute.

Quick version:

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
