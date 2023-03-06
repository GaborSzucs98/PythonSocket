from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import sys
from datetime import datetime, timedelta
from select import select

server_addr = (sys.argv[1], int(sys.argv[2]))

lst = []

with socket(AF_INET,SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    socketek = [ server ]
    
    while True:
        r,w,e = select(socketek,[],[],1)
		
        if not (r or w or e):
            continue
        for s in r:
            if s is server:
                client, client_addr = s.accept()
                socketek.append(client)
            else:
                data = s.recv(50)
                if not data:
                    socketek.remove(s)
                    s.close()
                else:
                    dat = data.decode().split('|')
                    if (dat[0] == 'KI'):
                        size = len(lst)
                        index = 0
                        van = False
                        while (index<size and not van):
                            if (lst[index][0] == dat[1]):
                                van = True
                            else:
                                index = index+1
                        if (not van):
                            msg = '0| '
                            s.sendall(msg.encode())
                        else :
                            now = datetime.now()
                            if (now-timedelta(seconds = 60) > lst[index][1]):
                                lst.pop(index)
                                msg = '0| '
                                s.sendall(msg.encode())
                            else:
                                msg = lst[index][2]+'|'+lst[index][3]
                                s.sendall(msg.encode())
                    elif (dat[0] == 'BE'):
                        now = datetime.now()
                        row = (dat[1],now,dat[3],dat[4])
                        lst.append(row)
                        ans = 'OK'
                        s.sendall(ans.encode())