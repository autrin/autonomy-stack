PYTHON ?= python
PKG	:= autonomy_stack

.PHONY: lint test run install

install:
$(PYTHON) -m pip installl -e ".[dev]"

lint:
	ruff check $(PKG) tests
	mypy

test:
	pytest

run:
	$(PYTHON) -m $(PKG).nodes.replay --log logs/sample_session.parquet

