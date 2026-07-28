from roasterbro.constants import EXCLUDED_FILES , EXTENSION_LANGUAGE_MAP, SUSPICIOUS_PATTERNS
import os
from git import Repo
from datetime import datetime
import git

def check_important_files(files: list[str], directories: list[str]) -> dict[str, bool]:
    """Check whether basic important files and directories are present in the repo."""
    
    results = {
        "README.md": False,
        "LICENSE": False,
        "dockerfile": False,
        "gitignore": False,
        "has_test": False,
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
            results["dockerfile"] = True
        elif f == ".gitignore":
            results["gitignore"] = True
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
            results["has_test"] = True

    return results

def languages_present(files) -> dict[str, int]:
    """Return all unique languages used in the directory."""
    detected_languages = {}
    for filename in files:
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext in EXTENSION_LANGUAGE_MAP:
            language = EXTENSION_LANGUAGE_MAP[ext]
            if language in detected_languages:
                detected_languages[language] += 1
            else:
                detected_languages[language] = 1
                
    return detected_languages

def analyze_git_repository(path: str) -> dict:
    """Analyze hidden git file and return git related metadata"""
    try:
        git_repo = Repo(path, search_parent_directories=True)
        git_file_path = git_repo.git_dir
        commit_count = git_repo.git.rev_list('--count' , 'HEAD')
        last_commit = git_repo.head.commit.committed_date
        last_commit_date = datetime.fromtimestamp(last_commit)
        human_readable_date = last_commit_date.strftime("%B %d, %Y, at %I:%M %p")
        unique_contributors_count = len(git_repo.git.shortlog("-sn", "HEAD").splitlines())

        today = datetime.now()
        age_diff = today - last_commit_date
        days_ago = age_diff.days

        return {
            "Git Repository": True,
            "Hidden Git File Path": git_file_path,
            "Total Contributors": unique_contributors_count,
            "Total Commits": commit_count,
            "Last Commit date": human_readable_date,
            "Days Since Last Commit": days_ago
        }
    
    except git.exc.InvalidGitRepositoryError:
        return {
            "Git Repository": False,
            "Error": "No git file detected"
        }
    except git.exc.NoSuchPathError:
        return {
            "Git Repository": False,
            "Error": "Path doesn't exists"
        }

def check_suspicious_file(files: list) -> list:
    """Check for the suspicious files (e.g. .env ) in the repo"""
    suspicious_files = []
    for file in files:
        f = os.path.normpath(file).lower().replace("\\", "/")
        if any(pattern in f for pattern in SUSPICIOUS_PATTERNS):
            suspicious_files.append(f)

    return suspicious_files

def repo_scan_findings(cwd) -> dict:
    """Analyze the repo and return root repo path , files path and directories the repo"""
    root_path = str(cwd)
    files = []
    directories = []
    for item in cwd.rglob("*"):
        if any(part in item.parts for part in EXCLUDED_FILES):
            continue
        elif item.is_dir():
            directories.append(str(item.relative_to(cwd)))
        else:
            files.append(str(item.relative_to(cwd)))

    imp_file = check_important_files(files=files, directories=directories)

    return {
        "root_path":root_path,
        "files":files,
        "directories":directories,
        "imp_file": imp_file
    }