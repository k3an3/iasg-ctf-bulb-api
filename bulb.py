#!/usr/bin/env python3
"""
bulb.py
~~~~~~~
Part of https://github.com/keaneokelley/home

This module is for communicating with the MagicHome LED bulb over the network.

Wire protocol:

-------------------------------------
|header(1)|data(5-70)|0f|checksum(1)|
-------------------------------------

header:
    31 color & white
    41 camera
    51 custom
    61 function

color, white, camera (8 bytes):
    00-ff red
    00-ff green
    00-ff blue
    00-ff white
    mode:
        0f white
        f0 color

functions (5 bytes):
    25-38 modes
    1f-01 speed (decreasing)
    0f who knows

custom (70 bytes):
    64 bytes of r, g, b, 0 (empty color is 0x01020300)
    1f-01 speed (decreasing)
    3a,3b,3c gradual, jumping, strobe
    ff tail

tail:
    0f
    checksum (sum of data fields)
"""
import socket
import sys
from typing import Dict

SUPPORTED_MODES = ['31', '41', '61']
SUPPORTED_FUNCTIONS = list(range(25, 39))
TAIL = '0f'

seven_color_cross_fade = 0x25
red_gradual_change = 0x26
green_gradual_change = 0x27
blue_gradual_change = 0x28
yellow_gradual_change = 0x29
cyan_gradual_change = 0x2a
purple_gradual_change = 0x2b
white_gradual_change = 0x2c
red_green_cross_fade = 0x2d
red_blue_cross_fade = 0x2e
green_blue_cross_fade = 0x2f
seven_color_strobe_flash = 0x30
red_strobe_flash = 0x31
green_strobe_flash = 0x32
blue_stobe_flash = 0x33
yellow_strobe_flash = 0x34
cyan_strobe_flash = 0x35
purple_strobe_flash = 0x36
white_strobe_flash = 0x37
seven_color_jumping = 0x38

prepare_hex = lambda x: format(x, 'x').zfill(2)

CONTROL_PORT = 5577


def num(n: int):
    try:
        return int(n)
    except ValueError:
        return 0


class Bulb:
    """
    A class representing a single MagicHome LED Bulb.
    """

    def __init__(self, host: str):
        self.host = host

    def change_color(self, red: int = 0, green: int = 0, blue: int = 0, white: int = 0, brightness: int = 255,
                     mode: str = '31', function: str = None, speed: str = '1f') -> None:
        """
        Provided RGB values and a brightness, change the color of the
        bulb with a TCP socket.
        """
        if mode not in SUPPORTED_MODES:
            raise NotImplementedError

        if function:
            if num(function) not in SUPPORTED_FUNCTIONS:
                raise NotImplementedError
            data = bytearray.fromhex(mode + function + speed + TAIL)
        else:
            red = num(red * brightness / 255)
            green = num(green * brightness / 255)
            blue = num(blue * brightness / 255)
            white = num(white * brightness / 255)
            color_hex = (prepare_hex(red) + prepare_hex(green) + prepare_hex(blue)
                         + prepare_hex(white))
            if white:
                color_mode = '0f'
            else:
                color_mode = 'f0'
            # Build packet
            data = bytearray.fromhex(mode + color_hex
                                     + color_mode + TAIL)
        try:
            # Compute checksum
            data.append(sum(data) % 256)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, CONTROL_PORT))
            sock.send(data)
            sock.close()
        except Exception as e:
            print(e)

    def fade(self, start: Dict = None, stop: Dict = None, bright: int = None, speed: int = 1) -> None:
        speed = abs(speed)
        if start:
            bright = bright or 255
            while bright > 0:
                self.change_color(**start, brightness=bright, mode='41')
                bright -= speed
        if stop:
            bright = bright or 0
            while bright < 255:
                self.change_color(**stop, brightness=bright, mode='41')
                bright += speed

    def off(self):
        self.change_color(white=0)

    def on(self):
        self.change_color(white=255)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit('Nope')
    colors = list(map(lambda x: int(x), sys.argv[2:]))
    print(colors)
    b = Bulb(sys.argv[1])
    b.change_color(*colors)
