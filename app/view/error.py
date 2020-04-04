from flask import make_response, Blueprint, request
import json
# 错误信息显示视图
errorBlurprint = Blueprint('error', __name__)
@errorBlurprint.route('/')
def error():
    return  make_response(json.dumps({
        'status' : request.args.get('status'),
        'info'   : request.args.get('info')
    }), request.args.get('status'))