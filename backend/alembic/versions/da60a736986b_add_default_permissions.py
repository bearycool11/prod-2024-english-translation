"""Add default permissions

Revision ID: da60a736986b
Revises: ebe590969bac
Create Date: 2024-03-31 23:02:17.708231

"""
from alembic import op
from database.models import DBPermission
from sqlalchemy.sql import text
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = 'da60a736986b'
down_revision = 'ebe590969bac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(text("INSERT INTO permissions (name, level, can_grant) VALUES ('viewer', 1, False)"))
    connection.execute(text("INSERT INTO permissions (name, level, can_grant) VALUES ('editor', 2, False)"))
    connection.execute(text("INSERT INTO permissions (name, level, can_grant) VALUES ('reviewer', 3, False)"))
    connection.execute(text("INSERT INTO permissions (name, level, can_grant) VALUES ('admin', 4, True)"))
    connection.execute(text("INSERT INTO permissions (name, level, can_grant) VALUES ('owner', 5, True)"))

def downgrade() -> None:
    pass
