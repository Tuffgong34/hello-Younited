"""initial table design

Revision ID: aa351f41cf0c
Revises: 
Create Date: 2018-12-19 14:02:42.585351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa351f41cf0c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # yn_user
    op.create_table(
        'yn_user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(200), nullable=True),
        sa.Column('phone_number', sa.String(24), nullable=True),
        sa.Column('password', sa.String(60)),
        sa.Column('salt', sa.String(32)),
        sa.Column('confirmed', sa.Integer),
        sa.Column('confirmation_id', sa.String(32)),
        sa.Column('status', sa.String(10), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now())
    )
    # player
    op.create_table(
        'player',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(100), nullable=True),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('shirt_number', sa.Integer),
        sa.Column('date_of_birth', sa.Date),
        sa.Column('height_cm', sa.Integer),
        sa.Column('club_id', sa.Integer),
        sa.Column('position_id', sa.Integer),
        sa.Column('shirt_color', sa.String(10)),
        sa.Column('yn_user_id', sa.Integer),    
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now())
    )
    # club
    op.create_table(
        'club',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(250), nullable=False),
        sa.Column('founded', sa.Date),
        sa.Column('information', sa.String),
        sa.Column('contact', sa.String),
        sa.Column('location', sa.String),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('division_id', sa.Integer)
    )
    # position - available player positions
    op.create_table(
        'position',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(32)),
        sa.Column('description', sa.String),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now())
    )
    # match
    op.create_table(
        'match',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('home_club_id', sa.Integer),
        sa.Column('away_club_id', sa.Integer),
        sa.Column('played', sa.TIMESTAMP),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now())
    )
    # event
    op.create_table(
        'event',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('event_type_id', sa.Integer),
        sa.Column('player_1_id', sa.Integer),
        sa.Column('player_2_id', sa.Integer),
        sa.Column('information', sa.String),
        sa.Column('match_id', sa.Integer),
        sa.Column('occured_at', sa.TIMESTAMP)
    )
    # lineup
    op.create_table(
        'lineup',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('player_id', sa.Integer),
        sa.Column('match_id', sa.Integer),
        sa.Column('position_id', sa.Integer),
        sa.Column('created_at', sa.TIMESTAMP)
    )
    # membership - tracking when people joined teams
    op.create_table(
        'membership',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('player_id', sa.Integer, nullable=False),
        sa.Column('club_id', sa.Integer, nullable=False),
        sa.Column('joined_at', sa.TIMESTAMP, nullable=False),
        sa.Column('left_at', sa.TIMESTAMP, nullable=False)
    )
    # league
    op.create_table(
        'league',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(40), nullable=False),
        sa.Column('location', sa.String(100)),
        sa.Column('description', sa.String(250)),
        sa.Column('founded', sa.TIMESTAMP)
    )
    # division
    op.create_table(
        'division',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(40), nullable=False),
        sa.Column('location', sa.String(100)),
        sa.Column('description', sa.String(250)),
        sa.Column('league_id', sa.Integer),
        sa.Column('founded', sa.TIMESTAMP)
    )
    # training session
    op.create_table(
        'training_session',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('location', sa.String(100)),
        sa.Column('notes', sa.String(250)),
        sa.Column('player_id', sa.Integer),
        sa.Column('date_of_session', sa.TIMESTAMP),
        sa.Column('length_mins', sa.Integer),
        sa.Column('created_at', sa.TIMESTAMP)
    )
    # event_type - 
    op.create_table(
        'event_type',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),  
        sa.Column('description', sa.String(400))
    )
    # status
    op.create_table(
        'status',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(25), nullable=False),
        sa.Column('description', sa.String(100))
    )
    # status_history
    op.create_table(
        'status_history',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('player_id', sa.Integer),
        sa.Column('status_id', sa.Integer),
        sa.Column('start', sa.TIMESTAMP),
        sa.Column('end', sa.TIMESTAMP)
    )
    # sponsor
    op.create_table(
        'sponsor',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(40)),
        sa.Column('description', sa.String(400)),
        sa.Column('club_id', sa.Integer),
        sa.Column('start', sa.TIMESTAMP),
        sa.Column('end', sa.TIMESTAMP)
    )
    
def downgrade():
    op.drop_table('yn_user')
    op.drop_table('player')
    op.drop_table('club')
    op.drop_table('position')
    op.drop_table('match')
    op.drop_table('event')
    op.drop_table('lineup')
    op.drop_table('membership')
    op.drop_table('league')
    op.drop_table('division')
    op.drop_table('training_session')
    op.drop_table('event_type')
    op.drop_table('status')
    op.drop_table('status_history')
    op.drop_table('sponsor')
    

