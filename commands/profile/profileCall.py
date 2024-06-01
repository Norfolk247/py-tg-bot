from telebot import TeleBot

from database.userController import getUser


def profileCall(call, connection, bot: TeleBot):
    _, level, userHash, egp, _, _, _ = getUser(connection, call.from_user.id)
    replyMessage = f"""
name {call.from_user.first_name}
username {call.from_user.username}
баланс egp {egp}
баланс coins {userHash}
уровень {level}
"""
    bot.send_message(call.message.chat.id, replyMessage)
