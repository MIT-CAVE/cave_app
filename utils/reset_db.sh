#!/bin/bash

source /cave_cli/utils.sh

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_DIR=$(dirname "$SCRIPT_DIR")

# Poll for postgres to be up
for i in {1..6}; do
  if [ ! $i -eq 6 ]; then
    if (source /app/.env && python3 -c "import psycopg2; psycopg2.connect(\"dbname='$DATABASE_NAME' user='$DATABASE_USER' host='$DATABASE_HOST' password='$DATABASE_PASSWORD'\")" 2>/dev/null); then
      break
    fi
  else
    printf "Postgres never came up...\nMaking one last attempt and logging any errors that occur:\n" 2>&1 | pipe_log "WARN"
    if (source /app/.env && python3 -c "import psycopg2; psycopg2.connect(\"dbname='$DATABASE_NAME' user='$DATABASE_USER' host='$DATABASE_HOST' password='$DATABASE_PASSWORD'\")"); then
      break
    else
      printf "Postgres never came up, exiting...\n" 2>&1 | pipe_log "ERROR"
      exit 1
    fi
  fi
  printf "Waiting for postgres ($i)...\n" 2>&1 | pipe_log "DEBUG"
  sleep 3
done

# Log the current DB migrations
mkdir "./tmp"
printf "$(ls ./cave_core/migrations/*.py)" > "./tmp/init.txt"

# Make and apply any new migrations
python "$APP_DIR/manage.py" makemigrations cave_core --deployment_type development 2>&1 | pipe_log "DEBUG"
python "$APP_DIR/manage.py" migrate --deployment_type development 2>&1 | pipe_log "DEBUG"
python "$APP_DIR/manage.py" createcachetable 2>&1 | pipe_log "DEBUG"

# Determine new DB migration files and delete them
printf "$(ls ./cave_core/migrations/*.py)" > "./tmp/after.txt"
grep -Fxvf ./tmp/init.txt ./tmp/after.txt > ./tmp/new.txt
cat ./tmp/new.txt | while read migration_name; do
  rm $migration_name
done
rm -r "./tmp"

# Generate data
python "$APP_DIR/data_gen.py" --deployment_type development 2>&1 | pipe_log "DEBUG"
