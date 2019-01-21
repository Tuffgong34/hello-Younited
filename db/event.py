from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
import datetime
from utils.dbutils import get_base
import uuid

Base = get_base()

# Event_Types
#  id |    name     | description
# ----+-------------+-------------
#   1 | Goal        |
#   2 | Yellow Card |
#   3 | Red Card    |
#   4 | Kick-off    |
#   5 | Corner      |
#   6 | Throw-In    |
#   7 | Penalty     |
#   8 | Foul        |
#   9 | Full-time   |


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    event_type_id = Column(Integer)
    player_1_id = Column(Integer)
    player_2_id = Column(Integer)
    information = Column(String)
    match_id = Column(Integer)
    occurred_at = Column(TIMESTAMP) 
    
    def __init__(self, event_type_id, player_1_id, match_id):
        self.player_1_id = player_1_id
        self.event_type_id = event_type_id
        self.match_id = match_id

    def __repr__(self):
        return '<Event {} in match: {}, player: {} and support: {}, at: {}>'.format(self.event_type_id, self.match_id, self.player_1_id, self.player_2_id, self.occurred_at)

  