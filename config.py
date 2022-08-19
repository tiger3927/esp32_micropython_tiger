try:
    import os
except:
    import uos as os
import json


def save_ssid_password(k):
    try:
        os.remove("ssid_password.json")
    except:
        pass
    if "enable" in k.keys():
        pass
    else:
        k["enable"]=True
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
        k=load_ssid_password()
        if k is not None:
            if k["enable"]==True:
              return 1
            else:
              return -1
        else:
            return 0
    else:
        return 0
        
def disable_ssid_password():
  if has_ssid_password()==1:
    k=load_ssid_password()
    k["enable"]=False
    save_ssid_password(k)
  else:
    pass

def enable_ssid_password():
  if has_ssid_password()==-1:
    k=load_ssid_password()
    k["enable"]=True
    save_ssid_password(k)
  else:
    pass



if __name__ == "__main__":
    print(has_ssid_password())
    k = {}
    k["SSID"] = "edge_ai_tiger"
    k["Password"]="yjkj123456"
    save_ssid_password(k)
    print(has_ssid_password())
    print(load_ssid_password())
    disable_ssid_password()
    print(load_ssid_password())
    enable_ssid_password()
    print(load_ssid_password())
    disable_ssid_password()


