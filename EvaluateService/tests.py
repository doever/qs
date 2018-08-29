#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'doever'
__date__ = '2018/8/23 10:13'

import socket
from network import Network


class Test(Network):
    def __init__(self):
        super().__init__()

    def run(self):
        self.udp_send({"type": 9}, ('192.168.5.113', 707))


if __name__ == '__main__':
    t = Test()
    t.run()
