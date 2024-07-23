from database.init import databaseConnection as connectionType
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from bot.messages.init import messages
from telebot import TeleBot
import logging

# logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

spamMedia = ('text', '', '')


class adminMessageHandler:
    def __init__(self, databaseConnection: connectionType, botInstance: TeleBot):
        self._bot = botInstance
        self._connection = databaseConnection
        self._messages = messages()

    def sendSpam(self, message, afterCancelHandler):
        reply = self._messages.admin.descriptions.confirm
        reply += '\nОтправленное сообщение:\n\n'
        reply += spamMedia[1]

        replyMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
        replyMarkup.add(KeyboardButton(self._messages.admin.descriptions.send))
        replyMarkup.add(KeyboardButton(self._messages.admin.descriptions.cancel))

        match spamMedia[0]:
            case 'text':
                self._bot.send_message(message.chat.id, reply, reply_markup=replyMarkup)
            case 'photo':
                self._bot.send_photo(message.chat.id, spamMedia[2], reply, reply_markup=replyMarkup)
            case 'video':
                self._bot.send_video(message.chat.id, spamMedia[2], caption=reply, reply_markup=replyMarkup)
            case 'document':
                self._bot.send_document(message.chat.id, spamMedia[2], caption=reply, reply_markup=replyMarkup)

        def confirmSending(nextMessage):
            match nextMessage.text:
                case self._messages.admin.descriptions.send:
                    userIds = self._connection.userController.getAllUsersIds()
                    for userId in userIds:
                        try:
                            match spamMedia[0]:
                                case 'text':
                                    self._bot.send_message(userId, spamMedia[1])
                                case 'photo':
                                    self._bot.send_photo(userId, spamMedia[2], spamMedia[1])
                                case 'video':
                                    self._bot.send_video(userId, spamMedia[2], caption=spamMedia[1]
                                                         )
                                case 'document':
                                    self._bot.send_document(userId, spamMedia[2], caption=spamMedia[1]
                                                            )
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
            global spamMedia
            match nextMessage.content_type:
                case 'text':
                    spamMedia = ('text', nextMessage.text)
                case 'photo':
                    spamMedia = ('photo', nextMessage.caption if nextMessage.caption is not None else '',
                                 nextMessage.json['photo'][1]['file_id'])
                case 'video':
                    spamMedia = ('video', nextMessage.caption if nextMessage.caption is not None else '',
                                 nextMessage.json['video']['file_id'])
                case 'document':
                    spamMedia = ('document', nextMessage.caption if nextMessage.caption is not None else '',
                                 nextMessage.json['document']['file_id'])
                case _:
                    self._bot.send_message(nextMessage.chat.id, self._messages.admin.descriptions.wrongMessageType)
                    self._bot.register_next_step_handler(nextMessage, setSpamMessage)
                    return

            afterHandler(nextMessage)

        self._bot.register_next_step_handler(message, setSpamMessage)
