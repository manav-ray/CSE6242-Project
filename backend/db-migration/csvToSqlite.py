import csv
from datetime import datetime
import sqlite3

def main():

    conn = sqlite3.connect('./../db/nba-elo-db.db')
    cur = conn.cursor()

    with open('nba_elo_latest.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        line_num = 0
        for row in reader:
            if line_num != 0:
                date = row[0]
                playoff = row[3]
                team1 = row[4]
                team2 = row[5]
                team_1_elo_pre = row[6]
                team_2_elo_pre = row[7]
                team_1_score = row[22]
                team_2_score = row[23]

                date = datetime.strptime(date, '%Y-%m-%d').date()

                cur.execute('''INSERT OR IGNORE INTO "games" ("team_1", "team_2", "playoff", "team_1_score", "team_2_score", "date") VALUES (?, ?, ?, ?, ?, ?)''', [team1, team2, playoff, team_1_score, team_2_score, date])
                conn.commit()

                cur.execute('''INSERT OR IGNORE INTO "elo" ("team", "elo", "date") VALUES (?, ?, ?)''', [team1, team_1_elo_pre, date])
                conn.commit()
                
                cur.execute('''INSERT OR IGNORE INTO "elo" ("team", "elo", "date") VALUES (?, ?, ?)''', [team2, team_2_elo_pre, date])
                conn.commit()

            line_num += 1


main()