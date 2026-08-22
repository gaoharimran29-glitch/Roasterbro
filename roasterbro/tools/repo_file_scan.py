import os

from roasterbro.tools.repo_basic_scan import is_test_path

def file_metrics(files: list , has_test: bool , directories: list) -> dict[str , int]:
    """Analyze the files of the repo and return deep metrics"""
    file_lines = {}
    file_sizes = {}
    for file in files:
        try:
            with open(file, "r" , encoding='utf-8' , errors='ignore') as f:
                line_count = sum(1 for line in f)
                size = os.path.getsize(file)
                file_lines[file] = line_count
                file_sizes[file] = size

        except (FileNotFoundError, PermissionError, IsADirectoryError, OSError):
            # File vanished, is unreadable, or is some non-regular file
            # (broken symlink, socket, etc.) - skip it instead of crashing.
            continue


    if not file_lines:
        return {
            "file_lines": {},
            "file_sizes": {},
            "total_loc": 0,
            "largest_loc_file": 0,
            "readme_loc": None,
            "empty_files": [],
            "files_gt_500loc": [],
            "files_gt_1000loc": [],
            "largest_file_size": 0,
            "average_file_size": 0,
            "test_files": [],
            "test_files_count": 0,
        }
    
    total_loc = sum(file_lines.values())
    largest_loc_file = max(file_lines.values())
    # Case-insensitive lookup so "readme.md" / "Readme.md" etc. still
    # resolve, and restricted to the repo root (not a nested docs/README.md)
    # to match check_important_files()'s definition of "the README".
    readme_loc = next(
        (loc for path, loc in file_lines.items() if path.lower() == "readme.md"),
        None
    )

    empty_files = []
    files_gt_500loc = []
    files_gt_1000_loc = []
    for file , loc in file_lines.items():
        if loc == 0:
            if "__init__.py" in file:
                continue
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
        test_files = [d for d in directories if is_test_path(d)] + [f for f in files if is_test_path(f)]
        test_files_count = len(test_files)

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
        "test_files_count" : test_files_count
    }
