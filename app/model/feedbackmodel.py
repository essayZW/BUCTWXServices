# -*- encoding: utf8 -*-
# 引入数据库配置
from ..config import AppCofig
# 向数据库添加一条记录
def add(data):
    '''
    这个函数需要完善
    主要功能就是连接数据库，然后添加data 参数到数据库，关闭数据库，返回布尔值是否添加完成
    data是一个dict,其中包含了反馈的内容，三个评分的分数，时间
    data = {
        content : '',
        time : '',
        score : [
            '分数1', '分数2', '分数3'
        ]
    }
    数据库中表的声明：
    content字段是text类型(或者longtext)，有点忘了
    time字段是一个varchar(20)，存储的是一个时间戳
    score的三个项都是int类型，如果用户没有填写就是-1
    建议score的三个字段名字为use_score, style_score, fun_score
    '''
    # print(data)
    return True