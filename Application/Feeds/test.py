
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("python.org" , 80))
s.sendall(b"GET / HTTP/1.1\n\n")
print(s.recv(4096))
s.close()