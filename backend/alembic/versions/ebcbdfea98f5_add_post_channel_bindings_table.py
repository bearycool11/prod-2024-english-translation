"""add post_channel_bindings table

Revision ID: ebcbdfea98f5
Revises: e1f15fd2ea7f
Create Date: 2024-04-01 21:01:25.653878

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'ebcbdfea98f5'
down_revision = 'e1f15fd2ea7f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_channel_bindings',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('post_id', 'channel_id'),
    sa.UniqueConstraint('post_id', 'channel_id', name='_post_channel_bindings_uc')
    )
    op.alter_column('posts', 'comment',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'comment',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_table('post_channel_bindings')
    # ### end Alembic commands ###
