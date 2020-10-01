#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 12:24
# @Author  : Menzel3
# @Site    : 
# @File    : star_calculator.py
# @Software: PyCharm
# @version : 0.0.1

from skyfield.api import Topos, Loader

class calculator:
    def __init__(self, lat, lon, elevation, innerStarConfig, observer='earth', star='sun'):
        '''
        innerStarConfig的格式为 [True/False, [Right ascension, Declination]]，True表示使用指定的[RA, DEC]进行追踪，
        False表示使用 sky 库支持的天体追踪

        :param lat: 纬度
        :param lon: 经度
        :param elevation: 海拔
        :param innerStarConfig: innerStarConfig = [True/False, [Right ascension, Declination]]
        :param observer: 观察者所在位置
        :param star: 观测的星
        :return:
        '''
        # self.debug = debug
        self.isInnerStar = innerStarConfig[0]
        if not self.isInnerStar:
            self.starPosition = innerStarConfig[1]  # [Right ascension, Declination]
        self.load = Loader('./Data', expire=False)  # Python37\Lib\site-packages\skyfield\data
        self.planets = self.load('de421.bsp')
        print(self.planets.names())
        self.lon, self.lat, self.elevation, self.observer, self.star = lon, lat, elevation, observer, star
        self.sun = self.planets[star]
        self.location = self.planets[observer] \
                        + Topos(str(lat) + ' N', str(lon) + ' E', elevation_m=elevation)

    def setLongitude(self, lon):
        '''

        :param lon: 经度
        '''
        self.lon = lon
        self.location = self.planets[self.observer] \
                        + Topos(str(self.lat) + ' N', str(self.lon) + ' E', elevation_m=self.elevation)

    def setLatitude(self, lat):
        '''

        :param lat: 维度
        '''
        self.lat = lat
        self.location = self.planets[self.observer] \
                        + Topos(str(self.lat) + ' N', str(self.lon) + ' E', elevation_m=self.elevation)

    def setElevation(self, elevation):
        '''

        :param elevation: 海拔
        '''
        self.elevation = elevation
        self.location = self.planets[self.observer] \
                        + Topos(str(self.lat) + ' N', str(self.lon) + ' E', elevation_m=self.elevation)

    def getStarPosition(self):
        '''
        获取当前所追的星的位置
        '''
        return self.starPosition[0], self.starPosition[1]

    def setStar(self, RA, DEC):
        '''
        设置星提所在的赤经和赤纬

        :param RA: 赤经
        :param DEC: 赤纬
        '''
        self.isInnerStar = False
        self.starPosition[0] = float(RA)
        self.starPosition[1] = float(DEC)

    def setStar(self, star):
        '''
        通过支持列表设置星体

        :param star: 
        '''
        self.isInnerStar = True
        self.sun = self.planets[star]

    def getStarList(self):
        '''
        返回支持直接获得跟踪坐标的星体列表
        '''
        return self.planets.names()

    def compute(self):
        '''
        计算当前指定星体的坐标

        :return: HaDegree 高度, Declination 赤纬
        '''
        ts = self.load.timescale(builtin=True)
        t = ts.now()
        if self.isInnerStar:
            astrometric = self.location.at(t).observe(self.sun)
            apparent = astrometric.apparent()
            ra, dec, distance = apparent.radec(epoch='date')
            self.starPosition[0], self.starPosition[1] = ra.hours, dec._degrees

        LST = (t.gmst * 15 + self.lon) / 15
        Ha = LST - self.starPosition[0]
        HaDegree = Ha * 15

        # offset
        # HaDegree = HaDegree + RA_offset
        # sunDec = sunDec + DEC_offset

        if HaDegree > 180:
            HaDegree = HaDegree - 360

        # if self.debug is True:
        #     HaDegree += float(input("ha="))
        #     sunDec += float(input("dec="))
        #     print("ha: ", HaDegree, "| dec: ", sunDec)

        # problem telescope unit is hour or degree
        # self.starPostion = [Right ascension, Declination]
        return HaDegree, self.starPostion[1]

class FrameCorrection:
    '''
    矫正球坐标系偏移
    '''
    def Rangle(self, alpha, r):
        pass