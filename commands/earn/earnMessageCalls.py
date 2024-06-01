from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from time import time
from database.userController import getUser, editUser
from configparser import ConfigParser

# consts
config = ConfigParser()
config.read('config/config.ini')
channelInvite = config.get('urls', 'channelInvite')


def clickerReplyMessage(currentClicks, maximumClicks, level, userHash):
    return f"""
Сегодня: {currentClicks}/{maximumClicks}
    
Прогресс: {round(currentClicks / maximumClicks * 100)}%
    
Хэш за клик: {increaseHash(level)}
Уровень: {level}
Баланс: {userHash}
    """


def nextLevelCost(level):
    return round(80000 * 1.2 ** (level - 1))


def increaseHash(level):
    return round(100 * 1.2 ** (level - 1))


# earn -> click
def clickerDataMessage(message, connection, bot: TeleBot):
    _, level, userHash, _, currentClicks, maximumClicks, _ = getUser(connection, message.from_user.id)
    reply_markup = InlineKeyboardMarkup(row_width=1)
    reply_markup.add(
        InlineKeyboardButton('Клик', callback_data='click'),
    )
    bot.send_message(message.chat.id, clickerReplyMessage(currentClicks, maximumClicks, level, userHash),
                     reply_markup=reply_markup)


def clickCall(call, connection, bot: TeleBot):
    userId, level, userHash, _, currentClicks, maximumCLicks, update = getUser(connection, call.from_user.id)
    update = round(time()) if update is None else update
    if currentClicks < maximumCLicks:
        _, level, userHash, _, currentClicks, maximumCLicks, _ = editUser(connection,
                                                                          userId,
                                                                          userHashDiff=increaseHash(level),
                                                                          currentClicksDiff=1,
                                                                          update=update)
        reply_markup = InlineKeyboardMarkup(row_width=1)
        reply_markup.add(
            InlineKeyboardButton('Клик', callback_data='click'),
        )
        bot.edit_message_text(
            clickerReplyMessage(currentClicks, maximumCLicks, level, userHash),
            chat_id=call.message.chat.id,
            message_id=call.message.id, reply_markup=reply_markup)
        return
    reply_markup = InlineKeyboardMarkup(row_width=1)
    reply_markup.add(
        InlineKeyboardButton('заработать деньги', url=channelInvite)
    )
    bot.send_message(call.message.chat.id, 'Максимум кликов', reply_markup=reply_markup)


# earn -> levelUp
def levelUpMessage(message, connection, bot: TeleBot):
    _, level, _, _, _, _, _ = getUser(connection, message.from_user.id)
    reply_markup = InlineKeyboardMarkup(row_width=1)
    reply_markup.add(
        InlineKeyboardButton('Повысить уровень майнеров', callback_data='levelUp'),
    )
    bot.send_message(message.chat.id, f'текущий уровень {level}. Стоимость перехода {nextLevelCost(level)}',
                     reply_markup=reply_markup)


def levelUpCall(call, connection, bot: TeleBot):
    userId, level, userHash, _, _, _, update = getUser(connection, call.from_user.id)
    if level == 2:
        bot.send_message(call.message.chat.id, 'Обратитесь к администратору для перехода на следующий уровень')
        return
    if userHash >= nextLevelCost(level):
        editUser(connection, userId, 1, -nextLevelCost(level))
        bot.send_message(call.message.chat.id, 'Уровень повышен!')
        return
    bot.send_message(call.message.chat.id, f'Недостаточно денег, нужно еще {nextLevelCost(level) - userHash}')
