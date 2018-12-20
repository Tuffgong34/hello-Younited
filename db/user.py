from sqlalchemy import Column, Integer, String
from utils.dbutils import get_base
import uuid

Base = get_base()

class User(Base):
    __tablename__ = 'yn_user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), unique=False)
    last_name = Column(String(100), unique=False)
    email = Column(String(200))
    phone_number = Column(String(24))
    password = Column(String(60))
    salt = Column(String(32))    
    confirmed = Column(Integer)
    confirmation_id = Column(String(32))
    status = Column(String(10))

    def __init__(self, first_name, last_name, phone_number=None, email=None, password=None, salt=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.salt = salt


    def __repr__(self):
        return '<User {}, {}>'.format(self.name, self.email)

  