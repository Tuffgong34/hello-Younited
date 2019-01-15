from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
import datetime
from utils.dbutils import get_base
import uuid

Base = get_base()

class ResultCache(Base):
    __tablename__ = 'result_cache'
    id = Column(Integer, primary_key=True)
    competition_id = Column(Integer)
    club_id = Column(Integer)
    win = Column(Integer)
    loss = Column(Integer)
    draw = Column(Integer)
    points = Column(Integer)
    goals_against = Column(Integer)
    goals_for = Column(Integer)
    goal_difference = Column(Integer)
    updated_at = Column(TIMESTAMP)

    def __init__(self, club_id, competition_id):
        self.club_id = club_id
        self.competition_id = competition_id

    def __repr__(self):
        return '<ResultCache comp_id:{} club_id:{}, w:{}, l:{}, d:{}, points:{}>'.format(
                self.competition_id,
                self.club_id, 
                self.win, 
                self.loss,
                self.draw,
                self.points
            )

  