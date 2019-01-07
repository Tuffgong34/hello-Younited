from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
import datetime
from utils.dbutils import get_base
import uuid

Base = get_base()

class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), unique=False)
    last_name = Column(String(100), unique=False)
    shirt_number = Column(Integer)
    date_of_birth = Column(Date)
    height_cm = Column(Integer)
    club_id = Column(Integer)    
    position_id = Column(Integer)
    profile_filename = Column(String(200))
    yn_user_id = Column(Integer)
    created_at = Column(TIMESTAMP)

    def __init__(self, last_name, club_id):
        self.club_id = club_id
        self.last_name = last_name
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<Player {} {}, {}>'.format(self.first_name, self.last_name, self.shirt_number)

  