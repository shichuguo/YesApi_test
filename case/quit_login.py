'''
@author: liudixuan
@software: SeleniumTest
@file: quit_login.py
@time: 2020/4/3 14:42
@desc:
'''
from lib.util import *
from setting import *
import ddt
import unittest
import requests
import random


@ddt.ddt
class QuitLogin(unittest.TestCase):
    @ddt.file_data(os.path.join(DATA_PATH,'quit_login.yaml'))
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
        quit_login_url = case.get("quit_login_url")   #退出登录接口地址
        method = case.get("method")
        quit_login_data = case.get("quit_login_data") #退出登录的数据
        check = case.get("check")         #断言
        outdated = case.get("outdated")   #需要过期的token标识
        more = case.get("more")           #需要token少于规定长度
        less = case.get("less")           #需要token长于规定长度
        self._testMethodDoc = case.get("detail")
        #获取token
        token = get_token(url=login_url,app_key=app_key,username=username,password=password)[1]
        #添加最新token
        if quit_login_data["token"] == True:
            quit_login_data["token"] = token
        # 如果less存在，获取token长度少1的时候,截取到倒数第二位
        if less:
            quit_login_data["token"] = token[:-2]
        # 如果more存在，token长度大于规定长度，随机生成
        if more:
            quit_login_data["token"] = token + random.choice(H)
        #发送请求
        if method.lower() == 'post':
            re = requests.post(url=quit_login_url, data=quit_login_data)
        else:
            re = requests.get(url=quit_login_url, params=quit_login_data)
        #验证token为过期时再发送一次请求
        if outdated:
            if method.lower() == 'post':
                re = requests.post(url=quit_login_url, data=quit_login_data)
            else:
                re = requests.get(url=quit_login_url, params=quit_login_data)



        #断言
        results = set_res_data(re.text)
        for i in check:
            self.assertIn(i,results)


if __name__ == '__main__':
    unittest.main()