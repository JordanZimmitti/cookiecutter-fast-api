from asyncio import run
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from {{cookiecutter.package_name}}.core.database import TableBase
from {{cookiecutter.package_name}}.core.settings import settings

# Sets the alembic config with values from the alembic.ini file
config = context.config

# Interprets the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Sets the target metadata from the base-model
target_metadata = TableBase.metadata

# The database schema the tables should be created in
app_schema = "public"

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
        db_uri = settings.API_DB_CONN_URI.get_secret_value()

    # Creates the connection engine to the database
    engine = create_async_engine(db_uri)

    # Runs the migrations online
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    # Disposes the connection pool
    await engine.dispose()


def do_run_migrations(connection):
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
        version_table_schema=app_schema
    )

    # Runs the migrations
    with context.begin_transaction():
        context.execute(f"SET search_path TO {app_schema}")
        context.run_migrations()


# Runs the migrations in either offline_mode or online_mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run(run_migrations_online())
