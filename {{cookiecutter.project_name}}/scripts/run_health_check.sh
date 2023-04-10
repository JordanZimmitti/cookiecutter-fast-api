#!/bin/bash

# Hits the health-check endpoint to check whether the {{cookiecutter.friendly_name}} server is running
curl -f http://{{cookiecutter.package_name}}:2000/api/v1/health/check
