from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
import datetime
from utils.dbutils import get_base
import uuid

Base = get_base()

class Shirt(Base):
    __tablename__ = 'shirt'
    id = Column(Integer, primary_key=True)
    # style := solid, solid_arms, stripes, hoops
    style = Column(String(40))
    primary_color = Column(String(40))
    secondary_color = Column(String(40))
    
    def __init__(self, style, primary):
        allowed_styles = ['solid', 'solid_arm', 'stripes', 'hoops']
        if style not in allowed_styles:
            print("ERROR: Unknown style {}".format(style))

        self.style = style
        self.primary_color = primary

    def __repr__(self):
        return '<Shirt {}: {}, {}>'.format(self.style, self.primary_color, self.secondary_color)

  