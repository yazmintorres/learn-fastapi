"""add foreign key to posts table

Revision ID: 0da1d4b6f15e
Revises: 9a1e13fc4997
Create Date: 2024-02-26 10:50:50.675618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0da1d4b6f15e'
down_revision: Union[str, None] = '9a1e13fc4997'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", "posts", "users", ["owner_id"], ["id"], ondelete="CASCADE") 


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", "posts")
    op.drop_column("posts", "owner_id")
