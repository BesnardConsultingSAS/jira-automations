set -ex

source assets/common/.env.sh

# https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04#installing-the-packages-from-the-ubuntu-repositories

sudo apt update -y
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl -y

# Configure PostgreSQL
sudo -u postgres psql -c "CREATE DATABASE ${postgres_db_name};"
sudo -u postgres psql -c "CREATE USER ${postgres_username} WITH PASSWORD '${postgres_password}';"
sudo -u postgres psql -c "ALTER ROLE ${postgres_username} SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE ${postgres_username} SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE ${postgres_username} SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${postgres_db_name} TO ${postgres_username};"


# Configure Poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
printf '\nexport PATH="~/.poetry/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
printf "$PATH"

# Configure SSH
ssh-keygen -q -t ed25519 -C "${email_address}" -N '' -f ~/.ssh/id_ed25519 <<<y 2>&1 >/dev/null
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
printf "\n\n" && cat ~/.ssh/id_ed25519.pub && printf "\n\n"
printf "\n\nPlease add the ssh key (already copied into your clipboard) to your repository. Example for GitHub: https://docs.github.com/en/developers/overview/managing-deploy-keys#setup-2.\n"
read -n 1 -r -s -p $'Press any key to continue once the SSH key is added to your remote repository...\n'
cat assets/server/ssh_config >> ~/.ssh/config

# Clone the repo
git clone ${github_repo_ssh} ~/${app_folder_name}


## Install the Django app
cd ~/${app_folder_name}/${backend_folder_app_name}
~/.poetry/bin/poetry install --no-dev

cp -f ~/deploy_django/assets/server/.env ~/${app_folder_name}/${backend_folder_app_name}/${django_app_name}/.env
~/.poetry/bin/poetry run python manage.py migrate
~/.poetry/bin/poetry run python manage.py collectstatic --noinput


sudo ufw allow 8000
~/.poetry/bin/poetry run python manage.py runserver 0.0.0.0:8000

~/.poetry/bin/poetry run gunicorn --bind 0.0.0.0:8000 ${django_app_name}.wsgi


export gunicorn_path=$(~/.poetry/bin/poetry run which gunicorn)
sudo cp ~/deploy_django/assets/server/gunicorn.socket.base /etc/systemd/system/gunicorn.socket
sudo cp ~/deploy_django/assets/server/gunicorn.service.base /etc/systemd/system/gunicorn.service
echo -e "User=${username}" | sudo tee -a /etc/systemd/system/gunicorn.service
echo -e "Group=www-data" | sudo tee -a /etc/systemd/system/gunicorn.service
echo -e "WorkingDirectory=/home/${username}/${app_folder_name}/${backend_folder_app_name}" | sudo tee -a /etc/systemd/system/gunicorn.service
echo -e "ExecStart=${gunicorn_path} --access-logfile - \
--workers ${number_of_workers}  --bind unix:/run/gunicorn.sock ${django_app_name}.wsgi:application" | sudo tee -a /etc/systemd/system/gunicorn.service


echo -e "\n[Install]\nWantedBy=multi-user.target" | sudo tee -a /etc/systemd/system/gunicorn.service
sudo cat /etc/systemd/system/gunicorn.service

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

sudo systemctl status gunicorn.socket

file /run/gunicorn.sock


curl --unix-socket /run/gunicorn.sock localhost



# https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04#configure-nginx-to-proxy-pass-to-gunicorn
echo -e "server {

    access_log  /var/log/nginx/access.https.log;

    listen 80;
    server_name ${ip_address} ${domain_name_1} ${domain_name_2};

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        access_log  /var/log/nginx/access.static.log;
        alias /home/${username}/${app_folder_name}/${backend_folder_app_name}/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}" | sudo tee /etc/nginx/sites-available/"${django_app_name}"
sudo cat /etc/nginx/sites-available/"${django_app_name}"

sudo rm -f /etc/nginx/sites-enabled/"${django_app_name}"
sudo ln -s /etc/nginx/sites-available/"${django_app_name}" /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl restart nginx

sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'

printf "Check how make your domain name point to your server: https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars"
printf "Going to this page may help you: https://cloud.digitalocean.com/networking/domains"

read -n 1 -r -s -p "Press any key to continue once your domain names are configured (${domain_name_1} and ${domain_name_2})...\n"
