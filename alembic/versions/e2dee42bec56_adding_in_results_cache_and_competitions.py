"""adding in results cache and competitions

Revision ID: e2dee42bec56
Revises: c5fd8a28bce6
Create Date: 2019-01-14 19:14:42.455540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2dee42bec56'
down_revision = 'c5fd8a28bce6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'competition',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('description', sa.String),
        sa.Column('start_date', sa.Date),
        sa.Column('end_date', sa.Date)
    )

    op.create_table(
        'result_cache',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('competition_id', sa.Integer),
        sa.Column('club_id', sa.Integer),
        sa.Column('win', sa.Integer),
        sa.Column('loss', sa.Integer),
        sa.Column('draw', sa.Integer),
        sa.Column('points', sa.Integer),
        sa.Column('goals_against', sa.Integer),
        sa.Column('goals_for', sa.Integer),
        sa.Column('goal_difference', sa.Integer),
        sa.Column('updated_at', sa.TIMESTAMP)
    )

    op.add_column('match', sa.Column('competition_id', sa.Integer))
    op.add_column('division', sa.Column('display_competition_id', sa.Integer))

def downgrade():
    op.drop_table('competition')
    op.drop_table('result_cache')

    op.drop_column('match', 'competition_id')
    op.drop_column('division', 'display_competition_id')
