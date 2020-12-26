# -*- coding: utf-8 -*-
import websocket
import json
import requests
import talib
import numpy
import smtplib
import config
import mailing_list
from time import time, sleep

try:
    import thread
except ImportError:
    import _thread as thread

#BTC 클라이언트 
#기본값 = 0 == 안보냈다, 1==보냈다
flag = 0

#실시간 가격과 비교 
def on_message(ws, message):
    global flag
    x = json.loads(message)
    candle = x['data']['last']
    # print(candle)
  
    f = open("data_LINK-PERP.py", "r")
    content = float(f.read())
    # print(content)

    #이평가와 비교
    if content < candle and flag==0:
        send_email("LINK-PERP", "LONG NOW is {} and MA is {} from SERVER https://ftx.com/trade/LINK-PERP".format(candle,content))
        flag = 1
        print(flag)
    
        #아래로 내려오면 리셋  
    if content > candle and flag==1:
        print("ssss")
        send_email("LINK-PERP", "SHORT NOW is {} and MA is {} from SERVER https://ftx.com/trade/LINK-PERP".format(candle,content))
        flag = 0
        print("RESET")

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

# 워치타워 확장
def on_open(ws):
   ws.send("{\"op\": \"subscribe\", \"market\": \"LINK-PERP\", \"channel\": \"ticker\" }")

# 이메일 보내기 
def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(config.EMAIL_ADDRESS, mailing_list.EMAIL_LIST, message)
        server.quit()
        print("LINK-PERP MAIL SENT")
    except:
        print("EMAIL FAILED")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ftx.com/ws/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever(ping_interval=10)