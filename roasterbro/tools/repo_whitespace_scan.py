
def whitespace_scan(files: list) -> dict[str, list[int]]:
    """Check whitespaces in all files and return filenames along with 
    line_numbers containing trailing whitespaces 
    """
    whitespaces = {}

    for file in files:
        whitespaces_lines = []
        try:
            with open(file, encoding="utf-8") as f:
                for line_num, line in enumerate(f, start=1):
                    no_newlines = line.rstrip("\r\n")

                    if not no_newlines.strip():
                        continue
                    
                    if no_newlines.endswith((" ", "\t")):
                        whitespaces_lines.append(line_num)

                if whitespaces_lines:
                    whitespaces[file] = whitespaces_lines

        except (UnicodeDecodeError, FileNotFoundError):
            pass

    return whitespaces
