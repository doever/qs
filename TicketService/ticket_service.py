#!/usr/bin/python3
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout
from PyQt5.QtGui import QIcon, QPainter, QPixmap
# 数据
from TicketService.models.org_data import Org_Data
from TicketService.models.business_data import Business_Data
# 视图
from TicketService.views.base_ui import DefaultViewMiXin
from TicketService.views.select_org_ui import SelectOrgView
from TicketService.views.take_ticket_ui import TakeTicketView
# 设置
from TicketService.settings import *


class TicketService(QMainWindow, DefaultViewMiXin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clean_ui(self)
        self.setWindowIcon(QIcon('../static/images/TicketSTray.ico'))
        self.start()

    def paintEvent(self, event):
        # 添加背景图片
        painter = QPainter(self)
        pixmap = QPixmap("static/images/background.png")
        painter.drawPixmap(self.rect(), pixmap)

    def start(self):
        print("-"*30)
        print(Org_Data.Multiple_Org_Dict)
        if len(ORG_LIST) > 1:
            First_View = SelectOrgView(Org_Data.Org_Ui_List)
        else:
            First_View = TakeTicketView(Business_Data.get_business_data()['1'])
        # First_View = TakeTicketView() if len(ORG_LIST)>1 else SelectOrgView(Org_Data.Org_Ui_List)
        self.setCentralWidget(First_View)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Vi = TicketService()
    Vi.show()
    sys.exit(App.exec_())