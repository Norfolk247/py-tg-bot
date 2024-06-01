from time import time


def checkIfUserExists(connection, userId):
    cursor = connection.cursor()
    cursor.execute('SELECT 1 FROM userdata WHERE userid = %s', (userId,))
    return False if cursor.fetchone() is None else True


def getUser(connection, userId):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM userdata
        WHERE userid = %s;
    """, (userId,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("""
            INSERT INTO userdata (userid, level, hash, egp, current_clicks, maximum_clicks)
            VALUES (%s, 1, 0, 0, 0, 100);
        """, (userId,))
        connection.commit()
        cursor.execute("""
                SELECT * FROM userdata
                WHERE userid = %s;
            """, (userId,))
        result = cursor.fetchone()
    userId, level, userHash, egp, currentClicks, maximumClicks, update = result
    if update is None or update + 24 * 60 * 60 > round(time()):
        return result
    cursor.execute('UPDATE userdata SET current_clicks = 0, update = NULL WHERE userid = %s', (userId,))
    connection.commit()
    return userId, level, userHash, egp, 0, maximumClicks, None


def editUser(connection, userId, levelDiff=0, userHashDiff=0, currentClicksDiff=0, egpDiff=0, update=None):
    cursor = connection.cursor()
    if update is None:
        cursor.execute("""
                    UPDATE userdata
                    SET level = level + %s, hash = hash + %s, current_clicks = current_clicks + %s, egp = egp + %s
                    WHERE userid = %s;
                """, (levelDiff, userHashDiff, currentClicksDiff, egpDiff, userId))
        connection.commit()
        return getUser(connection, userId)
    cursor.execute("""
            UPDATE userdata
            SET level = level + %s, hash = hash + %s, current_clicks = current_clicks + %s, update = %s, egp = egp + %s
            WHERE userid = %s;
        """, (levelDiff, userHashDiff, currentClicksDiff, update, egpDiff, userId))
    connection.commit()
    return getUser(connection, userId)


def userPlaceByHash(connection, userId):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT COUNT (1) FROM (
        SELECT hash FROM userdata WHERE hash >= (
        SELECT hash FROM userdata WHERE userid = %s
        ));
        ''', (userId,))
    return cursor.fetchone()[0]
