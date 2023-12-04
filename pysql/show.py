from .config import cursor

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