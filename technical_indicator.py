
# -*- coding: utf-8 -*-

import requests
import talib
import numpy
from time import time, sleep


#한시간봉 20이평선가격

string1 = '''1INCH-PERP
AAVE-PERP
ADA-PERP
ALGO-PERP
ALT-PERP
AMPL-PERP
ATOM-PERP
AVAX-PERP
BAL-PERP
BCH-PERP
BNB-PERP
BRZ-PERP
BSV-PERP
BTC-PERP
BTMX-PERP
CHZ-PERP
COMP-PERP
CREAM-PERP
CUSDT-PERP
DEFI-PERP
DMG-PERP
DOGE-PERP
DOT-PERP
DRGN-PERP
EOS-PERP
ETC-PERP
ETH-PERP
EXCH-PERP
FIL-PERP
FLM-PERP
GRT-PERP
HNT-PERP
HT-PERP
KNC-PERP
LEO-PERP
LINK-PERP
LTC-PERP
MATIC-PERP
MID-PERP
MKR-PERP
MTA-PERP
NEO-PERP
OKB-PERP
OMG-PERP
PAXG-PERP
PRIV-PERP
RUNE-PERP
SHIT-PERP
SNX-PERP
SOL-PERP
SUSHI-PERP
SXP-PERP
THETA-PERP
TOMO-PERP
TRX-PERP
TRYB-PERP
UNI-PERP
UNISWAP-PERP
USDT-PERP
VET-PERP
WAVES-PERP
XAUT-PERP
XLM-PERP
XRP-PERP
XTZ-PERP
YFI-PERP
ZEC-PERP'''
chunks = string1.split('\n')
# print(chunks)

print(200-time()%60)

def tracker(TICKER):
    global response
    response = requests.get("https://ftx.com/api/markets/{}/candles?resolution=3600".format(TICKER))

    # 파일 만들어서 각자관리하게끔,
    candle = response.json()
    xx = candle['result']

    val = []
    for i in range(len(xx)):
        val.append(xx[i]['close'])
    # 파이썬 넘파이로 변환 
    arr = numpy.array(val)

    ## 이평 구현  == 소스는 클로즈, 길이 20
    MA = talib.SMA(arr, timeperiod=20)
    print(MA[-1])

    f = open("data_{}.py".format(TICKER), "w")
    f.write(str(MA[-1]))
    # return MA[-1]

while True:
    sleep(200-time()%60)
    for TICKER in chunks:
        tracker(TICKER)

 