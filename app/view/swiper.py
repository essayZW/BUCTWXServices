# -*- encoding: utf8 -*-
from flask import Blueprint
import json
swiperBlueprint = Blueprint('swiper', __name__)
# 由于事件关系，暂时不链接数据库，内容写在文件里面

@swiperBlueprint.route('/getAll', methods=['POST'])
def getAllSwiperData():
    notice = '''# V1.0.4.200705更新日志
## BUG修复
1. IOS端无法登陆账户，无法输入
2. 日历待办页面切换回来初始化问题
3. 平板环境下图标登陆页面图标未居中
4. 关于 页面的小程序码未替换
5. 成绩查询界面对于名字过长的课程显示错乱问题
6. 第一次使用成绩查询配置好用户名密码后返回查询页面时个人信息不更新
## 用户体验优化
1. 成绩查询页面添加 `点击头像或者右滑选择学期查询` 提醒字样
2. 登陆界面添加隐私声明链接
## 新增功能
1. 添加服务器通知推送功能'''
    return json.dumps({
        'data' : {
            'swiper' : [
                {
                    'type' : 'src',
                    'dataset' : {
                        'src' : '/pages/jwgrade/jwgrade',
                        'alertcontent' : ''
                    },
                    'image': 'https://s1.ax1x.com/2020/05/13/YamReS.png'
                },
                {
                    'type': 'src',
                    'dataset' : {
                        'src' : '/pages/help/help',
                        'alertcontent' : ''
                    },
                    'image': 'https://s1.ax1x.com/2020/05/13/YamgL8.png'
                },
                {
                    'type' : 'alert',
                    'dataset' : {
                        'src' : '',
                        'alertcontent' : notice
                    },
                    'image' : 'https://s1.ax1x.com/2020/05/13/YamWdg.png'
                }
            ],
            'notice' : {
                'id' : '',
                'content' : ''
            }
        }        
        ,
        'info' : 'success',
        'status' : True
    })