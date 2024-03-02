"""addd content column to posts table

Revision ID: 2ba41e691efa
Revises: 450706d5ec55
Create Date: 2024-02-26 10:22:19.635832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ba41e691efa'
down_revision: Union[str, None] = '450706d5ec55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
