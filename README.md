# BUCTWXServices

为参加BUCT小程序比赛的后端项目

# 注意事项

1. 开发时需要修改`app/config.py`中的`debug`为`True`,这样可以开启Flask的Debug模式，并且忽略接口需要的Token安全验证

2. 一个功能模块使用一个Flask蓝图，对应一个`app/view/` 下的python文件，添加新的view视图文件需要在`app/view/__init__.py`中做相应的引入。

   例如：

   现有文件`app/view/test.py`，其代码内容如下

   ```python
   # 引入蓝图功能
   from flask import Blueprint
   
   '''
   引入对应的模型
   其文件为app/model/test_model.py
   '''
   from ..model import test_model
   # 创建一个蓝图，在main.py中注册
   testBlueprint = Blueprint('test', __name__)
   
   @testBlueprint.route('/')
   def index():
       # 调用模型中的函数
       # 模型在下一条中讲到，这里返回hello world
       return test_model.test()
   ```

   因此需要在`app/view/__init__.py`中添加如下代码

   ```python
   '''
   从当前的目录下引入test.py文件
   '''
   from . import test
   ```

   来保证正确引入视图，在`main.py`中通过以下绑定蓝图

   ```python
   from app import view # 引入所有的视图
   from app import App  # 引入应用实例
   '''
   注册了view/test.py中的testBlueprint蓝图对象
   '''
   App.register_blueprint(view.test.testBlueprint, url_prefix = '/test')
   ```

   这样就可以访问`/test/`路径获得了输出`hello world`

3. 若视图需要数据库支持，需要将数据库相关代码在`app/model`中创建模型，并且在`app/model/`中引入相关文件。

   另外数据库的配置需要导入配置文件`app/config.py`

   现有模型文件`app/model/test_model.py`

   ```python
   # 导入父目录中的config.py中的AppConfig配置数组
   from ..config import AppCofig
   
   def test():
       return 'hellow world!'
   ```

   在`app/model/__init__.py`中需要添加如下代码以引入改模型

   ```python
   '''
   测试代码，在这里引入该包下面的test_model.py
   '''
   from . import test_model
   ```

   在`app/view/test.py`视图中引入模型

   ```python
   '''
   引入对应的模型
   其文件为app/model/test_model.py
   '''
   from ..model import test_model
   ```

   就可以通过`test_model.test()`调用模型中的函数

4. 所有包中的`__init__.py`文件首行应该注明当前路径，以防止多个`__init__.py`混淆

   如`app/model/__init__.py`中

   ```python
   # app/model/__init__.py
   
   '''
   测试代码，在这里引入该包下面的test_model.py
   '''
   from . import test_model
   # 测试代码结束
   ```

5. 导入爬虫以及相关的自定义的模块

   所有的爬虫模块或者自定义的模块都应该放在`app/module`目录下面，如现有爬虫模块`jwrobot`

   ```text
   module
   │  __init__.py
   │
   ├─jwrobot
   │  │  hex2b64.py
   │  │  robot.py
   │  │  RSAJS.py
   │  │  __init__.py
   ```

   这是目录结构，其中`app/module/__init__.py`中需要引入模块

   ```python
   # 教务类
   from . import jwrobot
   ```

   至于`jwrobot` 这个模块就自定义`__init__.py`文件。

   在`app/view/jw.py`中使用该模块

   ```python
   # 引入教务爬虫
   from ..moudle.jwrobot import Robot
   '''
   其意思是从当前目录的上一个目录(app/)中的module模块中的jwrobot模块中引入其中的一个Robot类
   或者这样也可以引入
   from ..module import jwrobot
   这样就引入了整个jwrobot模块，调用爬虫就需要使用jwrobot.Robot
   '''
   ```

6. 对应所有`module`下的`__pycache__`文件应该在`.gitignore`文件中忽略，其实缓存文件，没必要使用git管理

   比如现有`.gitignore`文件内容如下：

   ```text
   test.py
   # pycache
   app/__pycache__/
   app/**/__pycache__/
   ```
   
7. API返回数据的大概格式
   
   ```json
   {
       'status' : True, // 此次请求是否成功
       'info'   : '',    // 请求处理的相关信息，一般成功了的话就是success,失败的话就是大概的错误信息
       'data'	 : ''	 // 所请求的数据，没有则为空
   }
   ```
   
   以上三项是必须的，可以适当增加，但是必须要在文档说明
#  教务管理系统

## 成绩查询

成绩查询包含两个部分

* 查询指定学年学期的所有成绩信息
* 查询某学年某科目的的成绩明细

### 查询学年学期成绩

URL: `/jw/getAllGrade`

Method: **POST**

Params: 

|   参数名    |  类型  |         说明         |
| :---------: | :----: | :------------------: |
|     xnm     |  int   |       学年编号       |
|     xqm     |  int   |       学期编号       |
|  username   | string |      教务用户名      |
|  password   | string |       教务密码       |
| vpnusername | string | w.buct.edu.cn 用户名 |
| vpnpassword | string | w.buct.edu.cn  密码  |

Response Type: **JSON**

Response Date:

```json
{
    'status' : True, // 此次请求是否成功
    'info'   : '',    // 请求处理的相关信息，一般成功了的话就是success,失败的话就是大概的错误信息
    'data'	 : '',	 // 所请求的数据，没有则为空
    'sinfo'  : ''	 // 该学生的班级以及名字信息
}
```



### 查询指定科目成绩

URL: `/jw/getSingleGrade`

