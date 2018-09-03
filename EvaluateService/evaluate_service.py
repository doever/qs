#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import socket
import json
import queue
import threading
import time

from EvaluateService.config_related import ConfigMixin
from EvaluateService.network import Network


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


class UdpSocket():
    def __init__(self):
        self.Queue = queue.Queue()

    @staticmethod
    def produce_socket():
        try:
            Udp_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as e:
            print(f"Strange error creating Socket:{e}")
        else:
            return Udp_Socket

    @staticmethod
    def udp_bind(Address: tuple):
        Udp_Recieve_Socket = UdpSocket.produce_socket()
        try:
            Udp_Recieve_Socket.bind(Address)
        except socket.gaierror as e:
            print(f"Error: Udp Socket bind address:{Address} Failed!, Except:{e}")
        else:
            return Udp_Recieve_Socket

    @staticmethod
    def udp_send(Data_Dict, Sendto_Address):
        '''udp 发送数据报'''
        Udp_Send_Socket = UdpSocket.produce_socket()
        Msg_Str = json.dumps(Data_Dict, ensure_ascii=False)
        Msg_Str_Byte = Msg_Str.encode('utf-8')
        # print("Msg_Str_Byte:", Msg_Str_Byte, "type(Msg_Str_Byte):", type(Msg_Str_Byte))
        # self.Udp_Socket.sendto(Msg_Str, Sendto_Address)           #TypeError: a bytes-like object is required, not 'str'
        print("Sendto：[ IP:", Sendto_Address[0], ", port:", Sendto_Address[1], ", Data_Dict:", Data_Dict, "]#####")
        Udp_Send_Socket.sendto(Msg_Str_Byte, Sendto_Address)

    def listen(self, Address):
        print("开始网络监听\n")
        Udp_Recieve_Socket = UdpSocket.udp_bind(Address)
        while True:
            Receive_Data, From_Address = Udp_Recieve_Socket.recvfrom(SOCKET_RECEIVE_SIZE)
            try:
                Receive_Data = json.loads(Receive_Data)
                if isinstance(Receive_Data, dict) and 'type' in Receive_Data.keys():
                    print(f"收到数据:{Receive_Data}")
                else:
                    continue
            except Exception as e:
                print(f'非预期数据包{e}')
                continue
            else:
                self.Queue.put(Receive_Data)
                if Receive_Data['type'] == REBOOT_CODE:
                    break
        Udp_Recieve_Socket.close()
        print("监听结束")


class SocketConfig(Network):
    def __init__(self):
        super().__init__()

    def listen(self, Address):
        print("开始网络监听...")
        Udp_Recieve_Socket = super().udp_bind(Address)
        while True:
            Receive_Data, From_Address = self.Udp_Recieve_Socket.recvfrom(SOCKET_RECEIVE_SIZE)
            try:
                Receive_Data = json.loads(Receive_Data)
                if isinstance(Receive_Data, dict) and 'type' in Receive_Data.keys():
                    print(f"收到数据:{Receive_Data}")
                else:
                    continue
            except Exception as e:
                print(f'非预期数据包{e}')
                continue
            else:
                self.Queue.put(Receive_Data)
                if Receive_Data['type'] == REBOOT_CODE:
                    break
        self.Udp_Recieve_Socket.close()
        # Udp_Recieve_Socket.close()
        print("监听结束")
        print("producer threading will be end...")


class EvaluateService:
    def __init__(self, Service_Sequence=1):
        self.Evaluate_Socket = SocketConfig()
        self.Evaluate_Config = EvaluateConfig()
        self.Config_Data = self.Evaluate_Config.Config_Data
        self.Evaluate_Data = self.Evaluate_Config.get_evaluate_config(self.Config_Data, Service_Sequence)
        self.Producer_Threading = self.producer_threading()
        self.Customer_Threading = self.customer_threading()
        self.Service_Sequence = Service_Sequence

    def producer_threading(self):
        # Evaluate_Data = self.Evaluate_Config.get_evaluate_config()
        Evaluate_Address = (self.Evaluate_Data['Evaluate_Service_Ip'], self.Evaluate_Data['Evaluate_Service_Port'])
        Listen_Threading = threading.Thread(target=self.Evaluate_Socket.listen, args=(Evaluate_Address,), name='producer')
        return Listen_Threading

    def customer_threading(self):
        return threading.Thread(target=self.data_transfer, name='customer')

    def data_transfer(self):
        Window = self.Evaluate_Config.window_map(self.Evaluate_Data)
        Backed_Url = self.Evaluate_Config.get_backed_address('lzqs.ini')
        Send_Window_Type = [1, 2, 3, 4, 5, 7, 8]
        Send_Server_Type = [6, ]
        while True:
            Message = self.Evaluate_Socket.Queue.get()
            if Message['type'] in Send_Window_Type:
                # Tips = f"叫号:{Message['ticketNumber']}"
                try:
                    self.Evaluate_Socket.udp_send(Message, Window[Message['windowName']])
                    # print("*******收到回包*******", self.Evaluate_Socket.Udp_Send_Socket.recv(1024).decode('utf-8'))
                except KeyError:
                    print(f"未配置{Message['windowName']}号窗口,消息发送失败")
                    continue
            elif Message['type'] in Send_Server_Type:
                self.Evaluate_Config.request(f'http://{Backed_Url[0]}:{Backed_Url[1]}/back/ticket_evaluate', 'put', Message)
            elif Message['type'] == 9:
                # self.Evaluate_Socket.Udp_Send_Socket.close()
                break
            else:
                print(f"未定义的消息type:{Message['type']}")
                continue
            # print(self.Evaluate_Config.tips_map(Message))
        print("customer threading will be end...")

    def reboot(self):
        self.__init__()
        self.run()

    def run(self):
        # print("服务启动成功")
        self.Producer_Threading.start()
        self.Customer_Threading.start()
        self.Producer_Threading.join()
        self.Customer_Threading.join()
        if not self.Evaluate_Socket.Queue.empty():
            self.data_transfer()
        print(f"评价服务{self.Service_Sequence}即将重启...\n")
        time.sleep(3)
        self.reboot()


if __name__ == '__main__':
    App = EvaluateService(1)
    App.run()




