from pydantic import BaseModel, Field

from {{cookiecutter.package_name}}.utils.pydantic_utils import form_body


def test_form_body():
    """
    Tests the form_body function for completion. The form_body function should return the pydantic
    model class with a class signature that contains the fast-api form instances
    """

    # Creates a test pydantic model class
    class TestModel(BaseModel):
        arg_one: str = Field(...)
        arg_two: int = Field(0)

    # Checks whether the class signature contains the fast-api form instances
    model_with_form_body = form_body(cls=TestModel)
    assert "Form(Ellipsis)" in str(model_with_form_body(arg_one="test-arg-one").__signature__)
    assert "Form(0)" in str(model_with_form_body(arg_one="test-arg-one").__signature__)
