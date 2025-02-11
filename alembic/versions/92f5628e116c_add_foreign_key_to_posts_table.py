"""add foreign-key to posts table

Revision ID: 92f5628e116c
Revises: 8dc66a48ac7c
Create Date: 2024-09-06 11:32:05.709229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92f5628e116c'
down_revision: Union[str, None] = '8dc66a48ac7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'],remote_cols=['id'], ondelete="CASCADE")


    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts','owner_id')
    pass
