#!/bin/bash
echo $ID_RSA | sed 's/;/\n/g'>/id_rsa
chmod 400 /id_rsa
echo "    IdentityFile /id_rsa" >> /etc/ssh/ssh_config
#ansible-inventory -i hetzner-inventory.py --list
ansible-playbook -i hetzner-inventory.py install.yml
