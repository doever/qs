#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'doever'
__date__ = '2018/8/28 14:37'

import re

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize

from TicketService.settings import STATIC_ROOT, BASE_DIR


# 特殊的样式:pressed-image --> 按下后的背景图片
SPECIAL_STYLE = ['pressed-image', 'pressed-color']
# 需要px单位的样式
PX_STYLE = ['font-size', 'width', 'height', 'border', 'padding', 'margin']
PATH_STYLE = ['border-image', 'background-image', 'pressed-image']


def build_button(Button: QPushButton, Style: dict, Coord: tuple=(0, 0)) -> None:
    '''
    Definition of style
    :param Button:
    :param Style:{"color":"blue","font-size":"24px","border-image":"url(../static/images/button.png)"}
    :param Coord:(150, 150)
    :return:
    '''
    Pre_Sheet = Sheet = ''
    for k, v in Style.items():
        if k in SPECIAL_STYLE:# and k == 'pressed-image':
            if k == 'pressed-image':
                Cell_Sheet = f"border-image:url({Style[k]})"
            else:
                Cell_Sheet = f"background-color:black"
            Pre_Sheet += Cell_Sheet + ";"

        else:
            # 大小样式忘传px
            if k in PX_STYLE and not re.search('px', Style[k]):
                Cell_Sheet = f"{k}:{Style[k]}px"
            else:
                if k in PATH_STYLE:
                    Cell_Sheet = f"{k}:url({Style[k]})"
                else:
                    Cell_Sheet = f"{k}:{Style[k]}"

            Sheet += Cell_Sheet + ";"

    if ('border-image' or 'background-image') in Style.keys():
        path = Style['border-image'] or Style['background-image']
        pix = QPixmap(path)
        Width = pix.width()
        Height = pix.height()
        # print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        # print(Width, Height)
        assert Width and Height, f'背景图片路径传入错误,path:{path}'
    else:
        Width = 400
        Height = 80
    Button_Style = "QPushButton{%s}""QPushButton:pressed{%s}" % (Sheet, Pre_Sheet)
    Button.setStyleSheet(Button_Style)
    # assert 'x' and 'y' in Style.keys(), '设置按钮样式需要传入坐标值'
    Button.setGeometry(Coord[0], Coord[1], Width, Height)


if __name__ == '__main__':
    import re
    a = re.search('px', '24')
    print(a)
