import random
import time 

from db.player import Player
from db.club import Club
from db.match import Match
from db.event import Event

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
            match.played = datetime.datetime.strptime(match.played, '%m/%d/%Y %I:%M %p')
            # print(type(match.played))
            match.competition_id = competition_id
            print(match)
            session.add(match)
            session.commit()
            # Now create some events for that match
            #   1 | Goal        |
            #   2 | Yellow Card |
            #   3 | Red Card    |
            #   4 | Kick-off    |
            #   5 | Corner      |
            #   6 | Throw-In    |
            #   7 | Penalty     |
            #   8 | Foul        |
            #   9 | Full-time        |
            kick_off = Event(4, None, match.id)
            kick_off.occurred_at = match.played

            full_time = Event(9, None, match.id)
            # 90 min game plus 10 min half time
            full_time.occurred_at = match.played + datetime.timedelta(minutes=100)
            session.add(kick_off)
            session.add(full_time) 

            goals = random.randint(1, 10)
            timeingame = 0
            # Randomly generate 
            if random.randint(0, 2) > 1:                
                for g in range(0, goals):
                    timeingame += random.randint(5,10)
                    players = session.query(Player).filter_by(club_id=home_club.id).all()
                    players.extend(session.query(Player).filter_by(club_id=away_club.id).all())
                    player = random.choice(players)

                    goal = Event(1, player.id, match.id)
                    goal.occurred_at = match.played + datetime.timedelta(minutes=timeingame)
                    print(goal) 
                    session.add(goal)
            
            session.commit()
 