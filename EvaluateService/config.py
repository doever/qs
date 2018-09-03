#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import socket

from EvaluateService.config_related import ConfigMixin


SOCKET_RECEIVE_SIZE = 512
REBOOT_CODE = 9
LOCAL_CONFIG_NAME = 'lzqs.ini'


def check_result(func):
    def wrapper(self, Data, *args, **kwargs):
        assert isinstance(Data, dict), '传入数据类型错误'
        # assert 'evaluate' in Data.keys(), '配置数据中无evaluate'
        if Data['resCode'] != 0:
            print(f"系统未找到服务配置")
            return None
        return func(self, Data, *args, **kwargs)
    return wrapper


class EvaluateConfig(ConfigMixin):
    def __init__(self):
        pass
        self.Config_Data = super().read_service_config('evaluate_service_config')

    def config_parser(self, Url_Path: tuple) -> dict:
        File_Path = f"{os.getcwd()}\\{LOCAL_CONFIG_NAME}"
        Config_Parse = EvaluateConfig.config_reader({File_Path})
        try:
            Settings = (Config_Parse['lzqs']['ip'],
                        Config_Parse['lzqs']['port'],
                        Config_Parse['lzqs']['org_id'])
        except KeyError:
            print(f'文件:{File_Path}配置错误')
        else:
            Url_Path = '/'.join(Url_Path)
            Url = f"http://{Settings[0]}:{Settings[1]}/{Url_Path}/{Settings[2]}"
            print(f"请求地址:{Url}")
            Res = self.request(Url_Path, 'get')
            return Res

    @check_result
    def get_service_address(self, Config_Data: dict, Service_Name='evaluate') -> list:
        '''
        获取服务的ip和port信息
        :param: service name, dict data
        :return: service address list
        '''
        Service_Name = Service_Name.lower()
        Ip_List = socket.gethostbyname_ex(socket.gethostname())[2]
        Service_Address_List = []
        # if Config_Data['resCode'] != 0:
        #     print(f"系统未配置{Service_Name}服务")
        #     return Service_Address_List
        try:
            Service_Config_Msg = Config_Data[Service_Name]
            for i in Service_Config_Msg:
                Service_Ip = i[f'{Service_Name}ServiceIp']
                Service_Port = i[f'{Service_Name}ServicePort']
                # Service_Address = (Service_Ip, Service_Port) if Service_Ip in Ip_List else ()
                if Service_Ip in Ip_List:
                    Service_Address = (Service_Ip, Service_Port)
                    Service_Address_List.append(Service_Address)

        except KeyError:
            print(f'配置中无{Service_Name}参数')
        else:
            return Service_Address_List

    def get_backed_address(self, File_name):
        try:
            Config_Parser = self.config_reader({f'{os.getcwd()}\\{File_name}'})
            Lzqs = Config_Parser['lzqs']
            Address = (Lzqs['ip'], Lzqs['port'], Lzqs['org_id'])
        except KeyError:
            print(f'本地配置文件{File_name}错误')
        else:
            return Address

    @check_result
    def get_evaluate_config(self, Data: dict, Sequence=1):
        Evaluate_Config = dict()
        Nums = len(Data['evaluate'])
        for Item in range(0, Nums):
            Evaluate_Service_Ip = Data['evaluate'][Item]['evaluateServiceIp']
            Evaluate_Service_Port = Data['evaluate'][Item]['evaluateServicePort']
            Evaluate_Port = Data['evaluate'][Item]['evaluatePort']
            Evaluate_Control_Window = Data['evaluate'][Item]['evaluateControlWindow']
            Evaluate_Config[f"evaluate{Item+1}"] = dict(Evaluate_Service_Ip=Evaluate_Service_Ip,
                                                        Evaluate_Service_Port=Evaluate_Service_Port,
                                                        Evaluate_Port=Evaluate_Port,
                                                        Evaluate_Control_Window=Evaluate_Control_Window)

        return Evaluate_Config[f"evaluate{Sequence}"]

    # @check_result
    def window_map(self, Data):
        Window_List = Data['Evaluate_Control_Window']
        Evaluate_Port = Data['Evaluate_Port']
        Map = dict()
        for Item in Window_List:
            Window_Name = Item['windowName']
            Evaluate_Ip = Item['evaluateIp']
            # Item = {}
            # Map = {**Map, **Item}
            Map[Window_Name] = (Evaluate_Ip, Evaluate_Port)
        return Map

    def tips_map(self, Data):
        if Data['type'] == 1:
            Tips = f"叫号:{Data['ticketNumber']}"
        elif Data['type'] == 2:
            Tips = f"开始办理:{Data['ticketNumber']}"
        elif Data['type'] == 3:
            Tips = f"办理结束:{Data['ticketNumber']}"
        elif Data['type'] == 4:
            Tips = f"窗口：{Data['windowName']}--> 暂停服务"
        elif Data['type'] == 5:
            Tips = f"窗口：{Data['windowName']}--> 恢复服务"
        elif Data['type'] == 6:
            Tips = f"更新评价:{Data}"
        elif Data['type'] == 7:
            Tips = f"窗口：{Data['windowName']} --> 用户登录"
        elif Data['type'] == 8:
            Tips = f"窗口：{Data['windowName']} --> 用户退出"
        else:
            Tips = ''
        return Tips






