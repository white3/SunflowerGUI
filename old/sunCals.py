from skyfield.api import Star, Topos, Loader
from skyfield.data import hipparcos

import configparser

cf = configparser.ConfigParser()
cf.read('config.ini')

lon = float(cf.get("location", "lon"))
lat = float(cf.get("location", "lat"))
elevation = float(cf.get("location", "elevation"))

RA_offset = float(cf.get("offset", "RA_offset"))
DEC_offset = float(cf.get("offset", "DEC_offset"))
debug = cf.getboolean("debug", "status")

class sunCalculation:
    def __init__(self):
        self.debug = debug
        self.load = Loader('./res', expire=False)
        planets = self.load('de421.bsp')
        earth = planets['earth']
        self.sun = planets['sun']
        self.Yanqi = earth + \
                     Topos(str(lat) + ' N', str(lon) + ' E', elevation_m=elevation)
        # compute geocentric coordinates, as shown in the example above,
        # or topocentric coordinates specific to your location on the Earth’s surface

    def computeSunHA(self):
        # Python37\Lib\site-packages\skyfield\data

        # V432 Sct - HIP 90651 - SAO 161528
        # sunRA = (18) + (30) / 60 + (56.42) / 3600
        # sunDec = (-1) * ((14) + (33)/60 + (59.6) / 3600)

        # σSct - HIP 91726 - SAO 142515
        # sunRA = (18) + (43) / 60 + (23.31) / 3600
        # sunDec = (-1) * ((9) + (1)/60 + (52) / 3600)

        # 银心
        # sunRA = (17) + (46) / 60 + (56.69) / 3600
        # sunDec = (-1) * ((29) + (00)/60 + (47.1) / 3600)

        # 13 Sgr - HIP 89341 - SAO 186497
        # sunRA = (18) + (14) / 60 + (58.88) / 3600
        # sunDec = (-1) * ((21) + (03)/60 + (4.9) / 3600)

        ts = self.load.timescale(builtin=True)

        t = ts.now()

        astrometric = self.Yanqi.at(t).observe(self.sun)
        apparent = astrometric.apparent()

        ra, dec, distance = apparent.radec(epoch='date')

        sunRA = ra.hours  # 赤经
        sunDec = dec.degrees  # 赤纬

        LST = (t.gmst * 15 + lon) / 15 # gmst时间 + lon
        Ha = LST - sunRA
        HaDegree = Ha * 15
        '''
        earth, sun = planets['earth'], planets['sun']
        ts = load.timescale(builtin=True)
        t = ts.now()
        astrometric = earth.at(t).observe(sun)
        ra, dec, distance = astrometric.radec(epoch='date')
        HaDegree = ((t.gmst * 15 + lon) / 15 - ra.hours) * 15

        WRI     : LST = gmst时间 + 经度/15

        另一个  : LST =  恒星时 + 北京时间 - (北京经度 - 经度)/15
        '''
        # offset
        HaDegree = HaDegree + RA_offset
        sunDec = sunDec + DEC_offset

        if HaDegree > 180:
            HaDegree = HaDegree - 360

        if self.debug is True:
            HaDegree += float(input("ha="))
            sunDec += float(input("dec="))
            print("ha: ", HaDegree, "| dec: ", sunDec)

        print('Sun RA:', sunRA, ' Sun Dec:', sunDec, ' Sun HA degree: ', HaDegree)

        # problem telescope unit is hour or degree
        return HaDegree, sunDec
