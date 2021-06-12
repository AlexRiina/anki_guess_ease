import json
import pathlib
from setuptools import setup, find_packages


with (pathlib.Path(__file__).resolve().parent / "anki_guess_ease" / "manifest.json").open() as fp:
    manifest = json.load(fp)


setup(
    name=manifest["package"],
    version=manifest["human_version"],
    tests_require=["PyQt5-stubs" "anki", "black", "flake8", "isort", "mypy"],
    packages=["anki_guess_ease"],
    package_data={
        "anki_guess_ease": ["manifest.json"],
    },
)
