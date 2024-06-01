from os import getenv
from dotenv import load_dotenv
import telebot

from commands import init as commands
from database import init as database

load_dotenv()

bot = telebot.TeleBot(getenv('TOKEN'))
db = database.init()
commands.init(bot, db)

if __name__ == '__main__':
    bot.polling(none_stop=True)
