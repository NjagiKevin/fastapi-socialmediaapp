"""add content column to posts table

Revision ID: 3fba914b30cc
Revises: d3657d7615cc
Create Date: 2024-09-06 10:36:27.561825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fba914b30cc'
down_revision: Union[str, None] = 'd3657d7615cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)  # Use sa.Column instead of sa.column
    )



def downgrade():
    op.drop_column(
        'posts',
        'content'
    )
    pass
