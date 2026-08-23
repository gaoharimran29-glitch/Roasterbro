from pathlib import Path
from setuptools import setup, find_packages

BASE_DIR = Path(__file__).parent

requirements = [
    line.strip()
    for line in (BASE_DIR / "requirements.txt").read_text().splitlines()
    if line.strip() and not line.startswith("#")
]

long_description = (BASE_DIR / "README.md").read_text(encoding="utf-8")

setup(
    name="roasterbro",
    version="0.1.0",
    description="A CLI that scans your codebase, interrogates you, and then roasts it.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Gaohar Imran",
    url="https://github.com/gaoharimran29-glitch/Roasterbro",
    project_urls={
        "Source": "https://github.com/gaoharimran29-glitch/Roasterbro",
        "Bug Tracker": "https://github.com/gaoharimran29-glitch/Roasterbro/issues",
    },
    license="MIT",
    license_files=["LICENSE"],
    keywords=["cli", "code-analysis", "git", "roast", "developer-tools", "llm"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Utilities",
    ],
    python_requires=">=3.11",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "roasterbro=roasterbro.main:main",
        ],
    },
)
