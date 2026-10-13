"""make email unique

Revision ID: 9c32f1cd1891
Revises: 6f5a25ba593e
Create Date: 2026-10-13 11:36:18.068126

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "9c32f1cd1891"
down_revision: Union[str, None] = "6f5a25ba593e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
