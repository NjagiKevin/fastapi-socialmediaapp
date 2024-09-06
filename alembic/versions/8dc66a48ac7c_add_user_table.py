"""add user table

Revision ID: 8dc66a48ac7c
Revises: 3fba914b30cc
Create Date: 2024-09-06 10:47:59.150289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8dc66a48ac7c'
down_revision: Union[str, None] = '3fba914b30cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
pass


def downgrade():
    op.drop_table('users')
    pass
