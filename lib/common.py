# 登陆装饰器

# 登陆认证装饰器
import logging.config
from conf import settings
from functools import wraps
def get_auth(func):
    from core import src  # 将第一次登陆的用户字典 进行保存判断
    @wraps(func)
    def inner(*args,**kwargs):
        # 原函数执行之前的添加功能
        if src.user_info['name']:
            res = func(*args,**kwargs)
            # 原函数执行之后要添加的功能
            return res
        else:
            # 否则去重新登陆
            src.login()
    return inner

# hashlib对用户米密码进行加密

import hashlib

def get_md5(pwd):
    new_md= hashlib.md5()
    str1 = 'user_info'
    # 加点盐
    new_md.update((str1).encode('utf-8'))
    new_md.update((pwd).encode('utf-8'))

    return new_md.hexdigest()



# 配置日志字典：函数
def get_logger(data):  #  参数是用户自己传的

    logging.config.dictConfig(settings.LOGGING_DIC)  # 自动加载字典中的配置
    logger1 = logging.getLogger(data)  # 内容不应该别写死
    # logger1.debug('好好的 不要浮躁 努力就有收获')  # debug 内容不应该让他认为输入
    return logger1  # 返回日志对象

