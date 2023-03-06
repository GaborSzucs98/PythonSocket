from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct
import sys

server_addr = (sys.argv[1], int(sys.argv[2]))
packer = struct.Struct('1s I')

op = "<"
eq = "="

def sending(op, n):
	values = (op.encode(), int(n))
	packed_data = packer.pack(*values)
	client.sendall(packed_data)
	print (values)
	
with socket(AF_INET, SOCK_STREAM) as client:
	rmax = 100
	rmin = 1
	current = rmax/2
	end = 0
	client.connect(server_addr)
	while not end and not rmax-rmin == 1:
		sending(op,current)
		data = client.recv(packer.size)
		ans = packer.unpack(data)
		print (ans)
		if ans[0].decode() in ["Y", "V", "K"]:
			end = 1
			client.close()
		elif ans[0].decode() == "I" :
			rmax = current
			current = int((rmax+rmin)/2)
		elif ans[0].decode() == "N" :
			rmin = current
			current= int((rmax+rmin)/2)
	if not end :
		sending(op,rmax)
		data = client.recv(packer.size)
		ans = packer.unpack(data)
		print (ans)
		if ans[0].decode() == "I" :
			sending(eq,rmin)
			data = client.recv(packer.size)
			ans = packer.unpack(data)
			print (ans)
			if ans[0].decode() in ["Y", "V", "K"] :
				end = 1
				client.close()
		else :
			sending(eq,rmax)
			data = client.recv(packer.size)
			ans = packer.unpack(data)
			print (ans)
			if ans[0].decode() in ["Y", "V", "K"] :
				end = 1
				client.close()
				