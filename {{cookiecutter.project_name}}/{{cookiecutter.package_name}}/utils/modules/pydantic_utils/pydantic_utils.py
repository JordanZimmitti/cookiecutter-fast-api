from fastapi import Form
from pydantic.fields import ModelField

def form_body(cls):
    """
    Decorator function that creates a fast-api form from a pydantic model. This allows for POST
    endpoints in swagger to take advantage of fast-api form fields. The fast-api endpoint must
    depend on the pydantic model in order for the decorator's affects to show

    :param cls: The pydantic model class instance the decorator is attached to

    :return: The pydantic model that is fast-api form compatible
    """

    # Creates a list of pydantic model form parameters
    form_parameters = []
    for parameter in cls.__signature__.parameters.values():

        # Gets the pydantic model field info
        model_field: ModelField = cls.__fields__.get(parameter.name)
        title = model_field.field_info.title
        description = model_field.field_info.description

        # Sets the fast-api form as the new default
        if str(parameter.default) == "<class 'inspect._empty'>":
            required_form = Form(..., title=title, description=description)
            form_parameter = parameter.replace(default=required_form)
        else:
            optional_form = Form(parameter.default, title=title, description=description)
            form_parameter = parameter.replace(default=optional_form)

        # Appends the updated parameter to the list
        form_parameters.append(form_parameter)

    # Adds fast-api form compatibility to a pydantic model class
    cls.__signature__ = cls.__signature__.replace(parameters=form_parameters)
    return cls
