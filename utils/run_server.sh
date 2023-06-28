#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_DIR=$(dirname "$SCRIPT_DIR")

source /cave_cli/utils.sh
source ./utils/helpers/utils_backup.sh
source ./utils/helpers/ensure_postgres_running.sh
source ./utils/helpers/ensure_db_setup.sh

python "$APP_DIR/manage.py" runserver 0.0.0.0:8000 2>&1 | pipe_log "INFO"
