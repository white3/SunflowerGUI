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
from sunflower.internal.util.decorator import debugLog


class Communicator(object):
    INSERT_POWER = '7B 00 40 7D 0D 0A 4F'  # 驱动上电
    DROP_POWER = '7B 00 41 7D 0D 0A 50'  # 驱动断电
    # INSERT_POWER = '7B 01 40 7D 0D 0A 50'  # connect
    # DROP_POWER = '7B 01 41 7D 0D 0A 51'  # disconnect
    RESET = '7B 00 42 7D 0D 0A 51'
    POSITION = '7B 01 13 7D 0D 0A 23'  # read position
    STOP = '7B 01 47 7D 0D 0A 57'  # stop move
    isConnect = False  # 是否连接
    isElectric = False  # 是否上电
    serialChannel = None  # 串口通信通道

    def __init__(self, serialChannel: serial.Serial):
        """
        配置串口, 这里会直接进行串口连接
        :param comNumber: 串口号
        :param freq: 串口频率
        :return:
        """
        self.serialChannel = serialChannel

    def __del__(self):
        """
        发送急停后, 再发送断电指令, 并断开连接
        :return:
        """
        # self.stop()
        self.drop_power()
        print("Security close connection.")

    @debugLog
    def isConnect(self):
        """
        返回本机COM口连接状态

        :return:
        """
        return self.isConnect

    @debugLog
    def drop_power(self):
        """
        发送断电指令, 并断开与电机的连接
        :return:
        """
        bytesCommandCode = bytes.fromhex(self.DROP_POWER)
        self.__send(bytesCommandCode=bytesCommandCode)
        self.serialChannel.close()
        self.isConnect = False

    @debugLog
    def insert_power(self):
        """
        发送上电指令, 并保持与电机的连接
        :return:
        """
        bytesCommandCode = bytes.fromhex(self.INSERT_POWER).decode('utf-8')
        self.__send(bytesCommandCode=bytesCommandCode)
        rMsg = self.__receieve()
        rgMsg = self.__receieve()
        print(rMsg)
        print(rgMsg)
        ##tests do check##
        # tM=b'7B 01 40 O K 7D 0D 0A'
        # if 'O' in str(tM) and 'K' in str(tM):
        #     print('OK')
        if 'O' in str(rMsg) and 'K' in str(rMsg):
            self.isConnect = True
            return True
        else:
            return False

    # @debugLog
    def getPosition(self, isDisp=True):
        '''
        :param isDisp: 是否通过print输出
        :return: Hourangle, declination
        '''
        # print('sys back', self.serialChannel.readline())
        bytesCommandCode = bytes.fromhex(self.POSITION)
        self.__send(bytesCommandCode=bytesCommandCode)
        teleMsg = self.__receieve()
        self.__receieve()

        # teleMsg shoulde be remove 'com_begin' and 'com_end = '7D 0D 0A'
        # print('tele location msg: ', teleMsg)
        locaStr = bytes.decode(teleMsg, encoding='cp1252')
        sysPos = locaStr[3:-7]

        HA = sysPos[0:7]
        Dec = sysPos[7:-1]
        if isDisp:
            print('tele location in sys is HA :', HA, '  Dec :', Dec)
        return float(HA), float(Dec)

    @debugLog
    def stop(self):
        """
        发送急停指令

        :return:
        """
        bytesCommandCode = bytes.fromhex(self.STOP)
        self.__send(bytesCommandCode)
        self.__receieve()  # invalid data
        self.__receieve()  # invalid data

    @debugLog
    def point(self, ha, dec):
        """
        追踪坐标 angle、angle

        :param ha:
        :param dec:
        :return:
        """
        hexCommandCode = self.__generateComd(ha, dec, True, True)
        bytesCommandCode = bytes.fromhex(hexCommandCode)
        self.__send(bytesCommandCode)
        self.__receieve()  # invalid data
        self.__receieve()  # invalid data

    def verifyCode(self, comd):
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
        return v_value.upper()

    @debugLog
    def commdSpwOr(self, speed: int, orient: str):
        """
        使望远镜以speed的速度向orient方向移动

        :param speed:
        :param orient:
        :return:
        """
        com_begin = '7B 01 43'
        com_end = '7D 0D 0A'
        orient_Str = '31'
        if orient == 'CW':
            orient_Str = '31'
        elif orient == 'CCW':
            orient_Str = '32'
        elif orient == 'UP':
            orient_Str = '33'
        elif orient == 'DOWN':
            orient_Str = '34'

        speed_Str = '0' + str(speed)

        comd_c = com_begin + ' ' + orient_Str + ' ' + speed_Str + ' ' + com_end
        vrc = self.verifyCode(comd_c)

        comd_full = comd_c + ' ' + vrc
        # print('comf:',comd_full)
        bytesCommandCode = bytes.fromhex(comd_full)
        # encode 'ISO-8859-1'
        self.__send(bytesCommandCode=bytesCommandCode)
        # print(self.serialChannel.readline())
        self.__receieve()
        self.__receieve()

    def __send(self, bytesCommandCode):
        time.sleep(0.5)
        self.serialChannel.write(bytesCommandCode)

    def __receieve(self):
        time.sleep(0.5)
        self.message = self.serialChannel.readline()
        return self.message

    def __generateComd(self, ha, dec, isRaMove=False, isDecMove=False, isDisp=True):
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
        va = self.verifyCode(comd_m)
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

    @debugLog
    def reset(self):
        """
        望远镜视向置为 0,47.8
        :return:
        """
        # bytesCommandCode = bytes.fromhex(self.RESET)
        # self.__send(bytesCommandCode=bytesCommandCode)

        hexCommandCode = self.__generateComd(0, 42.8, True, True)
        bytesCommandCode = bytes.fromhex(hexCommandCode)
        self.__send(bytesCommandCode=bytesCommandCode)
