from machine import ADC, Pin
import machine
from umqtt_simple import MQTTClient
import network
import time
import ntptime
from config import load_ssid_password, has_ssid_password, disable_ssid_password, save_status, load_status,\
    compare_status,get_status,set_status,reset_status
import json

wlan = None
myid = "invalid"

clientmqtt: MQTTClient = None


def sub_cb(topic, msg):
    global clientmqtt, myid
    # print((topic, msg))
    if msg == b"welcome":
        report_status()
        return
    try:
        s = json.loads(msg)
    except:
        print("msg json error", msg)
        report_status()
        return
    sss = {}
    if "switch_1" in s.keys():
        sss["switch_1"] = s["switch_1"]
    if "switch_2" in s.keys():
        sss["switch_2"] = s["switch_2"]
    if "switch_3" in s.keys():
        sss["switch_3"] = s["switch_3"]
    if "switch_4" in s.keys():
        sss["switch_4"] = s["switch_4"]
    set_status(sss)
    report_status()


def report_status(firstinfo=False):
    global clientmqtt
    sss = get_status()
    if firstinfo:
        sss["first"] = 1
    else:
        sss["first"] = 0
    m = json.dumps(sss)
    t = "esp8266_switch/info/" + myid
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
    while (wlan.ifconfig()[0] == '0.0.0.0') or not wlan.isconnected():
        if count > 10:
            print("can't connect wifi !!! disable ssid password ----! REBOOT ----")
            disable_ssid_password()
            return False
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
    return True


def run():
    global wlan,myid, clientmqtt

    reset_status()

    SERVER = "mqtt.lohasapp.com.cn"
    username = 'username'
    password = 'password'

    state = 0
    clientmqtt = None
    # Catch exceptions,stop program if interrupted accidentally in the 'try'
    if has_ssid_password() == 1:
        r=False
        try:
            k = load_ssid_password()
            r=connectWifi(k["SSID"], k["Password"])
        except Exception as e:
            print(e)
            print("error connect wifi.....reboot....to get wifi ssid pwd!")
            disable_ssid_password()
            r=False
        if r==False:
            try:
                wlan.disconnect()
            except:
                print("wlan disconnect error")
            try:
                wlan.active(False)
                while (wlan.active() == True):
                    time.sleep(0.1)
            except:
                print("wlan close error")
            return
    else:
        print("has no wifi ssid .......!")
        return

    try:
        server = SERVER
        TOPIC = b"esp8266_switch/" + str.encode(myid)

        clientmqtt = MQTTClient(myid, server, 0, username, password)  # create a mqtt client
        clientmqtt.set_callback(sub_cb)  # set callback
        clientmqtt.connect()  # connect mqtt
        clientmqtt.subscribe(TOPIC)  # client subscribes to a topic
        print("Connected to %s, subscribed to %s topic" % (server, TOPIC))
        report_status(firstinfo=True)
        lasttime = time.time()
        lasttime_info = time.time()
        while True:
            if time.time() - lasttime > 30:
                lasttime = time.time()
                clientmqtt.ping()
            if time.time() - lasttime_info > 60:
                lasttime_info = time.time()
                report_status()
            clientmqtt.check_msg()  # wait message
            time.sleep(0.1)
    except Exception as e:
        print("mqtt  loop  error",e)
    finally:
        try:
            if (clientmqtt is not None):
                clientmqtt.disconnect()
        except:
            print("mqtt disconnect error")
            pass
        try:
            wlan.disconnect()
        except:
            print("wlan disconnect error")
        print("mqtt connection quit-------!----wlan close")
        wlan.active(False)
        while(wlan.active()==True):
            time.sleep(0.1)

if __name__ == "__main__":
    run()

