# 银行接口层业务
from db import db_handles
from lib import common


def transfer_interface(from_name, to_user, money):
    # 拿到转账给谁的用户字典
    to_user_dict = db_handles.select(to_user)
    # 判断一下用户是否存在
    if not to_user_dict:
        return False, '改用户不存在'
    # 在的话： 在获取用户的字典
    from_user_dict = db_handles.select(from_name)
    # 判断金额是否大于转账的金额
    # 小于返回 记得是一一对应的哈 返回与接收是一致的
    if not from_user_dict["balance"] > money:
        return False, '穷鬼自己养不活还给别人转钱'
    # 大于大于直接扣钱
    from_user_dict['balance'] -= money
    # 收到放加钱
    to_user_dict['balance'] += money

    # 生成一个对象
    logger_obj = common.get_logger('用户转账功能')


    # 保存好
    db_handles.save(to_user_dict)


    db_handles.save(from_user_dict)

    # 记录日志
    logger_obj.debug('用户：%s 转账给%s 金额：%d￥' % (from_user_dict['name'], to_user_dict['name'], money))

    return True, '用户：%s 转账给%s 金额：%d￥' % (from_user_dict['name'], to_user_dict['name'], money)


def withdraw_interface(name, money):
    # 获取当前用户

    user_dict = db_handles.select(name)
    # 判断余额
    # 手续费：
    # 取现总额度：money2 = money+money*0.05
    money1 = money * 0.05
    money2 = money + money * 0.05
    if not user_dict['balance'] > money2:
        return False, '小伙子没有钱了'
    user_dict['balance'] -= money
    logger_obj = common.get_logger('用户取现功能')  # 导入函数就阶段就定义号了 所以也可以放到导入函数下面
    info = '用户%s 取现金额：%d 手续费：%d' % (user_dict['name'], money, money1)
    logger_obj.warning(info)
    # user_dict["flow"].append(info)
    # 拿到用户流水的值
    user_dict["flow"].append(info)
    # 保存用户操作记录
    db_handles.save(user_dict)
    # print(user_dict, '--------------')
    #
    # print(info, type(info))  # None <class 'NoneType'>  type:None
    """
    {'name': 'aaa', 'pwd': '85f4573d52ae1d38ac175e4afcd89b74', 'balance': 12590, 'flow': [None, None, None, None, None, None, None], 'shopping_car': {}} --------------
    None <class 'NoneType'>
    None

    """
    return True, info

# 还款
def repay_interface(name, money):
    # 获取用户
    user_dict = db_handles.select(name)
    # 直接操作
    user_dict['balance'] -= money
    # 保存一下
    logger_obj = common.get_logger('用户还款功能')
    # 拼写 用户流水、日志记录内容
    # 将拼写的用户信息添加到flow 中
    user_dict['flow'].append('返款%s成功' % money)
    # print(user_dict)

    # 把保存用户信息
    db_handles.save(user_dict)
    # 生成日志记录 信息
    logger_obj.error('返款%s成功' % money)

    return True,'返款%s成功' % money


def check_user_flow_interface(name):
    # 拿到这个用户
    user_dict = db_handles.select(name)
    # 返回用户流水字典里面是 列表
    return user_dict['flow']


# 获取用户银行卡的余额
def check_user_bank_balance_interface(name):
    user_dict = db_handles.select(name)
    # 拿到用户直接返回用户的余额
    return user_dict['balance']


# 银行支付功能能
def pay_cost_interface(name, cost):
    user_dict = db_handles.select(name)
    if not user_dict['balance'] > cost:
        return False, '余额小于cost支付失败'
    # 用户当前额度：用户余额-商品的总价
    user_dict['balance'] -= cost
    # 当支付成功后可以将购物车清空
    user_dict['shopping_car'] = {}
    # 保存更新当前用户的详情信息
    db_handles.save(user_dict)
    return True, '支付成功'
