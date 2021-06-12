import json
from setuptools import setup, find_packages


with open("manifest.json") as fp:
    manifest = json.load(fp)


setup(
    name=manifest["package"],
    version=manifest["human_version"],
    tests_require=["PyQt5-stubs" "anki", "black", "flake8", "isort", "mypy"],
    packages=find_packages("src"),
    package_dir={"": "src"},
)
