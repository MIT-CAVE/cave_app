#!/bin/bash

echo "Starting DEV server..."

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_DIR=$(dirname "$SCRIPT_DIR")

# Poll for postgres to be up
while ! (source /app/.env && python3 -c "import psycopg2; psycopg2.connect(\"dbname='$DATABASE_NAME' user='$DATABASE_USER' host='$DATABASE_HOST' password='$DATABASE_PASSWORD'\")" 2>/dev/null) do
  printf "Waiting for postgres...\n"
  sleep 1
done

python "$APP_DIR/manage.py" makemigrations cave_core --deployment_type development
python "$APP_DIR/manage.py" migrate --deployment_type development
python "$APP_DIR/manage.py" createcachetable
python "$APP_DIR/data_gen.py" --deployment_type development
python "$APP_DIR/manage.py" runserver 0.0.0.0:8000
