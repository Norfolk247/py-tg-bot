from telebot import TeleBot


def faqCall(call, bot: TeleBot):
    bot.send_message(call.message.chat.id, 'faq')
