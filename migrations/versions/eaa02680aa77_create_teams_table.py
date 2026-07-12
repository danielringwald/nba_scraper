"""create teams table

Revision ID: eaa02680aa77
Revises: 
Create Date: 2026-07-09 21:28:35.930214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eaa02680aa77'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("abbreviation", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("abbreviation")
    )


def downgrade() -> None:
    op.drop_table("teams")
