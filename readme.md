# Fast-API Postgres Cookiecutter Template (MacOS/Linux)
Create a fully-working production-ready Fast-API server in minutes!

## Features

* **Project Configuration**
    * Black, Flake8, and Isort pre-commits configured
    * Poetry package manager for enhanced package management
    * Script for easy local environment setup
  
* **Docker**
    * Production-Ready dockerfile configured
    * Docker-Compose configured with Fast-API server and Postgres database
    
* **Fast-API Server**
    * Application-Level context management 
    * Environment-Variables `settings.py` class for easy environment management 
    * Gunicorn server engine optimized for deployment in Kubernetes
    * HTTP status-code error handling
    * Key/Value pair line-logging optimized for Grafana/Loki

* **Testing**
    * 100% code-coverage on all template code
    * E2E, Integration, and Unit tests configured
    * Script for running all E2E/Unit tests
    * Script for running all Integration tests
  
* **Database** 
    * Postgres support via built-in database helper classes
    * Built-in Async Alembic migration for Postgres
