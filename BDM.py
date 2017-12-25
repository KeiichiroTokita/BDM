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
PORT_R2 = 19
PORT_G2 = 6
PORT_B2 = 13
SENSOR_PORT = 27

# GPIOポートの初期化 --- (*1)
GPIO.setmode(GPIO.BCM)  # BCMモードに設定
ports = [PORT_R, PORT_G, PORT_B, PORT_R2, PORT_G2, PORT_B2]
for port in ports:
    GPIO.setup(port, GPIO.OUT)

GPIO.setup(SENSOR_PORT, GPIO.IN)

# LEDをRGBの指定の色に設定 --- (*2)
def set_color(r, g, b):
    GPIO.output(PORT_R, r) # 赤のLEDを操作
    GPIO.output(PORT_G, g) # 緑のLEDを操作
    GPIO.output(PORT_B, b) # 青のLEDを操作

def set_color2(r, g, b):
    GPIO.output(PORT_R2, r) # 赤のLEDを操作
    GPIO.output(PORT_G2, g) # 緑のLEDを操作
    GPIO.output(PORT_B2, b) # 青のLEDを操作

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
today_weather2 = data['forecasts'][0]['temperature']['max']['celsius']
today_cold = (int(today_weather2) <= 10)

# 読み上げ
def exec(cmd):
    r = subprocess.check_output(cmd, shell=True)
    return r.decode("utf-8").strip()

#ライトの点灯

try:
    ntime = 0 # LED点灯時間を管理する変数 --- (*2)

    # 繰り返しセンサーの値を得る --- (*3)
    while True:
        v = GPIO.input(SENSOR_PORT)
        if v == GPIO.HIGH:
            if ntime <= 0:
                if today_rainy == True:
                    if today_cold == True:
                        set_color(0, 0, 1) #雨：青色
                        set_color2(1, 1, 1) #寒い：全部点灯
                        text = "今日は雨です、傘を忘れずに。寒いので防寒対策をしましょう。"
                        # 一文ずつ読み上げる
                        lines = text.split("。")
                        for s in lines:
                            if s == "": continue
                            print(s)
                            exec('./jtalk.sh "' + s + '"')

                    else:
                        set_color(0, 0, 1) #雨：青色
                        set_color2(0, 0, 0) #寒くない：消灯
                        text = "今日は雨です、傘を忘れずに。"
                        # 一文ずつ読み上げる
                        lines = text.split("。")
                        for s in lines:
                            if s == "": continue
                            print(s)
                            exec('./jtalk.sh "' + s + '"')

                else:
                    if today_cold == True:
                        set_color(1, 0, 0) #晴れ：赤色
                        set_color2(1, 1, 1) #寒い：全部点灯
                        text = "今日は晴れますが、寒いので防寒対策をしましょう。"
                        # 一文ずつ読み上げる
                        lines = text.split("。")
                        for s in lines:
                            if s == "": continue
                            print(s)
                            exec('./jtalk.sh "' + s + '"')

                    else:
                        set_color(1, 0, 0) #晴：赤色
                        set_color2(0, 0, 0) #寒くない：消灯

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
