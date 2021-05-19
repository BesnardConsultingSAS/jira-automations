set -ex

source assets/common/.env.sh

ssh -i "${ssh_file}" -t "${username}"@"${ip_address}" "sudo echo 'Hi!'"
