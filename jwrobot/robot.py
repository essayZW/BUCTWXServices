import re
import time
import json
import requests
from bs4 import BeautifulSoup
from jwrobot import RSAJS
from jwrobot.hex2b64 import HB64
class robot(object):
    def __init__(self, baseUrl, username, password):
        self.baseUrl = baseUrl
        self.username = username
        self.password = password
        self.nowTime = int(time.time())
        self.req = requests.session()
        self.modulus = None
        self.exponent = None
        self.__isLogin = False      #登录状态
        self.__indexCode = ''       #主页HTML代码
        self.useVpn = False         #是否使用vpn
        self.header = {
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Referer": self.baseUrl + '/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t=' + str(self.nowTime),
            "Upgrade-Insecure-Requests": "1",
        }
        self.csrfToken = None
    def RSAkey(self):
        #根据公匙加密密码
        rsaKey = RSAJS.RSAKey()
        rsaKey.setPublic(HB64().b642hex(self.modulus),HB64().b642hex(self.exponent))
        return HB64().hex2b64(rsaKey.encrypt(self.password))
    def getPublicKey(self):
        #得到RSA加密公匙
        _path = '/jwglxt'
        modulusPath = self.baseUrl + _path + '/xtgl/login_getPublicKey.html?time=' + str(self.nowTime)
        backJson = json.loads(self.req.get(modulusPath).text)
        self.modulus = backJson['modulus']
        self.exponent = backJson['exponent']
    def getCSRFToken(self):
        #得到隐藏域表单数据(CSRFToken)
        rep = self.req.get(self.baseUrl + '/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t=' + str(self.nowTime))
        csrfPattern = '<input type="hidden" id="csrftoken" name="csrftoken" value="(.*?)"/>'
        self.csrfToken = re.findall(csrfPattern, rep.text)
        if len(self.csrfToken) >= 1:
            self.csrfToken = self.csrfToken[0]
    def login(self):
        if self.__isLogin:
            return True
        #模拟用户登录
        self.getCSRFToken()
        self.getPublicKey()
        # print("%s : %s : %s\n" % (self.csrfToken, self.modulus, self.exponent))
        enpassword = self.RSAkey()
        #需要发送的表单数据
        data = {
            'yhm' : self.username,
            'mm' : enpassword,
            'csrftoken' : self.csrfToken
        }
        rep = self.req.post(self.baseUrl + '/jwglxt/xtgl/login_slogin.html', data = data, headers = self.header)
        # print(rep.text)
        print(rep.url)
        # print(self.req.cookies)
        if rep.url == self.baseUrl + '/jwglxt/xtgl/index_initMenu.html':
            self.__isLogin = True
            self.__indexCode = rep.text
            if __name__ == '__main__':
                print('您已经登录成功！')
            self.getUserInfo()
        else:
            self.__isLogin = False
            print('登录失败，用户名或者密码错误！')
    def getUserInfo(self):
        #得到当前登录用户的信息
        if not self.__isLogin:
            return
        apiUrl = '/jwglxt/xtgl/index_cxYhxxIndex.html?xt=jw&localeKey=zh_CN&_=' + str(self.nowTime) + '&gnmkdm=index&su=' + self.username
        rep = self.req.get(self.baseUrl + apiUrl)
        BS = BeautifulSoup(rep.text, 'html.parser')
        name = BS.select_one('.media-body>h4').text                 #得到姓名
        classInfo = BS.select_one('.media-body>p').text             #得到年级班级信息
        headImgUrl = BS.select_one('.media-object').attrs['src']    #得到照片的URL
        if __name__ == '__main__':
            print(name)
            print(classInfo)
        return {
            'name' : name,
            'classInfo' : classInfo,
            'headImgInfo' : headImgUrl
        }
    def getGrade(self, xnm, xqm):
        #得到该学生的成绩信息
        if not self.__isLogin:
            return None
        gradeUrl = self.baseUrl + '/jwglxt/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default&su=' + self.username
        xqm = [3, 12, 16][int(xqm) - 1]
        datas = {
            'xnm' : xnm,
            'xqm' : xqm,
            '_search' : False,
            'nd' : self.nowTime,
            'queryModel.showCount' : 15,
            'queryModel.currentPage' : 1,
            'queryModel.sortName' : ' ',
            'queryModel.sortOrder' : 'asc',
            'time' : 1
        }
        head = self.header
        head['X-Requested-With'] = 'XMLHttpRequest'
        head['Referer'] = gradeUrl
        head['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        head['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        if 'Upgrade-Insecure-Requests' in head:
            head.pop('Upgrade-Insecure-Requests')
        rep = self.req.post(self.baseUrl + '/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005', data = datas, headers = head)
        if __name__ == "__main__":
            num = 1
            gradeJSON = json.loads(rep.text)
            for i in gradeJSON['items']:
                print('第%d门课: %s\n班级: %s;\n成绩: %s ;\n绩点 : %s ;\n\n\n' % (num, i['kcmc'], i['bj'], i['cj'], i['jd']))
                num += 1
        return json.loads(rep.text)
    def isLogin(self):
        #供外界调用获取是否登录
        return self.__isLogin

    def vpnLogin(self, username, password):
        if self.useVpn:
            return True
        vpnUrl = 'https://w.buct.edu.cn/users/sign_in'
        indexBack = self.req.get(vpnUrl, headers = self.header)
        # print(indexBack.text)
        indexCode = indexBack.text
        csrfParamPattern = '<meta name="csrf-param" content="(.*?)" />'
        csrfParam = re.findall(csrfParamPattern, indexCode)
        if len(csrfParam) >= 1:
            csrfParam = csrfParam[0]
        csrfTokenPattern = '<meta name="csrf-token" content="(.*?)" />'
        csrfValue = re.findall(csrfTokenPattern, indexCode)
        if len(csrfValue) >= 1:
            csrfValue = csrfValue[0]
        data = {
            'user[login]' : username,
            'user[password]' : password,
            'user[dymatice_code]' : 'unknown',
            'commit' : '登录 Login'
        }
        data[csrfParam] = csrfValue
        login = self.req.post(vpnUrl, data = data, headers = self.header)
        # print(login.text)
        searchLoginStatus = '<li><a rel="nofollow" data-method="delete" href="/users/sign_out">退出登录</a></li>'
        if searchLoginStatus in login.text:
            self.useVpn = True
            return True
        else:
            return False

if __name__ == "__main__":
    a = robot("http://jwglxt.w.buct.edu.cn", "2018040532", "dazw2000123")
    a.vpnLogin("2018040532", "dazw2000123")
