from sqlalchemy import Column, Integer, String, TIMESTAMP
import datetime
from utils.dbutils import get_base
import uuid

Base = get_base()

class League(Base):
    __tablename__ = 'league'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    location = Column(String(100))
    description = Column(String(250))
    founded = Column(TIMESTAMP)

    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return '<League {}, {}>'.format(self.name, self.location)

  