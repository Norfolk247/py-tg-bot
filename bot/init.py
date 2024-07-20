import time
from configparser import ConfigParser

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from bot.messages.init import messages
from database.init import databaseConnection as connectionType
from bot.handlers.init import handlers

config = ConfigParser()
config.read('bot/config/config.ini')
sponsorGroupChatId = config.get('ids', 'sponsorGroupChatId')


class bot:
    def __init__(self, token, databaseConnection: connectionType):
        self._database = databaseConnection
        self._botInstance = TeleBot(token)
        self._messages = messages()
        self._handlers = handlers(self._database, self._botInstance)
        self._setupHandlers()
        self._botInstance.infinity_polling(none_stop=True)
        #while True:
        #    try:
        #        self._botInstance.polling(none_stop=True)
        #    except Exception as e:
        #        print(e)
        #        time.sleep(3)
        #        continue

    def _setupHandlers(self):
        @self._botInstance.message_handler(commands=['start'], chat_types=['private'])
        def sendStartMessage(message):
            self._database.userController.createNewUser(message.from_user.id, message.text)

            replyMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
            replyMarkup.add(KeyboardButton(self._messages.menus.earn))
            replyMarkup.row(KeyboardButton(self._messages.menus.earnMore),
                            KeyboardButton(self._messages.menus.referral))
            replyMarkup.row(KeyboardButton(self._messages.menus.coinTrade),
                            KeyboardButton(self._messages.menus.userLadder))
            replyMarkup.row(KeyboardButton(self._messages.menus.profile), KeyboardButton(self._messages.menus.payments))
            replyMarkup.add(KeyboardButton(self._messages.menus.faq))
            replyMarkup.add(KeyboardButton(self._messages.menus.promo))

            self._botInstance.send_message(message.chat.id, self._messages.descriptions.selectMenuItem,
                                           reply_markup=replyMarkup)

        @self._botInstance.callback_query_handler(func=lambda call: True)
        def callbackHandler(call):
            self._botInstance.clear_step_handler_by_chat_id(call.message.chat.id)
            match call.data:
                case 'click':
                    self._handlers.callbacks.click(call)
                case 'levelUp':
                    self._handlers.callbacks.levelUp(call)
                case 'getGift':
                    self._handlers.callbacks.getGift(call)

        @self._botInstance.message_handler(content_types=['text'], chat_types=['private'])
        def messageHandler(
                message,
                next=lambda nextMessage:
                self._botInstance.send_message(nextMessage.chat.id, self._messages.descriptions.commandUnknown)
        ):
            if not self._database.userController.checkIfUserExists(message.from_user.id):
                sendStartMessage(message)
                return
            match message.text:
                case self._messages.menus.earn:
                    self._handlers.messages.earn(message)
                case self._messages.menus.earnMore:
                    self._handlers.messages.earnMore(message)
                case self._messages.menus.referral:
                    self._handlers.messages.referral(message)
                case self._messages.menus.coinTrade:
                    self._handlers.messages.coinTrade(message, messageHandler)
                case self._messages.menus.userLadder:
                    self._handlers.messages.userLadder(message)
                case self._messages.menus.profile:
                    self._handlers.messages.profile(message)
                case self._messages.menus.payments:
                    self._handlers.messages.payments(message, messageHandler)
                case self._messages.menus.faq:
                    self._handlers.messages.faq(message)
                case self._messages.menus.promo:
                    self._handlers.messages.promo(message, messageHandler)
                case self._messages.menus.mine:
                    self._handlers.messages.mine(message)
                case self._messages.menus.levelUp:
                    self._handlers.messages.levelUp(message)
                case self._messages.menus.mainMenu:
                    sendStartMessage(message)
                case _:
                    next(message)
        @self._botInstance.message_handler(func=lambda msg: msg.chat.id == sponsorGroupChatId)
        def handleIfUserLeftChat(message):
            return
