import random
import time 

from db.event_type import EventType

import datetime

from utils.dbutils import get_db_session

list_events = ["Goal", "Yellow Card", "Red Card", "Kick-off", "Corner", "Throw-In", "Penalty", "Foul", "Full-time"]
session = get_db_session()

for l in list_events:
    next_event = EventType(l)
    session.add(next_event)
    session.commit()