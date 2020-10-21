# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 19:33
# @Author  : luoxi
# @Email   : 18408258850@163.com
# @File    : request_method.py
# @Software: PyCharm

import  requests
class Method():
    def __init__(self):
        self.requests=requests.session()

    def get(self,url,header=None,data=None):
        if header==None:
            res=self.requests.get(url=url,data=data)
        else:
            res=self.requests.get(url=url,headers=header,data=data)
        return res
    def post(self, url, header=None, data=None):
        if header == None:
            res = self.requests.get(url=url, data=data)
        else:
            res = self.requests.get(url=url, headers=header, data=data)
        return res
    def post_json(self,url,header=None,data=None):
        if header==None:
            res=self.requests.get(url=url,json=data)
        else:
            res=self.requests.get(url=url,headers=header,json=data)
        return res
    def delete(self,url,header=None,data=None):
        if header==None:
            res=self.requests.get(url=url,json=data)
        else:
            res=self.requests.get(url=url,headers=header,json=data)
        return res

    def put(self,url,header=None,data=None):
        if header==None:
            res=self.requests.get(url=url,data=data)
        else:
            res=self.requests.get(url=url,headers=header,data=data)
        return res
    def options(self,url,header=None):
        if header==None:
            res=self.requests.options(url)
        else:
            res=self.requests.options(url,headers=header)
        return res

    def run_main(self,method,url,header=None,data=None):
        method = method.lower()
        if method=="get":
            res=self.get(url,header,data)
        elif method=="post":
            res=self.post(url,header,data)
        elif method=="post_json":
            res=self.post_json(url,header,data)
        elif method=="delete":
            res=self.delete(url,header,data)
        elif method=="put":
            res=self.put(url,header,data)
        elif method=="options":
            res=self.options(url,header)
        else:
            res = "请检查请求方法"
        return res

mymethod=Method()

if __name__ == '__main__':
    pass