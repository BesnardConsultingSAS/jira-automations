set -ex

cd ..
poetry run python manage.py shell -c "from django.core.management import utils; print(utils.get_random_secret_key())"
