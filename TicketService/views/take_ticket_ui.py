#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'doever'
__date__ = '2018/8/30 10:14'

import sys
import copy

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import QCoreApplication, Qt

from TicketService.utils.build_style import *
from TicketService.settings import *
from TicketService.views.base_ui import DefaultViewMiXin


class TakeTicketView(QWidget, DefaultViewMiXin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clean_ui(self)
        self.setup_ui()

    def setup_ui(self):
        pass


if __name__ == '__main__':
    Bus = []

    a = {
        "businessId": 14,
        "businessNumber": 5,
        "businessName": "征地养老",
        "ticketButtonShowLevel": "one_level",
        "businessHandleAmEndTime": "12:0:0",
        "businessHandlePmBeginTime": "12:0:0",
        "businessAmPeopleLimit": 999,
        "businessPmPeopleLimit": 999,
        "showWaitPeople": "显示",
        "ticketButtonXLocation": 200,
        "ticketButtonYLocation": 450,
        "style": {
            "labelStyle": {
                "font-size": 18,
                "font-family": "宋体",
                "color": "blue"
            },
            "buttonStyle": {
                "font-size": 28,
                "font-family": "楷体",
                "color": "black",
                "border-image": "../static/images/button.png/",
                "pressed-image": "../static/images/button_sx.png/"
            }
        }
    }

    b = copy.deepcopy(a)
    c = copy.deepcopy(a)
    d = copy.deepcopy(a)

    b['businessName'] = "测试业务"
    c['businessName'] = "综合业务"
    d['businessName'] = "医疗业务"
    li = []
    li.append(a)
    li.append(b)
    li.append(c)
    li.append(d)

    App = QApplication(sys.argv)
    Vi = TakeTicketView(li)
    Vi.show()
    sys.exit(App.exec_())