# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 19:33
# @Author  : luoxi
# @Email   : 18408258850@163.com
# @File    : LWJ_Log_case.py
# @Software: PyCharm

from config import LWJ_IP,HEADERS
import requests
import re

from tools.logger import GetLog

log = GetLog().get_logger()


class LWJ_Login_case():
    def __init__(self):
        self.url = LWJ_IP+'/security/lv_check?type=normal&returnUrl=http%3A%2F%2Fo.sales-staging.liweijia.com%2F'
        log.info(f'登录的url地址是{self.url}')
        self.header = {'Content-Type': 'application/x-www-form-urlencoded', 'LX-REQUEST-LOGIN-MODE': 'jwt'}
      #  self.cookies= self.get_cookies


    def get_cookies(self,lv_username,lv_password):
        """
        方法变更为属性
        :return: [sid,path]
        """
        cookies = []
        data = {'lv_username':lv_username,'lv_password':lv_password}
        res1 = requests.post(url=self.url,data=data,headers = self.header)
        print(res1.headers)
        print(res1.json())

        print(res1.headers['Set-Cookie'])
        res2=res1.headers['Set-Cookie']
       # sid=res2.split(";")[0]
        sid=re.findall(r'(sid=.+?);',res2)[0]
        print(sid)
      #  path=res2.split(";")[1].split(" ")[1].split(";")[0]
        path=re.findall(r'(LX-WXSRF-JTOKEN=.+?);',res2)[0]
        print("------------------------"+path)
        cookies.append(sid)
        cookies.append(path)
        return  cookies

     #   log.info(f'登录的url地址是{cookies}')

    def is_login(self,session,lv_username,lv_password):
        #header3={sid.split('=')[0]:sid.split('=')[1],path.split('=')[0]:path.split('=')[1]}
        cookies = self.get_cookies(lv_username,lv_password)
        header3 = {'Cookie':'Hm_lvt_1a37d6e50dc8404e45d7ab69adee8d9f=1598852416;'+cookies[0]+';'+cookies[1]}
        print(header3)
        url3="http://o.sales-staging.liweijia.com/services/ums/isLogin"
        res3 = session.get(url=url3,headers=header3)
        return  res3.json()

if __name__ == '__main__':
    pass

    #print(LWJ_Login().is_login(requests.session()))



