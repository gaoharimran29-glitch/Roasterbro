import json
import tomllib
import re
from pathlib import Path
from typing import Dict, Any, List

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
    
    with open(file, 'r', encoding='utf-8' , errors='ignore') as file:
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

def parse_pyproject(file_path: Path) -> Dict[str , Any]:
    """Parse the pyproject.toml file, then extract and return dependencies from it."""
    file_path = Path(file_path)
    if not file_path.exists() or not file_path.is_file():
        return {
            "dependency_count": 0,
            "dependencies": []
        }
    
    with open(file_path , "rb") as f:
        try:
            content = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            return {
                "Success" : False ,
                "Error" : str(e)
            }

    if "project" in content:
        # 1. PEP 621 Production Dependencies
        raw_deps = content["project"].get("dependencies", [])
        # 2. PEP 621 Dev / Optional Dependencies
        opt_deps_dict = content["project"].get("optional-dependencies", {})
        raw_dev_deps = []
        for group_deps in opt_deps_dict.values():
            raw_dev_deps.extend(group_deps)

        dependencies = raw_deps + raw_dev_deps
        return {
                "dependency_count": len(dependencies),
                "dependencies": dependencies
            }

    elif "tool" in content and "poetry" in content["tool"]:
        poetry_data = content["tool"]["poetry"]

        # 1. Poetry Production Dependencies
        prod_dict = poetry_data.get("dependencies", {})
        # Note: 'python' is often in this dict; you may want to filter it out
        raw_deps = [pkg for pkg in prod_dict.keys() if pkg != "python"]

        # 2. Poetry Dev Dependencies (Checks modern group syntax first, then legacy)
        dev_dict = (poetry_data.get("group", {}).get("dev", {}).get("dependencies", {}))
        if not dev_dict:
            dev_dict = poetry_data.get("dev-dependencies", {})

        raw_dev_deps = list(dev_dict.keys())
        dependencies = raw_deps + raw_dev_deps
        return {
                "dependency_count": len(dependencies),
                "dependencies": dependencies
            }

    else:
        return {
            "Success" : False ,
            "Error" : "Neither standard [project] nor [tool.poetry] sections found"
        }


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