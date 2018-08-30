#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'doever'
__date__ = '2018/8/29 11:16'

import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QPainter, QPixmap

from TicketService.settings import STATIC_ROOT, BASE_DIR
from TicketService.utils.build_style import *


TEST_BUTTON_STYLE_1 = {
                     "color": "blue",
                     "font-size": "24px",
                     "border-image": "../static/images/button.png",
                     "pressed-image": "../static/images/button_sx.png"
                     }

TEST_BUTTON_STYLE_2 = {
                     "color": "red",
                     "font-size": "24",
                     # "border-image": "../static/images/button.png",
                     "pressed-image": "../static/images/button_sx.png"
                     }

TEST_BUTTON_STYLE_3 = {
                     "color": "red",
                     "font-size": "24",
                     "border": "10",
                     "text-align": "left",
                     "border-image": "../static/images/button.png",
                     "pressed-image": "../static/images/button_sx.png"
                     }

TEST_BUTTON_STYLE = TEST_BUTTON_STYLE_1


class TestBuildButtonStyle(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # layout = QHBoxLayout()
        self.setup_ui()
        self.Button = QPushButton('业务1', self)
        build_button(Button=self.Button, Style=TEST_BUTTON_STYLE, Coord=(150, 150))

    def setup_ui(self):
        '''初始化界面'''
        # self.paintEvent(self)
        # 去除无边界
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 窗口透明
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 全屏显示
        # self.showFullScreen()
        self.setGeometry(280, 80, 800, 600)
        # 窗口的icon
        self.setWindowIcon(QIcon(os.path.join(STATIC_ROOT, 'images/TicketSTray.ico')))
        # 添加业务按钮
        # self.init_business()

    def paintEvent(self, event):
        # 添加背景图片
        painter = QPainter(self)
        pixmap = QPixmap(os.path.join(STATIC_ROOT, "images/background.png"))
        painter.drawPixmap(self.rect(), pixmap)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Vi = TestBuildButtonStyle()
    Vi.show()
    sys.exit(App.exec_())