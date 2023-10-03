#!/bin/sh
set -eu

pip install -e ./cave_api

exec "$@"
