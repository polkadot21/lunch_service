# Makefile

.PHONY: check


check:
	@echo "Running ruff format..."
	ruff format .
	@echo "Running ruff check..."
	ruff check . --fix
	@echo "Running mypy..."
	mypy .
	@echo "Running pytest tests..."
	pytest . -v