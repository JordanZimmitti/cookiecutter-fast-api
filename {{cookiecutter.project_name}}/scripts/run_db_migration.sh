#!/bin/bash

# Gets the {{cookiecutter.friendly_name}} server directory
FILE_DIR=$(dirname "$0")
cd "$FILE_DIR" || exit
cd ..

# Sets the current path as the python path
export PYTHONPATH=.

# Runs the database migration python script
exec python scripts/python/db_migration.py
