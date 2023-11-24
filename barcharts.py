from db import DatabaseConnection


class BarCharts:

    def __init__(self, connection):
        self.db = DatabaseConnection(connection)

    def displayPreAndPostSeasonEloComparison(self):
        allTeams = self.db.getAllTeams()
        for team in allTeams:
            print(self.db.getFirstAndFinalEloByTeam(team))