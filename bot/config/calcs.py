def nextLevelCost(level):
    return round(2500 * 1.2 ** (level - 1))


def HashPerClick(level):
    return round(100 * 1.2 ** (level - 1))


def exchangeRateHashToEGP(hashValue):
    return hashValue // exchangeRateEGPToHash(1)


def exchangeRateEGPToHash(egpValue):
    return egpValue * 400
