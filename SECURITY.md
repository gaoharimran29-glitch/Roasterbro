# Security Policy

## Supported Versions

RoasterBro is early-stage (`0.1.0`) and does not yet maintain multiple release branches. Security fixes are made against the latest release on `main`.

| Version | Supported |
|---|---|
| 0.1.x   | ✅ |
| < 0.1.0 | ❌ |

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.** Public issues are visible to everyone immediately, including anyone who might misuse the report before a fix ships.

Instead, report it privately and directly to the developer:

- GitHub: [@gaoharimran29-glitch](https://github.com/gaoharimran29-glitch)
- LinkedIn: [Gaohar Imran](https://www.linkedin.com/in/gaohar-imran-5a4063379/)

When reporting, please include:

- A description of the vulnerability and its potential impact
- Steps to reproduce it (a minimal repo/manifest file is ideal if the issue is scan/parsing related)
- The RoasterBro version and Python version you tested against
- Whether you're aware of it being exploitable in a way beyond what's described in [Known Limitations](README.md#-known-limitations)

This is currently a solo/early-stage project without a dedicated security team, so response times are best-effort rather than guaranteed — but reports will be taken seriously and acknowledged as soon as possible. Once a fix is available, it will be released and the reporter credited (if desired) in the release notes.

---

## Things to Know Before Running RoasterBro

RoasterBro is a local static-analysis CLI. It reads files from whatever `PATH` you point it at — it does not execute code from the scanned repository. That said, a few things are worth understanding before you run it against a repo you don't fully trust, or before you use the `roast` command:

### File contents are read locally, not uploaded
`scan`, `langs`, `deps`, `filestats`, `whitespace`, and `gitanalyze` operate entirely on your machine. File contents (LOC counts, whitespace scans, dependency manifests) are never sent anywhere by these commands.

### `roast` sends repository *metadata* — not raw file contents — to an LLM provider
When you run `roast` (or `fullscan`/`roast` with a cloud `--provider`), RoasterBro sends a JSON summary to the selected LLM to generate the roast. That payload includes things like:

- Detected languages and their file counts
- Dependency names and package managers (from `deps`)
- File statistics (LOC, largest files, empty files, test file paths)
- Git metadata (commit count, contributor count, branch names, last-commit date)
- **Filenames** flagged by suspicious-file detection (e.g. the fact that a `.env` file exists) — but not their contents

It does **not** send full file contents, secret values, or environment variable values.

If you use a **cloud** provider (`--provider openai/groq/google/mistral/anthropic`), that metadata leaves your machine and is subject to that provider's own data handling policies. If you'd rather nothing leave your machine, use `--provider ollama` with a local model instead — `roasterbro models` will show you what's available.

If you're scanning a private or sensitive codebase and want to double check what's included in that payload, run `fullscan --json out.json` first and inspect the file — it's the same shape of data `roast` builds internally.

### Suspicious-file detection is a heads-up, not a guarantee
`scan` flags filenames matching common secret-bearing patterns (`.env`, `id_rsa`, `credentials.json`, etc. — see `SUSPICIOUS_PATTERNS` in `roasterbro/utils/constants.py`) so you notice them. This is a simple filename match, not a secret scanner — it won't catch secrets embedded in arbitrary files, and it isn't a substitute for a dedicated tool like `git-secrets`, `trufflehog`, or `gitleaks` if that's what you actually need.

### `.env` and API keys
If you use cloud LLM providers, your API keys are read from environment variables (see `.env.example`). Keep your real `.env` out of version control — it's already covered by `.gitignore` — and never pass API keys on the command line where they could end up in your shell history.

### Running against untrusted repositories
RoasterBro doesn't execute anything from the scanned repo, but `gitanalyze`/`roast` do shell out to your local `git` installation (via GitPython) to read repository metadata. This carries the same general caution as running `git` commands against any repository you don't trust — RoasterBro doesn't introduce a new attack surface beyond what `git log`/`git shortlog` etc. already have, but "don't run tools against repos you don't trust" is still good general practice.

---

Thanks for helping keep RoasterBro and its users safe.
