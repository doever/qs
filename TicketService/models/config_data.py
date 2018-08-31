#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'doever'
__date__ = '2018/8/31 9:26'

from utils.config_related import ConfigMixin, RequestsMixin
from TicketService.settings import *


class Config(ConfigMixin):
    def __init__(self):
        pass
        # self.Config_Data = super().read_service_config()

    def config_parser(self):
        pass

    def get_backed_service(self) -> tuple:
        Data_Dict = self.config_reader(BACKED_SERVICE_PATH)
        try:
            Data = Data_Dict['lzqs']
        except KeyError:
            raise KeyError(f"{BACKED_SERVICE_PATH}文件配置错误!")
        else:
            Backed_Ip = Data.get('ip', '')
            Back_Port = Data.get('port', '')
            Org_Id = Data.get('org_id', '')
            return Backed_Ip, Back_Port, Org_Id


Back_Config = Config()


if __name__ == '__main__':
    c = Config()
    a = c.get_backed_service()
    print(a)
    print(type(a))
