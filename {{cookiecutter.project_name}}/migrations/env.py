from asyncio import run
from logging.config import fileConfig
from typing import Any

from alembic import context
from google.cloud.sql.connector import Connector, IPTypes, create_async_connector
from sqlalchemy.ext.asyncio import create_async_engine

from {{cookiecutter.package_name}}.core.database.tables import BaseTable
from {{cookiecutter.package_name}}.core.settings import settings

# Sets the alembic config with values from the alembic.ini file
config = context.config

# Interprets the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Sets the target metadata from the base-model
target_metadata = BaseTable.metadata

# The database schema the tables should be created in
namespace = settings.NAMESPACE
db_type = settings.API_DB_TYPE
db_schema = settings.API_DB_SCHEMA
db_password = settings.API_DB_PASSWORD_MIGRATIONS


def run_migrations_offline():
    """
    Run migrations in 'offline' mode

    This configures the context with just a URL and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation we don't even need a DBAPI to be available
    """

    # Configures the context before running the offline-migrations
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Runs the migrations offline
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """
    Run migrations in 'online' mode

    In this scenario we need to create an Engine and associate a connection with the context
    """

    # Gets the online database connection-uri
    db_uri = config.get_main_option("sqlalchemy.url")
    if not db_uri:
        db_uri = settings.API_DB_CONN_URI_MIGRATIONS.get_secret_value()
        is_cloud_db = db_type == "cloud"
        is_local_namespace = namespace == "http://localhost"
        is_local_password = db_password.get_secret_value() == "very-secure-password"
        if is_local_namespace and (is_cloud_db or not is_local_password):
            raise SystemExit("Error: Do not run migrations on a deployed database locally")

    # Gets a Cloud SQL URI and creator When the database type is set to cloud
    creator = None
    if db_type == "cloud":

        # Gets the Cloud SQL database URI
        db_uri = f"{settings.API_DB_DRIVER.get_secret_value()}://"

        # Creates a wrapper function for getting the Cloud SQL creator
        async def get_cloud_sql_creator():
            connector = await create_async_connector()
            return await _get_cloud_sql_creator(connector)

        # Gets a Cloud SQL creator
        creator = get_cloud_sql_creator

    # Creates the async engine for the database
    engine = create_async_engine(
        url=db_uri,
        async_creator=creator,
        pool_pre_ping=True,
        pool_size=settings.SQLALCHEMY_POOL_SIZE,
        max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
        echo=settings.IS_ECHO_SQLALCHEMY_LOGS,
        connect_args={
            "server_settings": {"application_name": f"{settings.PROJECT_NAME} Migration"}
        },
    )

    # Runs the migrations online
    async with engine.connect() as connection:
        await connection.run_sync(_run_migrations)

    # Disposes the connection pool
    await engine.dispose()


async def _get_cloud_sql_creator(connector: Connector) -> Any:
    """
    Function that gets a creator for creating
    connections to a Cloud SQL instance

    :param connector:

    :return a Cloud SQL creator
    """

    # Creates the creator for creating connections to a Cloud SQL instance
    creator = await connector.connect_async(
        enable_iam_auth=True,
        instance_connection_string=settings.API_DB_CLOUD_INSTANCE.get_secret_value(),
        driver=settings.API_DB_CLOUD_DRIVER.get_secret_value(),
        user=settings.API_DB_USER_MIGRATIONS.get_secret_value(),
        db=settings.API_DB_DB.get_secret_value(),
        ip_type=IPTypes.PRIVATE if settings.API_DB_CLOUD_IS_PRIVATE else IPTypes.PUBLIC,
    )

    # Returns a Cloud SQL creator
    return creator


def _run_migrations(connection):
    """
    Function that performs an
    online alembic migration

    :param connection: An active database connection
    """

    # Configures the context before running the migrations
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        version_table_schema=db_schema.get_secret_value(),
    )

    # Runs the migrations
    with context.begin_transaction():
        context.execute(f"SET search_path TO {db_schema.get_secret_value()}")
        context.run_migrations()


# Runs the migrations in either offline_mode or online_mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run(run_migrations_online())
