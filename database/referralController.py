from database.userController import editUser, getUser
from configparser import ConfigParser

from utils.generateId import generate_random_string

config = ConfigParser()
config.read('config/config.ini')
botInviteUrl = config.get('urls', 'botInviteUrl')


def newUser(connection, userId, referral):
    cursor = connection.cursor()
    cursor.execute('SELECT 1 FROM referrals WHERE userid = %s;', (userId,))
    result = cursor.fetchone()
    if result:
        return
    cursor.execute('INSERT INTO referrals (userid) VALUES (%s);', (userId,))
    getUser(connection, userId)
    referral = referral.split(' ')[1] if len(referral.split(' ')) > 1 else None
    if referral is None:
        connection.commit()
        return
    cursor.execute('SELECT userid FROM referrals WHERE referral = %s;', (referral,))
    inviterId = cursor.fetchone()
    editUser(connection, inviterId, egpDiff=60)
    connection.commit()


def generateReferral(connection, userId):
    cursor = connection.cursor()
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
    connection.commit()
    return botInviteUrl + referral
