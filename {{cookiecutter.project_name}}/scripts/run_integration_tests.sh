#!/bin/sh

# Gets the {{cookiecutter.friendly_name}} server directory
FILE_DIR=$(dirname "$0")
cd "$FILE_DIR" || exit
cd ..

# Function that gets the password from the user (hides the input)
getPassword() {
  echo "Enter password:"
  read -r -s PASSWORD
}

# Function that shows the available options
showHelp() {
  echo "------------------------------------------------------------------------------------------"
  echo "Run Integration Test Flags"
  echo "-a" "The api url the integration tests should hit"
  echo "-u" "The username for logging into the client"
  echo "-t" "The directory used to find and run the integration tests"
  echo "------------------------------------------------------------------------------------------"
}

# Sets the default variables
API="None"
PASSWORD="None"
USERNAME="None"
TESTDIR=tests/integration

# Shows the help information
if [ "$1" = "--help" ]; then
  showHelp
  exit 1
fi

# Gets the command arguments
while getopts a:u:p:t: flag
do
    case "${flag}" in
        a) API=${OPTARG};;
        u) USERNAME=${OPTARG};;
        t) TESTDIR=${OPTARG};;
        *) ;;
    esac
done

# Shows the help information
if [ "$USERNAME" != "None" ]; then
  getPassword
fi

# Runs the integration tests
python -m pytest \
  "$TESTDIR" \
  --username "$USERNAME" \
  --password "$PASSWORD" \
  --api_url "$API"
