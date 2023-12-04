from pymysql import Connection

# 连接到MySQL数据库
conn = Connection(
    host="localhost",
    port=3306,
    user="root",
    password="123456",
)

# 创建游标对象并执行SQL操作
cursor = conn.cursor()
# 选择数据库
conn.select_db("OnlineShoppingComparison")