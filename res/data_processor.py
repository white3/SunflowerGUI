#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/21 1:19
# @Author  : Menzel3
# @Site    : 
# @File    : 5.取数据拟合.py
# @Software: PyCharm
# @version : 0.0.1
import json
from target import Target
import sqlite3
import threading

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return {'__{}__'.format(o.__class__.__name__): o.__dict__}

class SqliteUtils(object):
    def __init__(self):
        self.lock = threading.Condition()
        self.conn = sqlite3.connect(database)
    def __del__(self):
        self.conn.close()
    def update(self, query, params):
        with self.lock:
            c = self.conn.cursor()
            c.execute(query, params)
            self.conn.commit()
    def executeQuery(self, query, params=()):
        with self.lock:
            cur = self.conn.cursor()
            cur.execute(query, params)
            self.conn.commit()
            rows = cur.fetchall()
            return rows

database = 'recorder-back.db'
sql_util = SqliteUtils()

def func(table="HAOffsetTable"):
    cursor = sql_util.executeQuery(
                query="SELECT id, target from "+table+" where id > 387;")
    offset_packages = []
    for row in cursor:
        offset_packages.append([row[0], json.loads(row[1])])
    for i in offset_packages:
        sql_util.update(
            query="UPDATE "+table+" SET ha = ?, version = 2 WHERE id = ?;",
            params=(i[1]['__Target__']['hourAngle'], i[0])
        )

def func2(table="DECOffsetTable"):
    cursor = sql_util.executeQuery(
                query="SELECT id, target from "+table+" where id > 387;")
    offset_packages = []
    for row in cursor:
        offset_packages.append([row[0], json.loads(row[1])])
    for i in offset_packages:
        sql_util.update(
            query="UPDATE "+table+" SET dec = ?, version = 2 WHERE id = ?;",
            params=(i[1]['__Target__']['declination'], i[0])
        )

def query_dec(version=(0, 3)):
    cursor = sql_util.executeQuery(
                query="SELECT dec, decOffset from DECOffsetTable where version > ? and version < ?;",
                params=version)
    offsets, angle = [], []
    for row in cursor:
        angle.append(row[0])
        offsets.append(row[1])
    return (angle, offsets)

def query_ha(version=(0, 3)):
    cursor = sql_util.executeQuery(
                query="SELECT ha, haOffset from HAOffsetTable where version > ? and version < ?;", 
                params=version)
    offsets, angle = [], []
    for row in cursor:
        angle.append(row[0])
        offsets.append(row[1])
    return (angle, offsets)


if __name__ == "__main__":
    import pprint
    pprint.pprint(query_ha())
    pprint.pprint(query_dec())