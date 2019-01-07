"""update_shirt_colors_capabilities

Revision ID: a1fc93bdf1ec
Revises: aa351f41cf0c
Create Date: 2019-01-07 14:06:14.336272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1fc93bdf1ec'
down_revision = 'aa351f41cf0c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('club', sa.Column('home_shirt_id', sa.Integer))
    op.add_column('club', sa.Column('away_shirt_id', sa.Integer))
    op.add_column('club', sa.Column('goalkeeper_shirt_id', sa.Integer))
    op.add_column('club', sa.Column('logo_filename', sa.String))

    # Update the player table
    op.drop_column('player', 'shirt_color')
    op.add_column('player', sa.Column('show_date_of_birth', sa.Integer))
    op.add_column('player', sa.Column('profile_filename', sa.String(200)))

    # create a shirt table to hold all possible shirts
    op.create_table(
        'shirt',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('style', sa.String(40)),
        sa.Column('primary_color', sa.String(40)),
        sa.Column('secondary_color', sa.String(40))
     )

def downgrade():
    op.drop_column('club', 'home_shirt_id')
    op.drop_column('club', 'away_shirt_id')
    op.drop_column('club', 'goalkeeper_shirt_id')
    op.drop_column('club', 'logo_filename')

    op.add_column('player', sa.Column('shirt_color', sa.String(10)))
    op.drop_column('player', 'show_date_of_birth')
    op.drop_column('player', 'profile_filename')

    op.drop_table('shirt')