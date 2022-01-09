install-dependencies:
	apt-get update && apt-get install -y libpq-dev postgresql-client
	pip install -r requirements/base.txt

install-dev-dependencies:
	pip install -r requirements/dev.txt

lint:
	flake8 src tests && black . --extend-exclude='/(generated|migrations)/' --check || exit;

lint-python: lint

format:
	black . --extend-exclude='/(generated|migrations)/' || exit;

test:
	pytest tests || exit;
