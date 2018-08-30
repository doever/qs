#  -*- coding: utf-8 -*-

import json
import socket
import queue
import threading

#常量
SOCKET_RECEIVE_SIZE = 512


class Network():
    '''通信组件，用于各组件间通信：接收、发送UDP数据包'''
    def __init__(self):
        try:
            self.Udp_Send_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as e:
            print(f"Strange error creating Udp_Send_Socket:{e}")
        try:
            self.Udp_Recieve_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as e:
            print(f"Strange error creating Udp_Recieve_Socket:{e}")
        self.Queue = queue.Queue()

    def udp_send(self, Data_Dict, Sendto_Address):
        '''udp 发送数据报'''
        Msg_Str = json.dumps(Data_Dict, ensure_ascii=False)
        # print("Msg_Str:", Msg_Str, "type(Msg_Str):", type(Msg_Str))
        Msg_Str_Byte = Msg_Str.encode('utf-8')
        # print("Msg_Str_Byte:", Msg_Str_Byte, "type(Msg_Str_Byte):", type(Msg_Str_Byte))
        # self.Udp_Socket.sendto(Msg_Str, Sendto_Address)           #TypeError: a bytes-like object is required, not 'str'
        print("Sendto：[ IP:", Sendto_Address[0], ", port:", Sendto_Address[1], ", Data_Dict:", Data_Dict, "]#####")
        self.Udp_Send_Socket.sendto(Msg_Str_Byte, Sendto_Address)

    def udp_bind(self, bind_address: tuple):
        '''绑定端口，用于接收数据报'''
        try:
            self.Udp_Recieve_Socket.bind(bind_address)
        except socket.gaierror as e:
            print(f"Error: Udp Socket bind address:{bind_address} Failed!, Except:{e}")
            return False
        else:
            print(f"Listen to Address:{bind_address}")
            return True

    def udp_receive_dgram(self):
        '''接收数据报，循环读取，放入队列缓存'''
        while True:
            #读取socket缓冲区，读取数据
            try:
                Receive_Data, Address = self.Udp_Recieve_Socket.recvfrom(SOCKET_RECEIVE_SIZE)
            except socket.error as e:
                print(f"Strange error while recvfrom dgram:{e}")
                continue
            else:
                print(f"Receive:[Address:{Address}, Receive_Data:{Receive_Data}]*****")
            #处理数据，是Json则存储，否则丢弃
            try:
                Json_Data = json.loads(Receive_Data)
                if type(Json_Data) != type(dict()):
                    continue
                # print(f"Json_Data:{Json_Data}, type(Json_Data):{type(Json_Data)}")
            except:
                print("Error: Parse Receive Data with JSON Fail! abandon data")
                continue
            else:
                self.Queue.put(Json_Data)
                #查看队列是否添加成功
                # print(f"**********************************:{self.Queue.get_nowait()}")

    def udp_listen(self):
        '''监听端口，读取数据报，单独线程，阻塞监听'''
        self.Thread = threading.Thread(target=self.udp_receive_dgram)
        self.Thread.start()


if __name__ == "__main__":
    '''测试通信组件'''
    net = Network()
    #测试接收
    Bind_Address = ("127.0.0.1", 706)
    if net.udp_bind(Bind_Address):
        net.udp_listen()

    #测试发送
    net.udp_send({"a":1,"b":"2", "chinese":"中国"}, ("127.0.0.1", 706))
