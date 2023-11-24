from fastapi import FastAPI
import sqlite3
from sqlite3 import Error
import json


app = FastAPI()

path = "./db/nba-elo-db.db"
try:
    connection = sqlite3.connect(path, check_same_thread=False)
    connection.text_factory = str
except Error as e:
    print("Error occurred: " + str(e))

@app.get('/all-games')
def getAllGames():
    query = "SELECT * FROM games"
    cursor = connection.execute(query)
    data = cursor.fetchall()
    return json.dumps(data)


def getAllTeams():
    query = "SELECT team FROM elo"
    cursor = connection.execute(query)

    teams = set()
    for i in cursor.fetchall():
        teams.add(i[0])
    
    return list(teams)


def getAllEloData():
    query = "SELECT * FROM elo"
    cursor = connection.execute(query)
    return cursor.fetchall()

def getEloByTeam(team):
    query = "SELECT * FROM elo WHERE team = '" + team + "' ORDER BY date"
    cursor = connection.execute(query)
    return cursor.fetchall()

def getFirstAndFinalEloByTeam(team):
    query = "SELECT * FROM (SELECT * FROM elo WHERE team = '" + team + "' ORDER BY date LIMIT 1) AS first UNION SELECT * FROM (SELECT * FROM elo WHERE team = '" + team + "' ORDER BY date DESC LIMIT 1) AS last"
    cursor = connection.execute(query)
    return cursor.fetchall()


def getBestMatchups():
    teams = getAllTeams()
    matchups = []
    for i in range(len(teams)):
        for j in range(i+1, len(teams)):
            matchups.append([teams[i], teams[j], 0])
    
    for i in matchups:
        team_1_elo = getFirstAndFinalEloByTeam(i[0])[1]
        team_2_elo = getFirstAndFinalEloByTeam(i[1])[1]

        i[2] = abs(team_1_elo[1] - team_2_elo[1])
    

    return sorted(matchups, key=lambda x: x[2], reverse=False)