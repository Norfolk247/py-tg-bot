from json import load

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot

from bot.config.calcs import exchangeRateEGPToHash
from bot.messages.init import messages
from database.init import databaseConnection as connectionType
from configparser import ConfigParser

with open('bot/config/banks.json', 'r') as f:
    banks = load(f)

config = ConfigParser()
config.read('bot/config/config.ini')
channelInvite = config.get('urls', 'channelInvite')


class messageHandler:
    def __init__(self, databaseConnection: connectionType, botInstance: TeleBot):
        self._bot = botInstance
        self._connection = databaseConnection
        self._messages = messages()

    def earn(self, message):
        reply_markup = ReplyKeyboardMarkup(row_width=1)
        reply_markup.add(
            KeyboardButton(self._messages.menus.mine),
            KeyboardButton(self._messages.menus.levelUp),
            KeyboardButton(self._messages.menus.mainMenu)
        )

        self._bot.send_message(
            message.chat.id,
            self._messages.descriptions.selectMenuItem,
            reply_markup=reply_markup
        )

    def mine(self, message):
        _, level, userHash, _, currentClicks, maximumClicks, _ = self._connection.userController.getUser(
            message.from_user.id)

        reply_markup = InlineKeyboardMarkup(row_width=1)
        reply_markup.add(
            InlineKeyboardButton(self._messages.callbacks.click, callback_data='click'),
        )

        self._bot.send_message(
            message.chat.id,
            self._messages.clickerReplyMessage(currentClicks, maximumClicks, level, userHash),
            reply_markup=reply_markup
        )

    def levelUp(self, message):
        _, level, _, _, _, _, _ = self._connection.userController.getUser(message.from_user.id)

        reply_markup = InlineKeyboardMarkup(row_width=1)
        reply_markup.add(InlineKeyboardButton(self._messages.callbacks.levelUp, callback_data='levelUp'))

        self._bot.send_message(
            message.chat.id,
            self._messages.nextLevelCost(level),
            reply_markup=reply_markup
        )

    def earnMore(self, message):
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton(self._messages.descriptions.followLink, url=channelInvite))
        reply_markup.add(InlineKeyboardButton(self._messages.callbacks.getGift, callback_data='getGift'))
        self._bot.send_message(message.chat.id, self._messages.descriptions.toEarnGiftFollowSponsorChannel,
                               reply_markup=reply_markup)

    def referral(self, message):
        self._bot.send_message(message.chat.id,
                               self._messages.referralMessage(self._connection.userController.generateReferral(message.from_user.id)))

    def coinTrade(self, message, messageHandler):
        userId, _, userHash, egp, _, _, _ = self._connection.userController.getUser(message.from_user.id)

        def nextStepMessageHandlerCoinsExchange(nextMessage):
            handledMsg = nextMessage.text.strip()
            if not handledMsg.isdigit():
                self._bot.send_message(message.chat.id, self._messages.descriptions.printNumberOr0ToCancel)
                self._bot.register_next_step_handler(
                    message,
                    lambda nextMessage: messageHandler(
                        nextMessage,
                        lambda msg: nextStepMessageHandlerCoinsExchange(msg)
                    )
                )
                return
            handledMsg = int(handledMsg)
            if handledMsg == '0':
                return
            if exchangeRateEGPToHash(max(int(handledMsg), 0)) > userHash:
                self._bot.send_message(message.chat.id, self._messages.descriptions.notEnoughHashToTrade)
                return
            self._connection.userController.editUser(
                userId,
                userHashDiff=-exchangeRateEGPToHash(handledMsg),
                egpDiff=handledMsg
            )
            self._bot.send_message(message.chat.id, self._messages.successfulAddedCoins(handledMsg))

        self._bot.send_message(message.chat.id, self._messages.coinTradeReplyMessage(userHash))
        self._bot.register_next_step_handler(
            message,
            lambda nextMessage: messageHandler(nextMessage, lambda msg: nextStepMessageHandlerCoinsExchange(msg))
        )

    def userLadder(self, message):
        place = self._connection.userController.userPlaceByHash(message.from_user.id)
        self._bot.send_message(message.chat.id, self._messages.userLadderReplyMessage(place))

    def profile(self, message):
        _, level, userHash, egp, _, _, _ = self._connection.userController.getUser(message.from_user.id)

        self._bot.send_message(message.chat.id, self._messages.profileReplyMessage(
            message.from_user.username,
            egp,
            userHash,
            level
        ))

    def payments(self, message, messageHandler):
        replyMarkup = ReplyKeyboardMarkup(row_width=2)
        for bank in banks:
            replyMarkup.add(KeyboardButton(bank))
        replyMarkup.add(self._messages.menus.mainMenu)

        def chooseBank(nextMessage):
            bank = nextMessage.text
            if bank not in banks:
                self._bot.send_message(nextMessage.chat.id, self._messages.descriptions.bankNotFound)
                return
            self._bot.send_message(nextMessage.chat.id, self._messages.descriptions.printEGPCount)
            self._bot.register_next_step_handler(
                message,
                lambda nextMessage: messageHandler(nextMessage, lambda msg: choosePaymentAmount(msg))
            )

        def choosePaymentAmount(nextMessage):
            if not nextMessage.text.isdigit():
                self._bot.send_message(nextMessage.chat.id, self._messages.descriptions.printNumberOr0ToCancel)
                self._bot.register_next_step_handler(nextMessage, choosePaymentAmount)
                return
            if int(nextMessage.text) <= 0:
                return
            userId, level, _, egp, _, _, _ = self._connection.userController.getUser(nextMessage.from_user.id)
            if int(nextMessage.text) > egp:
                self._bot.send_message(nextMessage.chat.id, self._messages.descriptions.notEnoughEGP)
                return
            if level < 3:
                self._bot.send_message(nextMessage.chat.id, self._messages.descriptions.EGPReceivingNotAvailable)
                return

        self._bot.send_message(message.chat.id, self._messages.descriptions.chooseBank, reply_markup=replyMarkup)
        self._bot.register_next_step_handler(
            message,
            lambda nextMessage: messageHandler(nextMessage, lambda msg: chooseBank(msg))
        )

    def faq(self, message):
        self._bot.send_message(message.chat.id, self._messages.descriptions.faq)

    def promo(self, message, messageHandler):

        def handlePromo(nextMessage):
            messageHandler(
                nextMessage,
                lambda messageWithPromo: self._bot.send_message(message.chat.id, self._messages.descriptions.wrongPromo)
            )

        self._bot.send_message(message.chat.id, self._messages.descriptions.printPromo)
        self._bot.register_next_step_handler(
            message,
            handlePromo
        )