Method: **POST**

Params: 

| 参数名 |              类型              |   说明   |
| :----: | :----------------------------: | :------: |
|  xnm   |              int               | 学年编号 |
|  xqm   |              int               | 学期编号 |
| classm | string |   课程名称(中文)   |
| username | string |      教务用户名      |
| password | string |       教务密码       |
| vpnusername | string | w.buct.edu.cn 用户名 |
| vpnpassword | string | w.buct.edu.cn  密码  |

Response Type: **JSON**

Response Date:

```json
{
    'status' : True, // 此次请求是否成功
    'info'   : '',    // 请求处理的相关信息，一般成功了的话就是success,失败的话就是大概的错误信息
    'data'	 : ''	 // 所请求的数据，没有则为空
}
```

## 查询学生基本信息

该项目包含一个API，查询学生的姓名，以及班级

### 查询信息

URL: `/jw/getStuInfo`

Method: **POST**

Params: 

| 参数名 |              类型              |   说明   |
| :----: | :----------------------------: | :------: |
| username | string |      教务用户名      |
| password | string |       教务密码       |
| vpnusername | string | w.buct.edu.cn 用户名 |
| vpnpassword | string | w.buct.edu.cn  密码  |

Response Type: **JSON**

Response Date:

```json
{
    'status' : True, // 此次请求是否成功
    'info'   : '',    // 请求处理的相关信息，一般成功了的话就是success,失败的话就是大概的错误信息
    'data'	 : ''	 // 所请求的数据，没有则为空
}
```

### 查询GPA

URL:`/jw/getGpa`

Method:**POST**

Params:

|   参数名    |  类型  |         说明         |
| :---------: | :----: | :------------------: |
|  username   | string |      教务用户名      |
|  password   | string |       教务密码       |
| vpnusername | string | w.buct.edu.cn 用户名 |
| vpnpassword | string | w.buct.edu.cn  密码  |

Response Type: **JSON**

Response Date:

```json
{
    'status' : True, // 此次请求是否成功
    'info'   : '',    // 请求处理的相关信息，一般成功了的话就是success,失败的话就是大概的错误信息
    'data'	 : ''	 // 所请求的数据，没有则为空
}
```

## 查询课表

URL:`/jw/getSchedule`

Method: **POST**

Params:

|   参数名    |  类型  |         说明         |
| :---------: | :----: | :------------------: |
|     xnm     |  int   |       学年编号       |
|     xqm     |  int   |       学期编号       |
|  username   | string |      教务用户名      |
|  password   | string |       教务密码       |
| vpnusername | string | w.buct.edu.cn 用户名 |
| vpnpassword | string | w.buct.edu.cn  密码  |

ResponseType:**JSON**

Response Date:

```json
{
    'status' : True, // 此次请求是否成功
    'info'   : '',    // 请求处理的相关信息，一般成功了的话就是success,失败的话就是大概的错误信息
    'data'	 : ''	 // 所请求的数据，没有则为空
}
```

## 考试信息查询

URL:`/jw/getExamInfo`

Method: **POST**

Params:

|   参数名    |  类型  |         说明         |
| :---------: | :----: | :------------------: |
|     xnm     |  int   |       学年编号       |
|     xqm     |  int   |       学期编号       |
|  username   | string |      教务用户名      |
|  password   | string |       教务密码       |
| vpnusername | string | w.buct.edu.cn 用户名 |
| vpnpassword | string | w.buct.edu.cn  密码  |

ResponseType:**JSON**

Response Date:

```json
{
    'status' : True, // 此次请求是否成功
    'info'   : '',    // 请求处理的相关信息，一般成功了的话就是success,失败的话就是大概的错误信息
    'data'	 : ''	 // 所请求的数据，没有则为空
}
```

# 小程序反馈接口

此模块暂时由一个接口。

* 添加一条反馈信息

## 添加反馈信息
URL:`/feedBack/add`

Method: **POST**

Params:

|     参数名     |  类型   |           说明           |
| :------------: | :-----: | :----------------------: |
|    content     | string  | 反馈内容,不超过400，必须 |
|     email      | string  |           邮箱           |
|   use_score    | integer |       使用操作分数       |
|  style_score   | integer |       界面样式分数       |
| function_score | integer |   w.buct.edu.cn 用户名   |
|      time      | string  |  提交时间，是一个时间戳  |

ResponseType:**JSON**

Response Date:

```json
{
    'status' : True, // 此次请求是否成功
    'info'   : '',    // 请求处理的相关信息，一般成功了的话就是success,失败的话就是大概的错误信息
    'data'	 : ''	 // 所请求的数据，没有则为空
}
```

# 小程序页面设置

该模块的视图提供了对于小程序的一些设置，小程序获取这些设置以更新部分内容

## 得到首页轮播图设置

URL:`/swiper/getAll`

Method: **POST**

Params:**None**

ResponseType:**JSON**

Response Date:

```json
{
    'status' : True, // 此次请求是否成功
    'info'   : '',    // 请求处理的相关信息，一般成功了的话就是success,失败的话就是大概的错误信息
    'data'	 : [
    	'type' : ''	//该轮播的类型，src代表页面跳转，alert代表弹出信息
    	'dataset' : {
    		'src': '', // 如果是src类型则该条描述了跳转至何处
        	'alertcontent' : ''	// 如果是alert类型则给该条携带了显示的信息
		},
		'image' : ''	// 轮播图的图片地址
    ]
}
```

