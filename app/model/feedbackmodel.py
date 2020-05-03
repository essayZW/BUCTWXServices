# -*- encoding: utf8 -*-
import pymysql
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
    # 连接数据库
    configSQL = {
        'host' : AppCofig['databasehost'],
        'port' : AppCofig['databaseport'],
        'user' : AppCofig['username'], 
        'passwd' : AppCofig['password'], 
        'db' : AppCofig['database'], 
        'charset' : 'utf8',
        'cursorclass' : pymysql.cursors.DictCursor
    }

    # 游标
    con = pymysql.connect(**configSQL)
    cursor = con.cursor()

    # 插入
    insert = "insert into feedback (email, content, time, use_score, style_score, fun_score) values(%s, %s, %s, %s, %s, %s)"

    flag = True
    try:
        # 执行
        cursor.execute(insert, (data['email'], data['content'], data['time'], data['score'][0], data['score'][1], data['score'][2]))
        # 提交
        con.commit()
    except:
        flag = False
    
    finally:
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        con.close()
    return flag