from pathlib import Path
from setuptools import setup, find_packages

BASE_DIR = Path(__file__).parent

requirements = [
    line.strip()
    for line in (BASE_DIR / "requirements.txt").read_text().splitlines()
    if line.strip() and not line.startswith("#")
]

setup(
    name="roasterbro",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "roasterbro=roasterbro.main:main",
        ],
    },
)
