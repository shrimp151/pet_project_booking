"""create Rooms table

Revision ID: 3e861091de16
Revises: 325c799694b8
Create Date: 2026-10-08 14:45:02.741603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e861091de16'
down_revision: Union[str, None] = '325c799694b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hotel_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('rooms')
