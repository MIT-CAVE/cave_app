#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_DIR=$(dirname "$SCRIPT_DIR")

source ./utils/helpers/shell_functions.sh
source ./utils/helpers/ensure_postgres_running.sh

# Make and apply any new migrations
python "$APP_DIR/manage.py" makemigrations cave_core --deployment_type development 2>&1 | pipe_log "DEBUG"