from roasterbro.constants import EXCLUDED_FILES , EXTENSION_LANGUAGE_MAP
import os
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
    }

    for file in files:
        f = file.lower()
        if f == "readme.md":
            results["README.md"] = True
        elif f == "license":
            results["LICENSE"] = True
        elif f == "dockerfile":
            results["dockerfile"] = True
        elif f == ".gitignore":
            results["gitignore"] = True
        elif f == "contributing.md":
            results["CONTRIBUTING.md"] = True
        elif f == "changelog.md":
            results["CHANGELOG.md"] = True
        elif f == "security":
            results["SECURITY.md"] = True
        elif f == "code_of_conduct.md":
            results["CODE_OF_CONDUCT.md"] = True
            
        if "test" in f:
            results["has_test"] = True

    for directory in directories:
        d = directory.lower()
        if "test" in d:
            results["has_test"] = True
        if d == ".github":
            results["CI/CD"] = True

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

def analyze_git_repository(path="."):
    try:
        git_repo = git.Repo(path, search_parent_directories=True)
        git_file_path = git_repo.git_dir

        return {
            "Git Repository": "Yes",
            "Hidden Git File Path": git_file_path
        }
    except git.exc.InvalidGitRepositoryError:
            return {
                "Git Repository: No"
            }

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

    imp_files = check_important_files(files , directories)
    language_present = languages_present(files)

    return {
        "root_path": root_path ,
        "files": files ,
        "directories": directories ,
        **imp_files ,
        "language_present":language_present
    }

def scanner(cwd):
    """Runs the repo_scan_findings function and 
    send the output to Repository Pydantic Model"""
    print("Scanning...")
    repo_finding = repo_scan_findings(cwd)
    return repo_finding