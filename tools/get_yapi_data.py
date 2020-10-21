# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 19:33
# @Author  : luoxi
# @Email   : 18408258850@163.com
# @File    : get_yapi_data.py
# @Software: PyCharm

import requests
import json
import time
import pandas as pd
from tools.logger import GetLog



class Yapi(object):

    def __init__(self, userapi, passwdapi, group_id):
        """连接yapi初始化信息

        :param userapi: yapi的登录账号
        :param passwdapi: yapi的登录密码
        :param group_id: yapi中所属产品的id
        """
        self.logger = GetLog().get_logger()
        self.userapi = userapi
        self.passwdapi = passwdapi
        self.group_id = group_id
        self.apiurl = "http://yapi.liweijia.com"  # yapi对应域名
        self.api = requests.session()
        self.pathmodlename = ""  # yapi上接口所属的模块名称
        self.pathname = ""  # 接口名称
        self.path_data_lists = []  # 接口数据(list)   其中列表中的每个值是一个字典
        self.path_key_dicts = {}  # 用于生成Excel中第一行值对应的参数
        self.list_params_path_address = []  # 所有的接口地址列表
        self.list_params_up_time = []  # 所有的接口更新时间列表
        self.list_params_add_time = []  # 所有的接口添加时间列表
        self.list_params_method = []  # 所有的参数方法列表
        self.list_params_modle_name = []  # 所有的接口所属模块名称列表
        self.list_params_request_form_data = []  # 所有的请求参数列表
        self.list_params_request_data_example = []  # 接口请求示例
        self.list_params_expected_response = []  # 所有的请求预期响应
        self.list_params_path_name = []  # 所有的请求接口名称
        self.list_params_path_creat_user = []  # 所有的接口创建者列表
        self.list_params_header = []
        self.count = 0
        loginjson = {'email': self.userapi,
                     'password': self.passwdapi}
        loginheader = {'Content-Type': 'application/json;charset=UTF-8'}
        self.logger.info("api后台登录状态:" +
                         str(self.api.post(url=self.apiurl + "/api/user/login", json=loginjson,
                                           verify=False, headers=loginheader).json().get("errmsg")))
        print("api后台登录状态:" +
                         str(self.api.post(url=self.apiurl + "/api/user/login", json=loginjson,
                                           verify=False, headers=loginheader).json().get("errmsg")))

    def get_path_data(self):
        """获取path信息 根据产品id(group_id) 获取对应的模块id"""
        getid = {'group_id': self.group_id, 'page': '1', 'limit': '500000'}
        ids = self.api.get(url=self.apiurl + "/api/project/list", verify=False, params=getid).json().get("data").get(
            "list")
        for i in range(0, len(ids)):
            self.pathmodlename = ids[i].get("name")
            self.get_pathid_by_mouled_id(ids[i].get("_id"))

    def get_pathid_by_mouled_id(self, _id):
        """通过模块id找寻path—id

        :param _id: 模块id
        """
        details = self.api.get(self.apiurl + "/api/interface/list?page=1&limit=9999&project_id=%s" % _id,
                               verify=False).json()
        for j in range(0, len(details.get("data").get("list"))):
            pathid = details.get("data").get("list")[j].get("_id")
            self.get_pathdata_by_pathid(pathid)

    def get_pathdata_by_pathid(self, pathid):
        """根据pathid获取每个接口的详细信息

        :param pathid: 接口id
        """
        pathdicts = {}  # 记录每个接口的信息
        pathdata = self.api.get(url=self.apiurl + "/api/interface/get?id=%s" % pathid, verify=False).json()
        pathdicts["path_address"] = pathdata.get("data").get("path")  # 接口地址
        pathdicts["up_time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime(int(pathdata.get("data").get("up_time"))))  # 接口变更时间
        pathdicts["add_time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime(int(pathdata.get("data").get("add_time"))))  # 接口添加时间
        pathdicts["method"] = pathdata.get("data").get("method")  # 接口请求方法
        pathdicts["modle_name"] = self.pathmodlename  # 接口所属模块名称
        key_value_dict = {}  # 请求表单的表单数据
        requests_data_example = {}  #请求参数示例
        req_params = pathdata.get("data").get("req_query") #获取表单的参数
        if len(req_params) != 0:   #若表单不为空
            for requestdatas in req_params:
                flag = requestdatas.get("required")
                key_value_dict[requestdatas.get("name")] = requestdatas.get("desc") + "(%s)" % ("必填" if flag == '1' else "非必填")
                requests_data_example[requestdatas.get("name")] = ("" if requestdatas.get("example")==None else requestdatas.get("example") )
        else:   #表单为空时，取body
            if pathdata.get("data").get("req_body_other") != None:
                res_data = pathdata.get("data").get("req_body_other")
                try:
                    req_body_other = json.loads(res_data).get("properties")
                    key_value_dict = req_body_other
                    requests_data_example = req_body_other
                except:
                    key_value_dict = res_data
                    requests_data_example = res_data

        pathdicts["request_form_data"] = "空" if key_value_dict =={} else key_value_dict  # 请求表单数据 key为参数名 value为字段说明(必填/非必填)
        pathdicts["requests_data_example"] = "空" if requests_data_example == {} else requests_data_example
        pathdicts["expected_response"] = pathdata.get("data").get("res_body")  # 预期响应
        pathdicts["path_name"] = pathdata.get("data").get("title")  # 接口名称

        header_list = pathdata.get("data").get("req_headers")
        print(header_list)

        if len(header_list) >= 1:
            header_dict = {}
            for head in header_list:
                header_name = head.get('name')
                header_value = head.get('value')
                header_dict[header_name] = header_value
            pathdicts["req_headers"] = header_dict  # 接口tou


        pathdicts["path_creat_user"] = pathdata.get("data").get("username")  # 接口创建者

        self.path_data_lists.append(pathdicts)  # 追加每个接口的数据信息到列表中
        self.count += 1
        self.logger.info("第%d个接口%s的数据已经抓取完毕" % (self.count, pathdicts["path_address"]))
        print("第%d个接口%s的数据已经抓取完毕" % (self.count, pathdicts["path_address"]))
    def pathdata_to_excel(self):
        """将api数据写入excel"""
        for pathdata in self.path_data_lists:
            self.list_params_path_address.append(pathdata.get("path_address"))
            self.list_params_up_time.append(pathdata.get("up_time"))
            self.list_params_add_time.append(pathdata.get("add_time"))
            self.list_params_method.append(pathdata.get("method"))
            self.list_params_header.append(pathdata.get("req_headers"))


            self.list_params_modle_name.append(pathdata.get("modle_name"))
            self.list_params_request_form_data.append(pathdata.get("request_form_data"))
            self.list_params_request_data_example.append(pathdata.get("requests_data_example"))
            self.list_params_expected_response.append(pathdata.get("expected_response"))
            self.list_params_path_name.append(pathdata.get("path_name"))
            self.list_params_path_creat_user.append(pathdata.get("path_creat_user"))
        self.path_key_dicts["接口名称"] = self.list_params_path_name
        self.path_key_dicts["接口地址"] = self.list_params_path_address
        self.path_key_dicts["接口请求方法"] = self.list_params_method
        self.path_key_dicts["接口请求头"] = self.list_params_header
        self.path_key_dicts["接口请求参数格式"] = self.list_params_request_form_data
        self.path_key_dicts["请求参数示例"] = self.list_params_request_data_example
        self.path_key_dicts["接口预期响应"] = self.list_params_expected_response
        self.path_key_dicts["接口所属模块名称"] = self.list_params_modle_name
        self.path_key_dicts["接口创建时间"] = self.list_params_add_time
        self.path_key_dicts["接口创建者"] = self.list_params_path_creat_user
        self.path_key_dicts["接口最新修改时间"] = self.list_params_up_time
        file_path = r'../data/apidata.xlsx'  # 文件需要保存路径
        writer = pd.ExcelWriter(file_path)
        df = pd.DataFrame(self.path_key_dicts)
        df.to_excel(writer, columns=self.path_key_dicts.keys(), index=False, encoding='utf-8',
                    sheet_name='base接口数据')
        writer.save()



if __name__ == "__main__":


    luoxi = Yapi(userapi="1059218389@qq.com", passwdapi="123456", group_id="215")
    luoxi.get_path_data()
    aipdatalist = luoxi.path_data_lists  # api数据都在list中
    luoxi.pathdata_to_excel()
