from utils.dbutils import get_db_session
from db.club import Club

# TODO: Must set the division id for the teams
# division_id = 4
session = get_db_session()

with open('league.csv') as f:
    content = f.read()
    content = content.split('\n')
    content = content[1:]
    for line in content:
        # print(line)
        if line.strip() != "":
            team_name = line.split(',')[1]
            club = Club(team_name, division_id)
            session.add(club)
            session.commit()
            print("[ADDED]: " + team_name)
            
    