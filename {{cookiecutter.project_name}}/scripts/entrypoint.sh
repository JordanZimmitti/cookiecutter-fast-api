#!/bin/bash

# Gets the {{cookiecutter.friendly_name}} server directory
FILE_DIR=$(dirname "$0")
cd "$FILE_DIR" || exit
cd ..

# Sets the current path as the python path
export PYTHONPATH=.

# Runs the {{cookiecutter.friendly_name}} server
exec python -m {{cookiecutter.package_name}}.main
