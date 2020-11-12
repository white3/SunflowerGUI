import time
from collections import deque
import serial
from sunCals import *
import time

WAIT_TIME = 1

#  ucas4.5m telescope control program for obs sun
#  serial port and communication protocol
#  see # http://pyserial.readthedocs.io/en/latest/shortintro.html
#  and CETC54 communication protocol
#  @Date 24-03-2018
#  @Author Lei
#
import configparser

cf = configparser.ConfigParser()
cf.read('config.ini')

COM_Number=cf.get("serial", "COM_Number")

class sTeleScope :
    #COM_Number=input('Please enter the COM number : ')
    #ser = serial.Serial('COM'+COM_Number, 9600, timeout=1)
    try:
        ser = None
        # serial.Serial(COM_Number, 9600, timeout=10)
    except Exception as e:
        print(e)

    def __init__(self):
        '''
        实例化算法对象, 设置连接、断开、停止、查询指令
        :return:
        '''
        # sudoPassword = 'jlratpc'
        # # command = 'chmod 777 /dev/ttyS0'
        # command = 'chmod 777 /dev/ttyUSB0'
        # os.system('echo %s|sudo -S %s' % (sudoPassword, command))
        #
        # # os.popen("sudo -S %s" % (command), 'w').write('sudoPassword')
        #
        # # self.ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
        # self.ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
        # # self.trace_fmtList=trace_fmtList
        # *******************************************
        # ucas location
        self.scalobj=sunCalculation() # 初始化算法类

        # *******************************************
        # command list
        self.CONNECT = '7B 01 40 7D 0D 0A 50'
        self.DISCONNECT = '7B 01 41 7D 0D 0A 51'
        # read position
        self.READPOS='7B 01 13 7D 0D 0A 23'
        # stop move
        self.STOP='7B 01 47 7D 0D 0A 57'
        ## connect
        # self.ser =serial.Serial('COM3', 9600, timeout=1)
        # self.ser = serial.Serial('COM4', 9600, timeout=1)
        # self.ser.write(self.CONNECT)
        # ser.write(b'hello')

    def disconnectTele(self):
        '''
        停止移动并休息100ms后，发送 断开指令
        :return:
        '''
        self.stopMove()
        time.sleep(WAIT_TIME)
        sHex = bytes.fromhex(self.DISCONNECT)
        self.ser.write(sHex)
        self.ser.close()

    def conSerPort(self):
        '''
        连接串口
        :return:
        '''
        self.ser=serial.Serial(COM_Number, 9600, timeout=1)


    def connectTele(self):
        '''
        发送连接指令并检测响应值
        :return:
        '''
        sHex=bytes.fromhex(self.CONNECT).decode('utf-8')
        print('class',sHex.__class__)
        self.ser.write(sHex.encode())
        rMsg=self.readAcuMsg()
        print('connect', rMsg)
        rgMsg=self.readAcuMsg()
        print('connect', rgMsg)
        ## test do check ##
        # tM=b'7B 01 40 O K 7D 0D 0A'
        # if 'O' in str(tM) and 'K' in str(tM):
        #     print('OK')
        if 'O' in str(rMsg) and 'K' in str(rMsg):
            return True
        else:
            return False
            # self.connectTele()

    def isOpenPort(self):
        '''
        返回端口连接状态
        :return:
        '''
        return self.ser.isOpen

    def getPosition(self,isDisp=1):
        # print('sys back', self.ser.readline())
        sHex=bytes.fromhex(self.READPOS)
        self.ser.write(sHex)
        teleMsg=self.ser.readline()
        # teleMsg shoulde be remove 'com_begin' and 'com_end = '7D 0D 0A'
        # print('tele location msg: ', teleMsg)

        locaStr = bytes.decode(teleMsg,encoding='cp1252')
        # print('msg from sys',locaStr)
        time.sleep(WAIT_TIME)
        backMsg=self.ser.readline()
        sysPos=locaStr[3:-7]

        HA_tele=sysPos[0:7]
        Dec_tele=sysPos[7:-1]
        if isDisp:
            print('tele location in sys is HA :',HA_tele,'  Dec :',Dec_tele)
        return HA_tele,Dec_tele

    def readAcuMsg(self):
        self.acuMsg=self.ser.readline()
        return self.acuMsg

    def stopMove(self):
        sHex=bytes.fromhex(self.STOP)
        self.ser.write(sHex)
        print('stop')
        time.sleep(WAIT_TIME)
        backMsg=self.readAcuMsg()
        backMsg = self.readAcuMsg()

    def generateComd(self, ha, dec, isRaMove=False, isDecMove=False,isDisp=1):
        '''

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
        else :
            ra_m = '30'
        if isDecMove:
            dec_m = '31'
        else :
            dec_m = '30'

        l_ha = self.formatNumStr(ha)
        l_dec =self.formatNumStr(dec)

        # print(l_ha)
        hexRa= l_ha.encode("utf-8").hex().upper()
        hexDec=l_dec.encode("utf-8").hex().upper()
        # print('hex test',hexRa)

        strHexRa=''
        strHexDec=''
        for it in range(2,len(hexRa)+2,2 ):
            strHexRa = strHexRa + hexRa[it-2:it]+' '
            strHexDec = strHexDec + hexDec[it - 2:it] + ' '
            # print(strHexRa)

        comd_m = com_begin + com_sp + ra_m+ com_sp  + strHexRa + \
               com_dec +com_sp + dec_m + com_sp + strHexDec + com_end
        va=self.verifyCode(comd_m)
        # print('va',va)
        commd_full=comd_m+' '+va
        if isDisp:
            print('full command is : '+commd_full)
        return  commd_full

    def formatNumStr(self,inputNum):
        '''
        将float类型转化为字符串类型
        :param inputNum:
        :return:
        '''
        if inputNum<0:
            s_Str='-'
            isNag=1
        else:
            s_Str='+'
            isNag=0
        inputStr= str("%3.2f" % float(inputNum))
        if isNag:
            inputStr=inputStr[1:]

        p_idx=inputStr.find('.')

        if p_idx != -1:
            if p_idx==1:
                return s_Str+'00'+inputStr
            elif p_idx==2:
                 return s_Str+'0'+inputStr
            elif p_idx==3:
                return s_Str+inputStr
            else:
                print('input num to str error')


    def verifyCode(self,comd):
        comdd=comd.replace(" ", "")
        va=0
        for it in range(2,len(comdd)+2,2):
            va=va+int(comdd[it - 2:it],16)
        vaStr=str(hex(va))
        v_value=vaStr[-2:]
        return  v_value.upper()

    def commdSpwOr(self,speed,orient):
        com_begin = '7B 01 43'
        com_end = '7D 0D 0A'
        orient_Str='31'
        if orient=='CW':
            orient_Str='31'
        elif orient=='CCW':
            orient_Str='32'
        elif orient=='UP':
            orient_Str = '33'
        elif orient=='DOWN':
            orient_Str= '34'

        speed_Str='0'+str(speed)

        comd_c=com_begin+' '+orient_Str+' '+speed_Str+' '+com_end
        vrc=self.verifyCode(comd_c)

        comd_full=comd_c+' '+vrc
        # print('comf:',comd_full)
        sHexM=bytes.fromhex(comd_full)
        #encode 'ISO-8859-1'
        self.ser.write(sHexM)
        # # print(self.ser.readline())
        # print(sHexM.encode('cp1252'))
        # print('tele move')
        time.sleep(WAIT_TIME)
        # print(self.ser.readline())
        backMsg=self.readAcuMsg()
        backMsg = self.readAcuMsg()
        time.sleep(WAIT_TIME)

    def getSunPosition(self):
        ha, dec, tp = self.scalobj.computeSunHA()
        return ha,dec

    def traceSun(self,ha,dec):
        comd_main=self.generateComd(ha,dec,True,True)
        strHexC = bytes.fromhex(comd_main)
        # print(comd_main)
        self.ser.write(strHexC)
        # time.sleep(0.1)
        backMsg=self.readAcuMsg()
        backMsg=self.readAcuMsg()
        # time.sleep(0.1)

    def resetTele(self):
        cmd=self.generateComd(1,1,True,True)
        strHexC = bytes.fromhex(cmd)
        self.ser.write(strHexC)
        time.sleep(WAIT_TIME)

    def traceToMove(self):
        CWoneSpeed='7B 01 43 31 01 7D 0D 0A 85'
        cwoneC= bytes.fromhex(CWoneSpeed)
        time.sleep(WAIT_TIME)
        self.ser.write(cwoneC)

    def ALL_REC(self):
        ALL_REC = '7B 00 45 41 31 45 31 7D 0D 0A 3C '
        ALL_REC_C= bytes.fromhex(ALL_REC)
        self.ser.write(ALL_REC_C)
        time.sleep(WAIT_TIME)
        res_bytes = self.ser.read_all()
        
        time.sleep(WAIT_TIME)
        return res_bytes

    def RA_REC(self):
        RA_REC = '7B 00 45 41 31 45 30 7D 0D 0A 3B'
        RA_REC_C= bytes.fromhex(RA_REC)
        time.sleep(WAIT_TIME)
        self.ser.write(RA_REC_C)

    def DEC_REC(self):
        DEC_REC = '7B 00 45 41 30 45 31 7D 0D 0A 3B'
        DEC_REC_C= bytes.fromhex(DEC_REC)
        self.ser.write(DEC_REC_C)
        time.sleep(WAIT_TIME)
# just test code
# testobj=sTeleScope()
# cc=testobj.generateComd(-29.332,0.2034,True,True)
# print(cc,'test')
# cs=testobj.verifyCode('7B 01 43 30 01 7D 0D 0A')
# print(cs)
# #
# testobj.commdSpwOr(3,'CW')