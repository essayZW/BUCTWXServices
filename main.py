# -*- encoding: utf-8 -*-
import time
import json
from app import App, view, AppCofig, encrypt, decrypt, TokenPathList, TestAccountList
from flask import request, make_response, redirect, url_for
from app import Aes

# 测试代码开始
'''
注册了view/test.py中的testBlueprint蓝图对象
'''
App.register_blueprint(view.test.testBlueprint, url_prefix = '/test')
# 测试代码结束

# 注册教务蓝图,并设置URL前缀为 /jw
App.register_blueprint(view.jw.jwBlueprint, url_prefix = '/jw')

# 注册反馈蓝图，URL前缀为 /feedBack
App.register_blueprint(view.feedback.feedBackBlueprint, url_prefix='/feedBack')

# 注册体验账号蓝图,URL前缀为 /testaccount
App.register_blueprint(view.testaccount.testAccountBlueprint, url_prefix='/testAccount')

# 注册轮播图设置蓝图，URL前缀为 /swiper
App.register_blueprint(view.swiper.swiperBlueprint, url_prefix='/swiper')
# 请求安全性验证
@App.before_request
def check():
    if not AppCofig['debug'] and not request.args.get('locationpath'):
        # 开发模式以及重定向情况下不执行
        # 对参数进行预处理
        requestData = dict(request.form)
        decryptList = ['username', 'password', 'vpnusername', 'vpnpassword']
        for i in decryptList:
            if not requestData.get(i):
                continue
            requestData[i] = decrypt(requestData[i])
        request.form = requestData

    # 判断是否是体验账号
    username = request.form.get('username')
    if username in TestAccountList and not request.args.get('locationpath'):
        return redirect(url_for('testAccount.route', locationpath=request.path, **request.form), code=302)

    if AppCofig['debug']:
        return
    
    # 判断是否在token保护列表中
    if request.path not in TokenPathList:
        return
    if not request.args.get('token') or not request.args.get('timetoken') or not request.args.get('random'):
        return make_response(json.dumps({
            'status' : 403,
            'info'   : 'forbidden'
        }), 403)
    timetoken = request.args.get('timetoken')
    try:
        timetoken = int(timetoken)
    except ValueError:
        # 时间戳不是一个合法数字
        return make_response(json.dumps({
            'status' : 500,
            'info'   : 'time error'
        }))
    nowtime = int(round(time.time() * 1000))
    if abs(nowtime - timetoken) > AppCofig['maxtime']:
        # URL过期
        return make_response(json.dumps({
            'status' : 500,
            'info'   : 'time limit exced'
        }), 500)
    randomNum = request.args.get('random')
    try:
        randomNum = int(randomNum)
    except ValueError:
        # 随机数不是一个数字
        return make_response(json.dumps({
            'status' : 500,
            'info'   : 'param error'
        }), 500)
    # 开始加密
    getToken = encrypt(timetoken, randomNum)
    flag = True
    lens = len(getToken)
    requestToken = request.args.get('token')
    for i in range(0, lens, 2):
        if not getToken[i] == requestToken[i]:
            flag = False
            break
    if not flag:
        return make_response(json.dumps({
            'status' : 403,
            'info'   : 'error token'
        }), 403)
# 处理响应数据
@App.after_request
def encryptResponse(rep):
    if request.path not in TokenPathList and not request.args.get('locationpath'):
        return rep
    if AppCofig['debug']:
        return rep
    # 低于1.2.3.200732版本的不进行加密
    version = request.args.get('version')
    if not version:
        return rep
    flag = False
    try:
        version = int(version.replace('.', ''))
        if version < 123200732:
            flag = True
    except ValueError:
        flag = True
    if flag:
        return rep

    aes = Aes(AppCofig['AESkey'], AppCofig['AESiv'])
    try:
        repData = json.loads(rep.get_data())
        if not repData.__contains__('data') or repData['data'] == None:
            return rep
        if isinstance(repData['data'], dict) or isinstance(repData['data'], list):
            repData['data'] = json.dumps(repData['data'])
        repData['data'] = aes.encrypt(repData['data']).decode("utf-8")
        rep.set_data(json.dumps(repData))
    except json.decoder.JSONDecodeError:
        pass
    return rep

# 处理500页面
@App.errorhandler(500)
def pageRuntimeError(e):
    return json.dumps({
        'status' : False,
        'info' : 'Runtime Error',
    }), 500

# 处理404界面
@App.errorhandler(404)
def pageNotFound(e):
    return json.dumps({
        'status' : False,
        'info' : 'Not Found'
    }), 404
if __name__ == "__main__":
    # 运行
    App.run(
        debug = AppCofig['debug'],
        port = AppCofig['port'],
        host = AppCofig['host']
    )
