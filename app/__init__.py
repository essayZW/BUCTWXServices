# app/__init__.py
# 引入flask
from flask import Flask
# 引入配置文件
from .config import AppCofig
from .config import encrypt
# 视图
from app import view
# 实例化Flask对象
App = Flask(__name__)
