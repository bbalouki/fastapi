"""Add content column to posts table

Revision ID: ba87515f80d0
Revises: c9f269571a98
Create Date: 2025-01-30 16:39:41.305166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba87515f80d0'
down_revision: Union[str, None] = 'c9f269571a98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
