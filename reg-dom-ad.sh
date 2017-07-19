#!/bin/bash
# Registra máquina Ubuntu no domínio do Active Directory
# Esse script tem a finalidade de inserir uma estação Ubuntu no domínio do AD

DOMAIN="seu.dominio.local"
ADMIN="sua.conta"

echo "Por favor autentique com a senha sudo"
sudo -v

if ! $(sudo which realmd 2>/dev/null); then
    sudo apt install realmd adcli sssd
fi

if ! $(sudo which ntpd 2>/dev/null); then
    sudo apt install ntp
fi

sudo mkdir -p /var/lib/samba/private
sudo realm join --user=$ADMIN $DOMAIN

if [ $? -ne 0 ]; then
    echo "AD join failed.  Please run 'journalctl -xn' to determine why."
    exit 1
fi

sudo systemctl enable sssd
sudo systemctl start sssd

echo "session required pam_mkhomedir.so skel=/etc/skel/ umask=0022" | sudo tee -a /etc/pam.d/common-session

# configure sudo
sudo apt install libsss-sudo

echo "%domain\ admins@$DOMAIN ALL=(ALL) ALL" | sudo tee -a /etc/sudoers.d/domain_admins

cat << EOF | sudo tee /etc/lightdm/lightdm.conf
[SeatDefaults]
greeter-show-manual-login=true
greeter-hide-users=true
user-session=ubuntu
EOF
