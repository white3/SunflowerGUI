#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 12:26
# @Author  : Menzel3
# @Site    : 
# @File    : communicator_ucas4_5.py
# @Software: PyCharm
# @version : 0.0.1

import serial
import time

class communicator_ucas4_5():
    CONNECT = '7B 01 40 7D 0D 0A 50'  # connect
    DISCONNECT = '7B 01 41 7D 0D 0A 51'  # disconnect
    READPOSITION = '7B 01 13 7D 0D 0A 23'  # read position
    STOP = '7B 01 47 7D 0D 0A 57'  # stop move
    isConnect = False

    def __init__(self, comNumber):
        '''
        配置串口.
        :param comNumber: 串口号
        :return:
        '''
        self.serialPort = serial.Serial(comNumber, 9600, timeout=1)

    def __del__(self):
        '''
        发送急停后, 再发送断电指令, 并断开连接
        '''
        self.stop()
        self.disconnect()
        print("Security close connection.")

    def isConnect(self):
        '''
        返回本机COM口连接状态
        '''
        return self.isConnect

    def disconnect(self):
        '''
        发送断电指令, 并断开与电机的连接
        '''
        bytesCommandCode = bytes.fromhex(self.DISCONNECT)
        self.__send(bytesCommandCode=bytesCommandCode)
        self.serialPort.close()
        self.isConnect = False

    def connect(self):
        '''
        发送上电指令, 并保持与电机的连接
        '''
        bytesCommandCode = bytes.fromhex(self.CONNECT).decode('utf-8')
        self.__send(bytesCommandCode=bytesCommandCode)
        time.sleep(1)
        rMsg = self.__receieve()
        rgMsg = self.__receieve()
        print(rMsg)
        print(rgMsg)
        ##test do check##
        # tM=b'7B 01 40 O K 7D 0D 0A'
        # if 'O' in str(tM) and 'K' in str(tM):
        #     print('OK')
        self.isConnect = True
        if 'O' in str(rMsg) and 'K' in str(rMsg):
            return True
        else:
            return True

    def reset(self):
        '''
        望远镜视向置为 1,1
        :return:
        '''
        cmd = self.__generateComd(1, 1, True, True)
        bytesCommandCode = bytes.fromhex(cmd)
        self.__send(bytesCommandCode=bytesCommandCode)
        time.sleep(0.1)

    def getPosition(self, isDisp=True):
        '''
        :param isDisp: 是否通过print输出
        :return: Hourangle, declination
        '''
        # print('sys back', self.serialPort.readline())
        bytesCommandCode = bytes.fromhex(self.READPOS)
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
        return HA, Dec

    def stop(self):
        '''
        发送急停指令
        '''
        bytesCommandCode = bytes.fromhex(self.STOP)
        self.__send(bytesCommandCode)
        self.__receieve()  # invalid data
        self.__receieve()  # invalid data

    def trace(self, ha, dec):
        '''
        追踪ha、dec地址
        '''
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
        va = 0;
        for it in range(2, len(comdd) + 2, 2):
            va = va + int(comdd[it - 2:it], 16)
        vaStr = str(hex(va))
        v_value = vaStr[-2:]
        return v_value.upper()

    def commdSpwOr(self, speed, orient):
        '''
        修改望远镜移动速度和移动方向

        :param speed:
        :param orient:
        :return:
        '''
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
        # print(self.serialPort.readline())
        self.__receieve()
        self.__receieve()
        time.sleep(0.1)

    def __send(self, bytesCommandCode):
        time.sleep(0.1)
        self.serialPort.write(bytes.fromhex(bytesCommandCode))

    def __receieve(self):
        self.message = self.serialPort.readline()
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
            # print(strHexRa)

        comd_m = com_begin + com_sp + ra_m + com_sp + strHexRa + \
                 com_dec + com_sp + dec_m + com_sp + strHexDec + com_end
        va = self.verifyCode(comd_m)
        # print('va',va)
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
