set -ex

source assets/common/.env.sh

# Copy the `deployment/` folder to `/home/${username}/deploy_django/` on the server
ssh -t  "${username}"@"${ip_address}" -i "${ssh_file}" "rm -rf ~/deploy_django/"
scp -i "${ssh_file}" -r $(pwd) "${username}"@"${ip_address}":~/deploy_django/

# Put here the scripts you want to run
ssh -t "${username}"@"${ip_address}" -i "${ssh_file}" "cd ~/deploy_django/ && bash maintenance/server/update_env_django.sh"

#ssh -t "${username}"@"${ip_address}" -i "${ssh_file}" "cd ~/deploy_django/ && bash maintenance/server/restart_everything.sh"

ssh -t  "${username}"@"${ip_address}" -i "${ssh_file}" "rm -rf ~/deploy_django/"
