# __Fast-API Postgres Cookiecutter Template (MacOS/Linux)__
Create a fully-working production-ready Fast-API server in minutes!

## __Install And Run Cookiecutter__

1. Install dependencies
   * `brew install python@3.12`
   * `brew install poetry`
   * `brew install cookiecutter`

2. Run cookiecutter to create template
    * `cookiecutter https://github.com/JordanZimmitti/cookiecutter-fast-api.git --checkout vx.x.x`

## __Features__

* **Project Configuration**
    * Python 12 support 
    * Black, Flake8, Isort, and Poetry pre-commits configured
    * Poetry package manager for enhanced package management
    * Script for easy local environment setup
  
* **Docker**
    * Production-Ready multi-stage dockerfile configured
    * Alpine base-image for the best os-security and smaller build sizes 
    * Docker-Compose configured with: 
        * Fast-API server 
        * Unit-Test runner
        * Integration-Test runner
        * Postgres database
        * Redis database
    
* **Fast-API Server**
    * Application-Level context management 
    * Environment-Variables `settings.py` class for easy environment management 
    * Gunicorn server engine optimized for deployment in Kubernetes
    * HTTP status-code error handling
    * Key/Value pair line-logging optimized for Grafana/Loki
    * Auto rotating of log files based on file size
    * Built-in health check and prometheus metrics endpoints
    * A Fast-API decorator for running repeated tasks 

* **Testing**
    * 100% code-coverage on all template code
    * API, Integration, and Unit tests configured
    * Script for running all API/Unit tests both deployed and locally
    * Script for running all Integration tests both deployed and locally
  
* **Database** 
    * SQLAlchemy 2.0 support 
    * Async Postgres support via built-in database helper classes
    * Built-in Async Alembic migration for Postgres

* **Caching**
    * Async Redis support via built-in redis helper classes 
    * Pipeline wrapper function for protecting transactions with retries and proper http errors

* **Utilities**
    * A pydantic utility decorator function that creates a fast-api form from a pydantic model
    * An async utility function to run synchronous code asynchronously
