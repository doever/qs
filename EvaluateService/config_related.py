import os
import abc
import configparser
import requests
import time


class ConfigParserMixin:
    @staticmethod
    def config_reader(Read_Set: set)->dict:
        """
        读取本地配置文件，编码为'utf-8'，扩展了读取失败的记录的保留
        :param Read_Set: 一个包含需要读取的文件集合
        :return: 返回一个OrderedDict（类似字典）
        """
        Config = configparser.ConfigParser()
        Read_Set -= set(Config.read(Read_Set, encoding='utf-8'))
        Fail_Set = Read_Set if Read_Set else set()
        print(f'读取失败的文件：{Fail_Set}')
        Return_Data = Config._sections
        Return_Data.update(fail_set=Fail_Set)
        return Return_Data


class RequestsMixin:
    Map = {'get': requests.get,
           'post': requests.post,
           'put': requests.put,
           'delete': requests.delete}

    @classmethod
    def request(cls, Url: str, Method: str, Json: str=None)->dict:
        """
        对requests四种请求的简单封装
        :param Url: 希望请求的地址
        :param Method: 希望使用的请求方法
        :param Json: 希望请求携带的数据，json格式，get方法将忽略此参数
        :return: 返回请求到的数据，已经过json解析，编码为'utf-8'
        """
        Method = Method.lower()
        while True:
            try:
                print(f'开始请求：{Url}\n')
                Res = cls.Map[Method](Url) if Method == 'get' else cls.Map[Method](Url, json=Json)
                if Res.status_code == requests.codes.ok:
                    break
            except requests.ConnectionError:
                print('请求失败，请在检查后重启\n')
                time.sleep(7)
        Res.encoding = 'utf-8'
        return Res.json()


class ConfigMixin(ConfigParserMixin, RequestsMixin, metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def config_parser(self, *args, **kwargs):
        pass

    @classmethod
    def read_service_config(cls, Url_Path: str)->dict:
        """
        六大服务共用的获取配置方法
        :param Url_Path: 获取网络配置的地址的关键部分
        :return: 解析后的后台服务返回包
        """
        File = f'{os.getcwd()}\\lzqs.ini'
        while True:
            print(f'正在读取：{File}')
            try:
                Lzqs = cls.config_reader(Read_Set={File})
                Lzqs = Lzqs['lzqs']
                print('找到章节[lzqs]')
                Url = f"http://{Lzqs['ip']}:{Lzqs['port']}/back/{Url_Path}/{Lzqs['org_id']}"
                print('成功读取ip, port, org_id')
            except KeyError:
                print('读取失败，请检查文件，章节名lzqs及内容ip, port, org_id，然后重启')
                time.sleep(7)
            else:
                return cls.request(Url=Url, Method='get')


if __name__ == '__main__':
    a = ConfigMixin.read_service_config('multiple_org_print_service_config')

