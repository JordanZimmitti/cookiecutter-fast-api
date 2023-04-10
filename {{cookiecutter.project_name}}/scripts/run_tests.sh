#!/bin/bash

# Ensures that errors boil-up properly
set -o pipefail
set -o errexit

# Creates the overridable environment variables
: "${SPEC_COVERAGE:="{{cookiecutter.package_name}}"}"
: "${SPEC_TEST:="tests/api tests/unit"}"
: "${TARGET_DIR:="target"}"

# Gets the {{cookiecutter.friendly_name}} server directory
FILE_DIR=$(dirname "$0")
cd "$FILE_DIR" || exit
cd ..

# Function that runs when the script starts
main() {

  # Converts the given path variables to arrays
  read -r -a spec_test_array <<< "$SPEC_TEST"
  read -r -a spec_coverage_array <<< "$SPEC_COVERAGE"

  # Runs the api and unit tests
  export ENV_FILE=tests/pytest.env
  python -m pytest "${spec_test_array[@]}" \
    --junitxml "$TARGET_DIR/junit.xml" \
    --cov "${spec_coverage_array[@]}" \
    --cov-report "xml:$TARGET_DIR/coverage.xml"
}
main
