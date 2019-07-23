# 用户购物接口 接口层
from db import db_handles
# 用户添加购物车到shop
def add_shopping_car_interface(name,shopping_car):
    user_dict = db_handles.select(name)
    # 将购物车当做值value 字典赋值属性 有则=更新 无则新增健值对
    user_dict['shopping_car'] = shopping_car
    db_handles.save(user_dict)  # 记得保存添加的数据
    return True,'商品添加成功'

# 用户查看购物车
def check_shopping_interface(name):
    user_dict = db_handles.select(name)
    # 值直接返回购物车
    return user_dict['shopping_car']