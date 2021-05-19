set -ex

poetry run black . --check
poetry run mypy .
poetry run flake8 .
poetry run python manage.py makemigrations --dry-run --check
poetry run pytest .