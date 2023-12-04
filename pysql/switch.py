# 维护和切换登录状态
stat = "user"

def switch_to_user():
    global stat
    stat = "user"

def switch_to_merchant():
    global stat
    stat = "merchant"

def switch_to_admin():
    global stat
    stat = "admin"

def get_stat() -> str:
    return stat


'''
def switch_to_npc():
    global stat
    # print("before " + stat)
    stat = "npc"
    # print("after " + stat)


def switch_to_player():
    global stat
    # print("before " + stat)
    stat = "player"
    # print("after " + stat)
'''