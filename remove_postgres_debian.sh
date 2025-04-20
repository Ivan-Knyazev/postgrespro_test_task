#!/bin/bash

sudo systemctl stop postgresql
sudo apt-get --purge remove postgresql\*
sudo rm -rf /var/lib/postgresql/
sudo rm -rf /etc/postgresql/
sudo deluser postgres
sudo delgroup postgres
sudo apt-get autoremove

sudo systemctl status postgresql
sudo -i -u postgres psql