from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
import datetime
from utils.dbutils import get_base
import uuid

Base = get_base()

class Position(Base):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    description = Column(String)
    created_at = Column(TIMESTAMP)

    def __init__(self, name):
        self.club_id = club_id
        self.last_name = last_name
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<Position {}: {}, {}>'.format(self.name, self.description, self.created_at)

  