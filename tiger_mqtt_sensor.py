from machine import ADC, Pin
import machine
from umqtt_simple import MQTTClient
import network
import time
import ntptime
from config import load_ssid_password, has_ssid_password, disable_ssid_password

wlan = None
myid = "invalid"
switch_1 = Pin(14, Pin.IN)  # D5
switch_2 = Pin(12, Pin.IN)  # D6

clientmqtt: MQTTClient = None


def sub_cb(topic, msg):
    global switch_1, switch_2, switch_3, switch_4, clientmqtt, myid
    print((topic, msg))
    if msg == b"report":
        print("report")
        report_status()
    elif msg == b"info":
        print("report")
        report_status()

def report_status():
    global switch_1, switch_2, clientmqtt, myid
    m = "%1d%1d%1d%1d" % (switch_1.value(), switch_2.value(),0,0)
    t = "esp8266_sensor/report/" + myid
    m = str.encode(m)
    t = str.encode(t)
    clientmqtt.publish(t, m)


def connectWifi(ssid, passwd):
    global wlan, myid
    wlan = network.WLAN(network.STA_IF)  # create a wlan object
    wlan.active(True)  # Activate the network interface
    # wlan.disconnect()                         #Disconnect the last connected WiFi
    wlan.connect(ssid, passwd)  # connect wifi
    count = 0
    while (wlan.ifconfig()[0] == '0.0.0.0'):
        if count > 10:
            print("can't connect wifi !!! disable ssid password ----! REBOOT ----")
            disable_ssid_password()
            machine.reset()
            return
        time.sleep(1)
        count += 1

    s = wlan.config('mac')
    myid = "esp8266_" + ('%02x%02x%02x%02x%02x%02x') % (s[0], s[1], s[2], s[3], s[4], s[5])
    print(myid)

    print("同步前本地时间：%s" % str(time.localtime()))
    try:
        ntptime.NTP_DELTA = 3155644800  # 设置  UTC+8偏移时间（秒），不设置就是UTC0
        ntptime.host = 'pool.ntp.org'  # 'ntp1.aliyun.com'  # 可选ntp服务器为阿里云服务器，默认是"pool.ntp.org"
        ntptime.settime()  # 修改设备时间,到这就已经设置好了
    except Exception as e:
        print(e)
    print("同步后本地时间：%s" % str(time.localtime()))


def run():
    global wlan, switch_1, switch_2, switch_3, switch_4, myid, clientmqtt

    SERVER = "mqtt.lohasapp.com.cn"
    username = 'username'
    password = 'password'

    state = 0
    clientmqtt = None
    # Catch exceptions,stop program if interrupted accidentally in the 'try'
    if has_ssid_password() == 1:
        try:
            k = load_ssid_password()
            connectWifi(k["SSID"], k["Password"])
        except Exception as e:
            print(e)
            print("error connect wifi.....reboot....to get wifi ssid pwd!")
            disable_ssid_password()
            machine.reset()
    else:
        print("has no wifi ssid .......!")
        time.sleep(15)
        machine.reset()

    try:
        server = SERVER
        TOPIC = b"esp8266_sensor/" + str.encode(myid)

        clientmqtt = MQTTClient(myid, server, 0, username, password)  # create a mqtt client
        clientmqtt.set_callback(sub_cb)  # set callback
        clientmqtt.connect()  # connect mqtt
        clientmqtt.subscribe(TOPIC)  # client subscribes to a topic
        print("Connected to %s, subscribed to %s topic" % (server, TOPIC))

        lasttime_ping = time.time()
        lasttime_report = 0.0
        while True:
            if time.time() - lasttime_ping > 30:
                lasttime_ping = time.time()
                clientmqtt.ping()
                print("ping")
            if time.time() - lasttime_report > 10:
                lasttime_report = time.time()
                report_status()
                print("report")
            clientmqtt.check_msg()  # wait message
            time.sleep(0.05)

        if (clientmqtt is not None):
            clientmqtt.disconnect()
        wlan.disconnect()
        wlan.active(False)
    finally:
        time.sleep(30)
        machine.reset()


if __name__ == "__main__":
    run()
