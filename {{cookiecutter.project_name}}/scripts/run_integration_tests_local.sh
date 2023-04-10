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
  echo "-u" "The username for logging into the client"
  echo "-t" "The directory used to find and run the integration tests"
  echo "------------------------------------------------------------------------------------------"
}

# Function that runs when the script starts
main() {

  # Shows the help information
  if [ "$1" = "--help" ]; then
    showHelp
    exit 1
  fi

  # Sets the default integration test variables
  local apiUrl="None"
  local username="None"
  local password="None"
  local spec_test="tests/integration"

  # Converts the given path variables to arrays
  read -r -a spec_test_array <<< "$spec_test"

  # Gets the command arguments
  while getopts a:u:p:t: flag
  do
      case "${flag}" in
          a) apiUrl=${OPTARG};;
          u) username=${OPTARG};;
          t) spec_test=${OPTARG};;
          *) ;;
      esac
  done

  # Gets the password from the user when a username is given
  if [ "$username" != "None" ]; then
    echo "Enter password:"
    read -r -s password
  fi

  # Runs the integration tests
  python -m pytest "${spec_test_array[@]}" \
    --api_url "$apiUrl" \
    --username "$username" \
    --password "$password"
}
main "$@"
