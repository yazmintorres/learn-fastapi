"""add users table

Revision ID: 9a1e13fc4997
Revises: 2ba41e691efa
Create Date: 2024-02-26 10:33:57.549786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a1e13fc4997'
down_revision: Union[str, None] = '2ba41e691efa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
                              nullable=False, server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint("id"), 
                    sa.UniqueConstraint("email")
                    )


def downgrade() -> None:
    op.drop_table("users")
