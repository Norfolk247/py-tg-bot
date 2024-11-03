from time import time
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config.calcs import HashPerClick, nextLevelCost
from bot.messages.init import messages
from database.init import databaseConnection as connectionType
from configparser import ConfigParser

config = ConfigParser()
config.read('bot/config/config.ini')
channelInvite = config.get('urls', 'channelInvite')
sponsorGroupChatId = config.get('ids', 'sponsorGroupChatId')


class callbackHandler:
    def __init__(self, databaseConnection: connectionType, botInstance: TeleBot):
        self._bot = botInstance
        self._connection = databaseConnection
        self._messages = messages()

    def click(self, call):
        userId, level, userHash, _, currentClicks, maximumCLicks, update = self._connection.userController.getUser(
            call.from_user.id)
        update = round(time()) if update is None else update
        if currentClicks < maximumCLicks:
            _, level, userHash, _, currentClicks, maximumCLicks, _ = self._connection.userController.editUser(
                userId,
                userHashDiff=HashPerClick(level),
                currentClicksDiff=1,
                update=update
            )
            reply_markup = InlineKeyboardMarkup(row_width=1)
            reply_markup.add(
                InlineKeyboardButton(self._messages.callbacks.click, callback_data='click'),
            )
            self._bot.edit_message_text(
                self._messages.clickerReplyMessage(currentClicks, maximumCLicks, level, userHash),
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=reply_markup
            )
            return
        reply_markup = InlineKeyboardMarkup(row_width=1)
        reply_markup.add(
            InlineKeyboardButton(self._messages.descriptions.followLink, url=channelInvite)
        )
        self._bot.send_message(call.message.chat.id, self._messages.descriptions.maxClicksToday,reply_markup=reply_markup)

    def levelUp(self, call):
        userId, level, userHash, _, _, _, update = self._connection.userController.getUser(call.from_user.id)
        if level == 2:
            reply = InlineKeyboardMarkup()
            reply.add(InlineKeyboardButton(self._messages.descriptions.followLink,url=channelInvite))
            self._bot.send_message(
                call.message.chat.id,
                self._messages.descriptions.connectWithSponsor,
                reply_markup=reply
            )
            return
        if userHash >= nextLevelCost(level):
            self._connection.userController.editUser(userId, 1, -nextLevelCost(level))
            self._bot.send_message(call.message.chat.id, self._messages.descriptions.successfulLevelUp)
            return
        self._bot.send_message(
            call.message.chat.id,
            self._messages.notEnoughHashToLevelUp(nextLevelCost(level) - userHash)
        )

    def getGift(self, call):
        try:
            # user left
            if self._bot.get_chat_member(sponsorGroupChatId, call.from_user.id).status == 'left':
                raise Exception('user left')
            # user already got gift
            if self._connection.userController.checkIfUserAlreadyJoined(call.from_user.id):
                self._bot.send_message(call.message.chat.id, self._messages.descriptions.bonusAlreadyClaimed)
                return
            # send gift
            self._connection.userController.editUser(call.from_user.id, egpDiff=1200)
            self._bot.send_message(call.message.chat.id, self._messages.descriptions.giftSend)
        except Exception as e:
            print(call.from_user.id,e)
            self._bot.send_message(call.message.chat.id, self._messages.descriptions.notSubscribed)
