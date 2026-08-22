import os
import json
import tomllib
import re
from pathlib import Path
from typing import Dict, Any, List
import click


def scan_and_validate(path: str | None, function_name: str) -> Path:
    if path is None:
        click.secho("Nothing specified, nothing added.", fg="red", bold=True)
        click.secho(f"hint: Maybe you wanted to say 'roasterbro {function_name} .'?", fg="yellow")
        raise click.exceptions.Exit(1)
        
    cwd = Path(path).resolve()
    
    if not cwd.exists():
        click.secho(f"✖ Error: Path doesn't exists -> {cwd}", fg="red", bold=True)
        raise click.exceptions.Exit(1)
    
    if not cwd.is_dir():
        click.secho(f"✖ Error: It is not a directory -> {cwd}", fg="red", bold=True)
        raise click.exceptions.Exit(1)

    os.chdir(cwd)
    return cwd


def parse_requirements(file_path: Path) -> Dict[str , Any]:
    """Parse the requirements.txt file, then extract and return dependencies from it."""
    file_path = Path(file_path)
    if not file_path.exists() or not file_path.is_file():
            return {
                "dependency_count": 0,
                "dependencies": []
            }
    
    dependencies = []
    with open(file_path, "r" , encoding='utf-8' , errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            if "#" in line:
                line = line.split("#")[0].strip()
            if line:
                dependencies = dependencies + [line]

    return {
            "dependency_count": len(dependencies),
            "dependencies": dependencies
        }


def parse_node(file_path: Path) -> Dict[str , Any]:
    """Parse the package.json file, then extract and return dependencies from it."""
    file_path = Path(file_path)
    if not file_path.exists() or not file_path.is_file():
        return {
            "dependency_count": 0,
            "dependencies": []
        }
    
    with open(file_path, 'r', encoding='utf-8' , errors='ignore') as file:
        try:
            content = json.load(file)
        except json.JSONDecodeError as e:
            return {
                "Success" : False ,
                "Error" : str(e)
            }
    
    prod_dependencies = content.get("dependencies" , {})
    dev_dependecies = content.get("devDependencies" , {})
    merged_dependencies = prod_dependencies | dev_dependecies
    dependencies = []

    for key in merged_dependencies:
        dependencies.append(key)

    return {
            "dependency_count": len(dependencies),
            "dependencies": dependencies
        }


def parse_pyproject(file_path: Path) -> Dict[str, Any]:
    """Parse pyproject.toml and extract production and development dependencies."""

    result = {
        "success": True,
        "dependency_count": 0,
        "dependencies": [],
        "error": None,
    }

    file_path = Path(file_path)

    if not file_path.exists():
        result["success"] = False
        result["error"] = f"File does not exist: {file_path}"
        return result

    if not file_path.is_file():
        result["success"] = False
        result["error"] = f"Path is not a file: {file_path}"
        return result

    try:
        with file_path.open("rb") as f:
            content = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        result["success"] = False
        result["error"] = f"Invalid TOML: {e}"
        return result
    except OSError as e:
        result["success"] = False
        result["error"] = f"Unable to read file: {e}"
        return result

    dependencies: list[str] = []

    # PEP 621: [project]
    project = content.get("project", {})

    if isinstance(project, dict):

        # Production dependencies
        raw_deps = project.get("dependencies", [])

        if isinstance(raw_deps, list):
            dependencies.extend(
                dep for dep in raw_deps
                if isinstance(dep, str)
            )

        # Optional dependencies / extras
        optional_dependencies = project.get(
            "optional-dependencies",
            {}
        )

        if isinstance(optional_dependencies, dict):
            for group_deps in optional_dependencies.values():
                if isinstance(group_deps, list):
                    dependencies.extend(
                        dep for dep in group_deps
                        if isinstance(dep, str)
                    )

    # PEP 735: [dependency-groups]
    dependency_groups = content.get("dependency-groups", {})

    if isinstance(dependency_groups, dict):
        for group_deps in dependency_groups.values():

            if isinstance(group_deps, list):
                dependencies.extend(
                    dep for dep in group_deps
                    if isinstance(dep, str)
                )

    # Poetry: [tool.poetry]
    tool = content.get("tool", {})

    if isinstance(tool, dict):
        poetry = tool.get("poetry", {})

        if isinstance(poetry, dict):

            # Production dependencies
            poetry_dependencies = poetry.get(
                "dependencies",
                {}
            )

            if isinstance(poetry_dependencies, dict):
                dependencies.extend(
                    package
                    for package in poetry_dependencies
                    if package != "python"
                )

            # Modern Poetry dev dependencies
            groups = poetry.get("group", {})

            if isinstance(groups, dict):
                for group in groups.values():

                    if not isinstance(group, dict):
                        continue

                    group_dependencies = group.get(
                        "dependencies",
                        {}
                    )

                    if isinstance(group_dependencies, dict):
                        dependencies.extend(
                            package
                            for package in group_dependencies
                        )

            # Legacy Poetry dev dependencies
            dev_dependencies = poetry.get(
                "dev-dependencies",
                {}
            )

            if isinstance(dev_dependencies, dict):
                dependencies.extend(
                    package
                    for package in dev_dependencies
                )

    # Remove duplicates while preserving order
    dependencies = list(dict.fromkeys(dependencies))

    result["dependencies"] = dependencies
    result["dependency_count"] = len(dependencies)

    return result


def parse_cargo(file_path: Path) -> Dict[str , Any]:
    """Parse the Cargo.toml file, then extract and return dependencies from it."""
    file_path = Path(file_path)
    if not file_path.exists() or not file_path.is_file():
        return {
            "dependency_count": 0,
            "dependencies": []
        }
    
    with open(file_path, "rb") as f:
        try:
            content = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            return {
                "Success": False,
                "Error": str(e)
            }

    dependencies = []
    
    prod_dependencies = content.get("dependencies", {})
    dependencies.extend(prod_dependencies.keys())
    
    dev_dependencies = content.get("dev-dependencies", {})
    dependencies.extend(dev_dependencies.keys())
    
    workspace_table = content.get("workspace", {})
    if isinstance(workspace_table, dict):
        workspace_dependencies = workspace_table.get("dependencies", {})
        dependencies.extend(workspace_dependencies.keys())

    return {
            "dependency_count": len(dependencies),
            "dependencies": dependencies
        }


def parse_gomod(file_path: Path, include_indirect: bool = False) -> Dict[str, Any]:
    """
    Parses a go.mod file to extract direct (and optionally indirect) dependencies.
    """
    file_path = Path(file_path)
    if not file_path.exists() or not file_path.is_file():
        return {
            "dependency_count": 0,
            "dependencies": []
        }

    direct_deps: List[str] = []
    indirect_deps: List[str] = []
    
    in_require_block = False

    with open(file_path, "r", encoding="utf-8" , errors='ignore') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("//"):
                continue

            if line.startswith("require ("):
                in_require_block = True
                continue

            if in_require_block and line == ")":
                in_require_block = False
                continue

            if in_require_block or line.startswith("require "):
                clean_line = re.sub(r"^require\s+", "", line).strip()
                
                parts = clean_line.split()
                if not parts:
                    continue

                module_path = parts[0]

                if "// indirect" in clean_line:
                    indirect_deps.append(module_path)
                else:
                    direct_deps.append(module_path)

    target_deps = direct_deps + (indirect_deps if include_indirect else [])

    return {
        "dependency_count": len(target_deps),
        "dependencies": target_deps
    }
