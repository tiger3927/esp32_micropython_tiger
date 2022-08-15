try:
    import usocket as socket        #importing socket
except:
    import socket
import network                      #importing network
import esp                          #importing ESP
esp.osdebug(None)
import gc
gc.collect()
ssid = 'ESP_AP'                     #Set access point name
password = '12345678'               #Set your access point password

ap = network.WLAN(network.AP_IF)
ap.active(True)                     #activating
ap.config(essid=ssid, password=password)

while ap.active() == False:
    pass
print('Connection is successful')
print(ap.ifconfig())
def web_page():
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body><h1>Welcome to microcontrollerslab!</h1></body></html>"""
    return html
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
s.bind(('', 80))
s.listen(5)
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    response = web_page()
    conn.send(response)
    conn.close()