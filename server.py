#!/usr/bin/env python3
import random
import socket

import os
import threading
from time import sleep

from bulb import Bulb

reg_color = [0xcc, 0x00, 0xcc, 0x00]
reg_color2 = [0xff, 0x3c, 0x00, 0x00]
colors = (reg_color, reg_color2)
reg_brightness = 255
flag = 'flag{lol}'


def flicker():
    for i in range(random.randint(1, 7)):
        sleep(random.randint(0, 200) / 1000)
        threading.Thread(target=bulb.change_color,
                         args=(*(random.choice(colors)), 0)).start()
        sleep(random.randint(100, 300) / 1000)
        threading.Thread(target=bulb.change_color,
                         args=(*(random.choice(colors)), reg_brightness)).start()
    threading.Thread(target=bulb.change_color,
                     args=(*reg_color, reg_brightness)).start()
    threading.Thread(target=bulb.change_color,
                     args=(*reg_color, reg_brightness)).start()
    sleep(10)
    threading.Thread(target=bulb.change_color,
                     args=(*reg_color, 0)).start()
    threading.Thread(target=bulb.change_color,
                     args=(*reg_color, 0)).start()


bulb = Bulb(host='192.168.4.170')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 6010))
s.listen(10)
try:
    while True:
        conn, addr = s.accept()
        print("Got conn from", addr[0])
        buf = conn.recv(32).decode()
        conn.close()
        print('"' + buf + '"')
        if buf == flag:
            print("good flag")
            flicker()
except KeyboardInterrupt:
    s.close()
