try:
    import os
except:
    import uos as os
import json
from machine import ADC, Pin


def save_ssid_password(k):
    try:
        os.remove("ssid_password.json")
    except:
        pass
    if "enable" in k.keys():
        pass
    else:
        k["enable"] = True
    f = open("ssid_password.json", "w")
    f.write(json.dumps(k))
    f.close()
    print("save_ssid_password")
    print(k)


def load_ssid_password():
    k = None
    try:
        f = open("ssid_password.json", "r")
        k = json.loads(f.read())
        f.close()
        return k
    except Exception as e:
        k = None
    return k


def delete_ssid_password():
    try:
        os.remove("ssid_password.json")
    except:
        pass


def has_ssid_password():
    files = os.listdir(".")
    if "ssid_password.json" in files:
        k = load_ssid_password()
        if k is not None:
            if k["enable"] == True:
                return 1
            else:
                return -1
        else:
            return 0
    else:
        return 0


def disable_ssid_password():
    if has_ssid_password() == 1:
        k = load_ssid_password()
        k["enable"] = False
        save_ssid_password(k)
    else:
        pass


def enable_ssid_password():
    if has_ssid_password() == -1:
        k = load_ssid_password()
        k["enable"] = True
        save_ssid_password(k)
    else:
        pass



switch_1 = Pin(16, Pin.OUT, value=0)
switch_2 = Pin(14, Pin.OUT, value=0)
switch_3 = Pin(12, Pin.OUT, value=0)
switch_4 = Pin(13, Pin.OUT, value=0)
switch_status = {}


def get_status():
    global switch_1, switch_2, switch_3, switch_4, switch_status
    s = {}
    s["switch_1"] = switch_1.value()
    s["switch_2"] = switch_2.value()
    s["switch_3"] = switch_3.value()
    s["switch_4"] = switch_4.value()
    return s


def set_status(status):
    global switch_1, switch_2, switch_3, switch_4, switch_status
    haschange = False
    try:
        if "switch_1" in status.keys():
            if switch_status["switch_1"] != status["switch_1"]:
                switch_status["switch_1"] = status["switch_1"]
                haschange = True
        if "switch_2" in status.keys():
            if switch_status["switch_2"] != status["switch_2"]:
                switch_status["switch_2"] = status["switch_2"]
                haschange = True
        if "switch_3" in status.keys():
            if switch_status["switch_3"] != status["switch_3"]:
                switch_status["switch_3"] = status["switch_3"]
                haschange = True
        if "switch_4" in status.keys():
            if switch_status["switch_4"] != status["switch_4"]:
                switch_status["switch_4"] = status["switch_4"]
                haschange = True
    except:
        print("set_status error compare", e)
    if haschange:
        save_status(switch_status)
        switch_1.value(switch_status["switch_1"])
        switch_2.value(switch_status["switch_2"])
        switch_3.value(switch_status["switch_3"])
        switch_4.value(switch_status["switch_4"])

def reset_status():
    global switch_status
    switch_status = get_status()
    s = load_status()
    set_status(s)

def save_status(s: {}):
    if not "switch_1" in s.keys():
        s["switch_1"] = 0
    if not "switch_2" in s.keys():
        s["switch_2"] = 0
    if not "switch_3" in s.keys():
        s["switch_3"] = 0
    if not "switch_4" in s.keys():
        s["switch_4"] = 0
    try:
        os.remove("status.json")
    except:
        pass
    f = open("status.json", "w")
    f.write(json.dumps(s))
    f.close()
    print("save_status", s)


def load_status():
    default_status = {}
    default_status["switch_1"] = 0
    default_status["switch_2"] = 0
    default_status["switch_3"] = 0
    default_status["switch_4"] = 0

    files = os.listdir(".")
    if "status.json" in files:
        try:
            f = open("status.json", "r")
            s = json.loads(f.read())
            f.close()
            print("load_status ", s)
            if not "switch_1" in s.keys():
                print("switch_1" in s.keys())
                s["switch_1"] = 0
            if not "switch_2" in s.keys():
                print("s2")
                s["switch_2"] = 0
            if not "switch_3" in s.keys():
                print("s3")
                s["switch_3"] = 0
            if not "switch_4" in s.keys():
                print("s4")
                s["switch_4"] = 0
        except Exception as e:
            print("load_status error----", e)
            s = default_status
        return s
    else:
        return default_status


def compare_status(currentstatus: {}, target: {}):
    try:
        if currentstatus["switch_1"] != target["switch_1"]:
            return False
        if currentstatus["switch_2"] != target["switch_2"]:
            return False
        if currentstatus["switch_3"] != target["switch_3"]:
            return False
        if currentstatus["switch_4"] != target["switch_4"]:
            return False
        return True
    except Exception as e:
        print("compare_status error----", e)
        return False


if __name__ == "__main__":
    s = load_status()
    s = {}
    save_status(s)
    s = load_status()
    sss = {}
    sss["switch_1"] = 0
    sss["switch_2"] = 0
    sss["switch_3"] = 0
    sss["switch_4"] = 0
    print(compare_status(s, sss))

    # print(has_ssid_password())
    # k = {}
    # k["SSID"] = "edge_ai_tiger"
    # k["Password"]="yjkj123456"
    # save_ssid_password(k)
    # print(has_ssid_password())
    # print(load_ssid_password())
    # disable_ssid_password()
    # print(load_ssid_password())
    # enable_ssid_password()
    # print(load_ssid_password())
    # disable_ssid_password()
