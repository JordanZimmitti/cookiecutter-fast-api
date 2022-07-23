# {{cookiecutter.friendly_name}}
{{cookiecutter.project_description}}

![Code Style](https://img.shields.io/badge/Code%20Style-flake8-blue)
![Formatter](https://img.shields.io/badge/Formatter-black-black)
![Imports](https://img.shields.io/badge/Imports-isort-orange)
![Testing](https://img.shields.io/badge/Testing-100%25-green)


## __Getting Started__
* Run the project setup script: `sh scripts/setup.sh`


## __Testing__

### __Running unit and e2e tests__
* Unit and e2e tests: `sh scripts/run_tests_local.sh`

### __Running integration tests__
* Integration tests: `sh scripts/run_integration_tests.sh`


## Docker Deployments
The {{cookiecutter.friendly_name}} project comes equipped with a dockerfile and docker-compose file. The 
docker-compose file is equipped to generate a production {{cookiecutter.friendly_name}} server instance 
and a development PostgreSQL instance

* To build a {{cookiecutter.friendly_name}} image: `docker compose build`
* To spin-down a {{cookiecutter.friendly_name}} and PostgreSQL instance: `docker compose down -v`
* To spin-up a {{cookiecutter.friendly_name}} and PostgreSQL instance: `docker compose up -d`
* To start an existing {{cookiecutter.friendly_name}} and PostgreSQL instance: `docker compose start`
* To stop an existing {{cookiecutter.friendly_name}} and PostgreSQL instance: `docker compose stop`


## __Helpful Commands__
* Run pre-commits: `pre-commit run --all-files`
