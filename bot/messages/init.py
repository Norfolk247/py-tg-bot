from bot.messages.descriptionMessages import descriptions
from bot.messages.menusMessages import menus
from bot.messages.callbacksMessages import callbacks
from bot.config.calcs import HashPerClick, nextLevelCost, exchangeRateHashToEGP, exchangeRateEGPToHash


class messages:
    def __init__(self):
        self.descriptions = descriptions()
        self.menus = menus()
        self.callbacks = callbacks()

    def clickerReplyMessage(self, currentClicks, maximumClicks, level, userHash):
        return f"""
        تم التعدين اليوم: {currentClicks}/{maximumClicks} ⛏️

        التقدم: {round(currentClicks / maximumClicks * 100)}% 📊

        الهاش لكل نقرة: {HashPerClick(level)} 🖱️
        المستوى: {level} 📈
        رصيد الهاش: {userHash} 💰
        """

    def coinTradeReplyMessage(self, userHash):
        return f"""أدخل رقم EGP أو 0 للإلغاء 👇
💰 رصيدك هو {userHash} تجزئة
🔒 يمكنك سحب {exchangeRateHashToEGP(userHash)} EGP

🔄 سعر الصرف {exchangeRateEGPToHash(1)} HASH = 1 EGP
        """

    def nextLevelCost(self, level):
        return f'المستوى الحالي {level}. تكلفة رفع المستوى {nextLevelCost(level)}'

    def notEnoughHashToLevelUp(self, hashDiff):
        return f'ليس هناك ما يكفي من التجزئة، بحاجة إلى {hashDiff} أكثر'

    def referralMessage(self, referralLink):
        return f"""
        💳 احصل على مكافأة مقابل دعوة الأصدقاء 👇
🔗 أرسل الرابط إلى صديق - {referralLink}

✅ تحصل على 1200 EGP لكل صديق تقوم بدعوته.
        """

    def successfulAddedCoins(self, coinsCount):
        return f'تم إضافة {coinsCount} EGP إلى ملفك الشخصي'

    def userLadderReplyMessage(self, place):
        return f"""
        📣 أنت اليوم في مكان {place + 8316} 🏆

🎁 للحصول على الجائزة يجب أن تكون من بين أفضل ثلاثة لاعبين حسب رصيد حسابك 🎁.

أعلى 🥇
الرصيد المطلوب : 15341 💶
الأجر : 680 💶

أعلى 🥈
الرصيد المطلوب : 12270 💶
الجائزة : 300 💶

أعلى 🥉
الرصيد المطلوب : 10442 💶
الجائزة : 150 💶
"""

    def profileReplyMessage(self, username, egp, userHash, level):
        return f"""
        👤 ملفي الشخصي:

🗂اسم المستخدم: {username}

💶 رصيد EGP: {egp}

💰هاش - الرصيد: {userHash}
📶 مستوى الغنائم: {level}
        """
