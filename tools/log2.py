import os
import time
from loguru import logger
path = os.path.dirname(os.path.dirname(__file__))

#logger日志配置
report_log_path = os.path.join(path, "log")
#年月日
today = time.strftime("%Y-%m-%d", time.localtime())
logging_file = os.path.join(report_log_path, "{}.log".format(today))

logger.add(
    logging_file,
    #格式
    format="{time:YYYY-MM-DD HH:mm:ss}|{level}|{message}",
    #文件最大大小
    rotation="500 MB",
    encoding="utf-8",
)
# loguru日志配置

#测试用例目录
YAML_PATH = os.path.join(path, "data")
# BeautifulReport配置
report_path = os.path.join(path, "report")

beautiful_filename = "report"
beautiful_description = "接口测试报告"


#文件格式，金支持yaml和json，运行不支持混用
TEST_CASE_FILE_FORMAL = "yaml"
#第一个yaml文件
first_test_case_file = "login.yaml"


#数据库
environment = "test"
if environment=="test":
    URI="https://jcp.justbon.com"
    DB_HOST="10.0.0.197"
    DB_PORT=3399
    DB_USER="root"
    DB_PASSWORD="Qq445813.."
    DB_DATABASE="test_http"