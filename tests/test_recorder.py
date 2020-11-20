#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 22:12
# @Author  : Menzel3
# @Site    : 
# @File    : test_recorder.py
# @Software: PyCharm
# @version : 0.0.1
import unittest
from sunflower.internal.controller.recorder import Recorder
from sunflower.internal.model.offset import Offset, Offset
from sunflower.internal.model.target import Target
from sunflower.internal.model.times import Times


class TestStringMethods(unittest.TestCase):
    recorder = Recorder()

    def test_write(self):
        target = Target(name='tests')
        ha = [23.76153215391256, 31.168754830018017, 31.853349116583416, 36.26792003332821, 38.68135271905504,
              41.260941232476746, 43.448195137480454, 45.61301352630765, 48.27885959218019, 50.34754611973788]
        offset_ha = [19.0, 19.0, 19.5, 19.25, 19.1, 18.9, 18.9, 18.9, 18.85, 18.85]

        dec = [-3.3922330810514882, -3.4001945563262996, -3.4009302916765476, -3.4056743106063454, -3.408267613265428,
               -3.4110392743056757, -3.413389245283975, -3.4157149860054545, -3.4185788314731047, -3.4208010416085095]
        offset_dec = [7.5, 8.5, 8.8, 9.0, 9.3, 9.5, 9.7, 9.8, 10.05, 10.15]
        for i in range(10):
            localTime = Times()
            target.hourAngle, target.declination = ha[i], dec[i]
            haOffset = Offset(angle=ha[i], offset=offset_ha[i], version=1)
            decOffset = Offset(angle=dec[i], decOffset=offset_dec[i], version=1)
            self.assertEqual(None, self.recorder.writeData(haOffset=haOffset, decOffset=decOffset, globalClock=localTime,
                                                      target=target))

    # def test_read(self):
    #     self.assertTrue(([23.76153215391256, ], [19.0, ]), self.recorder.readData(scale=[23, 25], kind=HA))
    #     self.assertTrue(([-3.3922330810514882, ], [7.5, ]), self.recorder.readData(scale=[-3, -3.4], kind=DEC))
    #
    # def test_correct(self):
    #     demo = Corrector(recorder=self.recorder)
    #     demo.update()
    #     demo.show()


if __name__ == '__main__':
    unittest.main()
