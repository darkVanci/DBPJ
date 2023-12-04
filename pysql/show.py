from .config import cursor

def show_user():
    cursor.execute("select * from user")
    results = cursor.fetchall()
    for r in results:
        print(r)

def show_merchant():
    cursor.execute("select * from merchant")
    results = cursor.fetchall()
    for r in results:
        print(r)

def show_admin():
    cursor.execute("select * from admin")
    results = cursor.fetchall()
    for r in results:
        print(r)

'''
def show_player():
    cursor.execute("select * from player")
    results = cursor.fetchall()
    for r in results:
        print(r)


def show_npc():
    cursor.execute("select * from npc")
    results = cursor.fetchall()
    for r in results:
        print(r)
'''
