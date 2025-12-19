"""create post table

Revision ID: 60e3a5d00c26
Revises: 
Create Date: 2025-12-18 22:22:35.720971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60e3a5d00c26'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('poststwo', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
            sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('poststwo')
    pass
