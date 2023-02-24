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

test:
	pytest tests

ready: lint test ## Make sure we're ready to ship the code in a PR