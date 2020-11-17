#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 19:35
# @Author  : Menzel3
# @Site    : 
# @File    : sqliteUtils.py
# @Software: PyCharm
# @version : 0.0.1
import sqlite3
import threading
from sunflower.internal.util.decorator import debugLog

# database
database = 'res/recorder.db'


class SqliteUtils(object):
    lock = threading.Condition()
    conn = None

    def __init__(self):
        pass

    @debugLog
    def update(self, query, params):
        try:
            self.lock.acquire()
            self.conn = sqlite3.connect(database)
            c = self.conn.cursor()
            c.execute(query, params)
            self.conn.commit()
        finally:
            self.conn.close()
            self.lock.release()

    @debugLog
    def executeQuery(self, query, params=()):
        try:
            self.lock.acquire()
            self.conn = sqlite3.connect(database)
            cur = self.conn.cursor()
            cur.execute(query, params)
            self.conn.commit()
            rows = cur.fetchall()
            return rows
        finally:
            if self.conn:
                self.conn.close()
            self.lock.release()
