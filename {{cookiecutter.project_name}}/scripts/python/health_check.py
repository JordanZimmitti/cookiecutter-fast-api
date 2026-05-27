from httpx import AsyncClient
from uvloop import run

from {{cookiecutter.package_name}}.core.settings import settings


async def main():
    """
    Script that checks the health
    of the {{cookiecutter.friendly_name}} server
    """

    # Gets the API prefix
    api_prefix = settings.API_PREFIX

    # Checks whether the {{cookiecutter.friendly_name}} server is up and running
    async with AsyncClient() as client:
        response = await client.get(f"http://{{cookiecutter.package_name}}:2000{api_prefix}/v1/health/check")
        assert response.status_code == 200


if __name__ == "__main__":
    run(main())
