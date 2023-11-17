#!/bin/bash
while true; do
    if nc -z "${DB_HOST}" "${DB_PORT}"; then
        echo "MySQL ready"
        break
    else
        echo "MySQL not ready yet, waiting"
        sleep 2
    fi
done

echo "Making Migrations"
python3 manage.py makemigrations
echo "Running Migrations"
python3 manage.py migrate
echo "Starting Server"
exec python3 manage.py runserver "${SERVER_HOST}:${SERVER_PORT}"
