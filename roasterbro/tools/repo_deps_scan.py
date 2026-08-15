import re
from typing import Any

from roasterbro.utils.constants import DEPENDENCY_MAP, FRAMEWORK_SIGNATURES

pattern = r'(==|>=|<=|~=|!=|@)'


def clean_name(dependencies: list) -> list:
    """Clean dependencies name For eg: "curl-cffi>=0.15.0" as a curl-cffi"""

    cleaned_dep = []
    for dep in dependencies:
        if dep.startswith("@"):
            clean = dep.replace("@" , "" , 1)
            cleaned_dep.append(clean)
        else:
            parts = re.split(pattern, dep)[0]
            clean = parts.replace("_" , "-").strip().lower()
            cleaned_dep.append(clean)

    return cleaned_dep


def dependencies_analyzer(files: list) -> dict[str, Any]:
    """Analyze the dependencies and find relevant ecosystem, 
    package_manager, dependencies, framework, lockfile etc. 
    """
    dependency_files = DEPENDENCY_MAP.keys()
    dep = {}
    
    for dep_file in dependency_files:
        actual_file_path = next((f for f in files if dep_file in f), None)
        if actual_file_path: 
            config = DEPENDENCY_MAP[dep_file] 
            ecosystem = config.get("ecosystem")
            lockfile_override = config.get("lockfile_override")
            parser = config.get("handler")
            default_pm = config.get("default_pm")
            pm = []
            if lockfile_override.keys():
                for lockfile in lockfile_override.keys():
                    if any(lockfile in f for f in files):
                        pm.append(lockfile_override.get(lockfile))

            if not pm:
                pm = default_pm

            parse_result = parser(actual_file_path)
            dependencies = parse_result.get('dependencies' , [])
            cleaned_dependencies = clean_name(dependencies)

            framework = []
            framework_categories = []
            overridden_frameworks = set()

            if isinstance(ecosystem, str):
                ecosystem = [ecosystem.lower()]

            if isinstance(ecosystem, list):
                ecosystem = [x.lower() for x in ecosystem]

            for eco in ecosystem:
                info = FRAMEWORK_SIGNATURES.get(eco, {})

                for clean_dep in cleaned_dependencies:
                    if clean_dep not in info:
                        continue

                    framework_info = info[clean_dep]

                    category = framework_info.get("category", "")
                    overrides = framework_info.get("overrides", [])

                    framework.append(clean_dep)
                    framework_categories.append(category)

                    overridden_frameworks.update(
                        x.lower() for x in overrides
                    )

            filtered = [
                (fw, category)
                for fw, category in zip(framework, framework_categories)
                if fw.lower() not in overridden_frameworks
            ]

            framework = [fw for fw, _ in filtered]
            framework_categories = [category for _, category in filtered]

            dep.update({
                actual_file_path: {
                    "ecosystem": ecosystem,
                    "package_manager": pm,
                    "dependencies" :  cleaned_dependencies,
                    "dep_count" : parse_result.get('dependency_count' , 0),
                    "framework": set(framework),
                    "framework_categories": set(framework_categories)
                }
            })
            
    return dep
