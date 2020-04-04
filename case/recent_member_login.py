'''
@author: yimeiling
@software: SeleniumTest
@file: member_list_004.py
@time: 2020/4/3 0:39
@desc:
'''
"""
获取最近会员登录列表
"""
import unittest
import ddt
import os
from setting import *
import requests
from lib.util import *


@ddt.ddt
class RecentMemberLogin(unittest.TestCase):
    """
    获取近期会员登录列表操作类
    """

    @ddt.file_data(os.path.join(DATA_PATH,"recent_member_login.yaml"))
    def test_recent_member_login(self,**case):
        url = case.get("url")
        data1 = case.get("data1")
        data = case.get("data")
        method = case.get("method")
        check = case.get("check")
        d = case.get("d")
        n = case.get("n")
        w = case.get("w")
        self._testMethodDoc = case.get("doc","该用例无描述信息")
        if d == True:
            #进行登录，获取token
            if 'password' in data1:
                data1["password"] = hash_code(data1["password"])
            if  method.lower == "post":
                rl = requests.post(url, data=data1)
            else:
                rl = requests.get(url, params=data1)
            respl = rl.json()
            data["token"] = respl.get("data").get("token")
        #获取会员近期登录列表
        if method.lower == "post":
            r = requests.post(url,data=data)
        else:
            r = requests.get(url,params=data)
        resp = set_res_data(r.text)
        for c in check:
            self.assertIn(c,resp)
        resp = r.json()
        members_list = resp.get("data").get("members")
        #判断响应中的members键对应的列表的长度
        if n == True:
            m_len = len(members_list)
            self.assertEqual(case.get("data").get("num"), m_len)
        now_time = int(time.time())
        if w == True:
            for m in members_list:
                self.assertTrue(now_time- m.get("login_time") < time_difference(30))


if __name__ == '__main__':
    unittest.main()