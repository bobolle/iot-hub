#!/bin/bash

if [ "$#" -lt 3 ]; then
    echo "Invalid format: example $0 <db_name> <db_user> <db_pass>"
    exit 1
fi

echo "Building iot-hub ..."

if [ "$#" = 3 ]; then

    DB_NAME=$1
    DB_USER=$2
    DB_PASS=$3
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
fi
