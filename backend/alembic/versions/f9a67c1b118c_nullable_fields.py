"""nullable fields

Revision ID: f9a67c1b118c
Revises: f3410fa02658
Create Date: 2024-04-02 20:57:40.216309

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'f9a67c1b118c'
down_revision = 'f3410fa02658'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("sent_post_info_pkey", "sent_post_info")
    op.execute("ALTER TABLE sent_post_info ADD CONSTRAINT sent_post_info_pkey PRIMARY KEY (id)")
    op.alter_column('sent_post_info', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('sent_post_info', 'channel_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE sent_post_info ADD CONSTRAINT sent_post_info_pkey PRIMARY KEY (id)")
    op.alter_column('sent_post_info', 'channel_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('sent_post_info', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
