import csv
import sqlite3

def main():

    conn = sqlite3.connect('./../db/nba-elo-db.db')
    cur = conn.cursor()

    with open('nba-data-historical.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        line_num = 0
        for row in reader:
            if line_num != 0 and row[2] == "2020":

                name = row[1]
                team = row[5]
                position = row[6]
                rap_war = row[22]

                cur.execute('''INSERT OR IGNORE INTO "players" ("name", "team", "position", "raptor_war") VALUES (?, ?, ?, ?)''', [name, team, position, rap_war])
                conn.commit()


            line_num += 1

    conn.close()

main()