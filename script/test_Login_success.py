from api.LWJ_Login_case import LWJ_Login_case
from tools.analyze_data import analyze_data
import pytest,requests
import allure
from api.LWJ_Login import LWJ_Login

class Test_Login_SUCCESS():
    def setup_class(self):

        self.session = requests.Session()
        # 实例化接口对象
        self.login_obj = LWJ_Login()

    @allure.feature('测试lwj登录成功功能')
    @allure.story('登录成功用例')
    @allure.severity('trivial')
    @allure.title('登录成功功能测试')
    @allure.link('http://o.sales-staging.liweijia.com', name="分销的访问地址")
    @allure.issue('http://o.sales-staging.liweijia.com')
    @allure.testcase('http://o.sales-staging.liweijia.com', 'testcase的访问地址')
  #  @pytest.mark.parametrize('args', analyze_data('login_data', 'test_login'))
    def test_Logincase(self):

       result = self.login_obj.login_success(self.session)

       print(result)

       assert '管理员' in str(result)


if __name__ == '__main__':
    pytest.main(['-s','test_LWJ_Login.py'])
