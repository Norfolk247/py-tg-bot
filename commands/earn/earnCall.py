from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def earnCall(call, bot: TeleBot):
    reply_markup = ReplyKeyboardMarkup(row_width=1)
    reply_markup.add(
        KeyboardButton('Нажать'),
        KeyboardButton('Лвлап'),
        KeyboardButton('Главное меню')
    )
    bot.send_message(call.message.chat.id, 'выберете пункт меню, чтобы заработать', reply_markup=reply_markup)
