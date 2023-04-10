#!/bin/bash

# Ensures that errors boil-up properly
set -o pipefail
set -o errexit

# Creates the overridable environment variables
: "${IS_RUN_ALL_INTEGRATION_TESTS:="true"}"
: "${API_URL:="http://{{cookiecutter.package_name}}:2000/api"}"
: "${USERNAME:=""}"
: "${PASSWORD:=""}"
: "${TARGET_DIR:="target"}"

# Gets the {{cookiecutter.friendly_name}} server directory
FILE_DIR=$(dirname "$0")
cd "$FILE_DIR" || exit
cd ..

# Function that runs all the integration tests or smoke tests
runTests() {
  if [[ "$IS_RUN_ALL_INTEGRATION_TESTS" == "true" ]]
  then
    python -m pytest "tests/integration" \
      --junitxml "$TARGET_DIR/integration_junit.xml" \
      --api_url "$API_URL" \
      --username "$USERNAME" \
      --password "$PASSWORD"
  else
    python -m pytest -m smoke "tests/integration" \
      --junitxml "$TARGET_DIR/smoke_junit.xml" \
      --api_url "$API_URL" \
      --username "$ITEST_LOGIN_USR" \
      --password "$ITEST_LOGIN_PSW"
  fi
}

# Function that runs when the script starts
main() {
  runTests
}
main
