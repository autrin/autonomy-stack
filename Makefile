PYTHON ?= python
PKG    := autonomy_stack

.PHONY: install lint format test check run

install:
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	ruff check $(PKG) tests
	mypy

# Auto-fix what's safely auto-fixable; format the rest.
format:
	ruff format $(PKG) tests
	ruff check --fix $(PKG) tests

test:
	pytest

# Single entry point for "is this PR good to go".
check: lint test

run:
	$(PYTHON) -m $(PKG).nodes.replay --log logs/sample_session.parquet