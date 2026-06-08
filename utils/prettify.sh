#!/bin/bash

source ./utils/helpers/shell_functions.sh

# Bring in the extra dev deps
uv sync --extra dev 2>&1 | pipe_log "DEBUG"

# Change to the script directory
cd $(dirname "$0")

# Lint and Autoformat the API code in place
# Remove unused imports
uv run autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports --exclude=api.py -r ../cave_api
# Perform all other steps
uv run black --config ../pyproject.toml ../cave_api

# Lint and Autoformat the code in place
# Remove unused imports
uv run autoflake --in-place --remove-all-unused-imports --exclude=__init__.py -r ../cave_app
uv run autoflake --in-place --remove-all-unused-imports --exclude=__init__.py -r ../cave_core
# Perform all other steps
uv run black --config ../pyproject.toml ../cave_app
uv run black --config ../pyproject.toml ../cave_core

