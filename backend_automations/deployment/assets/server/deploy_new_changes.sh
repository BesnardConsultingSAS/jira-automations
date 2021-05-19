set -ex

source .env.sh

cd ${full_path_to_backend_folder}

sudo -u "${username}" git fetch origin master

export regexp="Your branch is behind 'origin/master' by .* can be fast-forwarded"

if [[ ! "$(git status)" =~ $regexp ]]; then
    echo "No changes to apply"
    exit 0
fi

echo "New Deploy of the app"

sudo -u "${username}" git pull

/home/${username}/.poetry/bin/poetry install --no-dev
/home/${username}/.poetry/bin/poetry run python manage.py migrate
/home/${username}/.poetry/bin/poetry run python manage.py collectstatic --noinput


sudo nginx -t
sudo systemctl restart nginx

sudo systemctl restart gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket gunicorn.service
