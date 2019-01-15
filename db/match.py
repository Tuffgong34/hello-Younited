from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
import datetime
from utils.dbutils import get_base
import uuid

Base = get_base()

class Match(Base):
    __tablename__ = 'match'
    id = Column(Integer, primary_key=True)
    home_club_id = Column(Integer)
    away_club_id = Column(Integer)
    played = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP) 

    def __init__(self, home_club_id, away_club_id):
        self.home_club_id = home_club_id
        self.away_club_id = away_club_id

    def __repr__(self):
        return '<Match {} vs {} at {}>'.format(self.home_club_id, self.away_club_id, self.shirt_number)

  