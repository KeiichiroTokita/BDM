import RPi.GPIO as GPIO
import time, sys

# ポート番号の指定
PORT_R = 17
PORT_G = 27
PORT_B = 22
# GPIOポートの初期化 --- (*1)
GPIO.setmode(GPIO.BCM)  # BCMモードに設定 
ports = [PORT_R, PORT_G, PORT_B]
for port in ports:
    GPIO.setup(port, GPIO.OUT)

# LEDをRGBの指定の色に設定 --- (*2)
def set_color(r, g, b):
    GPIO.output(PORT_R, r) # 赤のLEDを操作
    GPIO.output(PORT_G, g) # 緑のLEDを操作
    GPIO.output(PORT_B, b) # 青のLEDを操作

try:
    # 繰り返し色を変える --- (*3)
    while True:
        set_color(1, 0, 0) # 赤
        time.sleep(0.3)
        set_color(0, 1, 0) # 緑
        time.sleep(0.3)
        set_color(0, 0, 1) # 青
        time.sleep(0.3)
except KeyboardInterrupt:
    pass
GPIO.cleanup() # クリーンアップ

