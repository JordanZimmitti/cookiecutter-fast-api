#!/bin/sh

# Gets the {{cookiecutter.friendly_name}} server base directory
FILE_DIR=$(dirname "$0")
cd "$FILE_DIR" || exit
cd ..

# Function that runs when the script starts
main() {

  # Create virtual environment
  poetry env use python3.10

  # Activates the virtual environment
  local poetryVenvPath
  poetryVenvPath="$(poetry env info --path)"
  . "$poetryVenvPath"/bin/activate

  # Installs the project's dependencies
  poetry install --no-root

  # Install pre-commit hooks and run pre-commits to check whether it is installed correctly
  pre-commit install
  pre-commit run --all-files
}

main