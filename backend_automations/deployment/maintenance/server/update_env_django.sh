set -ex

source assets/common/.env.sh

cp -f ~/deploy_django/assets/server/.env ~/${app_folder_name}/${backend_folder_app_name}/${django_app_name}/.env

