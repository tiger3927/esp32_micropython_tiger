import socket
import re

HOST = ''
PORT = 8000

# Read index.html, put into HTTP response data
index_content = '''
HTTP/1.x 200 ok
Content-Type: text/html

'''

file = open('index.html', 'r')
index_content += file.read()
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

# infinite loop
while True:
    # maximum number of requests waiting
    conn, addr = sock.accept()

    request = str(conn.recv(1024)).replace("b'", "")
    method = str(request.split(' ')[0]).replace("b'", "")
    src = request.split(' ')[1].replace(" ","")

    print('Connect by: ', addr)
    #print('Request is:\n', request)
    print("method: ", method)
    print("src is: ", src)
    content=""
    # deal wiht GET method
    if method == 'GET':
        if src == '/index.html' or src == '/':
            content = index_content
        elif src == '/T-mac.jpg':
            #content = pic_content
            pass
        elif re.match('^/\?.*$', src):
            entry = src.split('?')[1]  # main content of the request
            content = 'HTTP/1.x 200 ok\r\nContent-Type: text/html\r\n\r\n'
            content += entry
            content += '<br /><font color="green" size="7">register successs!</p>'
        else:
            pass

    # deal with POST method
    elif method == 'POST':
        form = request.split('\r\n')
        entry = form[-1]  # main content of the request
        content = 'HTTP/1.x 200 ok\r\nContent-Type: text/html\r\n\r\n'
        content += entry
        content += '<br /><font color="green" size="7">register successs!</p>'

    conn.sendall(bytes(content, encoding = "utf8"))

    # close connection
    conn.close()
