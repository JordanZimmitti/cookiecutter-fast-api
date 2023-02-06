#!/bin/sh

# Gets the Example API server base directory
FILE_DIR=$(dirname "$0")
cd "$FILE_DIR" || exit
cd ..

# Sets the coverage scope
if [ "$#" -eq 0 ]; then
  COVERAGE="{{cookiecutter.package_name}}"
elif [ "$#" -eq 1 ]; then
  COVERAGE="$1"
fi

# Runs the api and unit tests
export ENV_FILE=tests/pytest.env
python -m pytest tests/api tests/unit \
  --junitxml="target/junit.xml" \
  --cov "$COVERAGE" \
  --cov-report "xml:target/coverage.xml"
