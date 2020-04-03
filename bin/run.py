'''
@author: liudixuan
@software: SeleniumTest
@file: run.py
@time: 2020/4/2 18:34
@desc:
'''

import unittest,time
from setting import *
from BeautifulReport import BeautifulReport
from lib.util import *

creat_case_file('qsj_template.txt')
_time = time.strftime('%Y-%m-%d %H_%M_%S')
filename = '小白接口_{}.html'.format(_time)
discover = unittest.defaultTestLoader.discover(CASE_PATH,pattern='*.py') #创建测试集
BeautifulReport(discover).report(description="测试小白接口",
                                 report_dir=REPORT_PATH,filename=filename)#执行测试并生成报告