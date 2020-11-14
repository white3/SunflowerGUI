#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/14 8:31
# @Author  : Menzel3
# @Site    : 
# @File    : times.py
# @Software: PyCharm
# @version : 0.0.1
from datetime import datetime, date
import time
import pytz
import json


class Times(object):
    """
    唯一id表现为 stamp -> stamp
     from calculator 返回的 utc_datatime
     to 置换为全局时钟，表现形式有：lst, utc, localtime
     TODO: search difference from localtime and lst
    """
    timezone = None  # 时区
    stamp = None  # 本地时间戳
    local = None  # 本地时间
    lst = None  # 当地时区时间
    utc = None  # utc时间

    def toLST(self):
        # TODO
        pass

    def toLocalTime(self):
        # TODO
        pass

    def toUTC(self):
        # TODO
        self.local.toUTC()

    def __gt__(self, other):
        """
        重载 <
        :param other:
        :return:
        """
        if self.stamp > other.stamp:
            return False
        else:
            return True

    def __lt__(self, other):
        """
        重载 >
        :param other:
        :return:
        """
        if self.stamp < other.stamp:
            return False
        else:
            return True

    def __init__(self, local=None, utc=None,
                 lst=None, timezone='Asia/Shanghai', ticks=time.time()):
        """

        :param local: Local Time
        :param utc: Universal Time Coordinated
        :param lst: Local Standard Time
        """
        self.timezone = timezone
        self.stamp = ticks
        if lst is None:
            self.lst = datetime.now(pytz.timezone(timezone))
        else:
            self.lst = lst
        if utc is None:
            self.utc = self.lst.astimezone(pytz.UTC)
        else:
            self.utc = utc
        if local is None:
            self.local = time.asctime(time.localtime(self.stamp))
        else:
            self.local = local

    def to_json(self):
        return {
            'timezone': self.timezone,  # 时区
            'stamp': self.stamp,  # 本地时间戳
            'local': self.local,  # 本地时间
            'lst': self.lst,  # 当地时区时间
            'utc': self.utc  # utc时间
        }

    def __str__(self):
        return "{'LOCAL':'%s','UTC':'%s','LST':'%s', 'timezone', '%s'}" % (
            self.local, self.utc, self.lst, self.timezone)


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return {'__datetime__': o.replace(microsecond=0).isoformat()}
        return {'__{}__'.format(o.__class__.__name__): o.__dict__}


def decode_object(o):
    if '__Times__' in o:
        a = Times()
        a.__dict__.update(o['__Times__'])
        return a
    elif '__datetime__' in o:
        # TODO 查datetime自解码
        return datetime.strptime(o['__datetime__'], '%Y-%m-%dT%H:%M:%S+timezone')
    return o


if __name__ == '__main__':
    now = Times()
    print(now)
    temp = json.dumps(now, cls=CustomEncoder, ensure_ascii=False)
    print(temp)
    temp = json.loads(str(temp), object_hook=decode_object)
    print(temp.to_json())
