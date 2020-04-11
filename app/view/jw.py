# -*- coding: utf8 -*-
from flask import Blueprint,render_template,Flask,request,json
# 引入教务爬虫
from ..moudle.jwrobot import Robot
# 创建教务蓝图
jwBlueprint = Blueprint('jw', __name__)

@jwBlueprint.route('/getStuInfo', methods = ['POST'])
def getStuInfo():
    res = {
        'status' : False,
        'info' : '',
        'data' : None
    }
    userName = request.form.get('username')
    passWord = request.form.get('password')
    vpnUserName = request.form.get('vpnusername')
    vpnPassWord = request.form.get('vpnpassword')
    if not userName or not passWord or not vpnUserName or not vpnPassWord:
        res['info'] = '缺少参数'
        return json.dumps(res)
    robot = Robot('https://jwglxt.w.buct.edu.cn', userName, passWord)
    vpnlogon = robot.vpnLogin(vpnUserName, vpnPassWord)
    if not vpnlogon:
        res['info'] = 'VPN用户名或者密码错误'
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


@jwBlueprint.route('/getAllGrade',methods = ['POST'])
def getAllGrade():
    res = {
        'status' : False,
        'info' : '',
        'data' : None
    }
    
    userName = request.form.get('username')
    passWord = request.form.get('password')
    vpnUserName = request.form.get('vpnusername')
    vpnPassWord = request.form.get('vpnpassword')
    if not userName or not passWord or not vpnUserName or not vpnPassWord:
        res['info'] = '缺少参数'
        return json.dumps(res)
    robot = Robot('https://jwglxt.w.buct.edu.cn', userName, passWord)
    vpnlogon = robot.vpnLogin(vpnUserName, vpnPassWord)
    if not vpnlogon:
        res['info'] = 'VPN用户名或者密码错误'
        return json.dumps(res)
    robot.login()
    if not robot.isLogin():
        res['info'] = '用户名或者密码错误'
        return json.dumps(res)
    
    xnm = request.form.get('xnm')
    xqm = request.form.get('xqm')
    xqm = [3, 12, 16][int(xqm) - 1]

    allGrade = robot.getGrade(xnm,xqm)
    res['status'] = True
    res['data'] = allGrade
    res['info'] = 'success'
    return json.dumps(res)

@jwBlueprint.route('/getDetailScore',methods = ['POST'])
def getDetailScore():