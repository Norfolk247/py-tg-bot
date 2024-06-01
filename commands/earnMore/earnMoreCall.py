from configparser import ConfigParser
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# consts
config = ConfigParser()
config.read('config/config.ini')
channelInvite = config.get('urls', 'channelInvite')


def earnMoreCall(call, bot: TeleBot):
    reply_markup = InlineKeyboardMarkup()
    reply_markup.add(
        InlineKeyboardButton('Канал', url=channelInvite),
    )
    bot.send_message(call.message.chat.id, 'Для получения бонуса перейдите на канал', reply_markup=reply_markup)
