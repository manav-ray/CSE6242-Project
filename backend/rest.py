from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from sqlite3 import Error
import numpy as np
from sklearn.linear_model import LinearRegression


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
    query = "SELECT games.*, e1.elo, e2.elo FROM games INNER JOIN elo as e1 on (games.date = e1.date AND games.team_1 = e1.team) INNER JOIN elo as e2 on (games.date = e2.date AND games.team_2 = e2.team) ORDER BY games.date"
    cursor = connection.execute(query)
    res = []
    for elem in cursor.fetchall():
        game = {
            "homeTeam": elem[0],
            "awayTeam": elem[1],
            "homeScore": elem[3],
            "awayScore": elem[4],
            "date": elem[5],
            "homeElo": round(elem[6], 2),
            "awayElo": round(elem[7], 2)
        }

        res.append(game)

    connection.close()
    return res


@app.get("/predict")
def predictTradeEffect():
    tradeEffects = tradeEffect()
    players = getAllPlayersSorted()

    his_war = []
    his_elo = []
    for t in tradeEffects:
        player = t["player"]
        war = 0
        for p in players:
            if p["name"] == player:
                war = p["raptor_war"]
                
        
        if war != 0:
           his_war.append(war)
           his_elo.append(t["new_difference"])
        
    war_train = np.array(his_war).reshape(-1, 1)
    elo_train = np.array(his_elo)

    reg = LinearRegression().fit(war_train, elo_train)

    res = []

    for p in players:
        temp = [p["raptor_war"]]
        test = np.array(temp).reshape(-1, 1)

        elem = {
            "player": p["name"],
            "position": p["position"],
            "prediction": round(reg.predict(test)[0], 2)
        }


        res.append(elem)


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

@app.get('/elo-home-vs-away/{team}')
def getEloByTeamHomeVsAway(team):
    connection = create_connection()
    query = "SELECT elo.*, games.* FROM elo INNER JOIN games ON ((elo.team = games.team_1 OR elo.team = games.team_2) AND elo.date = games.date) WHERE team = '" + team + "' ORDER BY date"
    cursor = connection.execute(query)
    res = []
    for elem in cursor.fetchall():
        if team == elem[3]:
            elo = {
                "team": elem[0],
                "home_curr_elo": elem[1],
                "date": elem[2]
            }
        else:
            elo = {
                "team": elem[0],
                "away_curr_elo": elem[1],
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


@app.get('/trade-effect')
def tradeEffect():
    connection = create_connection()
    query = "SELECT * FROM trades"
    cursor = connection.execute(query)

    allEloDifferences = getFirstAndFinalEloByTeam()
    res = []

    for elem in cursor.fetchall():
        name = elem[0]
        old = elem[1]
        new = elem[2]

        if old == "CHA" or new == "CHA":
            continue
        

        effect = {
            "player": name,
            "old_team": old,
            "new_team": new
        }

        for d in allEloDifferences:
            if (d['team'] == old):
                effect['old_team_pre'] = d['preElo']
                effect['old_team_post'] = d['postElo']

            elif (d['team'] == new):
                effect['new_team_pre'] = d['preElo']
                effect['new_team_post'] = d['postElo']
            
        effect['new_difference'] = round(effect['new_team_post'] - effect['new_team_pre'], 3)
        effect['old_difference'] = round(effect['old_team_post'] - effect['old_team_pre'], 3)    
        res.append(effect)

    connection.close()
    return res

@app.get('/elo-margin-of-victory/{team}')
def getEloByMarginOfVictory(team):
    connection = create_connection()
    query = "SELECT elo.*, games.* FROM elo INNER JOIN games ON ((elo.team = games.team_1 OR elo.team = games.team_2) AND elo.date = games.date) WHERE team = '" + team + "' ORDER BY date"
    cursor = connection.execute(query)
    res = []

    i = 1

    data = cursor.fetchall()

    for elem in data:
        if team == elem[3]:
            score_diff = elem[6] - elem[7]
        else:
            score_diff = elem[7] - elem[6]

        if i == len(data):
            if score_diff > 0:
                elo_diff = 10
            else:
                elo_diff = -10
        else:
            elo_diff = data[i][1] - data[i-1][1]
        
        i += 1

        elo = {
            "team": elem[0],
            "curr_elo": elo_diff,
            "score_diff": score_diff,
            "date": elem[2]
        }

        res.append(elo)

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