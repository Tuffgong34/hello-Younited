from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
import datetime
from utils.dbutils import get_base
import uuid

Base = get_base()

class Club(Base):
    __tablename__ = 'club'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    founded = Column(Date)
    information = Column(String)
    contact = Column(String)
    location = Column(String)
    division_id = Column(Integer)    
    created_at = Column(TIMESTAMP)
    home_shirt_id = Column(Integer)
    away_shirt_id = Column(Integer)
    goalkeeper_shirt_id = Column(Integer)
    logo_filename = Column(String)

    def __init__(self, name, divison_id):
        self.name = name
        self.division_id = divison_id
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<Club {} {}, {}>'.format(self.name, self.information, self.id)

  