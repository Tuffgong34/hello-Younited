"""update the event table - spelling error

Revision ID: 8d2d12b33f51
Revises: e2dee42bec56
Create Date: 2019-01-21 10:33:27.545217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d2d12b33f51'
down_revision = 'e2dee42bec56'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('event', 'occured_at', new_column_name='occurred_at')


def downgrade():
    op.alter_column('event', 'occurred_at', new_column_name='occured_at')
