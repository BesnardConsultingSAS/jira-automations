set -ex

source assets/common/.env.sh

# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04

sudo apt install certbot python3-certbot-nginx -y

sudo ufw status
sudo ufw allow 'Nginx Full'

sudo certbot --nginx -d "${domain_name_1}" -d "${domain_name_2}" --non-interactive --agree-tos -m "${email_address}"

sudo ufw delete allow 'Nginx HTTP'
sudo ufw status

sudo systemctl status certbot.timer

sudo certbot renew --dry-run

sudo sed -i /"listen 80;"/d  /etc/nginx/sites-available/"${django_app_name}"

echo -e "\n\nserver {
        listen 80 default_server;
        server_name _;
        return 301 https://\$host\$request_uri;
}" | sudo tee -a /etc/nginx/sites-available/"${django_app_name}"

sudo nginx -t
sudo systemctl restart nginx


