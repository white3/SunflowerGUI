#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 12:33
# @Author  : Menzel3
# @Site    : 
# @File    : flower_service.py
# @Software: PyCharm
# @version : 0.0.1
from sunflower.communicator_ucas4_5 import communicator_ucas4_5
from sunflower.calculator import calculator

class service:
    def __init__(self, config):
        '''
        初始化 星体坐标计算对象、配置加载对象, 望远镜通信对象置空(在望远镜连接时初始化)
        :param config:
        '''
        self.__config = config
        self.__calculator = calculator(lat=self.__config.getValue('lat'), lon=self.__config.getValue('lon'),
                                       elevation=self.__config.getValue('elevation'), star='sun',
                                       innerStarConfig=self.__config.getValue(key='star'))
        self.__communicator = None

    def connectTelescope(self):
        '''
        初始化串口通信对象, 再通过该对象发送上电指令连接
        :return:
        '''
        self.__communicator = communicator_ucas4_5(comNumber=self.__config.getValue('comNumber'))
        self.__communicator.connect()

    def disconnectTelescope(self):
        '''
        断开望远镜, 并发送断电指令
        :return:
        '''
        self.__communicator.disconnect()

    def traceStar(self):
        '''
        望远镜追踪星体
        :return:
        '''
        ha, dec = self.__calculator.compute()
        self.__communicator.trace(ha=ha, dec=dec)

    def stopTelescope(self):
        '''
        望远镜停止转动
        :return:
        '''
        self.__communicator.stop()

    def resetTelescope(self):
        '''
        重置望远镜视角
        :return:
        '''
        self.__communicator.reset()

    def setStar(self, star):
        '''
        通过内置星体设置坐标
        :param star: planets[star]
        :return:
        '''
        self.__calculator.setStar(star=star)

    def setStar(self, rightAscension, declination):
        '''
        设置被观测星体的坐标
        :param rightAscension:
        :param declination:
        :return:
        '''
        self.__calculator.setStar(RA=rightAscension, DEC=declination)

    def commdSpwOr(self, speed, orient):
        '''
        配置望远镜转速和驱动模式
        :param speed:
        :param orient:
        :return:
        '''
        self.__communicator.commdSpwOr(speed=speed, orient=orient)

    def getInnerStarsList(self):
        '''
        :return: {
                    0: ['SOLAR_SYSTEM_BARYCENTER', 'SSB', 'SOLAR SYSTEM BARYCENTER'],
                    1: ['MERCURY_BARYCENTER', 'MERCURY BARYCENTER'],
                    2: ['VENUS_BARYCENTER', 'VENUS BARYCENTER'],
                    3: ['EARTH_BARYCENTER', 'EMB', 'EARTH MOON BARYCENTER', 'EARTH-MOON BARYCENTER', 'EARTH BARYCENTER'],
                    4: ['MARS_BARYCENTER', 'MARS BARYCENTER'],
                    5: ['JUPITER_BARYCENTER', 'JUPITER BARYCENTER'],
                    6: ['SATURN_BARYCENTER', 'SATURN BARYCENTER'],
                    7: ['URANUS_BARYCENTER', 'URANUS BARYCENTER'],
                    8: ['NEPTUNE_BARYCENTER', 'NEPTUNE BARYCENTER'],
                    9: ['PLUTO_BARYCENTER', 'PLUTO BARYCENTER'],
                    10: ['SUN'],
                    199: ['MERCURY'],
                    299: ['VENUS'],
                    399: ['EARTH'],
                    301: ['MOON'],
                    499: ['MARS']
                }
        '''
        return self.__calculator.getStarList()

    def getStarPosition(self):
        '''
        获取观测星体的坐标
        :return: [Right ascension, Declination]
        '''
        return self.__calculator.starPosition()

    def getTelescopeLocation(self):
        '''
        返回已配置的 望远镜坐标
        :return:
        '''
        return self.__config.getValue('lon'), self.__config.getValue('lat'), self.__config.getValue('elevation')

    def setTelescopeLocation(self, lon, lat, elevation):
        '''
        设置望远镜所在坐标
        :param lon: 经度
        :param lat: 纬度
        :param elevation: 海拔
        :return:
        '''
        if lon != self.__config.getValue('lon'):
            self.__config.setValue('lon', lon)
            self.__calculator.setLongitude(lon=lon)
        if lat != self.__config.getValue('lat'):
            self.__config.setValue('lat', lat)
            self.__calculator.setLatitude(lat == lat)
        if elevation != self.__config.getValue('elevation'):
            self.__config.setValue('elevation', elevation)
            self.__calculator.setElevation(elevation=elevation)

    def setCOM(self, comNumber):
        '''
        设置串口
        :param comNumber: 串口号
        :return:
        '''
        try:
            pass
            if self.__communicator != None and self.__communicator.isConnect():
                self.__communicator.disconnect()
                self.__communicator.__del__()
            self.__communicator = communicator_ucas4_5(comNumber=comNumber)
            self.__config.setValue(key='comNumber', value=comNumber)
        except Exception as identifier:
            print("The COM interface may be error")
            print("Failed to set COM ")
