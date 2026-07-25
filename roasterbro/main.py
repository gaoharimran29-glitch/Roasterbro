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
    print("README.md:       " , "Yes" if scanning_result['README.md'] else "No")
    print("LICENSE:         " , "Yes" if scanning_result['LICENSE'] else "No")
    print("Dockerfile:      " , "Yes" if scanning_result['dockerfile'] else "No")
    print("Git Ignore:      " , "Yes" if scanning_result['gitignore'] else "No")
    print("Test Files:      " , "Yes" if scanning_result['has_test'] else "No")
    print("CONTRIBUTING.md: " , "Yes" if scanning_result['CONTRIBUTING.md'] else "No")
    print("CHANGELOG.md:    " , "Yes" if scanning_result['CHANGELOG.md'] else "No")
    print("CI/CD:           " , "Yes" if scanning_result['CI/CD'] else "No")
    print("=========================")
    print("Languages Used")
    print("==========================")
    for lang , count in scanning_result['language_present'].items():
        print(f"{lang}: {count}")
    analayze_result = analyze_repo(scanning_result["files"], scanning_result['has_test'], directories=scanning_result['directories'])
    print("==========================")
    print("Deep Analysis")
    print("==========================")
    print("File LOC Breakdown")
    print("===========================")
    for file , loc in analayze_result['file_lines'].items():
        print(f"{file} : {loc} LOC")
    print("===========================")
    print("Total LOC:                 " , analayze_result['total_loc'])
    print("Largest LOC File:          " , analayze_result['largest_loc_file'])
    print("README LOC:                " , analayze_result['readme_loc'])
    print("Empty Files:               " , len(analayze_result['empty_files']))
    print("Files gt than 500 LOC:     " , len(analayze_result['files_gt_500loc']))
    print("Files gt than 1000 LOC:    " , len(analayze_result['files_gt_1000loc']))
    print("Average File size:         " , analayze_result['average_file_size'] , "KB")
    print("Test Files:                " , analayze_result['test_files'])
    print("Total test files:          " , len(analayze_result['test_files']))
    print("=================================")
    print("Dependencies used")
    print("=================================")
    for file , dep in analayze_result['dep'].items():
        print("File:             " , file)
        print("Ecosystem:        " , dep['ecosystem'])
        print("Package Manager:  " , dep['package_manager'])
        print("Dependencies:     " , dep['dependencies'])
        print("Dependency Count: " , dep['dep_count'])
        print("Frameworks:       " , dep['frameworks'])
        print("Category:         " , dep['category'])
        print("==============================")