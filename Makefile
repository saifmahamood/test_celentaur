.PHONY: install format lint test run clean

install:
	poetry install

format:
	poetry run black .
	poetry run isort .

lint:
	poetry run flake8 .

test:
	poetry run pytest --cov=spark_jobs --cov-fail-under=80

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	echo "Cleaned up build artifacts."
