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


@ddt.ddt
class MultiProfile(unittest.TestCase):
    '''
    批量获取会员信息
    '''

    @ddt.file_data(os.path.join(DATA_PATH, 'multiprofile.yaml'))
    def test_multiprofile(self, **cases):  # 用**cases接收
        # 构建数据
        url = cases.get('url')
        method = cases.get('method').lower()
        data = cases.get('data')
        m_assert = cases.get('assert')

        # 判断请求方法，并发送请求
        if method == 'get':
            res = requests.get(url, params=data)
        elif method == 'post':
            res = requests.post(url, data=data)
        # 获取返回值，并取出其data
        res = res.json()
        res_data = res.get('data')
        # 用例描述
        self._testMethodDoc = cases.get('doc')
        # 断言，ret、err_code、err_msg、uuid的个数
        for key in m_assert:
            if key == 'ret':
                self.assertEqual(res.get(key), m_assert.get(key))
            # data下数据
            elif key == 'err_code' or key =='err_msg':
                self.assertEqual(res_data.get(key), m_assert.get(key))
            # info_list长度
            elif key == 'info_list':
                self.assertEqual(len(res_data.get(key)), len(data.get('uuids').split(',')))

    if __name__ == '__main__':
        unittest.main()
