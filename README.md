Odoo bin upgrade
 - sudo systemctl stop odoo16
 - sudo su - odoo16
 - source odoo16-venv/bin/activate
 - odoo16/odoo-bin -c /etc/odoo16.conf -u all
 - press ctl + c to stop (Run odoo-bin = upgrade odoo and start odoo16 service)
 - exit
 - sudo systemctl start odoo16