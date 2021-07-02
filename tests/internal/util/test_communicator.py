#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/20 16:41
# @Author  : Menzel3
# @Site    : 
# @File    : test_communicator.py
# @Software: PyCharm
# @version : 0.0.1
from tests import context
import serial
from sunflower.internal.util.communicator import Communicator
from sunflower.internal.constants import constant

import unittest


class TestCommunicator(unittest.TestCase):
    ser = serial.Serial(port=constant.port, timeout=constant.timeout, baudrate=constant.baudrate)

    def test_insert_power(self):
        c = Communicator(serial_channel=self.ser)
        self.assertTrue(True, c.open_power())


if __name__ == '__main__':
    unittest.main()
