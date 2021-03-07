# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sunflower.internal.constants import constant

if __name__ == '__main__':
    print(constant.sql_util)