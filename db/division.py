from sqlalchemy import Column, Integer, String, TIMESTAMP
import datetime
from utils.dbutils import get_base
import uuid

Base = get_base()

class Division(Base):
    __tablename__ = 'division'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    location = Column(String(100))
    description = Column(String(250))
    league_id = Column(Integer)
    founded = Column(TIMESTAMP)
    display_competition_id = Column(Integer)

    def __init__(self, name, league):
        self.name = name
        self.league_id = league
        
    def __repr__(self):
        return '<Division {}, {}>'.format(self.name, self.location)

  