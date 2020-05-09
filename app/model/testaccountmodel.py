# -*- encoding: utf-8 -*-
from ..config import TestAccountList
import json
import os
def login(username, password):
    # 假装体验账号的教务登陆
    if username not in TestAccountList:
        return False
    if not TestAccountList[username]['password'] == password:
        return False
    return True

def vpnLogin(vpnusername, vpnpassword):
    # 假装体验账号的VPN登陆
    if vpnusername not in TestAccountList:
        return False
    if not TestAccountList[vpnusername]['vpnpassword']:
        return False
    return True

def getDataPath(filename):
    # 得到data文件夹下的某个数据文件
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', filename)

def getAllGrade(username):
    # 得到体验账号的所有成绩
    data = {}
    with open(getDataPath('jwAllGrade.txt'), 'r', encoding="utf-8") as f:
        data = f.read()
    data = json.loads(data)
    return data[username] if username in data else {}

def getSingleGrade(name):
    # 得到体验账号的单个成绩
    data = {}
    with open(getDataPath('jwSingleGrade.txt'), 'r', encoding="utf-8") as f:
        data = f.read()
    data = json.loads(data)
    return data[name] if name in data else []

def getGpa(username):
    #  得到体验账号的GPA
    data = {}
    with open(getDataPath('jwGPA.txt'), 'r', encoding="utf-8") as f:
        data = f.read()
    data = json.loads(data)
    return data[username] if username in data else {}

def getStuInfo(username):
    #  得到体验账号的个人信息
    data = {}
    with open(getDataPath('jwStuInfo.txt'), 'r', encoding="utf-8") as f:
        data = f.read()
    data = json.loads(data)
    return data[username] if username in data else {}
def getExamInfo(username):
    #  得到体验账号的个人信息
    data = {}
    with open(getDataPath('jwExamInfo.txt'), 'r', encoding="utf-8") as f:
        data = f.read()
    data = json.loads(data)
    return data[username] if username in data else {}