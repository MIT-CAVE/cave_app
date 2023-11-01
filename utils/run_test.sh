#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_DIR=$(dirname "$SCRIPT_DIR")

source ./utils/helpers/shell_functions.sh
  
if [[ ! -f "./cave_api/tests/$3" && "${ALL_FLAG}" != "true" ]]; then
    printf "Test $3 not found. Ensure you entered a valid test name.\n" | pipe_log "ERROR"
    printf "Tests available in 'cave_api/tests/' include \n $(ls cave_api/tests/)\n" | pipe_log "ERROR"
    exit 1
fi

printf "\n" | pipe_log "INFO"
# Run given test in docker
if [ "${ALL_FLAG}" != "true" ]; then
    python "./cave_api/tests/$3" 2>&1 | pipe_log "INFO"
else
    for f in ./cave_api/tests/*.py; do
        python "./$f" 2>&1 | pipe_log "INFO"
    done
fi