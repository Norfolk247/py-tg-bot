from telebot import TeleBot

from database.userController import userPlaceByHash


def userLadderCall(call, connection, bot: TeleBot):
    place = userPlaceByHash(connection, call.from_user.id)
    bot.send_message(call.message.chat.id, f'вы на {place + 8502} месте')
