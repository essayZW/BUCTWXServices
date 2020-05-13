# -*- encoding: utf8 -*-
from flask import Blueprint
import json
swiperBlueprint = Blueprint('swiper', __name__)

@swiperBlueprint.route('/getAll', methods=['POST'])
def getAllSwiperData():
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
                    'alertcontent' : '暂无'
                },
                'image' : 'https://s1.ax1x.com/2020/05/13/YamWdg.png'
            }
        ],
        'info' : 'success',
        'status' : True
    })