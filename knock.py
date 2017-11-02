import socket
from select import select
from threading import Thread
from time import sleep

import datetime

knock_ports = (6666, 9990, 55234, 8792, 65535, 10000)
sockets = []
clients = {}
delays = {}
FLAG = b'flag{real_flag_will_appear_here}'


def return_flag():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 6666))
    s.listen(10)
    while True:
        conn, addr = s.accept()
        if clients.get(addr[0]) and knock_ports[-1] in clients.get(addr[0]):
            print(addr[0], "PASSED")
            conn.send(FLAG)
        conn.close()


def cleanup():
    while True:
        sleep(10)
        print("cleaning")
        print(delays)
        for delay in delays:
            if delays[delay] and (datetime.datetime.now() - delays[delay]).seconds >= 10:
                print("deleting", delay)
                del clients[delay]
                delays[delay] = None


for port in knock_ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', port))
    sockets.append(s)

Thread(target=cleanup).start()
Thread(target=return_flag).start()
while True:
    r, _, _ = select(sockets, (), ())
    for s in r:
        buf, addr = s.recvfrom(32)
        port = s.getsockname()[1]
        delays[addr[0]] = datetime.datetime.now()
        print(addr[0], port)
        if clients.get(addr[0]):
            index = knock_ports.index(port)
            if index == 0 or knock_ports[index - 1] in clients[addr[0]]:
                clients[addr[0]].add(port)
        else:
            clients[addr[0]] = set()
            clients[addr[0]].add(port)
