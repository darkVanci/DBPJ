stat = "player"


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


def get_stat() -> str:
    return stat
