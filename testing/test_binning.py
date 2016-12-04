import unittest
from util import binning


class BinForValueTest(unittest.TestCase):
    def setUp(self):
        self.settings = {'start': 0,
                         'end': 1,
                         'bins': 3}

    def test_out_of_bounds(self):
        self.settings['value'] = self.settings['start'] - 1
        with self.assertRaises(ValueError):
            binning.bin_for_value(**self.settings)

        self.settings['value'] = self.settings['end'] + 1
        with self.assertRaises(ValueError):
            binning.bin_for_value(**self.settings)

    def test_minimum(self):
        self.settings['value'] = self.settings['start']
        self.assertEqual(binning.bin_for_value(**self.settings), 0)

    def test_maximum(self):
        self.settings['value'] = self.settings['end']
        self.assertEqual(binning.bin_for_value(**self.settings),
                         self.settings['bins'] - 1)

    def test_bin(self):
        self.settings['value'] = (  self.settings['end']
                                  + self.settings['start']) / 2
        self.assertEqual(binning.bin_for_value(**self.settings),
                         int(self.settings['bins'] / 2))
        
    def test_bin(self):
        self.settings['end'] = -1
        self.settings['value'] = (  self.settings['end']
                                  + self.settings['start']) / 2
        self.assertEqual(binning.bin_for_value(**self.settings),
                         int(self.settings['bins'] / 2))


class CenterForBinTest(unittest.TestCase):
    def setUp(self):
        self.settings = {'start': 0,
                         'end': 1,
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

    def test_center_negative(self):
        self.settings['end'] = -1
        self.settings['bin_'] = 1
        self.assertEqual(binning.center_for_bin(**self.settings), -0.5)
