from fastapi import Form


def form_body(cls):
    """
    Decorator function that creates a fast-api form from a pydantic model. This allows for POST
    endpoints in swagger to take advantage of fast-api form fields. The fast-api endpoint must
    depend on the pydantic model in order for the decorator's affects to show

    :param cls: The pydantic model class instance the decorator is attached to

    :return: The pydantic model that is fast-api form compatible
    """

    # Adds fast-api form compatibility to a pydantic model class
    cls.__signature__ = cls.__signature__.replace(
        parameters=[arg.replace(default=Form(...)) for arg in cls.__signature__.parameters.values()]
    )
    return cls
