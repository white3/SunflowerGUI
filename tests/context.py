# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sunflower

if __name__ == '__main__':
    print(sunflower.Config.getValue(section='time', option='timezone'))