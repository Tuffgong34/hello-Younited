from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
import datetime
from utils.dbutils import get_base
import uuid

Base = get_base()

class EventType(Base):
    __tablename__ = 'event_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<EventType {} - {}, Description: "{}">'.format(self.id, self.name, self.description)
