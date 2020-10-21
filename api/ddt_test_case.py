# -*- coding: utf-8 -*-
# @Time    : 2020/10/21 11:21
# @Author  : luoxi
# @Email   : 18408258850@163.com
# @File    : ddt_test_case.py
# @Software: PyCharm

import ddt,json
from tools.logger import GetLog
from tools.get_excel_data import OpExcel
from tools.request_method import Method
import unittest
base_url = "http://e.sales-staging.liweijia.com"
run_method = Method()

@ddt.ddt
class TestCase(unittest.TestCase):
    test_data = OpExcel().convert_data("base接口数据")

    @ddt.data(*test_data)
    def test_run_case(self, data):
        url = base_url + data["接口地址"]
        header = data["接口请求头"]
        print(type(header))
        req_method = data["接口请求方法"]
        req_data = data["请求参数示例"]
        if req_data == '空':
            req_data = None
        res = run_method.run_main(req_method,url,header,req_data)
        print(res.text)

if __name__ == '__main__':
    unittest.main()