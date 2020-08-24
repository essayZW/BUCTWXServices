# -*- encoding: utf8 -*-
from flask import Blueprint
import json
swiperBlueprint = Blueprint('swiper', __name__)
# 由于事件关系，暂时不链接数据库，内容写在文件里面

@swiperBlueprint.route('/getAll', methods=['POST'])
def getAllSwiperData():
    notice = '''# 1.2.4.200824 更新日志
## 新增功能
1. 小程序与服务器通信AES加密
## 其他
1. 课程表时间设置逻辑优化'''
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