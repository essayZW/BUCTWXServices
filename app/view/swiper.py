# -*- encoding: utf8 -*-
from flask import Blueprint
import json
swiperBlueprint = Blueprint('swiper', __name__)
# 由于事件关系，暂时不链接数据库，内容写在文件里面

@swiperBlueprint.route('/getAll', methods=['POST'])
def getAllSwiperData():
    notice = '''# 1.3.0.200907 更新日志
## BUG修复
1. 课程表日期设置页面逻辑优化以及BUG修复
2. 教务成绩等页面全局主题颜色适配优化
3. 修复日历以及课程表信息丢失BUG
4. 修复主题设置页面自定义输入框内容丢失BUG
## 其他
1. 登陆页面移除校园网密码一栏'''
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