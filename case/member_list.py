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
class MemberList(unittest.TestCase):
    """
    获取会员列表操作类
    """

    @ddt.file_data(os.path.join(DATA_PATH,"member_list.yaml"))
    def test_member_list(self,**case):
        url = case.get("url")
        data1 = case.get("data1")
        data = case.get("data")
        method = case.get("method")
        check = case.get("check")
        xs = case.get("xs")
        self._testMethodDoc = case.get("doc","该用例无描述信息")
        if xs.get("d") == True:
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
        users_list = resp.get("data").get("users")
        #判断响应中的users键对应的列表的长度
        if xs.get("n") == True:
            self.assertIsNotNone(len(users_list))
        if xs.get("m") == True:
            self.assertEquals(1,len(users_list))
        #判断会员列表是否按时间顺序排列（顺序或降序）
        if xs.get("s") == True:
            reg_time_list=reg_time(users_list)
            for i in range(1,len(reg_time_list)):
                if xs.get("sd") == True:
                    self.assertTrue(reg_time_list[i]>reg_time_list[i-1])
                else:
                    self.assertTrue(reg_time_list[i]<reg_time_list[i-1])
        #判断会员账号排列顺序
        if xs.get("zh") == True:
            users_list1 = username_list(users_list)
            for i in range(1, len(users_list1)):
                if xs.get("sd") == True:
                    self.assertTrue(users_list1[i] > users_list1[i - 1])
                else:
                    self.assertTrue(users_list1[i] < users_list1[i - 1])






if __name__ == '__main__':
    unittest.main()