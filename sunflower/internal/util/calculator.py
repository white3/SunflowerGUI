#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 12:24
# @Author  : Menzel3
# @Site    :
# @File    : calculator.py
# @Software: PyCharm
# @version : 0.0.1
from skyfield.api import Topos, Loader
from skyfield.positionlib import position_of_radec

load = Loader('res', expire=False)
planets = load('de421.bsp')

"""
{0: ['SOLAR_SYSTEM_BARYCENTER', 'SSB', 'SOLAR SYSTEM BARYCENTER'], 
1: ['MERCURY_BARYCENTER', 'MERCURY BARYCENTER'], 2: ['VENUS_BARYCENTER', 'VENUS BARYCENTER'], 
3: ['EARTH_BARYCENTER', 'EMB', 'EARTH MOON BARYCENTER', 'EARTH-MOON BARYCENTER', 'EARTH BARYCENTER'], 
4: ['MARS_BARYCENTER', 'MARS BARYCENTER'], 5: ['JUPITER_BARYCENTER', 'JUPITER BARYCENTER'], 
6: ['SATURN_BARYCENTER', 'SATURN BARYCENTER'], 7: ['URANUS_BARYCENTER', 'URANUS BARYCENTER'], 
8: ['NEPTUNE_BARYCENTER', 'NEPTUNE BARYCENTER'], 9: ['PLUTO_BARYCENTER', 'PLUTO BARYCENTER'], 
10: ['SUN'], 199: ['MERCURY'], 299: ['VENUS'], 399: ['EARTH'], 301: ['MOON'], 499: ['MARS']}
"""

from sunflower.internal.model.target import Target


class Calculator(object):
    def __init__(self, lat: str, lon: str, elevation: int, target: Target, observer='earth'):
        '''
        初始化时需要输入参数：望远镜所在经纬度、观测目标、观测星球
        :param lat: 纬度
        :param lon: 经度
        :param elevation: 海拔
        :param target: 观测目标
        :param observer:
        '''
        self.lon = float(lon)
        self.lat = float(lat)
        self.elevation = elevation
        if target.isInherent:  # 内置
            self.star = planets[target.name]
        else:  # 非内置, 设置一个坐标
            self.star = position_of_radec(ra_hours=self.target.hourAngle, dec_degrees=self.target.declination)
        # 设置观察者的位置
        self.Yanqi = planets[observer] + \
                     Topos(lat + ' N', lon + ' E', elevation_m=self.elevation)

    def computeLocation(self) -> list:
        """
        返回: 时角、赤纬、赤经、utc时间
        :return: float(haDegree), float(sunDec), float(ra), t.utc_datetime()
        """
        ts = load.timescale(builtin=True)
        t = ts.now()

        astrometric = self.Yanqi.at(t).observe(self.star)
        apparent = astrometric.apparent()
        ra, dec, distance = apparent.radec(epoch='date')

        sunRA = ra.hours  # 赤经
        sunDec = dec.degrees  # 赤纬

        LST = (t.gmst * 15 + self.lon) / 15  # gmst时间 + lon
        ha = (LST - sunRA) * 15

        if ha > 180:
            ha -= 360

        return float(ha), float(sunDec), float(sunRA), t.utc_datetime()

    def setTarget(self, target):
        '''
        通过支持列表设置星体

        :param star:
        '''
        self.target = target


if __name__ == '__main__':
    pass
