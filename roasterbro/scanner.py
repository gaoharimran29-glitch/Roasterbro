from roasterbro.constants import EXCLUDED_FILES , EXTENSION_LANGUAGE_MAP
import os

def check_important_files(files : list , directories : list) -> dict[str , bool]:
    readme = any(f.lower().startswith("readme") for f in files)
    _license = any(f.lower().startswith("license") for f in files)
    dockerfile = any(f.lower() == "dockerfile" for f in files)
    gitignore = any(f.lower() == ".gitignore" for f in files)
    has_test = any("test" in d.lower() for d in directories) or any("test" in f.lower() for f in files)
    return {
        "README":readme,
        "LICENSE":_license,
        "dockerfile":dockerfile,
        "gitignore":gitignore,
        "has_test":has_test
    }

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