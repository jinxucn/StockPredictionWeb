import talib as ta
import numpy as np
import matplotlib.pyplot as plt

def MACD(price):
    dif,dea,hist = ta.MACD(price)
    ema12=ta.EMA(price,12)
    ema26=ta.EMA(price,26)
    return hist[-15:]

def Bollinger_Bands(price,tp):
    price30d=price[-30:]
    upper, middle, lower = ta.BBANDS(np.asarray(price30d), timeperiod=tp, nbdevup=1, nbdevdn=1, matype=0)
    # plt.plot(price30d)
    # plt.plot(upper)
    # plt.plot(middle)
    # plt.plot(lower)
    # plt.show()
    return upper[15:],middle[15:],lower[15:]

def KDJ(high,low,close):
    slowk,slowd=ta.STOCH(high,low,close,
                         fastk_period=9,
                        slowk_period=3,
                        slowk_matype=0,
                        slowd_period=3,
                        slowd_matype=0)
    return slowk[12:],slowd[12:]