"""add_western_max_data

Revision ID: 03ea2b4842b5
Revises: 0555d3d29f6e
Create Date: 2025-04-19 18:38:51.477353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03ea2b4842b5'
down_revision: Union[str, None] = '0555d3d29f6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
