#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_DIR=$(dirname "$SCRIPT_DIR")

source ./utils/helpers/shell_functions.sh
source ./utils/helpers/ensure_postgres_running.sh
# Check if the app is functional before proceeding
if [ "$(python ./manage.py check --deployment_type development | grep "System check identified no issues" | wc -l)" -eq "0" ]; then
  printf "Unable to start the app due to an error in the code. See the stacktrace above." 2>&1 | pipe_log "ERROR"
  rm -r "./tmp"
  exit 1
fi
source ./utils/helpers/ensure_db_setup.sh

python "$APP_DIR/manage.py" runserver 0.0.0.0:8000 2>&1 | pipe_log "INFO"
