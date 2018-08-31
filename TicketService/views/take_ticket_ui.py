#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'doever'
__date__ = '2018/8/30 10:14'

import re
import sys
import copy

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QCoreApplication, Qt

from TicketService.utils.build_style import build_button, build_label
from TicketService.settings import *
from TicketService.views.base_ui import DefaultViewMiXin

PAGE_BUTTON_STYLE = {
                        "border-image": "../static/images/PageDown.png",
                        "pressed-color": "white"
                    }

BACK_BUTTON_STYLE = {
                        "border-image": "../static/images/back.png",
                        "pressed-color": "white"
                    }


class TakeTicketView(QWidget, DefaultViewMiXin):
    def __init__(self, Business: list, Referrer=None, Page=0, parent=None):
        super().__init__(parent)
        self.Page = Page
        self.Referrer = Referrer
        self.clean_ui(self)
        self.setup_ui(Business)

    def setup_ui(self, Business: list):
        for Item in Business:
            self.Bus_Button = QPushButton(Item['businessName'], self)
            build_button(Button=self.Bus_Button, Style=Item['style']['buttonStyle'], Coord=(Item['ticketButtonXLocation'], Item['ticketButtonYLocation']))
            X = self.Bus_Button.x()
            Y = self.Bus_Button.y()
            W = self.Bus_Button.width()
            H = self.Bus_Button.height()

            if Item['showWaitPeople'] == '显示':
                self.Wait_Label = QLabel(self)
                self.Wait_Label.setText(f"等待人数:{Item['waitNumber']}")
                build_label(self.Wait_Label, Style=Item['style']['labelStyle'])

                if re.search('上', Item['showWaitLocation']):
                    self.Wait_Label.setGeometry(X, Y-H/1.5, W, H)
                elif re.search('下', Item['showWaitLocation']):
                    self.Wait_Label.setGeometry(X, Y+H/1.5, W, H)
                elif re.search('左', Item['showWaitLocation']):
                    self.Wait_Label.setGeometry(X-250, Y, 250, H)
                else:
                    self.Wait_Label.setGeometry(X+250, Y, 250, H)

        if self.Page:
            self.Next_Page_Button = QPushButton("", self)
            build_button(self.Next_Page_Button, Style=PAGE_BUTTON_STYLE, Coord=((self.width()-50)/2, self.height()-140))
            self.Page_Label = QLabel(self)
            self.Page_Label.setText(f"当前:第{self.Page}页,共x页")
            build_label(self.Page_Label, Style={"font-size": 24, "color": "black"})
            self.Page_Label.move((self.width()-180)/2, self.height()-50)

        if self.Referrer:
            self.Back_Button = QPushButton("", self)
            build_button(self.Back_Button, Style=BACK_BUTTON_STYLE, Coord=(self.width()-210, self.height()-140))


if __name__ == '__main__':
    Bus = []

    a = {
        "businessId": 14,
        "businessNumber": 5,
        "businessName": "征地养老",
        "ticketButtonShowLevel": "one_level",
        "ticketButtonShowPage": 1,
        "businessHandleAmEndTime": "12:0:0",
        "businessHandlePmBeginTime": "12:0:0",
        "businessAmPeopleLimit": 999,
        "businessPmPeopleLimit": 999,
        "showWaitPeople": "显示",
        "showWaitLocation": "按钮下侧",
        "waitNumber": 58,
        "ticketButtonXLocation": 200,
        "ticketButtonYLocation": 50,
        "style": {
            "labelStyle": {
                "font-size": 24,
                "font-family": "宋体",
                "color": "blue"
            },
            "buttonStyle": {
                "font-size": 28,
                "font-family": "楷体",
                "color": "black",
                "border-image": "../static/images/button.png",
                "pressed-image": "../static/images/button_sx.png"
            }
        }
    }

    b = copy.deepcopy(a)
    c = copy.deepcopy(a)
    d = copy.deepcopy(a)

    b['businessName'] = "测试业务"
    b['ticketButtonYLocation'] = 200
    c['businessName'] = "综合业务"
    c['ticketButtonYLocation'] = 350
    d['businessName'] = "医疗业务"
    d['ticketButtonYLocation'] = 500

    Bus.append(a)
    Bus.append(b)
    Bus.append(c)
    Bus.append(d)
    print(Bus)
    # x = {"one_level":}

    App = QApplication(sys.argv)
    Vi = TakeTicketView(Business=Bus, Referrer='self.ticket', Page=1)
    Vi.show()
    sys.exit(App.exec_())