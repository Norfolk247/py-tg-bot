from bot.messages.descriptionMessages import descriptions
from bot.messages.menusMessages import menus
from bot.messages.callbacksMessages import callbacks
from bot.messages.adminMessages import admin
from bot.config.calcs import HashPerClick, nextLevelCost, exchangeRateHashToEGP, exchangeRateEGPToHash


class messages:
    def __init__(self):
        self.descriptions = descriptions()
        self.admin = admin()
        self.menus = menus()
        self.callbacks = callbacks()

    def clickerReplyMessage(self, currentClicks, maximumClicks, level, userHash):
        return f"""
📆 Hoy: {currentClicks}/{maximumClicks}

♻️ Progreso: {round(currentClicks / maximumClicks * 100)}%

⚖️ Hash por clic: {HashPerClick(level)}
📶 Nivel minero: {level}
💰 Saldo HASH: {userHash}
        """

    def coinTradeReplyMessage(self, userHash):
        return f"""Introduce la cantidad de HASH que quieres cambiar por bitcoin 👇
💰 Tu saldo: {userHash} HASH
🔒 Máximo disponible: {exchangeRateHashToEGP(userHash)} USD

🔄 Tarifa: {exchangeRateEGPToHash(1)} HASH = 1 USD
        """

    def nextLevelCost(self, level):
        return f'''📶 Nivel minero {level}. 
🆙 El costo para pasar al siguiente nivel es de {nextLevelCost(level)} hashes'''

    def notEnoughHashToLevelUp(self, hashDiff):
        return f'No hay suficiente hash, necesito más {hashDiff}'

    def referralMessage(self, referralLink):
        return f"""
👥 Dinero para amigo
💳  Obtenga bonos para amigos invitados 👇
🔗 Enviar enlace a un amigo - {referralLink} 

✅ 15 USD obtienes por cada amigo invitado
        """

    def successfulAddedCoins(self, coinsCount):
        return f'{coinsCount} USD se ha añadido a tu perfil'

    def userLadderReplyMessage(self, place):
        return f"""
📣 Hoy estás en {place + 8316} lugar 🏆

🎁 Para recibir una recompensa, debes estar entre los 3 primeros jugadores por saldo 🎁

------------------
Top 🥇
Necesita saldo: 6095 USD
Recompensa: 35 USD
------------------ 
Principal 🥈
Necesita saldo: 4437 USD
Recompensa: 10 USD
------------------
Superior 🥉
Necesita equilibrio: 4115 USD
Recompensa: 10 USD
"""

    def profileReplyMessage(self, username, egp, userHash, level):
        return f"""
👤 Mi perfil:

🗂Nombre de usuario: {username}

USD Saldo USD: {egp}

💰HASH - saldo: {userHash}
📶 Nivel minero: {level}
        """