set -ex

source assets/common/.env.sh

rm -rf /home/${username}/continuous_delivery/

mkdir /home/${username}/continuous_delivery/

cp /home/${username}/deploy_django/assets/server/deploy_new_changes.sh /home/${username}/continuous_delivery/deploy_new_changes.sh

printf "export full_path_to_backend_folder=/home/${username}/${app_folder_name}/${backend_folder_app_name}
export username=${username}" > ~/continuous_delivery/.env.sh

echo -e "$(sudo crontab -l)" | grep -v "deploy_new_changes.sh" | sudo crontab -

# This cronjob will be run by the root user since the restart of the app requires the root permissions
echo "$(echo -e "*/2 * * * * bash -c 'cd /home/${username}/continuous_delivery && /bin/bash deploy_new_changes.sh'" ; sudo crontab -l)" | sudo crontab -

sudo crontab -l

