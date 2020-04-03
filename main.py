from app import App, view, AppCofig
if __name__ == "__main__":
    # 测试代码开始
    '''
    注册了view/test.py中的testBlueprint蓝图对象
    '''
    App.register_blueprint(view.test.testBlueprint, url_prefix = '/test')
    # 测试代码结束

    # 注册教务蓝图,并设置URL前缀为 /jw
    App.register_blueprint(view.jw.jwBlueprint, url_prefix = '/jw')
    # 运行
    App.run(
        debug = AppCofig['debug'],
        port = AppCofig['port'],
        host = AppCofig['host']
    )