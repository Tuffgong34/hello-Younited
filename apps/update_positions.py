from utils.dbutils import get_db_session
from db.player import Player
from db.club import Club
import sys
session = get_db_session()

players = session.query(Player).all()
content = ""
with open('wearside_defenders.csv', 'r') as f:
    content = f.read()

content = content.split('\n')
for item in content:
    # print(item)
    item = item.split(' ')
    surname = item[1]
    firstname = item[0]
    # print(surname)
    found_item = False 
    for p in players:
        if p.last_name.lower()==surname.lower() and p.first_name.lower() == firstname.lower():
            p.position_id = 17
            session.add(p)
            print("Updating {}".format(p.id))
            session.commit()
            found_item = True

    if found_item is False:
        print("ERROR: Not found {}. {}".format(surname, firstname))

with open('wearside_midfielders.csv', 'r') as f:
    content = f.read()

content = content.split('\n')
for item in content:
    # print(item)
    item = item.split(' ')
    surname = item[1]
    firstname = item[0]
    # print(surname)
    found_item = False 
    for p in players:
        if p.last_name.lower()==surname.lower() and p.first_name.lower() == firstname.lower():
            p.position_id = 18
            session.add(p)
            print("Updating {}".format(p.id))
            session.commit()
            found_item = True

    if found_item is False:
        print("ERROR: Not found {}. {}".format(surname, firstname))

with open('wearside_forwards.csv', 'r') as f:
    content = f.read()

content = content.split('\n')
for item in content:
    # print(item)
    item = item.split(' ')
    surname = item[1]
    firstname = item[0]
    # print(surname)
    found_item = False 
    for p in players:
        if p.last_name.lower()==surname.lower() and p.first_name.lower() == firstname.lower():
            p.position_id = 16
            session.add(p)
            print("Updating {}".format(p.id))
            session.commit()
            found_item = True

    if found_item is False:
        print("ERROR: Not found {}. {}".format(surname, firstname))