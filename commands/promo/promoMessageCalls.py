from telebot import TeleBot


def getPromoMessage(message,bot: TeleBot):
    bot.send_message(message.chat.id,'чтобы получить промо обратитесь к нашему спонсору за информацией')