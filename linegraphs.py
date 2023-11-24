from db import DatabaseConnection


class LineGraph:

    def __init__(self, connection):
        self.db = DatabaseConnection(connection)

    def displayEloProgressionByTeam(self, team):
        print(self.db.getEloByTeam(team))
    