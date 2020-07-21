# -*- encoding: utf8 -*-
from flask import Blueprint
import json
swiperBlueprint = Blueprint('swiper', __name__)
# 由于事件关系，暂时不链接数据库，内容写在文件里面

@swiperBlueprint.route('/getAll', methods=['POST'])
def getAllSwiperData():
    notice = '''# V1.2.0.200720 更新日志
## 新增功能
1. 新增课程表功能
> 首次使用需要进入 `系统设置->课程表设置` 中进行课程表更新以及该学期第一周日期的设置
## BUG修复
1. 修复课程表对于单周双周课程解析的错误
## 其他
1. 首页布局修改优化'''
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