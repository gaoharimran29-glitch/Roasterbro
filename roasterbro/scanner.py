from pydantic import BaseModel , Field
from typing import List

excluded_files = [".git" , ".pyc" , "__pycache__"]

class Repository(BaseModel):
    root_path: str = Field(description="Root path of the current directory")
    files: List[str] = Field(description="List of all the files in the directory")
    directories: List[str] = Field(description="List of all folders in the directory")

def repo_scan_findings(cwd):
    """Analyze the repo and return root repo path , files path and directories the repo"""
    root_path = str(cwd)
    files = []
    directories = []
    for item in cwd.rglob("*"):
        if any(part in item.parts for part in excluded_files):
            continue
        elif item.is_dir():
            directories.append(str(item.relative_to(cwd)))
        else:
            files.append(str(item.relative_to(cwd)))

    return {
        "root_path": root_path ,
        "files": files ,
        "directories": directories
    }

def scanner(cwd):
    """Runs the repo_scan_findings function and 
    send the output to Repository Pydantic Model"""
    print("Scanning...")
    repo_finding = repo_scan_findings(cwd)
    repo_finding = Repository(**repo_finding)
    return repo_finding