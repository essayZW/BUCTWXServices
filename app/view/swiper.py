# -*- encoding: utf8 -*-
from flask import Blueprint
import json
swiperBlueprint = Blueprint('swiper', __name__)
# 由于事件关系，暂时不链接数据库，内容写在文件里面

@swiperBlueprint.route('/getAll', methods=['POST'])
def getAllSwiperData():
    notice = '''# 新版功能

## 教务

* 成绩查询
* 成绩详情查询
* GPA查询
* 考试信息查询

## 校园生活

* 日历功能
* 待办事件
* 自动整合考试信息到日历待办
* 待办与考试信息提醒

## 其他

* 自定义主题颜色切换'''
    return json.dumps({
        'data' : [
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
        'info' : 'success',
        'status' : True
    })