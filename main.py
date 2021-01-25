from machine import Timer
from machine import Pin

index_rear_led = 0
led_rear_left = Pin(2, Pin.OUT)

def connectToWifiAndUpdate():
    import time, machine, network, gc, app.secrets as secrets
    time.sleep(1)
    print('Memory free', gc.mem_free())

    from app.ota_updater import OTAUpdater

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    otaUpdater = OTAUpdater('https://github.com/tremblayraphael29/test_update.git', main_dir='app', secrets_file="secrets.py")
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()

def startApp():
    import app.start

def index_ms():
    global index_rear_led
    index_rear_led += 1
    led(index_rear_led)
    if index_rear_led == 800:
        index_rear_led = 0

def led(i):
    global index_rear_led
    led_rear_left.on() if 0 < i < 50 else False
    led_rear_left.off() if 50 < i < 100 else False
    led_rear_left.on() if 100 < i < 150 else False
    led_rear_left.off() if 150 < i < 200 else False
    index_rear_led = 0 if index_rear_led == 800 else index_rear_led


connectToWifiAndUpdate()
startApp()

tim0 = Timer(0)
tim0.init(period=10, mode=Timer.PERIODIC, callback=lambda t: index_ms())

