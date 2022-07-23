# Alembic Migrations
Alembic is a lightweight database migration tool for usage with the 
SQLAlchemy Database Toolkit for Python

## Common Commands
Below are common commands that are used with alembic

### Downgrade

* Downgrade to no revision: `alembic downgrade base`
* Downgrade to a specific revision: `alembic downgrade 'revision_number'`
* Downgrade to a relative revision: `alembic downgrade -1`

### Upgrade

* Upgrade to a latest revision: `alembic upgrade head`
* Upgrade to a specific revision: `alembic upgrade 'revision_number'`
* Upgrade to a relative revision: `alembic upgrade +1`

### Revisions

* Create a new revision: `alembic revision -m "Revision message"`
* Check revision history: `alembic history`