import os
import re
from roasterbro.constants import DEPENDENCY_MAP

pattern = r'(==|>=|<=|~=|!=|@)'

def clean_name(dependencies: list) -> list:
    """Clean dependencies name For eg: "curl-cffi>=0.15.0" as a curl-cffi"""

    cleaned_dep = []
    for dep in dependencies:
        parts = re.split(pattern, dep)[0]
        clean = parts.replace("_" , "-").strip().lower()
        cleaned_dep.append(clean)

    return cleaned_dep

def dependencies_analyzer(files: list) -> dict:
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
            
            dep.update({
                actual_file_path: {
                    "ecosystem": ecosystem,
                    "package_manager": pm,
                    "dependencies" :  cleaned_dependencies,
                    "dep_count" : parse_result.get('dependency_count' , 0)
                }
            })
            
    return dep
            
def analyze_repo(files: list , has_test: bool , directories: list) -> dict[str , int]:
    """Analyze the files of the repo and return deep metrics"""
    file_lines = {}
    file_sizes = {}
    for file in files:
        with open(file, "r" , encoding='utf-8' , errors='ignore') as f:
            line_count = sum(1 for line in f)
            size = os.path.getsize(file)
            file_lines[file] = line_count
            file_sizes[file] = size

    total_loc = sum(file_lines.values())
    largest_loc_file = max(file_lines.values())
    readme_loc = file_lines.get("README.md") or file_lines.get("readme")

    empty_files = []
    files_gt_500loc = []
    files_gt_1000_loc = []
    for file , loc in file_lines.items():
        if loc == 0:
            empty_files.append(file)
        elif loc >= 500 and loc<1000:
            files_gt_500loc.append(file)
        elif loc >= 1000:
            files_gt_1000_loc.append(file)

    largest_file_size = max(file_sizes.values())
    average_file_size = sum(file_sizes.values()) / len(file_sizes.values()) ## in kb
    average_file_size = round(average_file_size , 2)

    test_files = []
    test_files_count = 0

    if has_test:
        test_files = [d for d in directories if "test" in d.lower()] +  [d for d in files if "test" in d.lower()]
        test_files_count = len(test_files)

    dependencies_analyze = dependencies_analyzer(files)

    return {
        "file_lines" : file_lines ,
        "file_sizes" : file_sizes ,
        "total_loc" : total_loc ,
        "largest_loc_file" : largest_loc_file ,
        "readme_loc" : readme_loc ,
        "empty_files" : empty_files ,
        "files_gt_500loc" : files_gt_500loc ,
        "files_gt_1000loc" : files_gt_1000_loc ,
        "largest_file_size" : largest_file_size ,
        "average_file_size" : average_file_size ,
        "test_files" : test_files ,
        "test_files_count" : test_files_count ,
        "dep" : dependencies_analyze
    }