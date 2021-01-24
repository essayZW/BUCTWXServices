# -*- encoding: utf8 -*-
# app/__init__.py
# 引入flask
from flask import Flask
# 引入配置文件
from .config import AppCofig
from .config import encrypt
from .config import decrypt
from .config import TokenPathList
from .config import TestAccountList
# 视图
from app import view
# 加密
from .moudle import Aes
# 实例化Flask对象
App = Flask(__name__)
