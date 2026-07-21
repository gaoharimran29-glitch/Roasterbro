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
    print("Repository Summary")
    print("=========================")
    print("Root Path: " , scanning_result.root_path)
    print("Files Found: " , len(scanning_result.files))
    print("Directories Found: " , len(scanning_result.directories))