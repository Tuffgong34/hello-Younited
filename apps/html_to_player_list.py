import os
import sys
directory = "./data/wearside_league/players"
with open("wearside_players_output.csv", 'w+') as op:
    op.write("firstname, lastname, club,\n")
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            fn = os.path.join(directory, filename)
            with open(fn, 'r') as f:
                content = f.read()
                # content.replace("&gt;", "")
                offset = 0
                start = 1
                end = 0
                print(fn)
                while start != 0:
                
                    try:
                        start = content.find('lblSurname</span>"&gt;</span>', offset)
                        start += len('lblSurname</span>"&gt;</span>')
                        end = content.find("<", start)
                        last_name = content[start:end].capitalize()
            
                        start = content.find('lblFirstname</span>"&gt;</span>', offset)
                        start += len('lblFirstname</span>"&gt;</span>')
                        end = content.find("<", start)
                        first_name = content[start:end].capitalize()
                        first_out = first_name.split(" ")
                        first_name = ""
                        for fir in first_out:
                            first_name += fir.capitalize() + " "

                        first_name = first_name.strip()
                        
                        start = content.find('lblCurrentClub</span>"&gt;</span>', offset)
                        start += len('lblCurrentClub</span>"&gt;</span>')
                        end = content.find("<", start)
                        team_name = content[start:end]
                        if end < offset:
                            break
                        offset = end + 1
            
                        op.write("{},{},{},\n".format(first_name, last_name, team_name))
                        print("[FOUND]: {} {} - {}".format(first_name, last_name, team_name))
                    except Exception as e:
                        print("\nError occurred {}".format(e))
                        start = 0
                        
                        break
            # print(fn)