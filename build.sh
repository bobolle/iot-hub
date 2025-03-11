#!/bin/bash

DB_USER="db_admin"
DB_PASS="1234"
DB_NAME="db"

PACKAGES="python3 python3-pip python3-venv mosquitto mosquitto-clients postgresql" &&
apt-get install $PACKAGES -y &&
mv ./mosquitto.conf /etc/mosquitto/mosquitto.conf &&
systemctl start mosquitto.service &&
sudo -u postgres psql <<EOF
CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
CREATE DATABASE $DB_NAME WITH OWNER '$DB_USER';
EOF
echo "User '$DB_USER' and database '$DB_NAME' created successfully."
