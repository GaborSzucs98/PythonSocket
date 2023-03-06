from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct
from select import select
import sys
import random

server_addr = ('', int(sys.argv[2]))
pack = struct.Struct('1s I')

n = random.randint(1,100)
print (n)

with socket(AF_INET, SOCK_STREAM) as server:
	win = 0
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
				data = s.recv(pack.size)
				if not data:
					socketek.remove(s)
					s.close()
				else:
					while not win:
						unpdata = pack.unpack(data)
						if not unpdata[0].decode() == '=' :
							x = eval(str(n)+' '+unpdata[0].decode()+' '+str(unpdata[1]))
							if not x :
								a = "N"
								ans= (a.encode(),int(0))
								packed = pack.pack(*ans)
								s.sendall(packed)
							else :
								a = "I"
								ans= (a.encode(),int(0))
								packed = pack.pack(*ans)
								s.sendall(packed)
						else :
							x = eval(str(n)+' '+unpdata[0].decode()+unpdata[0].decode()+' '+str(unpdata[1]))
							if not x :
								a = "K"
								win = 1
								ans= (a.encode(),int(0))
								packed = pack.pack(*ans)
								s.sendall(packed)
							else :
								a = "Y"
								win = 1
								ans= (a.encode(),int(0))
								packed = pack.pack(*ans)
								s.sendall(packed)
						data = s.recv(pack.size)
					if win:
						a = "V"
						ans= (a.encode(),int(0))
						packed = pack.pack(*ans)
						s.sendall(packed)
						socketek.remove(s)
						s.close()