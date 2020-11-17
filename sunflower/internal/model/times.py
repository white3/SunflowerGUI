#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/14 8:31
# @Author  : Menzel3
# @Site    : 
# @File    : times.py
# @Software: PyCharm
# @version : 0.0.1
from sunflower.internal.constants import constant
from datetime import datetime
import pytz
import json


class Times(object):
    """
    唯一id表现为 stamp -> stamp
     from calculator 返回的 utc_datatime
     to 置换为全局时钟，表现形式有：lst, utc, localtime
     TODO: search difference from localtime and lst
    """
    utc_datetime = None  # utc时间

    def __init__(self, utc=None):
        """

        :param utc: Universal Time Coordinated datetime.datetime
        """
        if utc is None:
            self.utc_datetime = datetime.utcnow()
        else:
            self.utc_datetime = utc

    def toTimestamp(self) -> float:
        return self.utc_datetime.timestamp()

    def toLST(self):
        """
        Local Standard Time
        :return:
        """
        return self.utc_datetime.astimezone(pytz.timezone(constant.TIMEZONE))

    def toLocalTime(self):
        """
        Local Time
        :return:
        """
        return self.utc_datetime.astimezone(pytz.timezone(constant.TIMEZONE))

    def toUTC(self):
        """
        Universal Time Coordinated datetime.datetime
        :return:
        """
        return self.utc_datetime.astimezone()

    def __gt__(self, other):
        """
        重载 <
        :param other:
        :return:
        """
        if type(other) is Times:
            return self.utc_datetime.__gt__(other.utc_datetime)
        elif type(other) is datetime:
            return self.utc_datetime.__gt__(other)
        else:
            return False

    def __lt__(self, other):
        """
        重载 >
        :param other:
        :return:
        """
        # print(type(other))
        # print(str(other))
        if type(other) is Times:
            return self.utc_datetime.__lt__(other.utc_datetime)
        elif type(other) is datetime:
            return self.utc_datetime.__lt__(other)
        else:
            return True

    def __str__(self):
        return "{'LOCAL':'%s','UTC':'%s','LST':'%s', 'timezone', '%s'}" % (
            self.toLocalTime(), self.toUTC(), self.toLST(), constant.TIMEZONE)


def timestamp2Times(utc_timestamp) -> Times:
    """

    :param utc_timestamp: utc datetime
    :return:
    """
    return Times(utc=datetime.utcfromtimestamp(utc_timestamp))


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


#
# def toJson(time) -> str:
#     return str(json.dumps(time, cls=CustomEncoder, ensure_ascii=False))
#
#
# def fromJson(json_str: str):
#     test_time = datetime.utcfromtimestamp(1605347977.211388)
#     test_times = Times(utc=test_time)
#     print(temp)
#     temp = json.loads(json_str, object_hook=decode_object)
#     print(temp.to_json())


if __name__ == '__main__':
    test_time = datetime.utcfromtimestamp(1605347977.211388)
    test_times = Times(utc=test_time)
    temp = json.dumps(test_times, cls=CustomEncoder, ensure_ascii=False)
    print(temp)
    temp = json.loads(str(temp), object_hook=decode_object)
    print(temp.to_json())
