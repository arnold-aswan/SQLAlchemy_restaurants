"""create db

Revision ID: 2afd83d07fc6
Revises: 8647440bbcef
Create Date: 2023-09-02 16:02:49.683832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2afd83d07fc6'
down_revision: Union[str, None] = '8647440bbcef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
