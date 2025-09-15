"""Create account

Revision ID: 7168dd8128d5
Revises: 26318c50e974
Create Date: 2025-09-15 11:14:00.076341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7168dd8128d5'
down_revision: Union[str, Sequence[str], None] = '26318c50e974'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(
        sa.Table(
            'accounts',
            sa.MetaData(),
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('balance', sa.Float(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False)
        ),
        [
            {'id': 1, 'balance': 20.5, 'user_id': 2},
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM accounts WHERE id = 1;")
