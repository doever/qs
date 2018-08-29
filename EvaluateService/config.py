#!/usr/bin/python3
# -*- coding:utf-8 -*-


import requests
import configparser
import socket
import os
import time
from settings import *


class ConfigBase():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @staticmethod
    def config_parser(File_Path):
        Config_Parser = configparser.ConfigParser()
        while True:
            try:
                Config_Parser.read(File_Path)
                return Config_Parser
            except configparser.NoSectionError:
                print('未读取到配置文件，15秒后重新读取！\n')
                time.sleep(15)

    @staticmethod
    def request(url: str):
        while True:
            try:
                Res = requests.get(url)
                if Res.status_code == requests.codes.ok:
                    break
            except requests.ConnectionError:
                print(f'请求失败，url is {url}\n')
                time.sleep(3)
        return Res


class ConfigMixin():
    def read_service_config(self, Url_Path: str):
        return {"1": "1", "2": "2"}


if __name__ == '__main__':
    config = ConfigBase(path=("back", 'evaluate_service_config'))



