# axios

Python library and CLI to access the school electronic register from Axios

[![PyPI](https://img.shields.io/pypi/v/axios.svg)](https://pypi.org/project/axios/)
[![Changelog](https://img.shields.io/github/v/release/zmoog/axios?include_prereleases&label=changelog)](https://github.com/zmoog/axios/releases)
[![Tests](https://github.com/zmoog/axios/workflows/Test/badge.svg)](https://github.com/zmoog/axios/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/zmoog/axios/blob/master/LICENSE)

Command line utility to access https://family.axioscloud.it

## Installation

Install this tool using `pip`:

    pip install axios

## Usage

For help, run:

    axios --help

You can also use:

    python -m axios --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd axios
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest