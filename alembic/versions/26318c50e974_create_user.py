"""Create user

Revision ID: 26318c50e974
Revises: a281a3a00c70
Create Date: 2025-09-15 10:46:53.871486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.models import User
from app.services.password_service import PasswordService

# revision identifiers, used by Alembic.
revision: str = '26318c50e974'
down_revision: Union[str, Sequence[str], None] = 'e6f9f893263e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pwd_service = PasswordService()
    op.bulk_insert(
        sa.Table(
            'users',
            sa.MetaData(),
                sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('first_name', sa.String(), nullable=False),
                    sa.Column('last_name', sa.String(), nullable=False),
                    sa.Column('is_admin', sa.Boolean(), nullable=False),
                ),
        [
            {'id': 1, 'email': 'admin@admin.ru', 'password': pwd_service.get_password_hash('admin'), 'first_name': 'Greg', 'last_name': 'Brin', 'is_admin': True},
            {'id': 2, 'email': 'test@test.ru', 'password': pwd_service.get_password_hash('test'), 'first_name': 'John', 'last_name': 'Smith', 'is_admin': False}
        ]
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM users WHERE id IN (1, 2);")
