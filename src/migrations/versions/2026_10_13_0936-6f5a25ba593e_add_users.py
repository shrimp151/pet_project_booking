"""add users

Revision ID: 6f5a25ba593e
Revises: 6905b2ee8ea9
Create Date: 2026-10-13 09:36:55.425565

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "6f5a25ba593e"
down_revision: Union[str, None] = "6905b2ee8ea9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
