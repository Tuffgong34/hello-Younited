import random
from db.player import Player
from db.club import Club
import datetime

from utils.dbutils import get_db_session

first_name = [
    'Paul', 'Phil', 'Peter', 'Saul', 'Harrison', 'Doug', 'Ted', 'Robin', 'Robert', 
    'Todd', 'Thomas', 'Rob', 'Matt', 'Matthew', 'Simon', 'Christopher', 'Seb', 'Simian',
    'Loz', 'Lawrence', 'Sid', 'Ryan', 'Tom', 'Brad', 'George', 'William', 'Will'
    ]
last_name = [
    'Barrington', 'Snozzface', 'Tocksy', 'Flibblepip', 'Snook', 'Toxi', 'Bradlington', 'Smitherine',
    'Brilton', 'Tocksington', 'Plinker', 'Bomble', 'Waffer', 'Spoonface', 'Berker', 'Spoffy', 'Donker',
    'Mokser', 'Brimp', 'Flox', 'Clank', 'Spankyspanks', 'Barely-Warner', 'Sponky-Plonk II', 'Drong', 
    'Dinkle', 'Spratly'
]

# print(len(first_name))
session = get_db_session()
division_id = 2

# Create clubs
ids = []
for i in range(0,14):
    next_club = Club('Team {}'.format(i), 2)
    next_club.information = "Number {} of Penguins".format(i)
    next_club.home_shirt_id = random.randint(1,12)
    next_club.away_shirt_id = random.randint(1,12)
    next_club.founded = datetime.datetime.now()
    session.add(next_club)
    session.commit()
    ids.append(next_club.id)

for fn in first_name:
    for ln in last_name:
        next_player = Player(ln, random.randint(1,12))
        next_player.first_name = fn
        next_player.club_id = random.choice(ids)
        next_player.shirt_number = random.randint(1, 100)
        print(next_player)
        session.add(next_player)
        session.commit()