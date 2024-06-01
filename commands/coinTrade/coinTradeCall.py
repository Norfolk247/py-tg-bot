from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from database.userController import getUser, editUser


def exchangeRateHashToEGP(hashValue):
    return hashValue // exchangeRateEGPToHash(1)


def exchangeRateEGPToHash(egpValue):
    return egpValue * 200


def coinTradeCall(call, connection, bot: TeleBot):
    userId, _, userHash, egp, _, _, _ = getUser(connection, call.from_user.id)
    replyMessage = f"""
баланс {userHash} хэш
доступно к выводу {exchangeRateHashToEGP(userHash)} egp
курс обмена {exchangeRateEGPToHash(1)} Coins - 1 egp
введите количество egp для обмена или 0 для отмены
"""

    def nextStepMessageHandlerCoinsExchange(message):
        handledMsg = message.text.strip()
        if not handledMsg.isdigit():
            bot.send_message(call.message.chat.id, 'введите корректное число')
            bot.register_next_step_handler(call.message, nextStepMessageHandlerCoinsExchange)
            return
        handledMsg = int(handledMsg)
        if handledMsg == '0':
            return
        if exchangeRateEGPToHash(max(int(handledMsg), 0)) > userHash:
            bot.send_message(call.message.chat.id, 'недостаточно коинов для обмена')
            return
        editUser(connection, userId, userHashDiff=-exchangeRateEGPToHash(handledMsg),
                 egpDiff=handledMsg)
        bot.send_message(call.message.chat.id, f'успешно начислено {handledMsg} egp')

    bot.send_message(call.message.chat.id, replyMessage)
    bot.register_next_step_handler(call.message, nextStepMessageHandlerCoinsExchange)
