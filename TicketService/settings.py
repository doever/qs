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


BACKED_SERVICE_PATH = {
                        # os.path.join(BASE_DIR, 'lzqs.ini'),
                        '../lzqs.ini',
                        }

TEST_BUTTON_STYLE = {
                        "color": "blue",
                        "font-size": "24",
                        "border-image": "../static/images/button.png",
                        "pressed-image": "../static/images/button_sx.png"
                     }

ORG_LIST = ['1', '2', '3']

URL_MAP = {
                "multiple_org": "multiple_org_ticket_service_config",
                "ticket_service": "ticket_service_list",
                "business_list": "business_list",
                "bus_wait_count": "bus_wait_count",
                "ticket_func": "ticket_func",
                "ticket_begin": "ticket_begin",
                "ticket_end": "ticket_end",
                "ticket_validate": "ticket_reserve_validate",
            }

DEFAULT_ORG_STYLE = {
                        "font-size": "24",
                        "color": "red",
                        "background-color": "blue",
                        "pressed-color": "black",
                    }

if __name__ == '__main__':
    print(BASE_DIR)
    print(STATIC_ROOT)