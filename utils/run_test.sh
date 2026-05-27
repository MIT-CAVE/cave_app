#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_DIR=$(dirname "$SCRIPT_DIR")

source ./utils/helpers/shell_functions.sh

export PYTHONPATH=$PYTHONPATH:.

if [[ ! -f "./cave_api/tests/$1" ]]; then
    printf "Test %s not found. Ensure you entered a valid test name.\n" "$1" | pipe_log "ERROR"
    printf "Tests available in 'cave_api/tests/' include:\n" | pipe_log "ERROR"
    for f in ./cave_api/tests/*.py; do
        printf "  %s\n" "$(basename "$f")" | pipe_log "ERROR"
    done
    exit 1
fi


python "./cave_api/tests/$1" 2>&1 | pipe_log "INFO"
