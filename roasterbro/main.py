import argparse
from roasterbro.scanner import scanner
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
    print("=========================")
    print("Files Information")
    print("==========================")
    print("README:       " , "Yes" if scanning_result['README'] else "No")
    print("LICENSE:      " , "Yes" if scanning_result['LICENSE'] else "No")
    print("Dockerfile:   " , "Yes" if scanning_result['dockerfile'] else "No")
    print("Git Ignore:   " , "Yes" if scanning_result['gitignore'] else "No")
    print("Test Files:   " , "Yes" if scanning_result['has_test'] else "No")
    print("=========================")
    print("Languages Used")
    print("==========================")
    for lang , count in scanning_result['language_present'].items():
        print(f"{lang}: {count}")