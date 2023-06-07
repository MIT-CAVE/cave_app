#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_DIR=$(dirname "$SCRIPT_DIR")

python3 "$APP_DIR/manage.py" makemigrations cave_core --deployment_type development
python3 "$APP_DIR/manage.py" migrate --deployment_type development
python3 "$APP_DIR/manage.py" createcachetable
python3 "$APP_DIR/data_gen.py" --deployment_type development
python3 "$APP_DIR/manage.py" runserver
