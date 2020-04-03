'''
@author: 廖先容
@software: SeleniumTest
@file: get_user_longlist.py
@time: 2020/4/3 12:28
@desc:
'''
import unittest,requests,ddt
from lib.util import *
from setting import *
@ddt.ddt
class GetUserLongList(unittest.TestCase):
    @ddt.file_data(os.path.join(DATA_PATH,'get_user_longlist.yaml'))
    def test_get_user_longlist(self,**case):
        methods = case.get('methods')
        data = case.get('data')
        check = case.get('check')
        self._testMethodDoc = case.get('description','没有用例描述')
        if case.get('login'):#有login字段，表示需要uuid和token参数，登录获取uuid和token
            url = case.get('url')
            app_key = case.get('login').get('app_key')
            username = case.get('login').get('username')
            password = case.get('login').get('password')
            uuid, token = get_token(url=url,app_key=app_key,username=username,password=password)
            if case.get('set_flag') == 'all': #当set_flag标识为all时，重置data中的uuid和token字段的值
                data['uuid'],data['token'] = uuid,token
            elif case.get('set_flag') == 'uuid': #当set_flag标识为true时，只重置data中的uuid字段的值
                data['uuid'] = uuid
            elif case.get('set_flag') == 'token': #当set_flag标识为false时，只重置data中的token字段的值
                data['token'] = token
            else: #当没有set_flag标识字段时，不做任何操作
                pass
            if case.get('logout'): #存在key 'logout'
                case['logout']['uuid'],case['logout']['token'] = uuid,token #将登录返回的uuid赋给logout中的uuid
                requests.post(url=case.get('url_logout'),data=case.get('logout')) #需要时访问退出登录接口退出当前登录
        if methods.lower() == 'post':
            r = requests.post(url=case.get('url_getlist'),data=data) #发送post请求
        else:
            r = requests.get(url=case.get('url_getlist'),params=data) #发送get请求
        res = r.text
        results = set_res_data(res)
        if case.get('check_flag'): #断言
            self.assertEqual(check,res)
        else:
            for c in check:
                self.assertIn(c,results) #循环判断结果
if __name__ == '__main__':
    unittest.main()