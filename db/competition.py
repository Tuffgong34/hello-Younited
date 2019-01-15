from sqlalchemy import Column, Integer, String, TIMESTAMP, Date
import datetime
from utils.dbutils import get_base
import uuid

Base = get_base()

class Competition(Base):
    __tablename__ = 'competition'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return '<Competition {}, start:{} end:{}>'.format(self.name, self.start_date, self.end_date)
  