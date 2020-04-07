'''
@author: liudixuan
@software: SeleniumTest
@file: clear_all_session.py
@time: 2020/4/3 22:45
@desc:
'''
from lib.util import *
from setting import *
import ddt
import unittest
import requests
import random


@ddt.ddt
class ClearSession(unittest.TestCase):
    @ddt.file_data(os.path.join(DATA_PATH,'clear_all_session.yaml'))
    def test_qiut_login(self,**case):
        '''
        退出登录
        :return:
        '''
        #获取参数
        H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789' #所有任意字符
        app_key = case.get('app_key')
        username = case.get('username')              #用户名
        login_url = case.get("login_url")            #登录接口地址
        password = case.get('password')              #密码
        clear_session_url = case.get("clear_session_url")   #清空会员登录接口地址
        method = case.get("method")
        clear_session_data = case.get("clear_session_data") #退出登录的数据
        check = case.get("check")         #断言
        self._testMethodDoc = case.get("detail")
        #获取token
        token = get_token(url=login_url,app_key=app_key,username=username,password=password)[1]
        #添加最新token
        if "token" in clear_session_data:
                if clear_session_data["token"]:
                    clear_session_data["token"] = token
        #发送请求
        if method.lower() == 'post':
            re = requests.post(url=clear_session_url, data=clear_session_data)
        else:
            re = requests.get(url=clear_session_url, params=clear_session_data)

        #断言
        results = set_res_data(re.text)
        for i in check:
            self.assertIn(i,results)


if __name__ == '__main__':
    unittest.main()