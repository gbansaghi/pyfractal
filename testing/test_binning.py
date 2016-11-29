import unittest
from util import binning

class BoundsCheckTest(unittest.TestCase):
    def test_bounds_check(self):
        with self.assertRaises(ValueError):
            binning.bounds_check(2, 1)


class BinForValueTest(unittest.TestCase):
    def setUp(self):
        self.settings = {'min_': 0,
                         'max_': 1,
                         'bins': 3}

    def test_out_of_bounds(self):
        self.settings['value'] = self.settings['min_'] - 1
        with self.assertRaises(ValueError):
            binning.bin_for_value(**self.settings)

        self.settings['value'] = self.settings['max_'] + 1
        with self.assertRaises(ValueError):
            binning.bin_for_value(**self.settings)

    def test_minimum(self):
        self.settings['value'] = self.settings['min_']
        self.assertEqual(binning.bin_for_value(**self.settings), 0)

    def test_maximum(self):
        self.settings['value'] = self.settings['max_']
        self.assertEqual(binning.bin_for_value(**self.settings),
                         self.settings['bins'] - 1)

    def test_bin(self):
        self.settings['value'] = (  self.settings['max_']
                                  + self.settings['min_']) / 2
        self.assertEqual(binning.bin_for_value(**self.settings),
                         int(self.settings['bins'] / 2))


class CenterForBinTest(unittest.TestCase):
    def setUp(self):
        self.settings = {'min_': 0,
                         'max_': 1,
                         'bins': 3}

    def test_out_of_bounds(self):
        self.settings['bin_'] = -1
        with self.assertRaises(ValueError):
            binning.center_for_bin(**self.settings)

        self.settings['bin_'] = self.settings['bins']
        with self.assertRaises(ValueError):
            binning.center_for_bin(**self.settings)

    def test_center(self):
        self.settings['bin_'] = 1
        self.assertEqual(binning.center_for_bin(**self.settings), 0.5)
