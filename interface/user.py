# user接口层
from db import db_handles
from lib import common


def register_interface(name,pwd,balance=15000):
    user_dict = db_handles.select(name)
    if user_dict:
        return False,'用户已存在'
    # 对用户新注册的密码进行加密 存入文件
    new_md5 = common.get_md5(pwd)
    user_dict = {"name":name, "pwd":new_md5,"balance":balance,"flow":[],"shopping_car":{}}
    db_handles.save(user_dict)

    logger_obj = common.get_logger('用户注册功能')

    logger_obj.debug('尊敬的用户[%s] 您已成功注册我们ATM网站'%user_dict['name'])
    return True, '尊敬的用户[%s] 您已成功注册我们ATM网站'%user_dict['name']


# 登录接口层
def login_interface(name,pwd):
    user_dict = db_handles.select(name)
    if not user_dict:
        return False,'用户名不存在'
    # 调用公共功能层的登陆密码加密和文件中的密码进行对比判断是否一致
    new_md5 = common.get_md5(pwd)  # common 加密返回值 变量接收一下即可
    if new_md5 == user_dict['pwd']:  # 输入的加密密码是否和系统存的加密密码一致
        logger_obj = common.get_logger('用户登录功能')
        logger_obj.info('尊敬的%s用户您已成功登录'%name)
        return True, '%s登录成功' % user_dict['name']
    else:
        return False, '输入系统密码与系统密码不一致'

#用户查看余额
def check_balance_interface(name):
    user_dict = db_handles.select(name)
    if not user_dict['balance']:
        return '穷鬼'
    return '尊敬的用户%s您的余额为%d￥'%(user_dict['name'],user_dict['balance'])

# 用户注销

def logout_interface():
    # 如何注销 注销的是谁 从哪里来
    # 把user_info={}字典用户导过来
    from core import src
    src.user_info['name'] = None
    return '注销成功'

