# -*- coding: utf8 -*-
from flask import Blueprint, request
# 引入教务爬虫
from ..moudle.jwrobot import Robot

import json
# 创建教务蓝图
jwBlueprint = Blueprint('jw', __name__)

@jwBlueprint.route('/getStuInfo', methods = ['POST'])
def getStuInfo():
    res = {
        'status' : False,
        'info' : '',
        'data' : None
    }
    if not request.form.get('username') or not request.form.get('password') or not request.form.get('vpnusername') or not request.form.get('vpnpassword'):
        res['info'] = '缺少参数'
        return json.dumps(res)
    robot = Robot('https://jwglxt.w.buct.edu.cn', request.form.get('username'), request.form.get('password'))
    vpnlogon = robot.vpnLogin(request.form.get('vpnusername'), request.form.get('vpnpassword'))
    if not vpnlogon:
        res['info'] = 'VPN用户民或者密码错误'
        return json.dumps(res)
    robot.login()
    if not robot.isLogin():
        res['info'] = '用户名或者密码错误'
        return json.dumps(res)
    info = robot.getUserInfo()
    res['status'] = True
    res['data'] = info
    res['info'] = 'success'
    return json.dumps(res)

    