'''
@author: zhangqiuting
@software: API
@file: OtherProfile.py
@time: 2020/4/2 22:57
@desc:
'''
import unittest
import ddt
import requests
from setting import *
from lib.util import get_token


@ddt.ddt
class OtherProfile(unittest.TestCase):
    '''
    获取其他会员个人资料
    '''

    @ddt.file_data(os.path.join(DATA_PATH, 'otherprofile.yaml'))
    def test_multiprofile(self, **cases):  # 用**cases接收
        # 构建数据
        login_app_key = cases.get('login_app_key')
        login_url = cases.get('login_url')
        url = cases.get('url')
        method = cases.get('method').lower()
        data = cases.get('data')
        m_assert = cases.get('assert')

        # 分开组合'uuid', 'token', 'other_uuid'
        for i in ['uuid', 'token', 'other_uuid']:
            if isinstance(data.get(i), dict):
                username = data.get(i).get('username')
                password = data.get(i).get('password')
                j = 0
                if i == 'token':
                    j = 1
                data[i] = get_token(login_app_key, username, password, login_url)[j]

        # 判断请求方法，并发送请求
        if method == 'get':
            res = requests.get(url, params=data)
        elif method == 'post':
            res = requests.post(url, data=data)

        # 获取返回值，并取出其data
        res = res.json()
        res_data = res.get('data')
        # print(res)

        # 用例描述
        self._testMethodDoc = cases.get('doc')

        # 断言，ret、err_code、err_msg、uuid的个数
        for key in m_assert:
            # 处理单层数据
            if key != 'data' or m_assert.get('data') == {}:
                self.assertIn(str(m_assert.get(key)), str(res.get(key)))
            # 处理data多层数据
            else:
                m_data = m_assert['data']
                for data_key in m_data:
                    # 处理特殊数据info
                    if data_key == 'info':
                        if m_data.get('info'):
                            self.assertEqual(data.get('other_uuid'), res_data.get('info').get('uuid'))
                        else:
                            self.assertEqual(m_data.get('info'), res_data.get('info').get('uuid'))
                    # 处理data的普通数据
                    else:
                        self.assertEqual(m_data.get(key), res_data.get(key))


if __name__ == '__main__':
    unittest.main()
