from pydantic import BaseModel, ConfigDict, Field


class RequestMetadataModel(BaseModel):
    """
    Model for describing the properties
    of the metadata given in a request
    """

    # Config that makes all attributes immutable
    model_config = ConfigDict(frozen=True)

    method: str = Field(
        ...,
        title="Method",
        description="The type of request made (exp. get, post, put, delete)",
        alias="method",
    )
    url: str = Field(
        ...,
        title="Url",
        description="The full url address of the request",
        alias="url",
    )
    user_agent: str = Field(
        ...,
        title="User Agent",
        description="The device that the request is being made from",
        alias="userAgent",
    )
