'''
@author: qisijia
@software: SeleniumTest
@file: qsj_template.py
@time: 2020/4/3 21:00
@desc:
'''
import unittest
import requests,json
from lib.util import *
from setting import *
import os
import ddt
@ddt.ddt
class Change_group_admin(unittest.TestCase):
    @ddt.file_data(os.path.join(QSJ_DATA_PATH,'change_group_admin.yaml'))
    def test_change_group_admin(self,**case):
        url = case.get('url')
        method = case.get('method')
        login = case.get('login_data')
        check = case.get('check')
        change_data = case.get('change_data')
        self._testMethodDoc = case.get('test', "用例没有描述")
        if 'login_data' in case:
            login['password'] = hash_code(login['password'])  # 加密密码
            re_dict = json.loads(requests.post(url, data=login).text) #获取登录后的返回的json信息
            token = re_dict.get('data').get('token')
            if 'token_key' in case:#判断是否需要减少token的字符数量
                token = token[1:]
            if 'key' in case:#将token加入data进行传参
                change_data['token'] = token
        if method.lower() == 'post':
            r = requests.post(url=url,data=change_data)
        else:
            r = requests.get(url=url,params=change_data)
        rtext = set_res_data(r.text)  # 替换字符串拿到想要的数据
        for c in check:
            self.assertIn(c, rtext)
if __name__ == '__main__':
    unittest.main()