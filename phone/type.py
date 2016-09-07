# coding:utf8
from enum import Enum

ROLE_NAME  ={
    0 : u'狼人',
    1 : u'平民',
    2 : u'预言家',
    3 : u'女巫',
    4 : u'白痴',
    5 : u'猎人',
    6 : u'大叔',
}
ROLE_STATUS_NAME = {
    0 : u'活着',
    1 : u'死亡'
}
ROOM_STATUS = {
    0 : u'关闭',
    1 : u'等待中',
    2 : u'杀人中',
    3 : u'女巫活动中',
    4 : u'验人',
    5 : u'白天'
}

DEFALT_GOD = (
    ('2', '预言家'),
    ('3', '女巫'),
    ('4', '白痴'),
    ('5', '猎人'),
    ('6', '树人')
)
# 游戏进行中的房间状态

IN_ROOM = (2,3,4,5)
# 房间状态
class RoomStatus(Enum):
    CLOSE = 0
    WAIT = 1
    KILLING = 2 #杀人中
    WITCH = 3 # 女巫进行中
    WATCH = 4 # 验人
    DAY = 5 # 白天

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

class PlayerStatus(Enum):
        ALIVE = 0
        DIE = 1