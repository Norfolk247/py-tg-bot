from database.init import databaseConnection as connectionType
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from bot.messages.init import messages
from telebot import TeleBot
import logging

#logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

spamMessage = ''

class adminMessageHandler:
    def __init__(self, databaseConnection: connectionType, botInstance: TeleBot):
        self._bot = botInstance
        self._connection = databaseConnection
        self._messages = messages()

    def sendSpam(self, message, afterCancelHandler):
        reply = self._messages.admin.descriptions.confirm
        reply += '\nОтправленное сообщение:\n\n'
        reply += spamMessage

        replyMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
        replyMarkup.add(KeyboardButton(self._messages.admin.descriptions.send))
        replyMarkup.add(KeyboardButton(self._messages.admin.descriptions.cancel))

        self._bot.send_message(message.chat.id, reply, reply_markup=replyMarkup)

        def confirmSending(nextMessage):
            match nextMessage.text:
                case self._messages.admin.descriptions.send:
                    userIds = self._connection.userController.getAllUsersIds()
                    for userId in userIds:
                        try:
                            self._bot.send_message(userId,spamMessage)
                        except Exception as e:
                            logging.error(f'{userId} {e}')
                    afterCancelHandler(nextMessage)
                case self._messages.admin.descriptions.cancel:
                    afterCancelHandler(nextMessage)
                case _:
                    self._bot.register_next_step_handler(nextMessage, confirmSending)

        self._bot.register_next_step_handler(message, confirmSending)

    def setSpam(self, message, afterHandler):
        replyMarkup = ReplyKeyboardMarkup()
        replyMarkup.add(KeyboardButton(self._messages.admin.descriptions.cancel))

        self._bot.send_message(message.chat.id, self._messages.admin.descriptions.setSpamMessage,
                               reply_markup=replyMarkup)

        def setSpamMessage(nextMessage):
            if nextMessage.text == self._messages.admin.descriptions.cancel:
                return afterHandler(nextMessage)
            global spamMessage
            spamMessage = nextMessage.text
            afterHandler(nextMessage)

        self._bot.register_next_step_handler(message, setSpamMessage)