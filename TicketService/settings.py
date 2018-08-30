#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'doever'
__date__ = '2018/8/29 10:55'

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEBUG = True

TEST_BUTTON_STYLE = {"color": "blue",
                     "font-size": "24",
                     "border-image": "../static/images/button.png",
                     "pressed-image": "../static/images/button_sx.png"
                     }


if __name__ == '__main__':
    print(BASE_DIR)
    print(STATIC_ROOT)