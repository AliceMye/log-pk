# 启动

import os
import sys
from core import src

PATH = os.path.dirname(__file__)
sys.path.append(PATH)

if __name__ == '__main__':
    src.run()