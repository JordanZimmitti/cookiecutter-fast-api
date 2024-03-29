from fastapi import Form
from pydantic.fields import FieldInfo


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

        # Gets the pydantic field info
        field_info: FieldInfo | None = cls.model_fields.get(parameter.name)
        if not field_info:
            for model_field in cls.model_fields.values():
                if model_field.alias == parameter.name:
                    field_info = model_field
                    break

        # Gets the data from the field info
        title = field_info.title
        description = field_info.description
        metadata = field_info.metadata

        # Sets the fast-api form as the new default
        if str(parameter.default) == "<class 'inspect._empty'>":
            required_form = Form(..., title=title, description=description)
            required_form.metadata = metadata
            form_parameter = parameter.replace(default=required_form)
        else:
            optional_form = Form(parameter.default, title=title, description=description)
            optional_form.metadata = metadata
            form_parameter = parameter.replace(default=optional_form)

        # Appends the updated parameter to the list
        form_parameters.append(form_parameter)

    # Adds fast-api form compatibility to a pydantic model class
    cls.__signature__ = cls.__signature__.replace(parameters=form_parameters)
    return cls
