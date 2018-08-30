#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'doever'
__date__ = '2018/8/29 11:00'

import sys

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import QCoreApplication, Qt

from TicketService.utils.build_style import *
from TicketService.settings import *
from TicketService.views.base_ui import DefaultViewMiXin


class SelectOrgView(QWidget, DefaultViewMiXin):
    '''多机构选择界面'''
    def __init__(self, Orgs: list, parent=None):
        super().__init__(parent)
        self.clean_ui(self)
        self.setup_ui(Orgs)

    def setup_ui(self, Orgs):
        V_box = QVBoxLayout()
        for Org in Orgs:
            self.Org_Button = QPushButton(Org['org_name'], self)
            build_button(Button=self.Org_Button, Style=Org['org_style'])
            self.Org_Button.setFixedSize(800, 60)
            V_box.addWidget(self.Org_Button)

        Margin_Left = (self.width()-800) / 2

        V_box.setContentsMargins(Margin_Left, 50, Margin_Left, 50)
        V_box.setSpacing(10)
        self.setLayout(V_box)

    def get_self_size(self):
        return self.width(), self.height()


if __name__ == '__main__':
    Org = []

    a = {"org_id": 1,
         "org_name": "测试机构一",
         "org_style": {
             "font-size": "24",
             "color": "red",
             "border-image": "../static/images/order_button.png",
            }
         }

    b = {"org_id": 2,
         "org_name": "测试机构二",
         "org_style": {
             "font-size": "24",
             "color": "red",
             "background-color": "blue",
             "pressed-color": "black",
             # "border-image": "../static/images/order_button.png",
            }
         }
    # Org.append(a)
    for i in range(8):
        Org.append(b)

    App = QApplication(sys.argv)
    Vi = SelectOrgView(Org)
    Vi.show()
    sys.exit(App.exec_())
