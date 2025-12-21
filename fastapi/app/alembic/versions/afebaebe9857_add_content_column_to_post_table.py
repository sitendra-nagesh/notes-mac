"""add content column to post table

Revision ID: afebaebe9857
Revises: 60e3a5d00c26
Create Date: 2025-12-18 22:56:15.604424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afebaebe9857'
down_revision: Union[str, Sequence[str], None] = '60e3a5d00c26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("poststwo", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("poststwo", "content")
    pass
