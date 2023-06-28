#!/bin/bash

source /cave_cli/utils.sh
source ./utils/helpers/utils_backup.sh

# Change to the script directory
cd $(dirname "$0")

# Lint and Autoformat the API code in place
# Remove unused imports
autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports -r ../cave_api
# Perform all other steps
black --config pyproject.toml ../cave_api

if [ "$(has_flag -all "$@")" = "true" ]; then
    # Lint and Autoformat the code in place
    # Remove unused imports
    autoflake --in-place --remove-all-unused-imports --exclude=__init__.py -r ../cave_app
    autoflake --in-place --remove-all-unused-imports --exclude=__init__.py -r ../cave_core
    # Perform all other steps
    black --config pyproject.toml ../cave_app
    black --config pyproject.toml ../cave_core
fi

