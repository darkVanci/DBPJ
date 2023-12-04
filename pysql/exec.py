from .dict import functions
from .switch import get_stat


def exec_command(command: str):
    stat = get_stat()
    try:
        functions[stat][command]()
    except Exception as e:
        print(f"发生了错误：{type(e)}")
        print("请重新输入命令")
    # finally:
    #     print('stat:', stat)

