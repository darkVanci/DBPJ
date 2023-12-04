from .dict import functions
from .switch import get_stat


def exec_command(command: str):
    stat = get_stat()
    functions[stat][command]()
    print(stat)

