'''
@author: zhangqiuting
@software: API
@file: multiprofile.py
@time: 2020/4/2 22:57
@desc:
'''
import unittest
import ddt
import requests
from setting import *
from lib.util import get_token


@ddt.ddt
class MultiProfile(unittest.TestCase):
    '''
    批量获取会员信息
    '''

    @ddt.file_data(os.path.join(DATA_PATH, 'multiprofile.yaml'))
    def test_multiprofile(self, **cases):  # 用**cases接收
        # 构建数据
        login_url = cases.get('login_url')
        url = cases.get('url')
        method = cases.get('method').lower()
        data = cases.get('data')
        app_key = data.get('app_key')
        uuids = data.get('uuids')
        m_assert = cases.get('assert')

        # 组合非必填项
        for i in ['uuid', 'token']:
            if isinstance(data.get(i), dict):
                username = data.get(i).get('username')
                password = data.get(i).get('password')
                j = 0
                if i == 'token':
                    j = 1
                data[i] = get_token(app_key, username, password, login_url)[j]

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
                    # 处理特殊数据info_list
                    if data_key == 'info_list':
                        # 有数据时
                        if m_data.get(data_key) == 'len_uuids':
                            # print(res_data)
                            count = 0
                            # 通过uuid长度判断合法uuid数量
                            for i in uuids.split(','):
                                if len(i) == 32:
                                    count = count + 1
                            self.assertEqual(len(res_data.get(data_key)), count)
                        # 无数据时
                        else:
                            self.assertEqual(res_data.get(data_key), m_data.get(data_key))
                    # 处理data的普通数据
                    else:
                        self.assertEqual(m_data.get(key), res_data.get(key))


if __name__ == '__main__':
    unittest.main()
