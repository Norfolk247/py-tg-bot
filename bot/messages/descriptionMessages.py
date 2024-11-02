from configparser import ConfigParser

config = ConfigParser()
config.read('bot/config/config.ini')
channelInvite = config.get('urls', 'channelInvite')

class descriptions:
    def __init__(self):
        self.selectMenuItem = 'Seleccione un elemento de menú 👇'
        self.maxClicksToday = 'الحد الأقصى المستخرج اليوم'
        self.withdrawCash = 'retirar dinero'
        self.successfulLevelUp = 'Has alcanzado un nivel superior'
        self.connectWithSponsor = f'Conéctate con tu patrocinador para pasar al siguiente nivel {channelInvite}'
        self.followLink = 'Ir al canal 📲'
        self.toEarnGiftFollowSponsorChannel = """
        ❗️OBTENGA 1200 PESOS POR SUSCRIPCIÓN AL CANAL❗️

💫Debes suscribirte al canal del patrocinador, ver 25 publicaciones que aparezcan después de la suscripción, y luego puedes regresar aquí por tu recompensa, haciendo clic en el botón "Obtener recompensa". Y recibirás 1200 pesos!

⚠️Ten en cuenta: si te das de baja del canal del patrocinador, no se realizará el pago
        """
        self.printNumberOr0ToCancel = 'Ingrese un número válido o 0 para cancelar'
        self.printEGPCount = 'Ingresa la cantidad de USD a retirar'
        self.notEnoughHashToTrade = 'No hay suficiente hash para intercambiar'
        self.notEnoughEGP = 'Fondos insuficientes!'
        self.chooseBank = 'Retiros (Pagos)'
        self.bankNotFound = 'no existe tal banco'
        self.EGPReceivingNotAvailable = 'El retiro de USD solo está disponible desde el nivel de minería 3'
        self.faq = """
1. ¿Qué es este robot? Usando este bot en Telegram, puedes ganar USD
2. ¿Cómo funciona? Cada clic te otorga cierta potencia en nuestros servidores, permitiéndote minar criptomonedas.
3. ¿Cómo empezar a ganar dinero? Seleccione el elemento del menú Ganar Hash 💰 y presione Iniciar minería ⛏️ para comenzar a ganar. Por cada clic obtendrás una determinada cantidad de hash, que podrás cambiar por USD y retirar
4. ¿Cómo cambiar hash a USD? Haga clic en el botón Intercambiar Hash Ganado 🔄, luego ingrese la cantidad de USD
5. ¿Cómo retirar dinero? El retiro está disponible desde el nivel de minería 3. Para retirar fondos, debe seleccionar el elemento del menú Obtener pago 💵
6. ¿Por qué deberíamos subir el listón? Cada nivel aumenta la cantidad de hash extraído por clic. Para subir de nivel, debes recolectar una cierta cantidad de hachís.
7. ¿Cómo ganar más? Para ganar, hemos introducido un sistema de referencias y tareas de patrocinadores.
8. ¿Cómo ganar dinero en el sistema de referencias? Desde el elemento del menú, debe obtener el enlace de referencia y enviárselo a sus amigos para que se registren.
9. ¿Cuánto tiempo se tarda en pagar? Alrededor de 3-7 días hábiles
10. ¿Cuáles son los deberes de un pastor? Para poder pagar a todos los usuarios de nuestro bot, publicitamos diferentes personas y empresas. Por utilizar activamente nuestros anuncios, también le pagamos por ello. Ve a la lista 💸 con más dinero y conoce las reglas respecto a solicitudes de patrocinadores
11. ¿De dónde obtenemos dinero para los usuarios que pagan? Hoy en día, las criptomonedas generan enormes cantidades de dinero. Por eso creamos esta forma de minar criptomonedas, para que todos los participantes obtengan ganancias. Además, proporcionamos publicidad de diferentes blogueros y empresas estrechamente relacionadas con las criptomonedas."""
        self.printPromo = 'Seleccione un elemento de menú 👇'
        self.wrongPromo = 'Código de promoción no válido'
        self.commandUnknown = 'Lo siento, pero no eres un administrador /start'
        self.notSubscribed = '❌ no estás suscrito al canal ❌'
        self.giftSend = '1200 USD se han agregado exitosamente a su perfil'
        self.bonusAlreadyClaimed = 'La recompensa ya ha sido recibida'