# coding:utf8
from enum import Enum

# 房间状态
class RoomStatus(Enum):
    CLOSE = 0
    WAIT = 1
    UNDERWAY = 2

# 胜利条件
class WinModel(Enum):
    ALL = 0
    HALF = 1

# 角色
class Role(Enum):
    WOLF = 0        # 狼人
    CIVILIAN = 1    # 平民
    PROPHET = 2     # 预言家
    WITCH = 3       # 女巫
    IDIOT = 4       # 白痴
    HUNTER = 5      # 猎人
    TREE = 6        # 大树
