from typing import Any, Dict

from pydantic import BaseModel, Field


class HealthModel(BaseModel):
    """
    Model for describing the properties of a response that
    determines the health of the {{cookiecutter.friendly_name}} worker
    """

    # Config that makes all attributes immutable
    class Config:
        frozen = True

    status: str = Field(
        ...,
        title="Status",
        description="Whether the endpoint was sent successfully",
        alias="status",
    )

    version: str = Field(
        ..., title="Version", description="The current {{cookiecutter.friendly_name}} version", alias="version"
    )


class SettingsModel(BaseModel):
    """
    Model for describing the properties of a response that gets the
    environment settings of the running {{cookiecutter.friendly_name}} worker
    """

    # Config that makes all attributes immutable
    class Config:
        frozen = True

    settings: Dict[str, Any] = Field(
        ...,
        title="Settings",
        description="The {{cookiecutter.friendly_name}} worker environment settings",
        alias="settings",
    )
