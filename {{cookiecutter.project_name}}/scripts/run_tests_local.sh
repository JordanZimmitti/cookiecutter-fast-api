#!/bin/bash

# Ensures that errors boil-up properly
set -o pipefail
set -o errexit

# Gets the {{cookiecutter.friendly_name}} server base directory
FILE_DIR=$(dirname "$0")
cd "$FILE_DIR" || exit
cd ..

# Function that runs when the script starts
main() {

  # Gets the tests and coverage spec
  local spec_test=${1:-"tests/api tests/unit"}
  local spec_coverage=${2:-"{{cookiecutter.package_name}}"}

  # Converts the given path variables to arrays
  read -r -a spec_test_array <<< "$spec_test"
  read -r -a spec_coverage_array <<< "$spec_coverage"

  # Runs the api and unit tests
  export ENV_FILE=tests/pytest.env
  pre-commit run --all-files
  python -m pytest "${spec_test_array[@]}" \
    --cov "${spec_coverage_array[@]}" \
    --cov-report "term-missing:skip-covered"

  # Removes the unnecessary .coverage file
  rm -rf .coverage
}
main "$1" "$2"
