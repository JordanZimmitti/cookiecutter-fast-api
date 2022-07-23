def get_openapi_mock(**_):
    return {
        "openapi": "3.0.2",
        "info": {
            "title": "{{cookiecutter.friendly_name}}",
            "description": "{{cookiecutter.project_description}}",
            "version": "0.1.0",
        },
    }
