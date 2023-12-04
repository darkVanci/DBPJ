from pysql.config import conn
from pysql.exec import exec_command




print("Enter commands, or type 'exit' 'quit' 'e' 'q' to quit.")

while True:
    user_input = input("> ").strip()

    if user_input in ["exit", "quit", "e", "q"]:
        break
    else:
        exec_command(user_input)
        pass

conn.close()
