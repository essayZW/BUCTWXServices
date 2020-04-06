# -*- coding: utf8 -*-
# 引入蓝图功能
from flask import Blueprint

'''
引入对应的模型
其文件为app/model/test_model.py
'''
from ..model import test_model

testBlueprint = Blueprint('test', __name__)

@testBlueprint.route('/')
def index():
    # 调用模型中的函数
    return test_model.test()