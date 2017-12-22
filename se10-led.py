import RPi.GPIO as GPIO
from time import sleep

# GPIOポートの設定 --- (*1)
SENSOR_PORT = 27
LED_PORT = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PORT, GPIO.IN)
GPIO.setup(LED_PORT, GPIO.OUT)

try:
    ntime = 0 # LED点灯時間を管理する変数 --- (*2)
    
    # 繰り返しセンサーの値を得る --- (*3)
    while True:
        v = GPIO.input(SENSOR_PORT)
        if v == GPIO.HIGH:
            if ntime <= 0:
                GPIO.output(LED_PORT, GPIO.HIGH)
            ntime = 10
        else:
            ntime -= 1 # 点灯管理変数を1減らす
            if ntime < 0:
                GPIO.output(LED_PORT, GPIO.LOW)
        print(v, ntime)
        sleep(0.1)

except KeyboardInterrupt:
        pass

GPIO.cleanup()

