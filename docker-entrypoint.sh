#!/bin/sh
set -eu

export PYTHONUNBUFFERED=1
pip install -e ./cave_api

exec "$@"
