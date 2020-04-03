'''
@author: liudixuan
@software: SeleniumTest
@file: utils.py
@time: 2020/4/1 20:36
@desc:
'''
import hashlib
import os
from setting import *
import requests


def hash_code(pwd):
    '''
    MD5加密
    :param pwd:
    :return:
    '''
    md5 = hashlib.md5()  # 获取MD5对象
    md5.update(pwd.encode('utf-8'))  # 将传入的pwd编码后，更新MD5的状态
    return md5.hexdigest()  # 返回十六进制的MD5码


def set_res_data(res):
    '''
    处理响应结果，替换":"（有数据的情况）和":（key的值为空串）为=号
    :param res:
    :return:
    '''
    if res:
        return res.lower().replace('":"', '=').replace('":', '=')


def creat_case_file(filename):
    '''从data目录中读取多有的yaml文件，使用case_template.txt模板，
    生成测试用例文件，放到case目录下'''
    file_list = os.listdir(DATA_PATH)
    template_file = os.path.join(BASE_PATH, filename)
    for lis in file_list:
        if lis.endswith('.yaml') or lis.endswith('.yml'):
            data_file = lis.replace('.yaml', '').replace('.yml', '')
            method_file = data_file.lower()
            class_name = data_file.capitalize()
            data_dict = {'data_file': data_file, 'method_file': method_file, 'class_name': class_name}
            with open(template_file, 'r', encoding='utf-8') as temp:
                content = temp.read()
                content = content % data_dict
                with open(os.path.join(CASE_PATH, "test_{}.py".format(data_file)), 'w', encoding='utf-8') as f:
                    f.write(content)

# 获取某用户的uuid和token
def get_token(app_key, username, password,url):
    password = hash_code(password)  # 加密密码
    login_data = {'app_key': app_key,
                  'username': username,
                  'password': password}
    res = requests.get(url, params=login_data)
    resp = res.json()
    uuid = resp.get('data').get('uuid')
    token = resp.get('data').get('token')
    return uuid, token
