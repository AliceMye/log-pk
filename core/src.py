# 主要功能函数
from interface import user, bank, shop
import time

from lib import common

user_info = {"name": None}
def register():
    while True:
        # logger_return = common.get_logger('用户注册功能')
        name = input("输入用户姓名>>>:").strip()
        pwd = input("输入用户密码>>>:").strip()
        confirm_pwd = input("再次输入密码>>>:").strip()
        if pwd == confirm_pwd:
            flag, msg = user.register_interface(name, pwd)
            if flag:
                print(msg)
                # logger_return.debug('[%s]用户注册了我们的ATM网站'%user_info['name'])
                break
            else:
                print(msg)


def login():
    while True:
        name = input("输入用户姓名>>>:").strip()
        pwd = input("输入用户密码>>>:").strip()

        flag, msg = user.login_interface(name, pwd)
        if flag:
            print(msg)
            user_info['name'] = name  # 保存登陆状态
            break
        else:
            print(msg)


@common.get_auth
# 查看用户自己的余额
def check_balance():
    # 调用用户转接口
    msg = user.check_balance_interface(user_info['name'])
    print(msg)


@common.get_auth
def transfer():
    while True:
        # 给谁转账
        to_user = input('输入转账目标用户>>>:').strip()

        # 转多少钱
        money = input('输入值转账金额>>><q退出>>:').strip()

        if money == 'q': break
        if not money.isdigit(): continue
        money = int(money)
        flag, msg = bank.transfer_interface(user_info['name'], to_user, money)
        if flag:
            print(msg)
            break
        else:
            print(msg)


@common.get_auth
def withdraw():
    while True:
        # 用户取现 银行转接口
        money = input('输入金额>>>:').strip()
        if not money.isdigit():
            continue
        money = int(money)
        flag, msg = bank.withdraw_interface(user_info['name'], money)
        if flag:
            print(msg)
            break
        else:
            print(msg)


@common.get_auth
def repay():
    while True:
        money = input('输入还款金额：').strip()
        if not money.isdigit():
            continue
        money = int(money)
        flag,msg = bank.repay_interface(user_info['name'], money)

        if flag:
            print(msg)
            break
        else:
            print(msg)


@common.get_auth
def check_flow():
    # 用户调用
    flows = bank.check_user_flow_interface(user_info['name'])
    for line in flows:
        print(line)


@common.get_auth
def shopping():
    # 购物车

    """
    1.循环打印购物车的商品详情
    2.通过索引获取商品的名称和价格
    3.判断余额是否大于商品的价格  》》》调用银行接口车看用户的余额
    4.选则添加商品 >>> 判断是否已有改商品>>>有加1 shopping['num']+=1 无则1
    5.没添加一个商品cost+=price
    5.是否结算购买 >>>cost=0 则直接退出 否则是则调用接口层跳转 银行支付功能（银行接口层方面判断逻辑）
    6.购买成功


    """
    good_list = [
        ['百岁山', 10],
        ['苹果', 18],
        ['ipa', 1799],
        ['华为', 4888],
        ['mac_pro', 12888]

    ]

    shopping_car = {}
    cost = 0
    while True:
        for index, good in enumerate(good_list, 1):
            print(index, good)
            """
            0 ['百岁山', 10]
            1 ['苹果', 18]
            2 ['ipa', 1799]
            3 ['华为', 4888]
            4 ['mac_pro', 12888]
            """
        choice = input('请输入商品的编号>>>:').strip()
        if choice == 'q': break
        if not choice.isdigit():
            continue
        choice = int(choice) - 1
        print(choice)
        if not choice >= 0 and choice < len(good_list):
            print('您输入的商品编号不在我们的商品范围内')
            continue
        good_name, good_price = good_list[choice]
        print(good_name, '666')
        # 选择加入购物车
        # 判断用户余额是否大于 商品的价格
        user_balance = bank.check_user_bank_balance_interface(user_info['name'])  # 可以升为全局
        print(good_price, type(good_price))
        print(user_balance, type(user_balance))
        user_balance = int(user_balance)
        if user_balance > good_price:

            # 将商品添加到购物车字典 前判断判断如果有这加+1 么有1 字典
            if good_name in shopping_car:
                # 加+1
                shopping_car[good_name] += 1
            else:
                shopping_car[good_name] = 1
            cost += good_price
            # 调用用户shop购物接口 将商品添加到用户信息里面
            flag, msg = shop.add_shopping_car_interface(user_info['name'], shopping_car)
            if flag:
                print(msg)
                print('您已选择的商品：%s' % shopping_car)

                while True:

                    print('当前您的购物车商品总价：%s￥' % cost)
                    cmd = input('是否选择结算<y/n/>:').strip()

                    if cost == 0:
                        break

                    if cmd == 'y':
                        pay_cost(cost)
                        return
                    else:
                        print('暂时退出购买，回到商品列表<退出可以选择q>')

                        break

            else:
                print(msg)
        else:
            print('穷逼 自己心里要有点数,<q退出>')


@common.get_auth
def pay_cost(cost):
    while True:
        # 调用银行支付接口
        flag, msg = bank.pay_cost_interface(user_info['name'], cost)
        if flag:
            print(msg, time.strftime('%Y-%m-%d %H:%M:%S'))
            break
        else:
            print(msg)


@common.get_auth
def check_shopping():
    # 直接调用shop接口查看即可
    shopping_car = shop.check_shopping_interface(user_info['name'])
    if shopping_car:
        print(shopping_car)
    else:
        print('购物车已经清空')


def logout():
    # 方法一：直接清除
    # if user_info['name']:
    #     user_info.clear()
    #     print('注销成功')

    # 方法二：用转接口 将当前登录用户名字导过去 用什么导什么 src.user_info = None为空 返回 '注销成功'
    msg = user.logout_interface()
    # 接收信息
    print(msg)


func_dic = {
    "1": register,
    "2": login,
    "3": check_balance,
    "4": transfer,
    "5": withdraw,
    "6": repay,
    "7": shopping,
    "8": check_shopping,
    "9": logout,
    '0': check_flow,
}


def run():
    while True:

        print("""
        1.注册
        2.登录
        3.查看余额
        4.转账
        5.取现
        6.还款
        7.购物
        8.查看购物车
        9.注销
        0.查看流水
        q.退出
        """)
        choice = input('输入功能编号>>>:').strip()
        if choice == 'q':
            break
        elif choice in func_dic:
            func_dic.get(choice)()
        else:
            print('输入正确的选项')
