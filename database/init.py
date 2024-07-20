from psycopg2 import connect
from database.userController import userController


class databaseConnection:
    def __init__(self, user, password, host, databaseName, port=5432):
        self._connection = connect(
            user=user,
            password=password,
            host=host,
            database=databaseName,
            port=port
        )
        self._createTablesIfNotExist()
        self.userController = userController(self._connection)
        print('connection with db established')

    def _createTablesIfNotExist(self):
        try:
            cursor = self._connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS userdata (
                    userid BIGINT PRIMARY KEY,
                    level INTEGER NOT NULL,
                    hash INTEGER NOT NULL,
                    egp INTEGER NOT NULL,
                    current_clicks INTEGER NOT NULL,
                    maximum_clicks INTEGER NOT NULL,
                    update INTEGER
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS referrals (
                    userid BIGINT PRIMARY KEY,
                    referral VARCHAR(12) UNIQUE,
                    joined BOOLEAN DEFAULT FALSE
                );
            """)
            self._connection.commit()
            cursor.close()
        except Exception as e:
            print(e)
