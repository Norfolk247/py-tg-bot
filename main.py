from database.init import databaseConnection
from os import getenv
from dotenv import load_dotenv
from bot.init import bot
import logging

load_dotenv()
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

class app:
    def __init__(self):
        try:
            self._databaseConnection = databaseConnection(
                user=getenv('DATABASE_USER'),
                password=getenv('DATABASE_PASSWORD'),
                host='localhost',
                port=5432,
                databaseName=getenv('DATABASE_NAME')
            )
            self._botInstance = bot(getenv('TOKEN'), self._databaseConnection)
        except Exception as e:
            logging.error(e)



if __name__ == '__main__':
    myapp = app()
