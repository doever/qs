#!/usr/bin/python3
# -*- coding:utf-8 -*-

from TicketService.utils.config_related import RequestsMixin
from TicketService.models.org_data import OrgData
from TicketService.models.config_data import Back_Config
from TicketService.settings import URL_MAP


class BusinessData(RequestsMixin):
    def __init__(self):
        pass
        # self.OrgData = OrgData

    def get_business_data(self):
        Org_Dict = OrgData.get_multiple_org_data()
        Org_Bus_Dict = dict()
        for k, v in Org_Dict.items():
            Business_List = []
            for Item in v['business']:
                Style = dict()
                Style['labelStyle'] = dict()
                Style['buttonStyle'] = dict()
                Style['labelStyle']['font-size'] = Item['waitPeopleFontSize']
                Style['labelStyle']['font-family'] = Item['waitPeopleFontType']
                Style['labelStyle']['color'] = Item['waitPeopleFontColor']
                Style['buttonStyle']['font-size'] = Item['ticketButtonFontSize']
                Style['buttonStyle']['font-family'] = Item['ticketButtonFontType']
                Style['buttonStyle']['color'] = Item['ticketButtonFontColor']
                Style['buttonStyle']['border-image'] = f"..{Item['ticketButtonNormalBg']}"
                Style['buttonStyle']['pressed-image'] = f"..{Item['ticketButtonClickedBg']}"
                Item['style'] = Style
                Business_List.append(Item)

            Org_Bus_Dict[k] = Business_List
        return Org_Bus_Dict

    def get_first_business_data(self):
        pass


Business_Data = BusinessData()


if __name__ == '__main__':
    Bus = BusinessData()
    Res = Bus.get_business_data()
    print(Res)

