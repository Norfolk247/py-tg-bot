from json import load

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database.userController import getUser

with open('config/banks.json', 'r') as f:
    banks = load(f)


def paymentsCall(call, connection, bot: TeleBot):
    replyMarkup = ReplyKeyboardMarkup(row_width=2)
    for bank in banks:
        replyMarkup.add(KeyboardButton(bank))
    replyMarkup.add('Главное меню')

    def chooseBank(message):
        if message.text == 'Главное меню':
            reply_markup = InlineKeyboardMarkup(row_width=2)
            reply_markup.add(
                InlineKeyboardButton('Зарабатывать', callback_data='earn'),
                InlineKeyboardButton('Заработать больше', callback_data='earnMore'),
                InlineKeyboardButton('Рефералка', callback_data='referral'),
                InlineKeyboardButton('Обмен coins', callback_data='coinTrade'),
                InlineKeyboardButton('Топ пользователей', callback_data='userLadder'),
                InlineKeyboardButton('Профиль', callback_data='profile'),
                InlineKeyboardButton('Выплаты', callback_data='payments'),
                InlineKeyboardButton('FAQ', callback_data='faq'),
                InlineKeyboardButton('Промокод', callback_data='promo'),
            )
            bot.send_message(message.chat.id, 'главное меню', reply_markup=reply_markup)
            return
        bank = message.text
        if bank not in banks:
            bot.send_message(message.chat.id, 'Такого банка нет')
            return
        bot.send_message(message.chat.id, 'Введите сумму выплаты')
        bot.register_next_step_handler(message, choosePaymentAmount)

    def choosePaymentAmount(message):
        if not message.text.isdigit():
            bot.send_message(message.chat.id, 'Введено некорректное число, повторите ввод')
            bot.register_next_step_handler(message, choosePaymentAmount)
            return
        if int(message.text) <= 0:
            bot.send_message(message.chat.id, 'Ввод отменен')
            return
        userId, level, _, egp, _, _, _ = getUser(connection, message.from_user.id)
        if int(message.text) > egp:
            bot.send_message(message.chat.id, 'Недостаточно средств')
            return
        if level < 3:
            bot.send_message(message.chat.id, 'Ввывод возможен только с 3 уровня')
            return
        pass

    bot.send_message(call.message.chat.id, 'Выберете банк', reply_markup=replyMarkup)
    bot.register_next_step_handler(call.message, chooseBank)
