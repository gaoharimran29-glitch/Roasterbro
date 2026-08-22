import os
import re
import click
from typing import Any
from datetime import datetime
from pathlib import Path

from roasterbro.utils.constants import EXCLUDED_DIRS, SUSPICIOUS_PATTERNS, EXCLUDED_EXTENSIONS


TEST_PATTERN = re.compile(r"(^|[_.\-/])(test|spec)s?([_.\-/]|$)")


def is_test_path(path: str) -> bool:
    """Word-boundary aware check for whether a path looks like a test
    file/directory. Avoids false positives like 'latest_report.py' or
    'attestation.md' that a plain 'test' in path substring check would
    incorrectly flag.
    """
    return bool(TEST_PATTERN.search(path.lower()))


def check_important_files(files: list[str]) -> dict[str, bool]:
    """Check whether basic important files and directories are present in the repo."""
    
    results = {
        "README.md": False,
        "LICENSE": False,
        "Dockerfile": False,
        ".gitignore": False,
        "Test_Files": False,
        "CONTRIBUTING.md": False,
        "CHANGELOG.md": False,
        "SECURITY.md": False,
        "CODE_OF_CONDUCT.md": False,
        "CI/CD": False,
        "ISSUE_TEMPLATES": False,
        "PULL_REQUEST_TEMPLATE": False,
        "CODEOWNER": False,
        "FUNDING.yml": False,
    }

    for file in files:
        f = os.path.normpath(file).lower().replace("\\", "/")
        if f == "readme.md":
            results["README.md"] = True
        elif f.startswith("license"):
            results["LICENSE"] = True
        elif f == "dockerfile":
            results["Dockerfile"] = True
        elif f == ".gitignore":
            results[".gitignore"] = True
        elif f == "contributing.md":
            results["CONTRIBUTING.md"] = True
        elif f == "changelog.md":
            results["CHANGELOG.md"] = True
        elif f == "security.md":
            results["SECURITY.md"] = True
        elif f == "code_of_conduct.md":
            results["CODE_OF_CONDUCT.md"] = True
        elif f.startswith(".github/workflows") or f.startswith(".github/actions"):
            results["CI/CD"] = True
        elif f.startswith(".github/issue_template"):
            results["ISSUE_TEMPLATES"] = True
        elif f.startswith(".github/pull_request_template"):
            results["PULL_REQUEST_TEMPLATE"] = True
        elif f == ".github/codeowners":
            results['CODEOWNER'] = True
        elif f == ".github/funding.yml":
            results['FUNDING.yml'] = True     
        elif is_test_path(f):
            results["Test_Files"] = True

    return results


def check_suspicious_file(files: list) -> list:
    """Check for the suspicious files (e.g. .env) in the repo.

    Matches against the file's own basename (exact match, or basename
    startswith "pattern.") rather than a raw substring search across the
    whole path - a plain 'pattern in path' substring check false-positives
    on innocuous files like 'app.environment.json' matching '.env'.
    """
    suspicious_files = []
    for file in files:
        f = os.path.normpath(file).lower().replace("\\", "/")
        basename = f.rsplit("/", 1)[-1]

        for pattern in SUSPICIOUS_PATTERNS:
            if basename == pattern or basename.startswith(f"{pattern}."):
                suspicious_files.append(f)
                break

    return suspicious_files


def repo_scan_findings(cwd: Path) -> dict[str, Any]:
    """Analyze the repo and return root repo path , files path and directories the repo"""

    click.secho("")
    click.secho("─" * 50, fg="bright_black")
    click.secho(f"📂 Scanning: ", fg="cyan", bold=True, nl=False)
    click.secho(f"{cwd}", fg="white")
    click.secho("─" * 50, fg="bright_black")
    click.secho("")

    stat = cwd.stat()

    # True file-creation time is only available on some platforms
    # (e.g. macOS via st_birthtime). On Linux, most filesystems don't
    # track creation time at all, so we fall back to st_ctime - which is
    # the last time the *metadata* changed (permissions, ownership,
    # rename, etc.), NOT when the directory was created. We surface
    # `created_at_is_exact` so callers/formatters can label this
    # accurately instead of silently presenting an approximation as fact.
    created_at_is_exact = hasattr(stat, 'st_birthtime')
    created_time = getattr(stat, 'st_birthtime', stat.st_ctime)
    formatted_date = datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')
    total_bytes = sum(f.stat().st_size for f in cwd.rglob('*') if f.is_file())
    size_in_mb = total_bytes / (1024 * 1024)
    
    root_path = str(cwd)
    files = []
    directories = []
    for item in cwd.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in item.parts):
            continue

        if item.is_dir():
            directories.append(str(item.relative_to(cwd)))
            continue

        if not item.is_file():
            # Skips broken/dangling symlinks, sockets, devices, etc. -
            # is_dir() and is_file() both return False for these, so
            # without this check they'd fall through into `files` and
            # crash later when something tries to open() them.
            continue

        if item.suffix.lower() in EXCLUDED_EXTENSIONS:
            continue

        files.append(str(item.relative_to(cwd)))

    test_keywords = {"test", "tests", "__tests__", "spec", "specs"}

    has_test = (
    any(d.lower() in test_keywords for d in directories)
    or any(is_test_path(f) for f in files)
    )

    imp_file = check_important_files(files=files)
    suspicous_file = check_suspicious_file(files=files)

    return {
        "root_path":root_path,
        "files":files,
        "directories":directories,
        "created_at": formatted_date,
        "created_at_is_exact": created_at_is_exact,
        "size": round(size_in_mb, 2),
        "imp_file": imp_file,
        "suspicious_files": suspicous_file,
        "has_test": has_test
    }
