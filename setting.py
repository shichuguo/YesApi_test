'''
@author: liudixuan
@software: SeleniumTest
@file: settings.py
@time: 2020/4/1 20:35
@desc:
'''
import os
from pathlib import Path


BASE_PATH = Path(__file__).absolute().parent  #工程的绝对路径
p = Path(BASE_PATH)

DATA_PATH = p.joinpath("data")      #数据路径
CASE_PATH = p.joinpath('case')     #用例路径
REPORT_PATH = p.joinpath('report')  #报告路径
TEMPLATE_PATH = p.joinpath('template')  #模板路径
