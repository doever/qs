#!/usr/bin/python3
# -*- coding:utf-8 -*-

from TicketService.utils.config_related import RequestsMixin
from TicketService.utils.utils import singleton
from TicketService.models.config_data import Back_Config
from TicketService.settings import *


@singleton
class OrgData(RequestsMixin):
    def __init__(self):
        self.Multiple_Org_Dict = self.get_multiple_org_data()
        self.Org_Ui_List = self.org_ui_config()

    @classmethod
    def get_multiple_org_data(cls) -> dict:
        '''获取多机构的数据'''
        Backed_Data = Back_Config.get_backed_service()
        Org_Para = ','.join(ORG_LIST)
        Url = f"http://{Backed_Data[0]}:{Backed_Data[1]}/back/{URL_MAP['multiple_org']}/{Org_Para}"
        Multiple_Org_Dict = cls.request(Url=Url, Method='get')
        Di = dict()
        for k, v in Multiple_Org_Dict.items():
            if v['resCode'] == 0:
                Di[k] = v
            else:
                print(f"机构{k}不存在,请检查配置文件")

        # print(f"机构配置:{Di}")
        return Di

    def org_ui_config(self) -> list:
        '''多机构页面的数据,构造机构Button'''
        Org_Li = []
        for k, v in self.Multiple_Org_Dict.items():
            Temp_Di = dict()
            Temp_Di['org_id'] = v['orgId']
            Temp_Di['org_name'] = v['orgName']
            Temp_Di['org_style'] = DEFAULT_ORG_STYLE
            Org_Li.append(Temp_Di)

        return Org_Li


Org_Data = OrgData()


if __name__ == '__main__':
    Org = OrgData()
    a = Org.get_multiple_org_data()
    # print(a)

