from unittest.mock import MagicMock
from uuid import UUID

from {{cookiecutter.package_name}}.core.database.tables.table_base import StampMixin


def test_audit_table_created_by():
    """
    Tests the audit_table function when a 'created_by' property value exists. The
    audit_table function audit_table function set an uuid value to the 'updated_by' property
    """

    # Mocks the stamp-mixin class
    stamp_mixin_mock = MagicMock(spec=StampMixin)
    stamp_mixin_mock.created_by = "a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2"

    # Creates a test user-id
    user_id = UUID("a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2")

    # Invokes the audit_table function
    StampMixin.audit_table(self=stamp_mixin_mock, user_id=user_id)

    # Checks whether the user-id was set correctly
    assert stamp_mixin_mock.updated_by == user_id


def test_audit_table_no_created_by():
    """
    Tests the audit_table function when a 'created_by' property value does not exist. The
    audit_table function should set an uuid value to the 'created_by' property
    """

    # Mocks the stamp-mixin class
    stamp_mixin_mock = MagicMock(spec=StampMixin)
    stamp_mixin_mock.created_by = None

    # Creates a test user-id
    user_id = UUID("a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2")

    # Invokes the audit_table function
    StampMixin.audit_table(self=stamp_mixin_mock, user_id=user_id)

    # Checks whether the user-id was set correctly
    assert stamp_mixin_mock.created_by == user_id
