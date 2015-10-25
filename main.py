# main.py -- put your code here!

from machine import Pin
import time

led = Pin("GP16", Pin.OUT)

led.toggle()

def log(msg):
    print(msg)

def btnPressed(pin):
    led.toggle()
    time.sleep_us(100)

btn = Pin("GP17", Pin.IN, Pin.PULL_UP)
btn.irq(trigger=Pin.IRQ_FALLING, handler=btnPressed)

def home():
    global wifi
    if wifi.mode() != WLAN.STA:
        wifi.mode(WLAN.STA)
    wifi.connect(config.HOME_SSID, auth=(WLAN.WPA, config.HOME_PASSWORD))

def tc():
    global t, p
    import theta
    t = theta.Theta()
    p = t.connect()
    if not p:
        print("Connect failed!")
    else:
        answer = t.initPTP()
        print(answer)
