from .show import show_user, show_merchant, show_admin
from .switch import switch_to_user, switch_to_merchant, switch_to_admin

functions = {
    "user": {
        "show": show_user,
        "merchant": switch_to_merchant,
        "admin": switch_to_admin,
    },
    "merchant": {
        "show": show_merchant,
        "user": switch_to_user,
        "admin": switch_to_admin,
    },
    "admin": {
        "show": show_admin,
        "user": switch_to_user,
        "merchant": switch_to_merchant,
    },
}

'''
functions = {
    "player": {
        "show": show_player,
        "npc": switch_to_npc,
    },
    "npc": {
        "show": show_npc,
        "player": switch_to_player,
    },
}
'''