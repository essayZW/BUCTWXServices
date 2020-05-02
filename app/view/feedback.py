# -*- encoding: utf8 -*-
import json
from flask import Blueprint, request
# 引入模型
from ..model import feedbackmodel
# 创建反馈蓝图
feedBackBlueprint = Blueprint('feedBack', __name__)

@feedBackBlueprint.route('/add', methods=['POST'])
def addFeedBack():
    rep = {
        'status' : False,
        'info' : '',
        'data' : ''
    }
    content = request.form.get('content')
    time = request.form.get('time')
    score = list()
    score.append(request.form.get('use_score'))
    score.append(request.form.get('style_score'))
    score.append(request.form.get('function_score'))
    for i in range(3):
        score[i] = score[i] if score[i] else -1
        try:
            score[i] = int(score[i])
        except:
            score[i] = -1
        if score[i] > 5 or score[i] < -1:
            score[i] = -1

    # 内容和时间是必须的表单项 
    if not content or not time:
        rep['info'] = '缺少参数'
        return json.dumps(rep)
    
    # 验证长度以及数据类型
    if len(content) > 400:
        rep['info'] = '内容过长'
        return json.dumps(rep)
    
    # 调用模型中的add函数添加到数据库
    rep['status'] = feedbackmodel.add({
        'content' : content,
        'time'    : time,
        'score'   : score
    })
    if rep['status']:
        rep['info'] = 'success'
    else:
        rep['info'] = 'fail'
    return json.dumps(rep)