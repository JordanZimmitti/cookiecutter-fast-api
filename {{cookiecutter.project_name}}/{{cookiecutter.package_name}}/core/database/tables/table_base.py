from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import declarative_base

# Creates the base used by explicit models created in {{cookiecutter.friendly_name}}
BaseTable = declarative_base()


class StampMixin:
    """
    Mixin that adds creation and update metadata to an existing table
    """

    # StampMixin Columns
    created_by = Column(
        type_=UUID(as_uuid=True),
        nullable=False,
        comment="The user who created the row",
    )
    created_on = Column(
        type_=TIMESTAMP,
        nullable=False,
        default=datetime.utcnow,
        comment="The date when the row was created",
    )
    updated_by = Column(
        type_=UUID(as_uuid=True),
        nullable=True,
        comment="The user who updated the row",
    )
    updated_on = Column(
        type_=TIMESTAMP,
        nullable=True,
        onupdate=datetime.utcnow,
        comment="The date when the row was updated",
    )

    def audit_table(self, user_id: UUID):
        """
        Function that saves which user created or
        updated a row within the given table

        :param user_id: The unique identifier of the user who is creating or updating the row
        """

        # Adds the id of the user creating the row
        if not self.created_by:
            self.created_by = str(user_id)
            return

        # Adds the id of the user updating the row
        self.updated_by = str(user_id)


# Orders the StampMixin columns
StampMixin.created_by._creation_order = 9996
StampMixin.created_on._creation_order = 9997
StampMixin.updated_by._creation_order = 9998
StampMixin.updated_on._creation_order = 9999
