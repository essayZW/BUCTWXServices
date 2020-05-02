# -*- encoding: utf8 -*-
import random
import base64
# 配置文件
AppCofig = {
    # 应用运行相关设置
    # 是否开启DEBUG模式
    'debug'     : True,
    # 应用运行端口
    'port'      : 8888,
    # 运行地址
    'host'      : '127.0.0.1',


    # 数据库相关设置
    # 数据库用户名
    'username'      : '',
    # 数据库密码 
    'password'      : '',
    # 数据库地址
    'databasehost'  : '127.0.0.1',
    # 数据库端口
    'databaseport'  : '3306',
    # 数据库库名
    'database'      : '',

    # 请求安全性验证设置
    # URL过期时间，单位：毫秒，默认1分钟
    'maxtime'      : 60000 
}

# 加密函数
def encrypt(timetoken, randomnum):
    numArr = []
    while timetoken > 0:
        numArr.append(((timetoken % 10 + 40) ^ randomnum) % 256)
        timetoken = int(timetoken / 10)
    numArr.reverse()
    bstr = ''
    for i in numArr:
        tempstr = ''
        num = 0
        while i > 0:
            num += 1
            tempstr = str(0 if i % 2 == 1 else 1) + tempstr
            i = int(i / 2)
        while num < 8:
            tempstr = '0' + tempstr
            num += 1
        # print(tempstr)
        bstr += tempstr
    hexdict = ['F', 'A', 'C', '2', '5', '0', 'D', 'B', 'E', '1', '7', '9', '4', '8', '3', '6']
    lens = len(bstr)
    hexstr = ''
    for i in range(0, lens, 4):
        base = 1
        num = 0
        res = 0
        while num < 4:
            res += int(bstr[i + num]) * base
            num += 1
            base *= 2
        hexstr += (hexdict[res] + hexdict[random.randint(0, 15)])
    return hexstr
# 解密函数，与上面的加密函数不是一套
def decrypt(encryptStr):
    return base64.b64decode(encryptStr).decode('utf-8')
if __name__ == "__main__":
    import time
    a = int(round(time.time() * 1000))
    print(a)
    print(encrypt(a, 120))
