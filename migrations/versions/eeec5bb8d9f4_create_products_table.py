"""create products table

Revision ID: eeec5bb8d9f4
Revises:
Create Date: 2026-08-21 10:49:57.932955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'eeec5bb8d9f4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )



def downgrade() -> None:
    op.drop_table("products")
