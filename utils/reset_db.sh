#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_DIR=$(dirname "$SCRIPT_DIR")

source /cave_cli/utils.sh
source ./utils/helpers/cli_backup.sh
source ./utils/helpers/ensure_postgres_running.sh

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
