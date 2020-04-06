# -*- coding: utf8 -*-
from flask import Blueprint
# 引入教务爬虫
from ..moudle.jwrobot import Robot
# 创建教务蓝图
jwBlueprint = Blueprint('jw', __name__)

@jwBlueprint.route('/')
def index():
    return 'hellow world'