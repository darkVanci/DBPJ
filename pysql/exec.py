from .dict import functions
from .switch import get_stat


def exec_command(command: str):
    stat = get_stat()
    try:
        functions[stat][command]()
    except IndexError as e:
        print(e)
        print("发生了索引错误，请重新输入命令")
    except:
        print("发生了未知错误，请重新输入命令")
    finally:
        print('stat: ', stat)

