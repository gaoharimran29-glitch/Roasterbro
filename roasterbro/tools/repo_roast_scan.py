import click
from roasterbro.tools.repo_basic_scan import repo_scan_findings
from roasterbro.tools.repo_deps_scan import dependencies_analyzer
from roasterbro.tools.repo_file_scan import file_metrics
from roasterbro.tools.repo_git_scan import analyze_git_repository
from roasterbro.tools.repo_lang_scan import languages_present
from roasterbro.prompts.roaster_prompt import SYSTEM_PROMPT, USER_PROMPT
import json
import requests

def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, (set, tuple)):
        return list(obj)
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    else:
        return obj

def full_scan_for_roast(cwd):

    scanning_result = repo_scan_findings(cwd)

    files = scanning_result.get("files", [])
    languages = languages_present(files=files)

    dep = dependencies_analyzer(files=files)

    directories = scanning_result.get("directories" , [])
    has_test = scanning_result.get("has_test", False)
    stats = file_metrics(files=files, has_test=has_test, directories=directories)

    git_info = analyze_git_repository(cwd)

    del scanning_result['files']
    del scanning_result['directories']
    del stats['file_sizes']

    return {
        "Repo Info": scanning_result,
        "Languages": languages,
        "Dependencies": dep,
        "File Stats": stats,
        "Git Info": git_info
    }

def generate_roast(scan_data: dict):
    scan_data = make_json_safe(scan_data)
    payload = {
        "model": "llama3.2:3b",
        "system": SYSTEM_PROMPT,
        "prompt": f"Repo data:\n{json.dumps(scan_data)}\n\nRoast this repo.",
        "stream": True,
    }
    with requests.post("http://localhost:11434/api/generate", json=payload, stream=True) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if line:
                chunk = json.loads(line)
                print(chunk.get("response", ""), end="", flush=True)