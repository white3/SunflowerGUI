# -*- coding: utf-8 -*-

from .context import sunflower

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced tests cases."""

    def test_thoughts(self):
        self.assertIsNone(sunflower.hmm())


if __name__ == '__main__':
    unittest.main()
