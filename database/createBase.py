def createTable(connection):
    try:
        cursor = connection.cursor()
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
                referral VARCHAR(12) UNIQUE
            );
        """)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(e)
