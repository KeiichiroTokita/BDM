# 人感センサ・天気情報を入力し、三色LED・音声を出力する。

import RPi.GPIO as GPIO
import time, sys
from time import sleep
import urllib.request as req
import json, subprocess


# ポート番号の指定
PORT_R = 4
PORT_G = 2
PORT_B = 3
SENSOR_PORT = 27

# GPIOポートの初期化 --- (*1)
GPIO.setmode(GPIO.BCM)  # BCMモードに設定
ports = [PORT_R, PORT_G, PORT_B]
for port in ports:
    GPIO.setup(port, GPIO.OUT)

GPIO.setup(SENSOR_PORT, GPIO.IN)

# LEDをRGBの指定の色に設定 --- (*2)
def set_color(r, g, b):
    GPIO.output(PORT_R, r) # 赤のLEDを操作
    GPIO.output(PORT_G, g) # 緑のLEDを操作
    GPIO.output(PORT_B, b) # 青のLEDを操作

#天気関連

# 天気予報のJSONデータをダウンロード
id = "130010" # 東京
url = "http://weather.livedoor.com/forecast/webservice/json/v1?city=" + id
savename = "tenki.json"
req.urlretrieve(url, savename)

# JSONファイルを解析
data = json.load(open(savename, "r", encoding="utf-8"))
#print(data)

today_weather = data['forecasts'][0]['telop']
today_rainy = '雨' in today_weather #True:雨 False:降らない

#ライトの点灯

try:
    ntime = 0 # LED点灯時間を管理する変数 --- (*2)

    # 繰り返しセンサーの値を得る --- (*3)
    while True:
        v = GPIO.input(SENSOR_PORT)
        if v == GPIO.HIGH:
            if ntime <= 0:
                if today_rainy == True:
                    set_color(0, 0, 1) #雨：青色
                else:
                    set_color(1, 0, 0) #晴：赤色
            ntime = 10
        else:
            ntime -= 1 # 点灯管理変数を1減らす
            if ntime < 0:
                set_color(0, 0, 0)
        print(v, ntime)
        sleep(0.1)


except KeyboardInterrupt:
    pass
GPIO.cleanup() # クリーンアップ
