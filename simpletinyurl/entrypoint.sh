#!/bin/bash

# Wait for Postgres
if [ $DJANGO_DB_TYPE = "postgres" ]
then
    apk update
    apk add postgresql-client --no-cache 
    until [ "$(PGPASSWORD=$DJANGO_DB_PASSWORD psql -U $DJANGO_DB_USER -h $DJANGO_DB_HOST -tAc 'select 1' -d $DJANGO_DB_NAME || echo 0 )" = '1' ]; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
    done
fi

# Apply database migrations
echo "Apply database migrations"
python app/manage.py migrate

# Start server
echo "Starting server"
python app/manage.py runserver 0.0.0.0:8000