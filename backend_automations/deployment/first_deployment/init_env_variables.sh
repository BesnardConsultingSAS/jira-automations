set -ex

read -p "Enter the regular username you want to use for the server: " username
printf "\nexport username='${username}'" >> assets/common/.env.sh

read -p "Enter the username you want to use for the Django app user: " app_user_name
printf "\nexport app_user_name='${app_user_name}'" >> assets/common/.env.sh

read -p "IP address of your server: " ip_address
printf "\nexport ip_address='${ip_address}'" >> assets/common/.env.sh

read -p "SSH file to use: " ssh_file
printf "\nexport ssh_file='${ssh_file}'" >> assets/common/.env.sh

read -p "PostgreSQL DB Name: " postgres_db_name
printf "\nexport postgres_db_name='${postgres_db_name}'" >> assets/common/.env.sh

read -p "PostgreSQL Username: " postgres_username
printf "\nexport postgres_username='${postgres_username}'" >> assets/common/.env.sh

read -p "PostgreSQL Password: " postgres_password
printf "\nexport postgres_password='${postgres_password}'" >> assets/common/.env.sh

read -p "Email address: " email_address
printf "\nexport email_address='${email_address}'" >> assets/common/.env.sh

read -p "GitHub repo SSH address: " github_repo_ssh
printf "\nexport github_repo_ssh='${github_repo_ssh}'" >> assets/common/.env.sh

read -p "Django App name: " django_app_name
printf "\nexport django_app_name='${django_app_name}'" >> assets/common/.env.sh

read -p "Backend Folder name (containing manage.py): " backend_folder_app_name
printf "\nexport backend_folder_app_name='${backend_folder_app_name}'" >> assets/common/.env.sh

read -p "App Folder name (containing the backend and frontend folders): " app_folder_name
printf "\nexport app_folder_name='${app_folder_name}'" >> assets/common/.env.sh

read -p "Number of workers: " number_of_workers
printf "\nexport number_of_workers='${number_of_workers}'" >> assets/common/.env.sh

read -p "Domain name 1 (let empty if none): " domain_name_1
printf "\nexport domain_name_1='${domain_name_1}'" >> assets/common/.env.sh

read -p "Domain name 2 (let empty if none): " domain_name_2
printf "\nexport domain_name_2='${domain_name_2}'" >> assets/common/.env.sh
