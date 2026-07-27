import argparse
from roasterbro.scanner import scanner
from roasterbro.analyzer import analyze_repo
from pathlib import Path

def main():

    print("Welcome to RoasterBro !")

    parser = argparse.ArgumentParser(description="RoasterBro CLI Scanner")
    parser.add_argument("path",  type=str,  nargs="?",  default=".", 
                        help="The target directory path to scan (defaults to current directory)"
                        )
    args = parser.parse_args()
    
    cwd = Path(args.path).resolve()
    scanning_result = scanner(cwd)
    print("=========================")
    print("Repository Information")
    print("==========================")
    print("Root path: " , scanning_result['root_path'])
    print("Files found: " , len(scanning_result['files']))
    print("Directories Found: " , len(scanning_result['directories']))
    print("==========================")
    print("Files Information")
    print("==========================")
    print("README.md:             " , "Yes" if scanning_result['README.md'] else "No")
    print("LICENSE:               " , "Yes" if scanning_result['LICENSE'] else "No")
    print("Dockerfile:            " , "Yes" if scanning_result['dockerfile'] else "No")
    print("Git Ignore:            " , "Yes" if scanning_result['gitignore'] else "No")
    print("Test Files:            " , "Yes" if scanning_result['has_test'] else "No")
    print("CONTRIBUTING.md:       " , "Yes" if scanning_result['CONTRIBUTING.md'] else "No")
    print("CHANGELOG.md:          " , "Yes" if scanning_result['CHANGELOG.md'] else "No")
    print("CODE_OF_CONDUCT.md:    " , "Yes" if scanning_result['CODE_OF_CONDUCT.md'] else "No")
    print("SECURITY.md:           " , "Yes" if scanning_result['SECURITY.md'] else "No")
    print("CI/CD:                 " , "Yes" if scanning_result['CI/CD'] else "No")
    print("ISSUE_TEMPLATES:       " , "Yes" if scanning_result['ISSUE_TEMPLATES'] else "No")
    print("CODEOWNERS:            " , "Yes" if scanning_result['CODEOWNER'] else "No")
    print("PULL_REQUEST_TEMPLATE: " , "Yes" if scanning_result['PULL_REQUEST_TEMPLATE'] else "No")
    print("FUNDING.yml:           " , "Yes" if scanning_result['FUNDING.yml'] else "No")
    print("=========================")
    print("Languages Used")
    print("==========================")
    for lang , count in scanning_result['language_present'].items():
        print(f"{lang}: {count}")
    analyze_result = analyze_repo(scanning_result["files"], scanning_result['has_test'], directories=scanning_result['directories'])
    print("==========================")
    print("Deep Analysis")
    print("==========================")
    print("File LOC Breakdown")
    print("===========================")
    for file , loc in analyze_result['file_lines'].items():
        print(f"{file} : {loc} LOC")
    print("===========================")
    print("Total LOC:                 " , analyze_result['total_loc'])
    print("Largest LOC File:          " , analyze_result['largest_loc_file'])
    print("README LOC:                " , analyze_result['readme_loc'])
    print("Empty Files:               " , len(analyze_result['empty_files']))
    print("Files gt than 500 LOC:     " , len(analyze_result['files_gt_500loc']))
    print("Files gt than 1000 LOC:    " , len(analyze_result['files_gt_1000loc']))
    print("Average File size:         " , analyze_result['average_file_size'] , "KB")
    print("Test Files:                " , analyze_result['test_files'])
    print("Total test files:          " , len(analyze_result['test_files']))
    print("=================================")
    print("Dependencies used")
    print("=================================")
    for file , dep in analyze_result['dep'].items():
        print("File:               " , file)
        print("Ecosystem:          " , dep['ecosystem'])
        print("Package Manager:    " , dep['package_manager'])
        print("Dependencies:       " , dep['dependencies'])
        print("Total dependencies: " , dep['dep_count'])            
        print("Frameworks:         " , dep['framework'] if dep['framework'] else {}),
        print("Total Frameworks:   " , len(dep['framework']))
        print("Category:           " , dep['framework_categories'] if dep['framework_categories'] else {})
        print("==============================")