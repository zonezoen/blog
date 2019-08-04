# -*- coding: utf-8 -*-
__auth__ = 'zone'
__date__ = '2019/8/4 下午3:33'
'''
公众号：zone7
小程序：编程面试题库
'''

import contextlib
import pymysql

# 原始用法
conn = pymysql.connect()
cur = conn.cursor()
sql = "select * from users"
cur.execute(sql)
print(cur.fetchone())
conn.commit()
cur.close()
conn.close()


class MysqlDb():
    def __init__(self, database, host="localhost", user="root", prot=3306, password="root", charset="utf8mb4"):
        self.conn = pymysql.connect(host=host, user=user, password=password, port=prot, database=database,
                                    cursorclass=pymysql.cursors.DictCursor, charset=charset)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cur.close()
        self.conn.close()


with MysqlDb(database="test", ) as db:
    sql = "select * from users"
    db.execute(sql)
    print(db.fetchone())
    intert_sql = "INSERT INTO `users` (`name`, `password`, `age`, `sex`) VALUES (%s, %s, %s, %s)"
    db.execute(intert_sql, ('zone7', 'pwd', "18", "man"))


@contextlib.contextmanager
def get_mysql_cur(database, host="localhost", user="root", prot=3306, password="root", charset="utf8mb4"):
    conn = pymysql.connect(host=host, user=user, password=password, port=prot, database=database,
                           cursorclass=pymysql.cursors.DictCursor, charset=charset)
    cur = conn.cursor()
    yield cur
    conn.commit()
    cur.close()
    conn.close()


with get_mysql_cur(database="test", ) as db:
    sql = "select * from users"
    db.execute(sql)
    print(db.fetchone())
