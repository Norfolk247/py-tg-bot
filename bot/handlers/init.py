from bot.handlers.callbackHandler import callbackHandler
from bot.handlers.messageHandlers import messageHandler
from bot.handlers.adminMessageHandlers import adminMessageHandler


class handlers:
    def __init__(self, databaseConnection, botInstance):
        self.messages = messageHandler(databaseConnection, botInstance)
        self.callbacks = callbackHandler(databaseConnection, botInstance)
        self.adminMessages = adminMessageHandler(databaseConnection, botInstance)
