import os
from roasterbro.utils.constants import EXTENSION_LANGUAGE_MAP

def languages_present(files: list) -> dict[str, int]:
    """Return all unique languages used in the directory."""
    detected_languages = {}
    for filename in files:
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext in EXTENSION_LANGUAGE_MAP:
            language = EXTENSION_LANGUAGE_MAP[ext]
            if language in detected_languages:
                detected_languages[language] += 1
            else:
                detected_languages[language] = 1
                
    return detected_languages