from db import DatabaseConnection
import sqlite3
from sqlite3 import Error


class BarCharts:

    def __init__(self, connection):
        self.db = DatabaseConnection(connection)

    def displayAllGames(self):
        print(self.db.getAllGames())

    def displayEloProgressionByTeam(self, team):
        print(self.db.getEloByTeam(team))

    def displayPreAndPostSeasonEloComparison(self):
        allTeams = self.db.getAllTeams()
        for team in allTeams:
            print(self.db.getFirstAndFinalEloByTeam(team))
    