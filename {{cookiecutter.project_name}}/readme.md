# __{{cookiecutter.friendly_name}}__
{{cookiecutter.project_description}}

![Code Style](https://img.shields.io/badge/Code%20Style-flake8-blue)
![Formatter](https://img.shields.io/badge/Formatter-black-black)
![Imports](https://img.shields.io/badge/Imports-isort-orange)
![Testing](https://img.shields.io/badge/Testing-100%25-green)


## __Getting Started__
* Run the project setup script: `sh scripts/setup.sh`

### __Overriding Environment Variables__
To override environment variables found in `{{cookiecutter.package_name}}.core.settings` follow
the steps below:

1. Create a `local` folder in the root `[{{cookiecutter.project_name}}]` directory if one does not exist
2. Create an `override.env` file in the local folder
3. Create an `override-docker.env` file in the local folder
4. Create an `override-docker-integration.env` file in the local folder
4. Add any environment variable that should be overriden (exp. `LOG_LEVEL=DEBUG`)

* The `override.env` file is used when running the API natively
* The `override-docker.env` file is used when running the API in docker
* The `override-docker-integration.env` file is used when running the integration tests in docker


## __Testing__

### __Running api and unit tests__
* API and Unit tests: `sh scripts/run_tests_local.sh`

### __Running integration tests__
* Integration tests: `sh scripts/run_integration_tests_local.sh`


## __Docker Deployments__
The {{cookiecutter.friendly_name}} project comes equipped with a dockerfile and docker-compose file. The 
docker-compose file is equipped to generate a production {{cookiecutter.friendly_name}} server instance 
and a development PostgreSQL instance

* To build the {{cookiecutter.friendly_name}} images: `docker compose build`
* To spin-up a {{cookiecutter.friendly_name}}, PostgreSQL, and Redis instance: `docker compose up -d`
* To spin-down a {{cookiecutter.friendly_name}}, PostgreSQL, and Redis instance: `docker compose down -v`
* To start an existing {{cookiecutter.friendly_name}}, PostgreSQL, and Redis instance: `docker compose start`
* To stop an existing {{cookiecutter.friendly_name}}, PostgreSQL, and Redis instance: `docker compose stop`


## __Helpful Commands__
* Run pre-commits: `pre-commit run --all-files`
