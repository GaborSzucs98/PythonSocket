from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import hashlib
import sys

server_addr = (sys.argv[1], int(sys.argv[2]))
csserver_addr = (sys.argv[3], int(sys.argv[4]))
m = hashlib.md5()

with socket(AF_INET,SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)
    client, client_addr = server.accept()
    end = False
    with open(sys.argv[6], "wb") as f:
        while not end:
            data = client.recv(20)
            if data:
                m.update(data)
                f.write(data)
            else:
                client.close()
                end = True
                
with socket(AF_INET,SOCK_STREAM) as client:
    client.connect(csserver_addr)
    msg = 'KI'+'|'+sys.argv[5]
    client.sendall(msg.encode())
    ans = client.recv(50)
    anss = ans.decode().split('|')
    if (int(anss[0]) == m.digest_size and anss[1] == m.hexdigest()):
        print('CSUM OK')
    else:
        print('CSUM CORRUPTED')
    client.close()