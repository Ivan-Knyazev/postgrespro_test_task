#!/bin/bash

sudo systemctl stop postgresql
sudo dnf remove postgresql*
sudo systemctl daemon-reload
sudo rm -rf /var/lib/pgsql
sudo rm -rf /etc/postgresql
sudo rm -rf /var/log/postgresql
sudo dnf clean all

sudo find / -name "*postgresql*"
sudo systemctl status postgresql.service

sudo rm -rf /etc/firewalld/zones
sudo firewall-cmd --complete-reload
sudo firewall-cmd --list-all
