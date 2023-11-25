import csv
import sqlite3

def main():

    conn = sqlite3.connect('./../db/nba-elo-db.db')
    cur = conn.cursor()

    with open('nba-data-historical.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        line_num = 0
        player_dict = {}
        for row in reader:
            if line_num != 0 and (row[2] == "2020" or row[2] == "2019"):
                name = row[1]
                if (name in player_dict):
                    player_dict[name].append(row)
                else:
                    player_dict[name] = [row]

            line_num += 1
               
        for player in player_dict:
            if (len(player_dict[player]) != 2):
                continue
                
            if (player_dict[player][0][5] != player_dict[player][1][5]):
                if player_dict[player][0][2] == "2019":
                    oldTeam = player_dict[player][0][5]
                    newTeam = player_dict[player][1][5]
                else:
                    oldTeam = player_dict[player][1][5]
                    newTeam = player_dict[player][0][5]

                cur.execute('''INSERT OR IGNORE INTO "trades" ("player", "old_team", "new_team") VALUES (?, ?, ?)''', [player, oldTeam, newTeam])
                conn.commit()



    conn.close()

main()