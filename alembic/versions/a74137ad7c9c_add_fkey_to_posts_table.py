"""Add fkey to posts table

Revision ID: a74137ad7c9c
Revises: bfb3d314e66d
Create Date: 2025-01-30 16:48:34.369847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a74137ad7c9c'
down_revision: Union[str, None] = 'bfb3d314e66d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "owner_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    pass


def downgrade() -> None:
    pass
