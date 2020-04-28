# -*- encoding: utf8 -*-
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

    xnm = request.form.get('xnm')
    xqm = request.form.get('xqm')
    if not userName or not passWord or not vpnUserName or not vpnPassWord or not xnm or not xqm:
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
    

    allGrade = robot.getGrade(xnm,xqm)
    res['status'] = True
    res['data'] = allGrade
    res['info'] = 'success'
    res['sinfo'] = robot.getUserInfo()
    res['sinfo']['gpa'] = robot.getGPA()
    return json.dumps(res)

@jwBlueprint.route('/getSingleGrade',methods = ['POST'])
def getSingleGrade():
    res = {
        'status' : False,
        'info' : '',
        'data' : None
    }
    
    userName = request.form.get('username')
    passWord = request.form.get('password')
    vpnUserName = request.form.get('vpnusername')
    vpnPassWord = request.form.get('vpnpassword')

    xnm = request.form.get('xnm')
    xqm = request.form.get('xqm')
    classm = request.form.get('classm')
    if not userName or not passWord or not vpnUserName or not vpnPassWord or not xnm or not xqm or not classm:
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
    

    detailScore = robot.getScore(xnm,xqm,classm)
    res['status'] = True
    res['data'] = detailScore
    res['info'] = 'success'
    return json.dumps(res)

@jwBlueprint.route('/getSchedule',methods = ['POST'])
def getSchedule():
    res = {
        'status' : False,
        'info' : '',
        'data' : None
    }
    
    userName = request.form.get('username')
    passWord = request.form.get('password')
    vpnUserName = request.form.get('vpnusername')
    vpnPassWord = request.form.get('vpnpassword')
    xnm = request.form.get('xnm')
    xqm = request.form.get('xqm')
    if not userName or not passWord or not vpnUserName or not vpnPassWord or not xnm or not xqm:
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
    
    schedule = robot.getClassTable(xnm,xqm)
    res['status'] = True
    res['data'] = schedule
    res['info'] = 'success'
    return json.dumps(res)