# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : mysql_oper.py
# @Time     : 2021/1/10 8:52
# @Software : PyCharm
# @Introduce: This is

import MySQLdb


def connect_db():
    # 打开数据库连接    ip，username，password，dbname, encoding
    db = MySQLdb.connect("localhost", "root", "525907", "test", charset="utf8")

    # 使用 cursor() 方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法取执行 SQL 语句
    cursor.execute("select version()")
    # 使用 fetchone() 方法获取一条数据/多条数据
    data = cursor.fetchone()
    print data
    data = cursor.fetchmany(1)
    print data
    data = cursor.fetchall()
    print data
    db.close()


def insert_recording():
    # 打开数据库连接    ip，username，password，dbname, encoding
    db = MySQLdb.connect("localhost", "root", "525907", "test", charset="utf8")
    cursor = db.cursor()

    sql = """insert into user(username, password) values('hanzhenjiang','chunyu.521')"""
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()
    pass


def query_recording():
    # 打开数据库连接    ip，username，password，dbname, encoding
    db = MySQLdb.connect("localhost", "root", "525907", "test", charset="utf8")
    cursor = db.cursor()

    sql = "select *from user where id > 0"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        for row in results:
            username = row[1]
            password = row[2]
            print username, password
    except:
        print 'error: unable to fecth data'

    db.close()
    pass


def update_recording():
    # 打开数据库连接    ip，username，password，dbname, encoding
    db = MySQLdb.connect("localhost", "root", "525907", "test", charset="utf8")
    cursor = db.cursor()
    sql = "update user set password='525907' where username='hanzhenjiang'"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()
    pass


def delete_recording():
    # 打开数据库连接    ip，username，password，dbname, encoding
    db = MySQLdb.connect("localhost", "root", "525907", "test", charset="utf8")
    cursor = db.cursor()
    sql = "delete from user where username = 'www'"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()
    pass


query_recording()
delete_recording()
query_recording()
