# -*- encoding: utf-8 -*-
import time
import json
from app import App, view, AppCofig, encrypt, decrypt
from flask import request, make_response
if __name__ == "__main__":
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

    # 请求安全性验证
    @App.before_request
    def check():
        if AppCofig['debug']:
            return
        # 对参数进行预处理
        requestData = dict(request.form)
        decryptList = ['username', 'password', 'vpnusername', 'vpnpassword']
        for i in decryptList:
            if not requestData.get(i):
                continue
            requestData[i] = decrypt(requestData[i])
        request.form = requestData
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
    # 运行
    App.run(
        debug = AppCofig['debug'],
        port = AppCofig['port'],
        host = AppCofig['host']
    )
