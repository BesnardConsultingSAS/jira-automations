set -ex

source assets/common/.env.sh

sudo nginx -t
sudo systemctl restart nginx

sudo systemctl restart gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket gunicorn.service

# sudo tail -F /var/log/nginx/error.log
