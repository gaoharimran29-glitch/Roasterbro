# Contributing to RoasterBro

Thanks for considering a contribution — bug reports, docs fixes, and new ecosystem support are all genuinely useful at this stage.

## Table of Contents

- [Before You Start](#before-you-start)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Making Changes](#making-changes)
- [Adding Support for a New Ecosystem](#adding-support-for-a-new-ecosystem)
- [Adding Support for a New Language](#adding-support-for-a-new-language)
- [Manual Testing](#manual-testing)
- [Commit & PR Guidelines](#commit--pr-guidelines)
- [Reporting Bugs](#reporting-bugs)
- [Reporting Security Issues](#reporting-security-issues)
- [Code of Conduct](#code-of-conduct)

---

## Before You Start

All participants are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md) — the short version: roast the code, not the person.

RoasterBro is early (`0.2.0`) and the scope is intentionally limited right now — see the [Known Limitations](README.md#-known-limitations) and [Supported Languages & Ecosystems](README.md#-supported-languages--ecosystems) sections of the README before assuming something is broken. A lot of "missing" behavior (e.g. no PHP/Ruby/Java dependency parsing) is a known gap, not a bug — and it's a great place to contribute.

If you're planning something larger than a small fix (a new command, a big refactor, a new output format), please open an issue first to discuss the approach before writing code. Smaller fixes and new ecosystem parsers can go straight to a PR.

---

## Development Setup

```bash
# Fork the repo on GitHub, then clone your fork
git clone https://github.com/gaoharimran29-glitch/Roasterbro.git
cd Roasterbro

# Install in editable mode so your changes take effect immediately
pip install -e .
```

Requires **Python 3.11+** (RoasterBro uses the `tomllib` standard-library module, added in 3.11).

If you're working on the `roast` command or anything LLM-related, copy `.env.example` to `.env` and fill in whichever provider key you're testing against, or have Ollama running locally:

```bash
cp .env.example .env
```

Remote GitHub scans do not require a token for public repositories, but setting `GITHUB_TOKEN` is recommended for private repositories and higher API limits. Never commit the token to `.env` or source control.

---

## Project Structure

A quick map before you dive in:

```
roasterbro/
├── assets/
│   ├── roasterbro-logo.svg             # Roasterbro Logo
│
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
│   │   ├── repo_remote_scan.py         # Remote GitHub repository scanning
│   │   └── find_llm_models.py          # LLM model discovery
│   │
│   ├── utils/                          # Shared utilities and configuration
│   │   ├── helpers.py                  # Path validation and scanning helpers
│   │   ├── config.py                   # LLM provider/config resolution
│   │   ├── constants.py                 # Project-wide constants
│   │   └── github_api.py                # GitHub API client for remote scans
│   │
│   └── main.py                         # Click-based CLI entry point
│
├── setup.py                             # Package installation configuration
├── requirements.txt                     # Python dependencies
├── .env.example                         # Example environment variables
├── .gitignore                           # Git ignored files and directories
├── CONTRIBUTING.md                      # Contribution guide
├── CHANGELOG.md                         # Track the new unreleased changes
├── SECURITY.md                          # Security Policy
├── README.md                            # Project Documentation
├── MANIFEST.in                          # Distribution file inclusion
├── CODE_OF_CONDUCT.md                   # Contributor behavior guidelines
└── LICENSE                              # Project license
```

If you're fixing a display/wording issue, you probably want `output_formatter/` or `prompts/`. If you're fixing detection logic, you probably want `tools/` or `constants.py`.

---

## Making Changes

1. Create a feature branch off `main`:
   ```bash
   git checkout -b feature/short-description
   ```
2. Make your change. Keep the diff focused — unrelated formatting or renames make PRs harder to review.
3. Run the affected command(s) against a few different real repos (see [Manual Testing](#manual-testing)) before opening a PR.
4. Update `README.md` if you changed user-facing behavior (a flag, a default, a supported ecosystem, etc.) — stale docs are worse than no docs.
5. Update CHANGELOG.md under the [Unreleased] section if your change introduces a new feature, changes existing behavior, fixes a bug, or removes functionality.
6. Push and open a PR against `main`.

---

## Adding Support for a New Ecosystem

This is probably the highest-value contribution right now. To add a new ecosystem (e.g. PHP/`composer.json`, Ruby/`Gemfile`, Java/`pom.xml`):

1. **Write a parser** in `utils/helpers.py` following the existing pattern (see `parse_requirements`, `parse_node`, `parse_cargo`, `parse_gomod`). It should accept a file path and return:
   ```python
   {"dependency_count": int, "dependencies": list[str]}
   ```
2. **Register the manifest file** in `DEPENDENCY_MAP` in `utils/constants.py`:
   ```python
   "composer.json": {
       "ecosystem": "PHP",
       "default_pm": "composer",
       "lockfile_override": {"composer.lock": "composer"},
       "handler": parse_composer,
   }
   ```
3. **Add framework signatures**, if relevant, under the matching ecosystem key (lowercased) in `FRAMEWORK_SIGNATURES`. Each entry needs a `"packages"` list of the actual dependency-name strings that should trigger a match (not just the framework's display name — this bit an earlier version of RoasterBro, so double check your `packages` list actually matches what the parser outputs), a `"category"`, and an `"overrides"` list for frameworks that shouldn't also be flagged as a separate lower-level framework (e.g. Next.js overriding a bare React detection).
4. Test against a couple of real projects in that ecosystem and confirm `roasterbro deps <path>` reports what you expect.
5. Update the ecosystem table in `README.md`.

## Adding Support for a New Language

Language detection (`langs`) is just an extension-to-name lookup. To add a language, add its extension(s) to `EXTENSION_LANGUAGE_MAP` in `utils/constants.py`. No parser needed — this is a much smaller change than ecosystem support.

---

## Manual Testing

There isn't an automated test suite yet (contributions adding one — pytest, fixtures with sample repos of each supported ecosystem, etc. — are very welcome). Until then, please manually verify your change against a few real repositories before opening a PR:

```bash
# Basic sanity check
roasterbro scan .
roasterbro fullscan . --json /tmp/out.json

# If you touched dependency/framework detection, test against a repo
# that actually uses the ecosystem you changed
roasterbro deps ~/some-project-using-that-ecosystem

# If you touched git logic, test against:
#  - a normal repo with history
#  - a freshly `git init`'d repo with zero commits
#  - a non-git directory
roasterbro gitanalyze <path>

# If you touched remote scanning or GitHub API logic, test a public repository
# and, when credentials are available, a private repository or alternate ref.
roasterbro remote OWNER/REPO
roasterbro remote OWNER/REPO --ref BRANCH --json remote-report.json
```

If you changed anything path-related, also test scanning a repo that is **not** your current shell directory (`roasterbro scan ~/some-other-repo` from somewhere else) — path-resolution bugs are the easiest thing to miss here.

---

## Commit & PR Guidelines

- Write commit messages that describe *what* changed and, if it's not obvious, *why*.
- Keep PRs scoped to one change/fix. Multiple unrelated fixes in one PR slow down review.
- In the PR description, say what you tested it against (which repos/ecosystems) — this project has no CI yet, so this is currently the main signal a reviewer has.
- Be responsive to review feedback; if a PR goes stale for a long time, it may be closed and can be reopened later.

---

## Reporting Bugs

Please open an issue and include:

- The exact command you ran (`roasterbro deps .`, etc.)
- What you expected vs. what happened
- Your OS and Python version (`python3 --version`)
- If relevant, a minimal repro — a small sample repo/manifest file that reproduces the issue is extremely helpful for dependency/framework detection bugs specifically

## Reporting Security Issues

Please **do not** open a public issue for security vulnerabilities (e.g. anything related to the suspicious-file detection being bypassed, or a way to get RoasterBro to execute untrusted content). Report it directly to the developer instead — see the [Author](README.md#-author) section of the README for contact info.

## Code of Conduct

Be respectful and constructive. Disagreements about implementation are fine and expected; personal attacks aren't. Maintainers may edit, close, or lock issues/PRs that don't meet this bar.
