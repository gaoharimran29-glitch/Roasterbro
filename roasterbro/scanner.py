from pydantic import BaseModel , Field , computed_field , model_validator
from typing import List

excluded_files = [".git" , ".pyc" , "__pycache__"]

class ProjectInfo(BaseModel):
    files: List[str] = Field(default_factory=list, exclude=True)
    directories: List[str] = Field(default_factory=list, exclude=True)

    @computed_field
    @property
    def readme(self) -> bool:
        """Return whether README is present in the directory."""
        return any(f.lower().startswith("readme") for f in self.files)

    @computed_field
    @property
    def license_present(self) -> bool:
        """Return whether LICENSE is present in the directory."""
        return any(f.lower().startswith("license") for f in self.files)

    @computed_field
    @property
    def dockerfile(self) -> bool:
        """Return whether Dockerfile is present in the directory."""
        return any(f.lower() == "dockerfile" for f in self.files)

    @computed_field
    @property
    def gitignore(self) -> bool:
        """Return whether .gitignore is present in the directory."""
        return ".gitignore" in self.files

    @computed_field
    @property
    def tests(self) -> bool:
        """Return whether tests folder or test files are present."""
        has_test_dir = any("test" in d.lower() for d in self.directories)
        has_test_file = any("test" in f.lower() for f in self.files)
        return has_test_dir or has_test_file
    
class Repository(BaseModel):
    root_path: str = Field(description="Root path of the current directory")
    files: List[str] = Field(description="List of all the files in the directory")
    directories: List[str] = Field(description="List of all folders in the directory")
    projectinfo: ProjectInfo = Field(description="Contains special file information")

    @model_validator(mode="before")
    @classmethod
    def inject_files_to_projectinfo(cls , data: dict) -> dict:
        """Automatically inject parent files & directories into projectinfo."""
        if isinstance(data , dict):
            files = data.get("files" , [])
            dirs = data.get("directories" , [])
            info = data.get("projectinfo" , {})
            if isinstance(info , dict):
                info["files"] = files
                info["directories"] = dirs
                data["projectinfo"] = info
        return data

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