# 数据接口层
from conf import settings
import json
import os

# 取
# json.JSONEncoder
def select(name):
    # 拼接用户路径
    user_path = "%s\%s.json"%(settings.DB_PATH, name)
    # 判断
    if not os.path.exists(user_path):
        return
    with open(user_path,'r',encoding='utf-8')as f:

        user_dict = json.load(f)
        return user_dict
        # # res = f.read()
        # for line in f:
        #
        #     user_dict = json.loads(line)
        #     return user_dict

# 存 写入内存
def save(user_dict):
    # 打开写入
    with open('%s\%s.json'%(settings.DB_PATH, user_dict['name']),'w',encoding='utf-8')as f:

        res = json.dumps(user_dict)
        # # res = json.dump(user_dict,f)  # 为啥不能用dump（）存数据 内部直接帮我们写了不需要在写
        f.write(res)
        f.flush()
        # 写文件
        # json.dump(user_dict,f)
        # return True
