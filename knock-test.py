import socket

knock_ports = (6666, 9990, 55234, 8792, 65535, 10000)
for port in knock_ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('201.203.200.120', port))
    s.send(b"lol")
    s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('201.203.200.120', 6666))
print(s.recv(1024))
s.close()
