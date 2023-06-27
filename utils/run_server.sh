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

# Offer to reset the db if it has not yet been setup
if [ "$(python ./manage.py showmigrations --deployment_type development | grep "\[X\]" | wc -l)" -eq "0" ]; then
  printf "Your database has not been setup or is not properly configured." 2>&1 | pipe_log "WARN"
  # Ask the user if they want to reset the db
  printf "Would you like to reset the database using './utils/reset_db.sh'? (y/n): " 2>&1 | pipe_log "WARN"
  read -r reset_db
  if [ "$reset_db" = "y" ]; then
    printf "Resetting the database...\n" 2>&1 | pipe_log "WARN"
    source ./utils/reset_db.sh
    # Check if the db was reset successfully
    if [ "$(python ./manage.py showmigrations --deployment_type development | grep "\[X\]" | wc -l)" -eq "0" ]; then
      printf "Unable to reset the database.\n" 2>&1 | pipe_log "ERROR"
      exit 1
    fi
  else
    printf "Unable to start the app. Ensure your database is properly configured.\n" 2>&1 | pipe_log "ERROR"
    exit 1
  fi
fi

python "$APP_DIR/manage.py" runserver 0.0.0.0:8000 2>&1 | pipe_log "INFO"
