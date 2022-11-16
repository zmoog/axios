from setuptools import setup
import os

VERSION = "0.1.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="axios",
    description="Command line utility to access https://family.axioscloud.it",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Maurizio Branca",
    url="https://github.com/zmoog/axios",
    project_urls={
        "Issues": "https://github.com/zmoog/axios/issues",
        "CI": "https://github.com/zmoog/axios/actions",
        "Changelog": "https://github.com/zmoog/axios/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["axios"],
    entry_points="""
        [console_scripts]
        axios=axios.cli:cli
    """,
    install_requires=[
        "click",
        "lxml",
        "requests",
        "rich",
    ],
    extras_require={
        "test": [
            "black",
            "flake8",
            "isort",
            "pytest",
            "pytest-recording",
        ]
    },
    python_requires=">=3.7",
)
