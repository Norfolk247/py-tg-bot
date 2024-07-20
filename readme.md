# Установка в другой среде
## DE
    python 3.10
    pyTelegramBotAPI@4.17.0
    python-dotenv@1.0.1
    psycopg2@2.9.9
## БД
    postgresql 16.2
    создать бд в postgresql
## DE зависимости
    создать в корне .env файл вида
        TOKEN=токен бота
        DATABASE_USER=пользователь бд, по дефолту postgresql
        DATABASE_PASSWORD=пароль бд
        DATABASE_NAME=имя базы данных
    config/config.ini
        [urls]
            channelInvite=название канала спонсора
            botInviteUrl=ссылка на бота нужна для реферальных ссылок, чтобы заканчивалась на ?start=
        [ids]
            sponsorGroupChatId=id канала спонсора
## Настройка в botfather
    API TOKEN
    edit bot/
        edit description - описание при открытии чата с ботом
        edit about - описание в профиле и при отправлении ссылки на бота
        edit description picture - картинка вместе с описанием в чате
        edit commands - когда в чате с ботом пишется /, то всплывают эти команды
        edit botpic - аватарка бота
    bot settings/
        куча всякой хуйни, которая может че-то поломать и вообще не ебу, как она работает
## Запуск
    в главной директории python main.py