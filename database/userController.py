import string
import random
from time import time
from configparser import ConfigParser

config = ConfigParser()
config.read('bot/config/config.ini')
botInviteUrl = config.get('urls', 'botInviteUrl')


def generate_random_string():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))


class userController:
    def __init__(self, databaseConnection):
        self._connection = databaseConnection

    def createNewUser(self, userId, referral):
        cursor = self._connection.cursor()
        cursor.execute('SELECT 1 FROM referrals WHERE userid = %s;', (userId,))
        result = cursor.fetchone()
        if result:
            return
        cursor.execute('INSERT INTO referrals (userid) VALUES (%s);', (userId,))
        self.getUser(userId)
        referral = referral.split(' ')[1] if len(referral.split(' ')) > 1 else None
        if referral is None:
            self._connection.commit()
            return
        cursor.execute('SELECT userid FROM referrals WHERE referral = %s;', (referral,))
        inviterId = cursor.fetchone()
        if not inviterId is None:
            self.editUser(inviterId[0], egpDiff=1200)
            self._connection.commit()

    def getUser(self, userId):
        cursor = self._connection.cursor()
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
            self._connection.commit()
            cursor.execute("""
                        SELECT * FROM userdata
                        WHERE userid = %s;
                    """, (userId,))
            result = cursor.fetchone()
        userId, level, userHash, egp, currentClicks, maximumClicks, update = result
        if update is None or update + 24 * 60 * 60 > round(time()):
            return result
        cursor.execute('UPDATE userdata SET current_clicks = 0, update = NULL WHERE userid = %s', (userId,))
        self._connection.commit()
        return userId, level, userHash, egp, 0, maximumClicks, None

    def editUser(self, userId, levelDiff=0, userHashDiff=0, currentClicksDiff=0, egpDiff=0, update=None):
        cursor = self._connection.cursor()
        if update is None:
            cursor.execute("""
                            UPDATE userdata
                            SET level = level + %s, hash = hash + %s, current_clicks = current_clicks + %s, egp = egp + %s
                            WHERE userid = %s;
                        """, (levelDiff, userHashDiff, currentClicksDiff, egpDiff, userId))
            self._connection.commit()
            return self.getUser(userId)
        cursor.execute("""
                    UPDATE userdata
                    SET level = level + %s, hash = hash + %s, current_clicks = current_clicks + %s, update = %s, egp = egp + %s
                    WHERE userid = %s;
                """, (levelDiff, userHashDiff, currentClicksDiff, update, egpDiff, userId))
        self._connection.commit()
        return self.getUser(userId)

    def checkIfUserExists(self, userId):
        cursor = self._connection.cursor()
        cursor.execute('SELECT 1 FROM userdata WHERE userid = %s', (userId,))
        return False if cursor.fetchone() is None else True

    def userPlaceByHash(self, userId):
        cursor = self._connection.cursor()
        cursor.execute('''
            SELECT COUNT (1) FROM (
            SELECT egp FROM userdata WHERE egp >= (
            SELECT egp FROM userdata WHERE userid = %s
            ));
            ''', (userId,))
        return cursor.fetchone()[0]

    def generateReferral(self, userId):
        try:
            cursor = self._connection.cursor()
            cursor.execute('SELECT referral FROM referrals WHERE userid = %s', (userId,))
            result = cursor.fetchone()[0]
            if result:
                return botInviteUrl + result
            referral = generate_random_string()
            cursor.execute("""
                UPDATE referrals
                SET referral = %s
                WHERE userid = %s;
            """, (referral, userId))
            self._connection.commit()
            return botInviteUrl + referral
        except Exception as e:
            print(e)
            return self.generateReferral(userId)

    def checkIfUserAlreadyJoined(self, userId):
        cursor = self._connection.cursor()
        cursor.execute("SELECT joined FROM referrals WHERE userid = %s", (userId,))
        result = cursor.fetchone()
        if result[0]:
            return True
        cursor.execute("UPDATE referrals SET joined = true WHERE userid = %s", (userId,))
        self._connection.commit()
        return False

    def getAllUsersIds(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT userid FROM userdata")
        result = cursor.fetchall()
        return [row[0] for row in result]

    def countUsers(self):
        cursor = self._connection.cursor()
        cursor.execute('SELECT count(1) FROM userdata')
        result = cursor.fetchone()
        return result[0]