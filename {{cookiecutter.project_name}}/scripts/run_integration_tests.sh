#!/bin/bash

# Ensures that errors boil-up properly
set -o pipefail
set -o errexit

# Creates the overridable environment variables
: "${IS_RUN_SMOKE:="false"}"
: "${IS_RUN_WITH_WITH_EXTERNAL:="false"}"
: "${API_URL:="http://{{cookiecutter.package_name}}:2000/api"}"
: "${USER_ID:=""}"
: "${API_KEY:=""}"
: "${TARGET_DIR:="/home/nonroot/target"}"

# Gets the {{cookiecutter.friendly_name}} server directory
FILE_DIR=$(dirname "$0")
cd "$FILE_DIR" || exit
cd ..

# Function that runs when the script starts
main() {

  # Only runs the smoke tests
  if [[ "$IS_RUN_SMOKE" == "true" ]]
  then
    exec python -m "pytest" -m "smoke" "tests/integration" \
      --junitxml "$TARGET_DIR/integration_junit.xml" \
      --api_url "$API_URL"
#      --user_id "$USER_ID" \
#      --api_key "$API_KEY"

  # Runs All integration tests including ones that hit external sources
  elif [[ "$IS_RUN_WITH_WITH_EXTERNAL" == "true" ]]
  then
    exec python -m "pytest" "tests/integration" \
      --junitxml "$TARGET_DIR/smoke_junit.xml" \
      --api_url "$API_URL"
#      --user_id "$USER_ID" \
#      --api_key "$API_KEY"

  # Runs only the first-party integration tests
  else
    exec python -m "pytest" -m "not external" "tests/integration" \
        --junitxml "$TARGET_DIR/smoke_junit.xml" \
        --api_url "$API_URL"
#        --user_id "$USER_ID" \
#        --api_key "$API_KEY"
  fi
}
main
