import os

print(os.listdir("."))
print("tiger esp boot ! ")
import time
import gc

from tiger_mqtt_1 import run
from ap_web_server import ap_start
from config import save_ssid_password, load_ssid_password, has_ssid_password, reset_status, get_status, load_status
import machine

if __name__ == "__main__":
    maincounter = 0
    reset_status()
    while True:
        try:
            gc.collect()
            if has_ssid_password() == 1:
                print("has ssid password")
                run()
            else:
                print("no ssid password")
                ap_start()
        except:
            time.sleep(30)
            machine.reset()
        finally:
            time.sleep(10)
            maincounter += 1
            print("main loop counter ---------------", maincounter, "----------------")
