.PHONY: all
all:

.PHONY: install
install:
	python -m pip install -U pip -r requirements.txt

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
