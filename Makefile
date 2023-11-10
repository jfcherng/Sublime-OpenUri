.PHONY: all
all:

.PHONY: ci-check
ci-check:
	mypy -p plugin
	flake8 .
	black --preview --check --diff .
	isort --check --diff .

.PHONY: ci-fix
ci-fix:
	autoflake --in-place .
	black . --preview
	isort .
