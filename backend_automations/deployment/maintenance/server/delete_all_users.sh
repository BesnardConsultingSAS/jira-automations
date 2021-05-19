set -ex

source assets/common/.env.sh

cd ~/${app_folder_name}/${backend_folder_app_name}

~/.poetry/bin/poetry run python manage.py shell -c "from django.contrib.auth.models import User;
print(list(User.objects.all()));
User.objects.all().delete();
print(list(User.objects.all()));"
