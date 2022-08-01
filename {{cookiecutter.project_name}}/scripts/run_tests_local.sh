#!/bin/sh

# Gets the {{cookiecutter.friendly_name}} server base directory
FILE_DIR=$(dirname "$0")
cd "$FILE_DIR" || exit
cd ..

# Sets the coverage scope
if [ "$#" -eq 0 ]; then
  COVERAGE="{{cookiecutter.package_name}}"
elif [ "$#" -eq 1 ]; then
  COVERAGE="$1"
fi

# Runs the e2e and unit tests
export ENV_FILE=tests/pytest.env
pre-commit run --all-files
python -m pytest tests/api tests/unit \
  --cov "$COVERAGE" \
  --cov-report "term-missing:skip-covered"

# Removes the .coverage file
rm -rf .coverage