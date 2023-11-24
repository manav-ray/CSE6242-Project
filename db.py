class DatabaseConnection:

    def __init__(self, connection):
        self.connection = connection


    def getAllGames(self):
        query = "SELECT * FROM games"
        cursor = self.connection.execute(query)
        return cursor.fetchall()

    
    def getAllTeams(self):
        query = "SELECT team FROM elo"
        cursor = self.connection.execute(query)

        teams = set()
        for i in cursor.fetchall():
            teams.add(i[0])
        
        return list(teams)


    def getAllEloData(self):
        query = "SELECT * FROM elo"
        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def getEloByTeam(self, team):
        query = "SELECT * FROM elo WHERE team = '" + team + "' ORDER BY date"
        cursor = self.connection.execute(query)
        return cursor.fetchall()
    
    def getFirstAndFinalEloByTeam(self, team):
        query = "SELECT * FROM (SELECT * FROM elo WHERE team = '" + team + "' ORDER BY date LIMIT 1) AS first UNION SELECT * FROM (SELECT * FROM elo WHERE team = '" + team + "' ORDER BY date DESC LIMIT 1) AS last"
        cursor = self.connection.execute(query)
        return cursor.fetchall()


    def getBestMatchups(self):
        teams = self.getAllTeams()
        matchups = []
        for i in range(len(teams)):
            for j in range(i+1, len(teams)):
                matchups.append([teams[i], teams[j], 0])
        
        for i in matchups:
            team_1_elo = self.getFirstAndFinalEloByTeam(i[0])[1]
            team_2_elo = self.getFirstAndFinalEloByTeam(i[1])[1]

            i[2] = abs(team_1_elo[1] - team_2_elo[1])
        

        return sorted(matchups, key=lambda x: x[2], reverse=False)