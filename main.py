import time
import json
from app import App, view, AppCofig, encrypt
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

    # 请求安全性验证
    @App.before_request
    def check():
        if AppCofig['debug']:
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
    
    # 运行
    App.run(
        debug = AppCofig['debug'],
        port = AppCofig['port'],
        host = AppCofig['host']
    )
