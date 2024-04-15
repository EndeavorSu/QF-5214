# pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error

config = {
    'user': 'root',
    'password': '123456789',
    'host': '34.124.177.28',
    'database': 'qf5214 test',
    'raise_on_warnings': True
}

try:
    # 连接到数据库
    connection = mysql.connector.connect(**config)
    
    if connection.is_connected():
        db_info = connection.get_server_info()
        print("成功连接到 MySQL 数据库，服务器版本：", db_info)
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("你已连接到数据库：", record)

except Error as e:
    print("连接错误：", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL 连接已关闭")
