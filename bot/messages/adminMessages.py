class descriptions:
    def __init__(self):
        self.selectCommand = 'Выберите пункт меню'
        self.unknownCommand = 'Неизвестная команда. Для выхода из панели нажмите "Выход" на панели'
        self.confirm = 'Подтвердите выполнение'
        self.send = 'Отправить'
        self.cancel = 'Отменить'
        self.setSpamMessage = 'Напишите текст для сообщения рассылки'
        self.wrongMessageType = 'Неизвестный тип файла/файлов выберите другое сообщение'
class commands:
    def __init__(self):
        self.setSpam = 'Установить сообщение для рассылки'
        self.sendSpam = 'Отправить рассылку'
        self.countUsers = 'Количество людей в боте'
        self.quitAdmin = 'Выйти из админ панели'

class admin:
    def __init__(self):
        self.descriptions = descriptions()
        self.commands = commands()