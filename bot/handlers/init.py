from bot.handlers.callbackHandler import callbackHandler
from bot.handlers.messageHandlers import messageHandler


class handlers:
    def __init__(self, databaseConnection, botInstance):
        self.messages = messageHandler(databaseConnection, botInstance)
        self.callbacks = callbackHandler(databaseConnection, botInstance)
