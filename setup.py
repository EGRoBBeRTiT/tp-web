import pathlib

import pkg_resources
from setuptools import find_packages, setup


def requirements(filepath: str):
    with pathlib.Path(filepath).open() as requirements_txt:
        return [
            str(requirement)
            for requirement in pkg_resources.parse_requirements(requirements_txt)
        ]


setup(
    name="askme",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=requirements("requirements.txt"),
)