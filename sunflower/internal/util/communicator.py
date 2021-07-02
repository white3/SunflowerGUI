#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 12:26
# @Author  : Menzel3
# @Site    : 
# @File    : Communicator.py
# @Software: PyCharm
# @version : 0.0.1

import serial
import time
from setting import commands, frame_code
import threading
from sunflower.internal.util.decorator import debugLog

FSB = frame_code['FSB']
ADB = frame_code['ADB']
FEB = frame_code['FEB']
ENB = frame_code['ENB']


def append_verify_code(code):
    """
    生成校验码

    :param code:
    :return: 校验码
    """
    temp = code.replace(" ", "")
    va = 0
    for it in range(2, len(temp) + 2, 2):
        va = va + int(temp[it - 2:it], 16)
    v_value = str(hex(va))[-2:]
    return "%s %s" % (code, v_value.upper())


class Communicator(object):

    def __init__(self, serial_channel: serial.Serial):
        """
        配置串口
        :param serial_channel: 串口对象
        :return:
        """
        commands['by上'] = self.reset
        self.commands = {
            '驱动上电': self.open_power,
            '驱动断电': self.drop_power,
            '查询': self.get_position,
            '收藏': self.reset,
            '转至低位': self.low_location,
        }
        # 是否连接
        self.is_connect = False
        # 是否上电
        self.is_electric = False
        # 串口通信通道
        self.serial_channel = serial_channel
        self.__cmd_lock = threading.Condition()
        self.DROP_POWER = append_verify_code("%s %s %s %s %s" % (
            FSB, ADB, commands['驱动断电'], FEB, ENB))

        self.OPEN_POWER = append_verify_code("%s %s %s %s %s" % (
            FSB, ADB, commands['驱动上电'], FEB, ENB))

        self.POSITION = append_verify_code("%s %s %s %s %s" % (
            FSB, ADB, commands['查询'], FEB, ENB))

    def __del__(self):
        """
        发送急停后, 再发送断电指令, 并断开连接
        :return:
        """
        self.drop_power()
        print("Security close connection.")

    def rpc_exec(self, key: str):
        """
        查阅文档, 复位指令即为 复位
        新增指令: ['低速上转', '中速上转', '高速上转', '低速下转', '中速下转', '高速下转',
                '低速顺转', '中速顺转', '高速顺转', '低速逆转', '中速逆转', '高速逆转',
                '停转', ]

        :param key:
        :return:
        """
        if self.commands[key]:
            self.commands[key]()
        else:
            # 'FSB ADB CMB FEB ENB PAR'
            frame = "%s %s %s %s %s" % (FSB, ADB, commands[key], FEB, ENB)
            rpc_code = bytes.fromhex(frame + ' ' + self.__verify_code(frame))
            self.__send(rpc_code)
            self.__receieve()  # invalid data
            self.__receieve()  # invalid data

    @debugLog
    def drop_power(self):
        """
        发送断电指令, 并断开与电机的连接
        :return:
        """
        byte_code = bytes.fromhex(self.DROP_POWER)
        self.__send(byte_code=byte_code)
        self.serial_channel.close()
        self.is_connect = False

    @debugLog
    def open_power(self):
        """
        发送上电指令, 并保持与电机的连接
        :return:
        """
        byte_code = bytes.fromhex(self.OPEN_POWER)
        # .decode('utf-8')
        self.__send(byte_code=byte_code)
        rMsg = self.__receieve()
        rgMsg = self.__receieve()
        print(rMsg)
        print(rgMsg)
        if 'O' in str(rMsg) and 'K' in str(rMsg):
            self.is_connect = True
            return True
        else:
            return False

    def get_position(self):
        '''
        :param isDisp: 是否通过print输出
        :return: Hourangle, declination
        '''
        byte_code = bytes.fromhex(self.POSITION)
        self.__send(byte_code=byte_code)
        teleMsg = self.__receieve()
        self.__receieve()

        locaStr = bytes.decode(teleMsg, encoding='cp1252')
        sysPos = locaStr[3:-7]

        HA = sysPos[0:7]
        Dec = sysPos[7:-1]
        return float(HA), float(Dec)

    def low_location(self):
        """
        降低到低位
        :return:
        """
        hex_code = self.__data_guide(-90, -42.8, True, True)
        byte_code = bytes.fromhex(hex_code)
        self.__send(byte_code=byte_code)

    @debugLog
    def reset(self):
        """
        望远镜视向置为 0,47.8
        :return:
        """
        hex_code = self.__data_guide(0.5, 42.8, True, True)
        byte_code = bytes.fromhex(hex_code)
        self.__send(byte_code=byte_code)

    @debugLog
    def track(self, ha, dec):
        """
        追踪坐标

        :param ha: 时角, 度
        :param dec: 赤纬, 度
        :return:
        """
        hex_code = self.__data_guide(ha, dec, True, True)
        byte_code = bytes.fromhex(hex_code)
        self.__send(byte_code)
        # 文档提到需 200ms 间隙
        time.sleep(0.2)
        self.__receieve()  # invalid data
        self.__receieve()  # invalid data

    def __verify_code(self, comd):
        '''
        生成校验码

        :param comd:
        :return: 校验码
        '''
        comdd = comd.replace(" ", "")
        va = 0
        for it in range(2, len(comdd) + 2, 2):
            va = va + int(comdd[it - 2:it], 16)
        vaStr = str(hex(va))
        v_value = vaStr[-2:]
        print(v_value)
        return v_value.upper()

    def __send(self, byte_code):
        try:
            self.__cmd_lock.acquire()
            self.serial_channel.write(byte_code)
        finally:
            self.__cmd_lock.release()

    def __receieve(self):
        self.message = self.serial_channel.readline()
        return self.message

    def __data_guide(self, ha, dec, isRaMove=False, isDecMove=False, isDisp=True):
        '''
        生成追踪命令

        :param ha:
        :param dec:
        :param isRaMove:
        :param isDecMove:
        :param isDisp:
        :return:
        '''
        com_begin = '7B 01 44 41'
        com_dec = '45'
        com_end = '7D 0D 0A'
        com_sp = ' '
        if isRaMove:
            ra_m = '31'
        else:
            ra_m = '30'
        if isDecMove:
            dec_m = '31'
        else:
            dec_m = '30'

        l_ha = self.__formatNumStr(ha)
        l_dec = self.__formatNumStr(dec)

        hexRa = l_ha.encode("utf-8").hex().upper()
        hexDec = l_dec.encode("utf-8").hex().upper()

        strHexRa = ''
        strHexDec = ''
        for it in range(2, len(hexRa) + 2, 2):
            strHexRa = strHexRa + hexRa[it - 2:it] + ' '
            strHexDec = strHexDec + hexDec[it - 2:it] + ' '

        comd_m = com_begin + com_sp + ra_m + com_sp + strHexRa + \
                 com_dec + com_sp + dec_m + com_sp + strHexDec + com_end
        va = self.__verify_code(comd_m)
        commd_full = comd_m + ' ' + va
        if isDisp:
            print('full command is : ' + commd_full)
        return commd_full

    def __formatNumStr(self, inputNum):
        '''
        将float类型转化为字符串类型.

        :param inputNum:
        :return:
        '''
        if inputNum < 0:
            s_Str = '-'
            isNag = 1
        else:
            s_Str = '+'
            isNag = 0
        inputStr = str("%3.2f" % float(inputNum))
        if isNag:
            inputStr = inputStr[1:]

        p_idx = inputStr.find('.')

        if p_idx != -1:
            if p_idx == 1:
                return s_Str + '00' + inputStr
            elif p_idx == 2:
                return s_Str + '0' + inputStr
            elif p_idx == 3:
                return s_Str + inputStr
            else:
                print('input num to str error')
