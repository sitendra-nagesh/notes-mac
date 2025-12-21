"""remaining post columns

Revision ID: 9cf1a27124f1
Revises: 10711ebce6fb
Create Date: 2025-12-19 19:05:25.057267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cf1a27124f1'
down_revision: Union[str, Sequence[str], None] = '10711ebce6fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("poststwo", sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column("poststwo", sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("poststwo", "published")
    op.drop_column("poststwo", "created_at")
    pass
