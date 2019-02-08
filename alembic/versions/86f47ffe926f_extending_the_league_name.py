"""extending the league name

Revision ID: 86f47ffe926f
Revises: 8d2d12b33f51
Create Date: 2019-02-08 11:33:30.725427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86f47ffe926f'
down_revision = '8d2d12b33f51'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('league', 'name',
        existing_type=sa.String(length=40),
        type_=sa.String(length=200),
        existing_nullable=False)
    op.alter_column('division', 'name',
        existing_type=sa.String(length=40),
        type_=sa.String(length=200),
        existing_nullable=False)


def downgrade():
    op.alter_column('league', 'name',
        existing_type=sa.String(length=200),
        type_=sa.String(length=40),
        existing_nullable=False)
    op.alter_column('division', 'name',
        existing_type=sa.String(length=200),
        type_=sa.String(length=40),
        existing_nullable=False)
