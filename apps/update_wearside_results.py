from db.club import Club
from db.result_cache import ResultCache
import sys
from utils.dbutils import get_db_session

content = ""
with open('wearside_current_division_standing.csv', 'r') as f:
    content = f.read()

content = content.split('\n')
headers = content[0]

# headers = headers.split(',')
# for i, header in enumerate(headers):
#     print("{} : {}".format(i, header))

# sys.exit()
# 0 : Pos
# 1 : Club
# 2 : P
# 3 : W
# 4 : D
# 5 : L
# 6 : F
# 7 : A
# 8 : GD
# 9 : PT
# 10 : PA
# 11 : AP
session = get_db_session()
clubs = session.query(Club).all()

for line in content[1:]:
    items = line.split(',')
    club = items[1]#find club from name 
    bfound = False
    club_id = None
    for c in clubs:
        if c.name.lower().strip() == club.lower().strip():
            bfound = True
            club_id = c.id
    if bfound is True and club_id is not None:
        print("Found {}".format(club))
        rc = session.query(ResultCache).filter_by(club_id=club_id).filter_by(competition_id=2).first()
        if rc is None:
            rc = ResultCache(club_id, 2)
        rc.points = items[9]
        rc.win = items[3]
        rc.draw = items[4]
        rc.loss = items[5]
        rc.goals_for = items[6]
        rc.goals_against = items[7]
        rc.goal_difference = items[8]
        print(rc)
        session.add(rc)
        session.commit()
    else:
        print("Not Found {}".format(club))
    # print(club)