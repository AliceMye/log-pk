# 项目路径
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

DB_PATH = os.path.join(BASE_PATH,'db')


# logging 大字典
import os
import logging.config

# 定义三种日志输出格式 开始

standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]' #其中name为getlogger指定的名字

simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'



# 定义日志输出格式 结束
"""
下面的两个变量对应的值 需要你手动修改
"""
# #
# logfile_dir = os.path.dirname(os.path.dirname(__file__))  # log文件的目录
#
# logfile_name = 'aaa.log'  # log文件名  自定义文件名


# 拼接文件夹目录
logfile_dir = os.path.join(BASE_PATH,'log')
# 文件名
logfile_name = 'aaa.log' #  可以自己定义 先写啥就是写啥

# # 果不存在定义的日志目录就创建一个
# if not os.path.isdir(logfile_dir):  # 判断文件夹 目录如果没有就给创建一个存放日志的文件夹
#     os.mkdir(logfile_dir)  # 创建目录

# 判断路径是否存在如果不存

if not os.path.exists(logfile_dir):
    os.mkdir(logfile_dir)

# 拼接log全路径：logfile_path = 他的目录+文件名
logfile_path = os.path.join(logfile_dir, logfile_name)
# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
    },
    'filters': {},  # 过滤日志
    'handlers': {
        #打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        #打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path,  # 日志文件
            'maxBytes': 1024*1024*5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        #logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },  # 当键不存在的情况下 默认都会使用该k:v配置
    },
}