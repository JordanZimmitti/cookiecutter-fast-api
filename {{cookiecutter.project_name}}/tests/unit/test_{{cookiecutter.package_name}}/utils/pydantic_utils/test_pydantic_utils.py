from pydantic import BaseModel, Field

from {{cookiecutter.package_name}}.utils.modules.pydantic_utils import form_body


def test_form_body():
    """
    Tests the form_body function for completion. The form_body function should return the pydantic
    model class with a class signature that contains the fast-api form instances
    """

    # Creates a test pydantic model class
    class TestModel(BaseModel):
        arg_one: str = Field("test-arg-one")
        arg_two: int = Field("test-arg-two")

    # Checks whether the class signature contains the fast-api form instances
    model_with_form_body = form_body(cls=TestModel)
    assert "Form" in str(model_with_form_body().__signature__)
