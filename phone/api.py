# coding:utf8
from random import choice

from models import *
from type import *


def has_prophet(game):
    game = Game.objects.get(id=game)
    return game.room.has_prophet

def has_witch(game):
    game = Game.objects.get(id=game)
    return game.room.has_witch
# 删除不在房间的人
def delete_not_in_room():
    not_int_game = Identity.objects.filter(game__isnull=True).delete()

# 加入游戏
def join_room(user, num):
    try:
        games = Game.objects.filter(id=num)
        if games.count() > 0:
            # TODO 先判断房间是否有人。。。
            game = games[0]
            if int(game.status) is not RoomStatus.WAIT:
                return u'该房间已经开始'
            identity= Identity(user=user, game_id=games[0].id)
            current_headcount = game.current_headcount
            game.current_headcount = current_headcount+1
            game.save()
            identity.save()
            return 1
        else:
            return u'无此房间号'
    except Exception,e:
        return str(e)


# 获取死亡的人
def get_deth_people(user):
     users = Identity.objects.filter(user__username=user)
     if users.count() > 0:
         return users[0].game.kill
     else:
         return -1
# 验人
def check(user, check_num):
    users = Identity.objects.filter(user__username=check_num)
    if users.count()>0:
        game = users[0].game
        if game.room.has_witch:
            game.status = RoomStatus.WITCH
        else:
            game.status = RoomStatus.DAY
        game.save()
        if users[0].role == Role.WOLF:
            return u'狼人'
        else:
            return u'好人'
    else:
        return u'验人失败'
# 救人
def rescue_people(user,num):
    game = Identity.objects.filter(user__username=user)
    if game.count()>0:
        game[0].game.status = RoomStatus.DAY
        game[0].rescue = int(num)
        game[0].save()
        return u'救人成功'
    else:
        return u'救人失败'
# 杀人
def kill(user, num):
    identity = Identity.objects.filter(user__username=user)
    if identity.count()>0:
        game = identity[0].game

        game.kill = num
        game.killer_vote_num += 1
        game.status = RoomStatus.WATCH
        game.save()
        return u'杀人成功'
    else:
        return u'杀人失败'

# 获取房间状态
def get_room_status(room):
    obj = Game.objects.filter(id=room)
    if obj.count()>0:
        return obj[0].status
    else:
        return -1

def is_in_room(user):
    obj = Identity.objects.filter(user__username=user)
    if obj.count()> 0:
        user_list = []
        other_user = Identity.objects.filter(game_id=obj[0].game_id)
        for item in other_user:
            user_list.append(str(item.user.username)+', ')
        return obj[0].game.current_headcount, obj[0].game.id, obj[0].user.username, user_list
    else:
        return 0, None, None, None

# 获取角色
def get_role(user):
    users = Identity.objects.filter(user__username=user)
    if users.count() >0:
        return users[0].role, users[0].game.status, users[0].status
    else:
        return u'获取角色失败', None, None

# 开始游戏
def start_game(session):
    game_id = session['game']
    try:
        games = Game.objects.filter(id=game_id)
        if games[0].status == RoomStatus.WAIT:
            # 更改房间状态
            game = games[0]
            game.status = RoomStatus.KILLING
            # 分配身份, 房间中人数不会超过
            room = game.room
            role_list = []
            for i in range(room.wolf): role_list.append(0)
            for i in range(room .civilian): role_list.append(1)
            if room.has_prophet: role_list.append(2)
            if room.has_witch: role_list.append(3)
            if room.has_idiot: role_list.append(4)
            if room.has_hunter: role_list.append(5)
            if room.has_tree: role_list.append(6)
            room.save()
            game.save()

            users = Identity.objects.filter(game=game)
            for user in users:
                user.role = choice(role_list)
                user.status = PlayerStatus.ALIVE
                role_list.remove(user.role)
                user.save()
            # 分配角色成功
            return 1
        else:
            # 房间状态错误
            return -2
    except Exception,e:
        return e
# 用户创建游戏
def user_create_room(user, wolf, civilian, god, win):
    # 查看用户是否在房间
    god_list = []
    god_bool = []

    for num in god:
        god_list.append(int(num))
    identity = Identity.objects.filter(user__username=user)
    if identity.count() > 0:
        # 用户在房间中
        return -2, u'用户已在房间'+str(identity.room)
    else:
        for i in range(2, 7):
            if i in god_list:
                god_bool.append(True)
            else:
                god_bool.append(False)
        try:
            room = Room.objects.create(
                headcount=wolf+civilian+len(god),
                wolf=wolf,
                civilian=civilian,
                god=len(god_list),
                has_prophet=god_bool[0],
                has_witch=god_bool[1],
                has_idiot=god_bool[2],
                has_hunter=god_bool[3],
                has_tree=god_bool[4],
                win_model=int(win))
            user_exit(user)  # 退出所有的房间
            game, _ = Game.objects.get_or_create(room=room, current_headcount=1, master=user, status=RoomStatus.WAIT, killer_vote_num=0)
            if not _:
                return -2, u'用户已在房间'+str(game.room.id)
            identity = Identity.objects.create(game=game, user=user)
            room.save()
            game.save()
            identity.save()
            return game.id, None
        except Exception,e:
            return -1, u'创建房间失败 ' + str(e)

# 退出房间,游戏
def user_exit(user):
    game = Game.objects.filter(master__username=user)
    if game.count() > 0:
        for item in game: item.delete()
    id = Identity.objects.filter(user__username=user)
    if id.count() >0 :
        for item in id: item.delete()


# 查看药情况
def drug(game):
    games = Game.objects.filter(id=game)
    good = True
    bad = True
    if games.count>0:
        if games[0].rescue:
            good = False
        if games[0].poison_people:
            bad = False
    return good, bad


# 女巫救人
def witch_rescuse(user):
    pass


# 女巫毒人
def witch_poison(user):
    pass
