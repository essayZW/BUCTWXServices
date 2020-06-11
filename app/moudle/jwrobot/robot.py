# -*- encoding: utf8 -*-
import re
import time
import json
import requests
from bs4 import BeautifulSoup
if __name__ == '__main__':
    import RSAJS
    from hex2b64 import HB64
else:
    from . import RSAJS
    from .hex2b64 import HB64
requests.packages.urllib3.disable_warnings()
class Robot(object):
    def __init__(self, baseUrl, username, password):
        self.baseUrl = baseUrl
        self.__username = username
        self.__password = password
        self.__req = requests.session()
        self.__modulus = None
        self.__exponent = None
        self.__isLogin = False      #登录状态
        self.__indexCode = ''       #主页HTML代码
        self.nowTime = int(time.time())
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
    #根据公匙加密密码
    def __RSAkey(self):
        rsaKey = RSAJS.RSAKey()
        rsaKey.setPublic(HB64().b642hex(self.__modulus),HB64().b642hex(self.__exponent))
        return HB64().hex2b64(rsaKey.encrypt(self.__password))
    #得到RSA加密公匙
    def _getPublicKey(self):
        _path = '/jwglxt'
        modulusPath = self.baseUrl + _path + '/xtgl/login_getPublicKey.html?time=' + str(self.nowTime)
        backJson = json.loads(self.__req.get(modulusPath, verify = False).text)
        self.__modulus = backJson['modulus']
        self.__exponent = backJson['exponent']
    #得到隐藏域表单数据(CSRFToken)
    def _getCSRFToken(self):
        rep = self.__req.get(self.baseUrl + '/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t=' + str(self.nowTime), verify = False)
        csrfPattern = '<input type="hidden" id="csrftoken" name="csrftoken" value="(.*?)"/>'
        self.csrfToken = re.findall(csrfPattern, rep.text)
        if len(self.csrfToken) >= 1:
            self.csrfToken = self.csrfToken[0]
    # 登陆
    def login(self):
        if self.__isLogin:
            return True
        #模拟用户登录
        self._getCSRFToken()
        self._getPublicKey()
        enpassword = self.__RSAkey()
        #需要发送的表单数据
        data = {
            'yhm' : self.__username,
            'mm' : enpassword,
            'csrftoken' : self.csrfToken
        }
        rep = self.__req.post(self.baseUrl + '/jwglxt/xtgl/login_slogin.html', data = data, headers = self.header, verify = False)
        if rep.url == self.baseUrl + '/jwglxt/xtgl/index_initMenu.html':
            self.__isLogin = True
            self.__indexCode = rep.text
            if __name__ == '__main__':
                print('您已经登录成功！')
            self.getUserInfo()
        else:
            self.__isLogin = False
            if __name__ == '__main__':
                print('登录失败，用户名或者密码错误！')
    #获取是否登录
    def isLogin(self):
        return self.__isLogin
    # VPN登陆
    def vpnLogin(self, username, password):
        # 由于学校VPN系统变更，现在暂时不需要VPN登陆
        return True
        if self.useVpn:
            return True
        vpnUrl = 'https://w.buct.edu.cn/users/sign_in'
        indexBack = self.__req.get(vpnUrl, headers = self.header, verify = False)
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
        login = self.__req.post(vpnUrl, data = data, headers = self.header, verify = False)
        searchLoginStatus = '<li><a rel="nofollow" data-method="delete" href="/users/sign_out">退出登录</a></li>'
        if searchLoginStatus in login.text:
            self.useVpn = True
            return True
        else:
            return False


    #得到成绩信息
    def getGrade(self, xnm, xqm):
        if not self.__isLogin:
            return None
        gradeUrl = self.baseUrl + '/jwglxt/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default&su=' + self.__username
        xqm = [3, 12, 16][int(xqm) - 1]
        datas = {
            'xnm' : xnm,
            'xqm' : xqm,
            '_search' : False,
            'nd' : self.nowTime,
            'queryModel.showCount' : 30,
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
        rep = self.__req.post(self.baseUrl + '/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005', data = datas, headers = head, verify = False)
        if __name__ == "__main__":
            num = 1
            gradeJSON = json.loads(rep.text)
            for i in gradeJSON['items']:
                print('第%d门课: %s\n班级: %s;\n成绩: %s ;\n绩点 : %s ;\n\n\n' % (num, i['kcmc'], i['bj'], i['cj'], i['jd']))
                num += 1
        return json.loads(rep.text)
    
    #得到单科成绩信息
    def getScore(self, xnm, xqm, classm):
        xnm = int(xnm)
        xqm = int(xqm)
        classm = str(classm)
        # 先查询该学期的所有成绩
        allGrade = self.getGrade(xnm, xqm)
        xqm = [3, 12, 16][int(xqm) - 1]
        apiAddress = '/jwglxt/cjcx/cjcx_cxCjxq.html?gnmkdm=N305005&time=' + str(self.nowTime)
        jxbid = False
        # 获得教学班ID
        for i in allGrade['items']:
            if i['kcmc'] == classm:
                jxbid = i['jxb_id']
                break
        if not jxbid:
            return []
        # 发送请求
        datas = {
            'xnm' : xnm,
            'xqm' : xqm,
            'kcmc' : classm,
            'jxb_id' : jxbid
        }
        singleGrade = self.__req.post(self.baseUrl + apiAddress, data = datas, headers = self.header, verify= False)
        # 解析URL
        BS = BeautifulSoup(singleGrade.text, 'html.parser')
        tableArea = BS.select_one('tbody')
        trs = tableArea.select('tr')
        res = []
        for i in trs:
            tds = i.select('td')
            temp = []
            for j in tds:
                temp.append(j.string.replace('&nbsp;', '').replace('\xa0', '').replace('【', '').replace('】', '').replace(' ', ''))
            if '总评' in temp:
                temp[1] = '100%'
            res.append(temp)
        return res
     
    #得到登录用户的信息
    def getUserInfo(self):
        if not self.__isLogin:
            return
        apiUrl = '/jwglxt/xtgl/index_cxYhxxIndex.html?xt=jw&localeKey=zh_CN&_=' + str(self.nowTime) + '&gnmkdm=index&su=' + self.__username
        rep = self.__req.get(self.baseUrl + apiUrl, verify = False)
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


    # 得到课表
    def getClassTable(self, xnm, xqm):
        if not self.__isLogin:
            return None
        classTableUrl = self.baseUrl + '/jwglxt/kbcx/xskbcx_cxXskb.html?gnmkdm=N2151&layout=default&su=' + self.__username
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
        head['Referer'] = classTableUrl
        head['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        head['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        if 'Upgrade-Insecure-Requests' in head:
            head.pop('Upgrade-Insecure-Requests')
        rep = self.__req.post(self.baseUrl+'/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151', data = datas, headers = head, verify = False)
        return json.loads(rep.text)        

    # 得到考试信息
    def getExamInfo(self, xnm, xqm):
        if not self.__isLogin:
            return None
        xqm = [3, 12, 16][int(xqm) - 1]
        # ksmcdmb_id，需要动态获取
        ksmcList = []
        rep = self.__req.post(self.baseUrl + '/jwglxt/ksglcommon/common_cxKsmcByXnxq.html?gnmkdm=N358105', data = {
            'xqm' : xqm,
            'xnm' : xnm
        }, headers = self.header, verify = False)
        ksmcdmbJSON = json.loads(rep.text);
        for i in ksmcdmbJSON:
            ksmcList.append(i['KSMCDMB_ID'])
        # print(ksmcList)
        # 获取考试信息
        examInfoUrl = self.baseUrl + '/jwglxt/kwgl/kscx_cxXsksxxIndex.html?gnmkdm=N358105&layout=default&su=' + self.__username
        datas = {
            'xnm' : xnm,
            'xqm' : xqm,
            'ksmcdmb_id' : '',
            '_search' : False,
            'nd' : self.nowTime,
            'queryModel.showCount' : 30,
            'queryModel.currentPage' : 1,
            'queryModel.sortName' : ' ',
            'queryModel.sortOrder' : 'asc',
            'time' : 1
        }
        head = self.header
        head['X-Requested-With'] = 'XMLHttpRequest'
        head['Referer'] = examInfoUrl
        head['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        head['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        if 'Upgrade-Insecure-Requests' in head:
            head.pop('Upgrade-Insecure-Requests')
        ksxxList = []
        for j in range(len(ksmcList)):
            datas['ksmcdmb_id']=ksmcList[j]
            rep = self.__req.post(self.baseUrl + '/jwglxt/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105', data = datas, headers = head, verify = False)
            examInfoJSON = json.loads(rep.text)
            for i in examInfoJSON['items']:
                ksxxList.append(i)
            if __name__ == "__main__":
                None
                # print('考试名称：%s;\n课程名: %s;\n班级: %s;\n老师: %s ;\n时间 : %s ;\n地点 ：%s ;\n\n\n' % (i['ksmc'], i['kcmc'], i['bj'], i['jsxx'], i['kssj'], i['cdmc']))
        info = []
        for i in ksxxList:
            info.append({
                'kcmc' : i['kcmc'],
                'cdmc' : i['cdmc'],
                'kssj' : i['kssj'],
                'jsxx' : i['jsxx']
            })
        if ksxxList:
            return info
        else:
            # print(self.getExamTime())
            return self.getExamTime()

        
        
    
    #得到GPA
    def getGPA(self):
        if not self.__isLogin:
            return None
        gpaUrl = self.baseUrl + '/jwglxt/xsxy/xsxyqk_cxXsxyqkIndex.html?gnmkdm=N105515&layout=default&su=' + self.__username
        rep = self.__req.get(gpaUrl, verify = False)
        BS = BeautifulSoup(rep.text,'html.parser')
        allFont = BS.select('#alertBox>font')
        gpaFont = allFont[1].select_one('font').text
        timeFont = allFont[0].text
        timeCu = re.search('[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])\s+(20|21|22|23|[0-1]\d):[0-5]\d:[0-5]\d', timeFont)
        dict = {
            'gpa' : gpaFont ,
            'time': timeCu.group()
        }
        """
        'gpa' : gpa
        'time' : current time
        """
        head = self.header
        head['X-Requested-With'] = 'XMLHttpRequest'
        head['Referer'] = gpaUrl
        head['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        head['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        if 'Upgrade-Insecure-Requests' in head:
            head.pop('Upgrade-Insecure-Requests')
        # print(dict)
        #for value in dict.values():
            #print(format(value))
        return dict

    # 得到考试时间
    def getExamTime(self):
        if not self.__isLogin:
            return None
        examTimeUrl = self.baseUrl + '/jwglxt/design/funcData_cxFuncDataList.html?func_widget_guid=58944B9C2CD784DBE053839D04CA5AD7&gnmkdm=N358163&su=' + self.__username
        datas = {
            '_search' : False,
            'nd' : self.nowTime,
            'queryModel.showCount' : 15,
            'queryModel.currentPage' : 1,
            'queryModel.sortName' : ' ',
            'queryModel.sortOrder' : 'asc',
        }
        head = self.header
        head['X-Requested-With'] = 'XMLHttpRequest'
        head['Referer'] = examTimeUrl
        head['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        head['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        if 'Upgrade-Insecure-Requests' in head:
            head.pop('Upgrade-Insecure-Requests')
        rep = self.__req.post(self.baseUrl+'/jwglxt/design/funcData_cxFuncDataList.html?func_widget_guid=58944B9C2CD784DBE053839D04CA5AD7&gnmkdm=N358163', data = datas, headers = head, verify = False)
        examTime=json.loads(rep.text)
        #print(examTime)
        
        info = []
        pattern = re.compile('^(\d+?)\-(\d+?)\-(\d+?) (\d+?)\:(\d+?)\-(\d+?)\:(\d+?)$')
        for i in examTime['items']:
            dict = {
                'kcmc' : '',
                'cdmc' : '暂无',
                'kssj' : '',
                'jsxx' : '暂无'
            }
            #正则表达式修改时间格式  
            dict['kcmc'] = i['kcmc']
            dict['kssj'] = i['kssj']
            patternMatch = pattern.findall(dict['kssj'])
            if len(patternMatch):
                dict['kssj'] = '{0}-{1}-{2}({3}:{4}-{5}:{6})'.format(*patternMatch[0])
            info.append(dict)
        #print(info)
        return info     

if __name__ == "__main__":
    None

