import random
import time 

from db.player import Player
from db.club import Club
from db.match import Match

import datetime

from utils.dbutils import get_db_session

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)

# print randomDate("1/1/2008 1:30 PM", "1/1/2009 4:50 AM", random.random())

session = get_db_session()
clubs = session.query(Club).filter_by(division_id=2).order_by(Club.id)
competition_id = 2
for home_club in clubs:
    for away_club in clubs:
        if home_club.id != away_club.id:
            # Create a match plus events
            match = Match(home_club.id, away_club.id)
            match.played = randomDate("1/9/2018 1:30 PM", "1/3/2019 4:50 AM", random.random())
            match.competition_id = competition_id
            print(match)

            # Now create some events for that match


# Loop through each club and make sure they play a game 