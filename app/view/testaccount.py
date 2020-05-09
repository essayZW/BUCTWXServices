# -*- encoding: utf8 -*-
from flask import Blueprint, request, abort
import json
from ..model import testaccountmodel
testAccountBlueprint = Blueprint('testAccount', __name__)

# 验证体验账号的用户名密码是否正确
def checkLogin():
    username = request.args.get('username')
    password = request.args.get('password')
    vpnusername = request.args.get('vpnusername')
    vpnpassword = request.args.get('password')
    return testaccountmodel.login(username, password) and testaccountmodel.vpnLogin(vpnusername, vpnpassword)

# /jw/getAllGrade
def getAllGrade():
    rep = {
        'status' : False,
        'info' : '',
        'data' : ''
    }
    # 检查体验账号的登陆
    rep['status'] = checkLogin()
    if not rep['status']:
        rep['info'] = '登陆失败'
        return json.dumps(rep)
    # 从模型中得到预先准备的信息
    username = request.args.get('username')
    rep['data'] = testaccountmodel.getAllGrade(username)
    rep['status'] = True
    rep['info'] = 'success'
    rep['sinfo'] = testaccountmodel.getStuInfo(username)
    rep['sinfo']['gpa'] = testaccountmodel.getGpa(username)
    return json.dumps(rep)

# /jw/getSingleGrade
def getSingleGrade():
    classm = request.args.get('classm')
    rep = {
        'status' : False,
        'info' : '',
        'data' : ''
    }
    if not classm:
        rep['info'] = '缺少课程名'
        return json.dumps(rep)
    # 检查体验账号的登陆
    rep['status'] = checkLogin()
    if not rep['status']:
        rep['info'] = '登陆失败'
        return json.dumps(rep)
    # 从模型中得到预先准备的信息
    rep['data'] = testaccountmodel.getSingleGrade(classm)
    rep['status'] = True
    rep['info'] = 'success'
    return json.dumps(rep)

# 得到体验账号的GPA
def getGpa():
    rep = {
        'status' : False,
        'info' : '',
        'data' : ''
    }
    # 检查体验账号的登陆
    rep['status'] = checkLogin()
    if not rep['status']:
        rep['info'] = '登陆失败'
        return json.dumps(rep)
    # 从模型中得到预先准备的信息
    username = request.args.get('username')
    rep['data'] = testaccountmodel.getGpa(username)
    rep['status'] = True
    rep['info'] = 'success'
    return json.dumps(rep)
# 得到体验账号的考试信息
def getExamInfo():
    rep = {
        'status' : False,
        'info' : '',
        'data' : ''
    }
    # 检查体验账号的登陆
    rep['status'] = checkLogin()
    if not rep['status']:
        rep['info'] = '登陆失败'
        return json.dumps(rep)
    # 从模型中得到预先准备的信息
    username = request.args.get('username')
    rep['data'] = testaccountmodel.getExamInfo(username)
    rep['status'] = True
    rep['info'] = 'success'
    return json.dumps(rep)
# 自定义的路由列表，绑定函数以及对应的API地址
routeList = {
    '/jw/getAllGrade' : getAllGrade,
    '/jw/getSingleGrade' : getSingleGrade,
    '/jw/getGpa' : getGpa,
    '/jw/getExamInfo' : getExamInfo
}

@testAccountBlueprint.route('/')
def route():
    path = request.args.get('locationpath')
    if path not in routeList:
        abort(404)
    return routeList[path]()