# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 19:33
# @Author  : luoxi
# @Email   : 18408258850@163.com
# @File    : test_LWJ_Login.py
# @Software: PyCharm


from api.LWJ_Login_case import LWJ_Login_case
from tools.analyze_data import analyze_data
import pytest,requests
import allure
from api.LWJ_Login import LWJ_Login

class Test_LWJ_Login():
    #@allure.step('实例化接口对象')
    def setup_class(self):
        self.session = requests.Session()
        # 实例化接口对象
        self.login_obj = LWJ_Login_case()

    @allure.title('登录异常，测试数据是:{args}')
    #  @allure.title('测试用例登录')
    @allure.feature('测试lwj登录用例')
    @allure.story('登录用例')
    @allure.severity('trivial')
    @allure.link('http://o.sales-staging.liweijia.com', name="分销的访问地址")
    @allure.issue('http://o.sales-staging.liweijia.com', '前面没有name关键字的issue的访问地址')
    @allure.testcase('http://o.sales-staging.liweijia.com', 'testcase的访问地址')
    @pytest.mark.parametrize('args', analyze_data('login_data', 'test_login'))
    def test_Logincase(self,args):
        result = self.login_obj.is_login(self.session,args['lv_username'],args['lv_password'])
        assert args['exp'] in str(result)

