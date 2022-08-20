try:
    import usocket as socket  # importing socket
except:
    import socket
import machine
import network  # importing network
import esp  # importing ESP
from config import save_ssid_password, load_ssid_password, enable_ssid_password
import gc
import time
from machine import Timer


def web_server_for_ssid_password():
    HOST = ''
    PORT = 80

    # Read index.html, put into HTTP response data
    index_content = ""

    file = open('index.html', 'r')
    index_content += str(file.read())
    file.close()

    # Read reg.html, put into HTTP response data
    # reg_content = '''
    # HTTP/1.x 200 ok
    # Content-Type: text/html
    #
    # '''
    #
    # file = open('reg.html', 'r')
    # reg_content += file.read()
    # file.close()

    # Read picture, put into HTTP response data
    # file = open('T-mac.jpg', 'rb')
    # pic_content = '''
    # HTTP/1.x 200 ok
    # Content-Type: image/jpg
    #
    # '''
    # pic_content += file.read()
    # file.close()

    # Configure socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(100)
    print("web server listening on port:", PORT)

    # infinite loop
    while True:
        # maximum number of requests waiting
        conn, addr = sock.accept()
        should_reboot = False
        try:
            recv = conn.recv(1024)
            print("receive", len(recv), "  ", recv)
            request = str(recv).replace("b'", "")[:-1]
            method = str(request.split(' ')[0]).replace("b'", "")
            src = request.split(' ')[1].replace(" ", "")

            print('Connect by: ', addr)
            # print('Request is:\n', request)
            print("method: ", method)
            print("src is: ", src)
            content = ""
            # deal wiht GET method
            if method == 'GET':
                if src == '/index.html' or src == '/':
                    content = index_content
                elif src == '/T-mac.jpg':
                    # content = pic_content
                    continue
                else:
                    continue

                if len(content) > 0:
                    conn.send(str.encode('HTTP/1.0 200 OK\n'))
                    conn.send(str.encode('Content-Type: text/html\n'))
                    conn.send(str.encode('\n'))
                    conn.send(str.encode(content))
                    # time.sleep(0.1)
            # deal with POST method
            elif method == 'POST':

                recv = conn.recv(1024)
                print("second  receive", len(recv), "  ", recv)
                request = str(recv).replace("b'", "")[:-1]

                print("request", request)
                form = request.split("\\r\\n")
                print("form", form)
                entry = form[-1]  # main content of the request
                print("entry", entry)
                params = entry.split("&")
                print("param", params)
                k = {}
                for param in params:
                    # print(param)
                    key = param.split("=")[0]
                    value = param.split("=")[1]
                    # 替换特殊字符
                    value = value.replace("%60", "`")
                    value = value.replace("%5B", "[")
                    value = value.replace("%5D", "]")
                    value = value.replace("%5C", "\\")
                    value = value.replace("%3B", ";")
                    value = value.replace("%27", "'")
                    value = value.replace("%2C", ",")
                    value = value.replace("%2F", "/")

                    value = value.replace("%3D", "=")
                    value = value.replace("%2B", "+")

                    value = value.replace("%7B", "{")
                    value = value.replace("%7D", "}")
                    value = value.replace("%7C", "|")
                    value = value.replace("%3A", ":")
                    value = value.replace("%22", "\"")
                    value = value.replace("%3C", "<")
                    value = value.replace("%3E", ">")
                    value = value.replace("%3F", "?")

                    value = value.replace("%7E", "~")
                    value = value.replace("%21", "!")
                    value = value.replace("%40", "@")
                    value = value.replace("%23", "#")
                    value = value.replace("%24", "$")
                    value = value.replace("%25", "%")
                    value = value.replace("%5E", "^")
                    value = value.replace("%26", "&")
                    value = value.replace("%28", "(")
                    value = value.replace("%29", ")")

                    print("k-v", key, value)
                    k[key] = value
                print(k)
                if len(k["SSID"]) > 0 and len(k["Password"]) >= 6:
                    save_ssid_password(k)
                    should_reboot = True

                    content = '<html><body>'
                    content += k["SSID"] + "      " + k["Password"] + "      ! Reboot Please Waiting..."
                    content += "</body></html>"
                else:
                    content = index_content

                if len(content) > 0:
                    conn.send(str.encode('HTTP/1.0 200 OK\n'))
                    conn.send(str.encode('Content-Type: text/html\n'))
                    conn.send(str.encode('\n'))
                    conn.send(str.encode(content))
                    time.sleep(0.1)
        except Exception as e:
            print("Exception", e)
            pass

        # close connection
        conn.close()
        if should_reboot:
            print("ap_start now reboot --- !")
            machine.reset()


def callback_timer0(timer):
    timer.deinit()
    print("timer 0 incoming..............reboot......")
    machine.reset()
    pass


def ap_start():
    esp.osdebug(None)
    gc.collect()
    ssid = 'ESP_AP'  # Set access point name
    password = '12345678'  # Set your access point password

    # wdt = WDT() # 2 minute dog
    timer0 = Timer(-1)
    timer0.init(period=1000 * 120, mode=Timer.PERIODIC, callback=callback_timer0)

    enable_ssid_password()

    ap = network.WLAN(network.AP_IF)
    ap.active(True)  # activating

    # s = ap.config('mac')
    # print(ap.config())
    # myid = ('%02x%02x%02x%02x%02x%02x') %(s[0],s[1],s[2],s[3],s[4],s[5])
    # ssid=ssid+myid
    # print(ssid)

    ap.config(essid=ssid, password=password)

    while ap.active() == False:
        time.sleep(0.1)
        pass
    print('Connection is successful')
    print(ap.ifconfig())

    web_server_for_ssid_password()


if __name__ == "__main__":
    ap_start()
