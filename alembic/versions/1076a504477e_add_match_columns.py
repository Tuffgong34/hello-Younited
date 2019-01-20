"""add match columns

Revision ID: 1076a504477e
Revises: e2dee42bec56
Create Date: 2019-01-20 18:11:01.041484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1076a504477e'
down_revision = 'e2dee42bec56'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('match', sa.Column('competition_id', sa.Integer))


def downgrade():
    op.drop_column('match', 'competition_id')
