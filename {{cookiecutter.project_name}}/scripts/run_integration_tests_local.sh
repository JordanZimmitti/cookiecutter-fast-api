#!/bin/bash

# Ensures that errors boil-up properly
set -o pipefail
set -o errexit

# Gets the {{cookiecutter.friendly_name}} server directory
FILE_DIR=$(dirname "$0")
cd "$FILE_DIR" || exit
cd ..

# Function that shows the available options
showHelp() {
  echo "------------------------------------------------------------------------------------------"
  echo "Run Integration Test Flags"
  echo "-a" "The api url the integration tests should hit"
  echo "-u" "The user-id for logging into the client"
  echo "-e" "Runs all integration tests including ones that hit external sources"
  echo "-s" "Runs only integration tests that are smoke tests"
  echo "-t" "The directory used to find and run the integration tests"
  echo "------------------------------------------------------------------------------------------"
}

# Function that runs when the script starts
main() {

  # Shows the help information
  if [ "$1" = "--help" ]; then
    showHelp
    exit 0
  fi

  # Sets the default integration test variables
  local apiUrl="None"
  local userId="None"
  local apiKey="None"
  local spec_test="tests/integration"

  # Sets the default integration test mark variables
  local isRunExternalTests="false"
  local isRunSmokeTests="false"

  # Converts the given path variables to arrays
  read -r -a spec_test_array <<< "$spec_test"

  # Gets the command arguments
  while getopts a:u:p:est: flag
  do
      case "${flag}" in
          a) apiUrl=${OPTARG};;
          u) userId=${OPTARG};;
          e) isRunExternalTests="true";;
          s) isRunSmokeTests="true";;
          t) spec_test=${OPTARG};;
          *) ;;
      esac
  done

  # Gets the api-key from the user when a user-id is given
  if [ "$userId" == "None" ]; then
    echo "A user id must be provided"
    showHelp
    exit 1
  fi

  # Gets the API key
  echo "Enter API key:"
  read -r -s apiKey

  # Only runs the smoke tests
  if [[ "$isRunSmokeTests" == "true" ]]
  then
    exec python -m "pytest" -m "smoke" "${spec_test_array[@]}" \
      --api_url "$apiUrl"
#      --user_id "$userId" \
#      --api_key "$apiKey"

  # Runs All integration tests including ones that hit external sources
  elif [[ "$isRunExternalTests" == "true" ]]
  then
    exec python -m "pytest" "${spec_test_array[@]}" \
      --api_url "$apiUrl"
#      --user_id "$userId" \
#      --api_key "$apiKey"

  # Runs only the first-party integration tests
  else
    exec python -m "pytest" -m "not external" "${spec_test_array[@]}" \
      --api_url "$apiUrl"
#      --user_id "$userId" \
#      --api_key "$apiKey"
  fi
}
main "$@"
