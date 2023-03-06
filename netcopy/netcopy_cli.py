from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import hashlib
import sys

server_addr = (sys.argv[1], int(sys.argv[2]))
csserver_addr = (sys.argv[3], int(sys.argv[4]))
m = hashlib.md5()
fazon =sys.argv[5]

with socket(AF_INET,SOCK_STREAM) as client:
    with open(sys.argv[6], "rb") as f:
        client.connect(server_addr)
        l = f.read(20)
        while l:
            m.update(l)
            client.sendall(l)
            l = f.read(20)
        m.update(l)
        client.close()
with socket(AF_INET,SOCK_STREAM) as client2:
    client2.connect(csserver_addr)
    size = m.digest_size
    msg = 'BE'+'|'+fazon+'|'+'60'+'|'+str(size)+'|'+str(m.hexdigest())
    client2.sendall(msg.encode())
    ans = client2.recv(20)
    print(ans.decode())
    client2.close()