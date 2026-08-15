import os
import re
import click
from typing import Any
from datetime import datetime
from pathlib import Path

from roasterbro.utils.constants import EXCLUDED_DIRS, SUSPICIOUS_PATTERNS, EXCLUDED_EXTENSIONS


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
        elif "test" in f:
            results["Test_Files"] = True

    return results


def check_suspicious_file(files: list) -> list:
    """Check for the suspicious files (e.g. .env ) in the repo"""
    suspicious_files = []
    for file in files:
        f = os.path.normpath(file).lower().replace("\\", "/")
        if any(pattern in f for pattern in SUSPICIOUS_PATTERNS):
            suspicious_files.append(f)

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

        if item.suffix.lower() in EXCLUDED_EXTENSIONS:
            continue

        files.append(str(item.relative_to(cwd)))

    test_keywords = {"test", "tests", "__tests__", "spec", "specs"}

    has_test = (
    any(d.lower() in test_keywords for d in directories)
    or any(re.search(r"(^|[_\.\-])(test|spec)s?([_\.\-]|$)", f.lower()) for f in files)
    )

    imp_file = check_important_files(files=files)
    suspicous_file = check_suspicious_file(files=files)

    return {
        "root_path":root_path,
        "files":files,
        "directories":directories,
        "created_at": formatted_date,
        "size": round(size_in_mb, 2),
        "imp_file": imp_file,
        "suspicious_files": suspicous_file,
        "has_test": has_test
    }
