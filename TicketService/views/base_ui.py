#!/usr/bin/python3
# -*- coding:utf-8 -*-

from PyQt5.QtCore import Qt
from TicketService.settings import DEBUG


class DefaultViewMiXin():
    @staticmethod
    def clean_ui(self):
        # 去除窗口边界
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 窗口透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        if DEBUG:
            self.setGeometry(30, 30, 1300, 700)
        else:
            self.showFullScreen()
