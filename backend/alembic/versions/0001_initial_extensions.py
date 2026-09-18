"""Initial setup: extensions

Revision ID: 0001_initial_extensions
Revises: 
Create Date: 2026-09-18 19:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0001_initial_extensions'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.execute('CREATE EXTENSION IF NOT EXISTS "vector";')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pg_trgm";')

def downgrade() -> None:
    pass
