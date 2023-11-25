from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from sqlite3 import Error


# -------------- Rest API and DB Config ---------------
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_connection():
    path = "./db/nba-elo-db.db"
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
        connection.text_factory = str
        return connection
    except Error as e:
        print("Error occurred: " + str(e))
# -----------------------------------------------------

@app.get('/all-games')
def getAllGames():
    connection = create_connection()
    query = "SELECT * FROM games ORDER BY date"
    cursor = connection.execute(query)
    res = []
    for elem in cursor.fetchall():
        game = {
            "homeTeam": elem[0],
            "awayTeam": elem[1],
            "playoff": elem[2],
            "homeScore": elem[3],
            "awayScore": elem[4],
            "date": elem[5]
        }

        res.append(game)

    connection.close()
    return res




@app.get('/all-teams')
def getAllTeams():
    connection = create_connection()
    query = "SELECT team FROM elo"
    cursor = connection.execute(query)

    teams = set()
    for i in cursor.fetchall():
        teams.add(i[0])
    
    connection.close()
    return {"teams": list(teams)}



@app.get('/elo/{team}')
def getEloByTeam(team):
    connection = create_connection()
    query = "SELECT * FROM elo WHERE team = '" + team + "' ORDER BY date"
    cursor = connection.execute(query)
    res = []
    for elem in cursor.fetchall():
        elo = {
            "team": elem[0],
            "curr_elo": elem[1],
            "date": elem[2]
        }

        res.append(elo)

    connection.close()
    return res


@app.get('/elo-progression/')
def getFirstAndFinalEloByTeam():
    connection = create_connection()
    allTeams = getAllTeams()['teams']
    res = []
    for team in allTeams:
        query = "SELECT * FROM (SELECT * FROM elo WHERE team = '" + team + "' ORDER BY date LIMIT 1) AS first UNION SELECT * FROM (SELECT * FROM elo WHERE team = '" + team + "' ORDER BY date DESC LIMIT 1) AS last"
        cursor = connection.execute(query)

        queryResult = cursor.fetchall()
        if (queryResult[0][2] < queryResult[1][2]):
            elo = {
                "team": queryResult[0][0],
                "preElo": queryResult[0][1],
                "postElo": queryResult[1][1]
            }
        else:
            elo = {
                "team": queryResult[0][0],
                "preElo": queryResult[1][1],
                "postElo": queryResult[0][1]                
            }

        res.append(elo)

    connection.close()
    return res


@app.get('/all-players')
def getAllPlayersSorted():
    connection = create_connection()
    query = "SELECT * FROM players ORDER BY raptor_war DESC"
    cursor = connection.execute(query)
    res = []
    for elem in cursor.fetchall():
        if (elem[3] != ""):
            game = {
                "name": elem[0],
                "team": elem[1],
                "position": elem[2],
                "raptor_war": elem[3]
            }

            res.append(game)

    connection.close()
    return res


@app.get('/best-matchups')
def getBestMatchups():
    connection = create_connection()
    teams = getAllTeams()["teams"]
    matchups = []
    for i in range(len(teams)):
        for j in range(i+1, len(teams)):
            matchups.append([teams[i], teams[j], 0])
    
    for i in matchups:

        query1 = "SELECT elo FROM elo WHERE team = '" + i[0] + "' ORDER BY date DESC LIMIT 1"
        query2 = "SELECT elo FROM elo WHERE team = '" + i[1] + "' ORDER BY date DESC LIMIT 1"

        cursor = connection.execute(query1)
        team_1_elo = cursor.fetchall()[0][0]

        cursor = connection.execute(query2)
        team_2_elo = cursor.fetchall()[0][0]

        i[2] = abs(team_1_elo - team_2_elo)
    

    sortedList = sorted(matchups, key=lambda x: x[2], reverse=False)
    res = []
    for elem in sortedList:
        diff = {
            "team1": elem[0],
            "team2": elem[1],
            "elo_difference": elem[2]
        }

        res.append(diff)

    connection.close()
    return res