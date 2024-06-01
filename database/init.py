from psycopg2 import connect
from os import getenv
from dotenv import load_dotenv
from database.createBase import createTable

load_dotenv()


def init():
    connection = connect(
        user=getenv('DATABASE_USER'),
        password=getenv('DATABASE_PASSWORD'),
        host='localhost',
        port=5432,
        database=getenv('DATABASE_NAME')
    )
    print('connection with db established')
    createTable(connection)
    return connection
