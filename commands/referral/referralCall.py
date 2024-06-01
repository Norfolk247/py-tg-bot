from telebot import TeleBot

from database.referralController import generateReferral


def referralCall(call, connection, bot: TeleBot):
    replyMessage = f"""
    бонус за приглашенных друзей
{generateReferral(connection, call.from_user.id)}
    """
    bot.send_message(call.message.chat.id, replyMessage)
