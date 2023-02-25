.PHONY:

sources = axios tests
line_length = 79
black_options = --line-length=${line_length} ${sources}
isort_options = --line-length=${line_length} --py 39 --profile black ${sources}

lint: lint-black lint-isort lint-ruff  ## Lint the project on the host

lint-black:
	black --diff --check ${black_options}

lint-isort:
	isort --diff --check ${isort_options}

lint-ruff:
	@ruff check axios tests

fix-lint: fix-black fix-isort  ## Fix linting

fix-black:
	@black ${black_options}

fix-isort:
	@isort ${isort_options}

type-check:  ## Type check the project on the host
	mypy axios tests

test:
	pytest tests -vv

ready: lint type-check test ## Make sure we're ready to ship the code in a PR