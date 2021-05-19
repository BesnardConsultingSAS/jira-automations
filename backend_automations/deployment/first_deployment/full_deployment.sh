set -ex

bash first_deployment/init_env_variables.sh

source assets/common/.env.sh

# Remove the folder `/root/deploy_django/` from the server if it already exists
ssh -t -i "${ssh_file}" root@"${ip_address}" "rm -rf ~/deploy_django/"

# Copy the `deployment/` folder to `/root/deploy_django/` on the server
scp -i "${ssh_file}" -r $(pwd) root@"${ip_address}":~/deploy_django/

# https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04
ssh root@"${ip_address}" -i "${ssh_file}" "cd ~/deploy_django/ && bash first_deployment/server/create_regular_user.sh"

ssh -t -i "${ssh_file}" root@"${ip_address}" "rm -rf ~/deploy_django/"

bash first_deployment/check_connection_with_regular_user.sh

# Copy the `deployment/` folder to `/home/${username}/deploy_django/` on the server
ssh -t  "${username}"@"${ip_address}" -i "${ssh_file}" "rm -rf ~/deploy_django/"
scp -i "${ssh_file}" -r $(pwd) "${username}"@"${ip_address}":~/deploy_django/
ssh -t "${username}"@"${ip_address}" -i "${ssh_file}" "cd ~/deploy_django/ && bash first_deployment/server/install_django_app.sh"
ssh -t "${username}"@"${ip_address}" -i "${ssh_file}" "cd ~/deploy_django/ && bash first_deployment/server/install_lets_encrypt.sh"
ssh -t "${username}"@"${ip_address}" -i "${ssh_file}" "cd ~/deploy_django/ && bash first_deployment/server/setup_cronjobs.sh"
ssh -t "${username}"@"${ip_address}" -i "${ssh_file}" "cd ~/deploy_django/ && bash first_deployment/server/setup_git_changes_pulling.sh"
ssh -t "${username}"@"${ip_address}" -i "${ssh_file}" "cd ~/deploy_django/ && bash first_deployment/server/create_app_user.sh"
#
ssh -t  "${username}"@"${ip_address}" -i "${ssh_file}" "rm -rf ~/deploy_django/"
