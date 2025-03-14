#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_DIR=$(dirname "$SCRIPT_DIR")

source ./utils/helpers/shell_functions.sh
source ./utils/helpers/ensure_postgres_running.sh

# Log the current DB migrations
mkdir "./tmp"
printf "$(ls ./cave_core/migrations/*.py)" > "./tmp/init.txt"

# Check if the app is functional before proceeding
if [ "$(python ./manage.py check --deployment_type development | grep "System check identified no issues" | wc -l)" -eq "0" ]; then
  printf "Unable to reset the db due to an error in the code. See the stacktrace above." 2>&1 | pipe_log "ERROR"
  rm -r "./tmp"
  exit 1
fi

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

# Nuke the Cache
python "$APP_DIR/manage.py" clearcache --deployment_type development 2>&1 | pipe_log "DEBUG"

# Clear the current DB
python "$APP_DIR/manage.py" flush --noinput --deployment_type development 2>&1 | pipe_log "DEBUG"
# Generate data
python "$APP_DIR/data_gen.py" --deployment_type development 2>&1 | pipe_log "DEBUG"
