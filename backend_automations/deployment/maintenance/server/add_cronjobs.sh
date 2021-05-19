set -ex

source assets/common/.env.sh

cd ~/${app_folder_name}/${backend_folder_app_name}

export python_path=$(~/.poetry/bin/poetry run which python)
export EDITOR="tee"
echo "$(echo -e "*/20 * * * * ${python_path} ~/${app_folder_name}/${backend_folder_app_name}/manage.py update_jira_issues" ; crontab -l)" | crontab -

crontab -l