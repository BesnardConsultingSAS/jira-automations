set -ex

source assets/common/.env.sh

ssh "${username}"@"${ip_address}" -i "${ssh_file}"
