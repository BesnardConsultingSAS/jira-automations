set -ex
source assets/common/.env.sh

# https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04


printf "Welcome ${username}!"
adduser "${username}"
usermod -aG sudo "${username}"
ufw app list
ufw allow OpenSSH
ufw enable
ufw status
rsync --archive --chown="${username}":"${username}" ~/.ssh /home/"${username}"
