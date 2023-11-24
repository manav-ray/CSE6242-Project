from db import DatabaseConnection


class Tables:

    def __init__(self, connection):
        self.db = DatabaseConnection(connection)

    def displayBestMatchups(self):
        bestMatchups = self.db.getBestMatchups()
        print(bestMatchups)
    