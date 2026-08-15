import re
from typing import Any
from pathlib import Path

from roasterbro.utils.constants import DEPENDENCY_MAP, FRAMEWORK_SIGNATURES


pattern = r"(==|>=|<=|~=|!=)"


def clean_name(dependencies: list) -> list:
    """Clean dependency names while preserving npm scoped packages."""

    cleaned_dep = []

    for dep in dependencies:
        clean = re.split(pattern, dep, maxsplit=1)[0]
        clean = clean.replace("_", "-").strip().lower()
        cleaned_dep.append(clean)

    return cleaned_dep


def dependencies_analyzer(files: list) -> dict[str, Any]:
    """Analyze dependencies and find ecosystem, package manager,
    dependencies, frameworks, and lockfiles.
    """

    dependency_files = DEPENDENCY_MAP.keys()
    dep = {}

    for dep_file in dependency_files:
        matching_files = [
            f for f in files
            if Path(f).name == dep_file
        ]

        for actual_file_path in matching_files:
            config = DEPENDENCY_MAP[dep_file]

            ecosystem = config.get("ecosystem")
            lockfile_override = config.get("lockfile_override", {})
            parser = config.get("handler")
            default_pm = config.get("default_pm")

            pm = []

            for lockfile, package_manager in lockfile_override.items():
                if any(Path(f).name == lockfile for f in files):
                    pm.append(package_manager)

            if not pm:
                pm = default_pm

            parse_result = parser(actual_file_path)

            dependencies = parse_result.get("dependencies", [])
            cleaned_dependencies = clean_name(dependencies)

            framework = []
            framework_categories = []
            overridden_frameworks = set()

            if isinstance(ecosystem, str):
                ecosystem = [ecosystem.lower()]
            elif isinstance(ecosystem, list):
                ecosystem = [x.lower() for x in ecosystem]
            else:
                ecosystem = []

            for eco in ecosystem:
                info = FRAMEWORK_SIGNATURES.get(eco, {})

                for clean_dep in cleaned_dependencies:
                    for framework_name, framework_info in info.items():
                        packages = framework_info.get("packages", [])

                        if clean_dep not in packages:
                            continue

                        category = framework_info.get("category", "")
                        overrides = framework_info.get("overrides", [])

                        framework.append(framework_name)
                        framework_categories.append(category)

                        overridden_frameworks.update(
                            x.lower() for x in overrides
                        )

                        break

            filtered = [
                (fw, category)
                for fw, category in zip(
                    framework,
                    framework_categories
                )
                if fw.lower() not in overridden_frameworks
            ]

            framework = [fw for fw, _ in filtered]
            framework_categories = [category for _, category in filtered]

            dep.update({
                actual_file_path: {
                    "ecosystem": ecosystem,
                    "package_manager": pm,
                    "dependencies": cleaned_dependencies,
                    "dep_count": parse_result.get(
                        "dependency_count",
                        0
                    ),
                    "framework": set(framework),
                    "framework_categories": set(framework_categories),
                }
            })

    return dep
