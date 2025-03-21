"""add id sequence

Revision ID: f3410fa02658
Revises: ee9179c37c20
Create Date: 2024-04-02 20:48:25.443018

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy import Sequence

# revision identifiers, used by Alembic.
revision = 'f3410fa02658'
down_revision = 'ee9179c37c20'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE SEQUENCE IF NOT EXISTS sent_post_info_id_seq START 1")
    op.alter_column('sent_post_info', 'id',
                    existing_type=sa.Integer(),
                    type_=sa.Integer(),
                    existing_nullable=False,
                    autoincrement=True,
                    server_default=Sequence('sent_post_info_id_seq').next_value())
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
