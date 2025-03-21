#!/bin/bash

echo "Building iot-hub ..."

DEFAULT_DB_NAME="db"
DEFAULT_DB_USER="db_admin"
DEFAULT_DB_PASS="1234"

read -p "Enter name of database [$DEFAULT_DB_NAME]: " DB_NAME
DB_NAME=${DB_NAME:-$DEFAULT_DB_NAME}

read -p "Enter user for database [$DEFAULT_DB_USER]: " DB_USER
DB_USER=${DB_USER:-$DEFAULT_DB_USER}

read -s -p "Enter password for user [$DEFAULT_DB_PASS]: " DB_PASS
echo
DB_PASS=${DB_PASS:-$DEFAULT_DB_PASS}

PACKAGES="python3 python3-pip python3-venv mosquitto mosquitto-clients postgresql"

apt-get install $PACKAGES -y &&
cp ./mosquitto.conf /etc/mosquitto/mosquitto.conf &&
systemctl start mosquitto.service &&
systemctl start postgresql.service &&
{ sudo -u postgres psql <<EOF
    CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
    CREATE DATABASE $DB_NAME WITH OWNER '$DB_USER'; 
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME to $DB_USER;
EOF
} && echo "Done"
