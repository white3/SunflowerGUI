#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 19:35
# @Author  : Menzel3
# @Site    : 
# @File    : sqlite_utils.py
# @Software: PyCharm
# @version : 0.0.1
import sqlite3
import threading
from sunflower.internal.util.decorator import debugLog
from sunflower.internal.meta.singleton_meta import SingletonMeta

# database
database = 'res/recorder.db'


class SqliteUtils(metaclass=SingletonMeta):

    def __init__(self):
        self.lock = threading.Condition()
        self.conn = None

    def update(self, query, params):
        with self.lock:
            self.conn = sqlite3.connect(database)
            try:
                c = self.conn.cursor()
                c.execute(query, params)
                self.conn.commit()
                self.conn.close()
            finally:
                self.conn.close()

    def executeQuery(self, query, params=()):
        with self.lock:
            self.conn = sqlite3.connect(database)
            try:
                cur = self.conn.cursor()
                cur.execute(query, params)
                self.conn.commit()
                rows = cur.fetchall()
                return rows
            finally:
                self.conn.close()
