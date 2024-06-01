from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from commands.coinTrade.coinTradeCall import coinTradeCall
from commands.earn.earnCall import earnCall
from commands.earn.earnMessageCalls import clickerDataMessage, clickCall, levelUpCall, levelUpMessage
from commands.earnMore.earnMoreCall import earnMoreCall
from commands.faq.faqCall import faqCall
from commands.payments.paymentsCall import paymentsCall
from commands.profile.profileCall import profileCall
from commands.promo.promoCall import promoCall
from commands.promo.promoMessageCalls import getPromoMessage
from commands.referral.referralCall import referralCall
from commands.userLadder.userLadderCall import userLadderCall
from database.referralController import newUser
from database.userController import checkIfUserExists


# import configparser

# config = configparser.ConfigParser()
# config.read('config/config.ini')


def init(bot: TeleBot, connection):
    @bot.message_handler(commands=['start'])
    def startMessage(message):
        bot.clear_step_handler_by_chat_id(message.chat.id)
        newUser(connection, message.from_user.id, message.text)
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

    @bot.callback_query_handler(func=lambda call: True)
    def callbackHandler(call):
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        match call.data:
            case 'earn':
                earnCall(call, bot)
            case 'click':
                clickCall(call, connection, bot)
            case 'levelUp':
                levelUpCall(call, connection, bot)
            case 'earnMore':
                earnMoreCall(call, bot)
                pass
            case 'referral':
                referralCall(call, connection, bot)
            case 'coinTrade':
                coinTradeCall(call, connection, bot)
            case 'userLadder':
                userLadderCall(call, connection, bot)
            case 'profile':
                profileCall(call, connection, bot)
            case 'payments':
                paymentsCall(call, connection, bot)
            case 'faq':
                faqCall(call, bot)
            case 'promo':
                promoCall(call, bot)

    @bot.message_handler(content_types=['text'])
    def messageHandler(message):
        if not checkIfUserExists(connection, message.from_user.id):
            startMessage(message)
            return
        bot.clear_step_handler_by_chat_id(message.chat.id)
        match message.text:
            case 'Нажать':
                clickerDataMessage(message, connection, bot)
            case 'Лвлап':
                levelUpMessage(message, connection, bot)
            case 'Главное меню':
                startMessage(message)
            case 'Канал':
                pass
            case 'Получить бонус':
                pass
            case 'Получить промокод':
                getPromoMessage(message, bot)
            case _:
                bot.send_message(message.chat.id, 'Неизвестная команда')
                startMessage(message)
