#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 0:46
# @Author  : Menzel3
# @Site    : 
# @File    : recorder.py
# @Software: PyCharm
# @version : 0.0.1
from sunflower.internal.controller.controller import ConController
from sunflower.internal.model.offset import Offset
from sunflower.internal.model.times import Times, timestamp2Times
from sunflower.internal.model.target import Target
from sunflower.internal.meta import interruptible_thread
from sunflower.internal.constants import constant
from sunflower.internal.util.decorator import debugLog
from sunflower.internal.meta import singleton_meta
from sunflower.internal.controller import status
import json
import time
import copy

HA = "HAOffsetTabel"
DEC = "DECOffsetTabel"


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return {'__{}__'.format(o.__class__.__name__): o.__dict__}


class RecorderController(ConController):

    @status.status_log("init RecorderController", constant.MEDIUM)
    def __init__(self, **kwargs):
        interruptible_thread.ThreadMeta.__init__(self)
        self.view = kwargs['view']
        self.view.recordButton.clicked.connect(self.record)
        self.data = kwargs['data']
        self.recorder = Recorder()  # 配置记录器
        self.isRecording = False

    def record(self):
        if self.isRecording:
            self.isRecording = False
            self.wait()
            self.view.recordButton.setText("记录误差")
            status.display_status("停止记录", constant.MEDIUM)
        else:
            self.isRecording = True
            self.run()
            self.view.recordButton.setText("停止记录")
            status.display_status("开始记录", constant.MEDIUM)

    def work(self):
        """
        以RECORD_FLUSH_TIME为间隙，持续向数据库记录数据
        :return:
        """
        time.sleep(constant.RECORD_FLUSH_TIME)
        ha_offset = copy.deepcopy(self.data.get('haOffset'))
        dec_offset = copy.deepcopy(self.data.get('decOffset'))
        target = copy.deepcopy(self.data.get('target'))
        global_clock = copy.deepcopy(self.data.get('globalClock'))
        self.recorder.writeData(haOffset=ha_offset, decOffset=dec_offset,
                                target=target,
                                globalClock=global_clock)
        status.display_status("记录中... %s %s %s %s" % (ha_offset, dec_offset, target, global_clock), constant.MEDIUM)


class Recorder(metaclass=singleton_meta.SingletonMeta):
    def readData(self, scale=(-180, 180), kind=HA) -> object:
        """
        :param scale: 筛选数据范围, 区间为[scale[0], scale[1]]
        :param kind: 标记取HA、还是DEC
        :return: [[angle, offset, globalClock, version], [angle, offset, globalClock, version], ...]
        """
        if kind is HA:
            cursor = constant.sql_util.executeQuery(
                query="SELECT ha, haOffset, globalClock, version from HAOffsetTable where ha > ? and ha < ? and version!=-1",
                params=scale)
        else:
            cursor = constant.sql_util.executeQuery(
                query="SELECT dec, decOffset, globalClock, version from DECOffsetTable where dec > ? and dec < ? and version!=-1",
                params=scale)
        offset_packages = []
        for row in cursor:
            offset_packages.append([row[0], row[1], timestamp2Times(row[2]), row[3]])
        return offset_packages

    @debugLog
    def writeData(self, haOffset: Offset, decOffset: Offset, globalClock: Times, target: Target):
        """

        :param haOffset: 记录时角偏移量
        :param decOffset: 记录赤纬偏移量
        :param globalClock: 记录该偏移量对应的全局时钟
        :param target: 记录该偏移量对应的目标
        :return:
        """
        constant.sql_util.update(
            query="INSERT INTO HAOffsetTable (ha,haOffset,globalClock,version,target) VALUES (?, ?, ?, ?, ?)",
            params=(haOffset.angle, haOffset.offset, globalClock.toTimestamp(), haOffset.version,
                    json.dumps(target, cls=CustomEncoder, ensure_ascii=False))
        )
        constant.sql_util.update(
            "INSERT INTO DECOffsetTable (dec,DecOffset,globalClock,version,target) VALUES (?,?,?,?,?)",
            (decOffset.angle, decOffset.offset, globalClock.toTimestamp(), decOffset.version,
             json.dumps(target, cls=CustomEncoder, ensure_ascii=False))
        )
