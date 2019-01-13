"""update player object with age

Revision ID: c5fd8a28bce6
Revises: a1fc93bdf1ec
Create Date: 2019-01-13 08:23:52.301810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5fd8a28bce6'
down_revision = 'a1fc93bdf1ec'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('player', sa.Column('age', sa.Integer))
    op.add_column('player', sa.Column('age_added', sa.Date))
    op.add_column('player', sa.Column('dominant_foot', sa.String(10)))


def downgrade():
    op.drop_column('player', 'age')
    op.drop_column('player', 'age_added')
    op.drop_column('player', 'dominant_foot')
