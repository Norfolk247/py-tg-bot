from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def promoCall(call, bot: TeleBot):
    reply_markup = ReplyKeyboardMarkup(row_width=1)
    reply_markup.add(
        KeyboardButton('Получить промокод'),
        KeyboardButton('Главное меню')
    )
    bot.send_message(call.message.chat.id, 'Введите промокод', reply_markup=reply_markup)
    bot.register_next_step_handler(call.message, lambda message: bot.send_message(message.chat.id, 'Неверный промокод'))
