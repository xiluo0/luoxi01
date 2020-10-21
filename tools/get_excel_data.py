# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 19:33
# @Author  : luoxi
# @Email   : 18408258850@163.com
# @File    : get_excel_data.py
# @Software: PyCharm

import xlrd,os,json
import jsonpath
from xlutils import copy
from tools.logger import GetLog

class OpExcel():
    """从excel中读取参数，并转换 成字典"""
    def __init__(self):
        # 用一个字典来接收每个请求返回的数据，作为后面有参数关联的全局参数
        self.result_dict = {}
        self.logger = GetLog().get_logger()
    #从excel提取list[dict{}]
    def get_param(self,sheet_name):
        param_path = r"../data/apidata.xlsx"
        params_list = []
        if param_path.endswith('.xls') or param_path.endswith('.xlsx'):   #判断参数文件是否合法
            try:
                book = xlrd.open_workbook(param_path)   #打开excel
                sheet = book.sheet_by_name(sheet_name)      #获取sheet页
                title = sheet.row_values(0)
                for i in range(1,sheet.nrows):      #循环每一行
                    row_data = sheet.row_values(i)      #获取每行数据
                    data = dict(zip(title,row_data))    #将第标题和对应数据组装成dict
                    params_list.append(data)
            except Exception as e:
                self.logger.error('【%s】excel参数获取失败，错误信息为%s'%(param_path,e))
        else:
            self.logger.error('参数文件不合法>>%s'%param_path)
        return params_list

    def convert_data(self, sheet):
        """

        :param sheet:
        :return: 返回处理后的header和参数字典
        """
        data = OpExcel().get_param(sheet)
        for i in data:
            # print(i)
            req_data1 = i["接口请求头"]
            req_data2 = i["请求参数示例"]
            if req_data1 != '' and req_data1.endswith('}'):
                req_data1 = req_data1.replace('\'', '\"')
                i["接口请求头"] = json.loads(req_data1)

            if req_data2 != '' and req_data2.endswith('}'):
                req_data2 = req_data2.replace('\'', '\"')
                i["请求参数示例"] = json.loads(req_data2)
        return data

if __name__ == '__main__':
    data = OpExcel().get_param('base接口数据')
    for i in data:
        #print(i)
        req_data1 = i["接口请求头"]
        req_data2 = i["请求参数示例"]
        if req_data1 != '' and req_data1.endswith('}'):
            req_data1 = req_data1.replace('\'','\"')
            req_data1 = json.loads(req_data1)
            print(req_data1)
            print(type(req_data1))
        if req_data2 != '' and req_data2.endswith('}'):
            req_data2 = req_data2.replace('\'','\"')
            req_data2 = json.loads(req_data2)
            print(req_data2)
            print(type(req_data2)) 