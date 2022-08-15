from machine import ADC, Pin
from umqtt_simple import MQTTClient
import network
import time
import ntptime

SSID = "edgeai_1"
PASSWORD = "yjkj123456"

led = Pin(2, Pin.OUT, value=0)

SERVER = "yjkj.tech"
CLIENT_ID = "yourClientID"
TOPIC = b"yourTOPIC"
username = 'root'
password = 'tongji12'
state = 0
c = None

print("------------------------")

def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if msg == b"on":
        led.value(1)
        state = 0
        print("1")
    elif msg == b"off":
        led.value(0)
        state = 1
        print("0")
    elif msg == b"toggle":
        # LED is inversed, so setting it to current state
        # value will make it toggle
        led.value(state)
        state = 1 - state


def connectWifi(ssid, passwd):
    global wlan
    wlan = network.WLAN(network.STA_IF)  # create a wlan object
    wlan.active(True)  # Activate the network interface
    # wlan.disconnect()                         #Disconnect the last connected WiFi
    wlan.connect(ssid, passwd)  # connect wifi
    while (wlan.ifconfig()[0] == '0.0.0.0'):
        time.sleep(1)
    print("同步前本地时间：%s" % str(time.localtime()))
    ntptime.NTP_DELTA = 3155644800  # 设置  UTC+8偏移时间（秒），不设置就是UTC0
    ntptime.host = 'ntp1.aliyun.com'  # 可选ntp服务器为阿里云服务器，默认是"pool.ntp.org"
    ntptime.settime()  # 修改设备时间,到这就已经设置好了
    print("同步后本地时间：%s" % str(time.localtime()))


def demo():
    # Catch exceptions,stop program if interrupted accidentally in the 'try'
    try:
        connectWifi(SSID, PASSWORD)
        server = SERVER
        c = MQTTClient(CLIENT_ID, server, 0, username, password)  # create a mqtt client
        c.set_callback(sub_cb)  # set callback
        c.connect()  # connect mqtt
        c.subscribe(TOPIC)  # client subscribes to a topic
        print("Connected to %s, subscribed to %s topic" % (server, TOPIC))

        while True:
            c.wait_msg()  # wait message
    finally:
        if (c is not None):
            c.disconnect()
        wlan.disconnect()
        wlan.active(False)


if __name__ == "__main__":
    demo()

