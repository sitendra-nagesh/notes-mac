"""add foreign key to post table

Revision ID: 10711ebce6fb
Revises: 398db3dbddc3
Create Date: 2025-12-19 18:29:43.709301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10711ebce6fb'
down_revision: Union[str, Sequence[str], None] = '398db3dbddc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("poststwo", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_user_fkey", source_table="poststwo", referent_table="userstwo",
    local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_user_fkey", table_name="poststwo")
    op.drop_column("poststwo", "owner_id")
    pass
