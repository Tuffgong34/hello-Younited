from utils.dbutils import get_db_session
from db.player import Player
from db.club import Club

# TODO: Must set the division id for the teams
# division_id = 4
session = get_db_session()
err = open('error_wearside.csv', 'w+')
err.write('first_name,last_name,team_name\n')
with open('wearside_players_output.csv') as f:
    content = f.read()
    content = content.split('\n')
    content = content[1:]
    
    all_clubs = session.query(Club).all()
    
    for line in content:
        if line.strip() == "":
            continue

        # print(line)
        line = line.split(',')
        first_name = line[0]
        last_name = line[1]
        team_name = line[2]
        # print(first_name)
        # print(last_name)
        # print(team_name)

        club_id = None
        for club in all_clubs:        
            if club.name.lower() == team_name.lower():
                # print("Found club")
                club_id = club.id
    
        if club_id is not None:
            player = Player(last_name, club_id)
            player.first_name = first_name
            session.add(player)
            session.commit()
            print("[ADDED]: {} {}   -  {}".format(first_name, last_name, team_name))
        
        else:
            err.write("{},{},{}\n".format(first_name, last_name, team_name))
            print("ERROR {} is unknown".format(team_name))
err.close()

    # content = f.read()
    # content = content.split('\n')
    # content = content[1:]
    # for line in content:
    #     # print(line)
    #     if line.strip() != "":
    #         player_name = line.split(',')[1]
    #         player_name = player_name.split(' ')
    #         first_name = player_name[0].capitalize()
    #         if first_name.find('-') != -1:
    #             ind = first_name.index('-')
    #             fn_tmp = first_name[:ind]
    #             fn_tmp += "-"
    #             fn_tmp += first_name[ind+1:].capitalize()
    #             first_name = fn_tmp
    #             print(first_name)

    #         last_name = ""
    #         for item in player_name[1:]:
    #             last_name += item.capitalize() + " "
    #         last_name = last_name.strip()

    #         team_name = line.split(',')[2]
    #         team_name = team_name.replace("&amp;", "&")

    #         all_clubs = session.query(Club).all()
    #         club_id = None
    #         for club in all_clubs:        
    #             if club.name.lower() == team_name.lower():
    #                 # print("Found club")
    #                 club_id = club.id
    #         if club_id is not None:
    #             player = Player(last_name, club_id)
    #             player.first_name = first_name
    #             session.add(player)
    #             session.commit()
    #             print("[ADDED]: {} {}   -  {}".format(first_name, last_name, team_name))
            
    #         else:
    #             print("ERROR {} is unknown".format(team_name))
    #         # club = Club(team_name, division_id)
    #         # session.add(club)
    #         # session.commit()
    #         # print("[ADDED]: {} {}   -  {}".format(first_name, last_name, team_name))
            
    