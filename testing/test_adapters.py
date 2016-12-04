import unittest
from util.adapters import GrayscaleChannel, GrayscaleAdapter, RGBAdapter
from util.sparsematrix import SparseMatrix
from PIL import Image, ImageDraw


class GrayscaleChannelTest(unittest.TestCase):
    def setUp(self):
        self.channel = GrayscaleChannel(2, 2)
        self.max_value = 255

    def test_max(self):
        self.assertEqual(self.channel.fill(1, 1), self.max_value)

    def test_zero(self):
        self.assertEqual(self.channel.fill(0, 1), 0)

    def test_value(self):
        value = 63
        self.assertEqual(self.channel.fill(value, self.max_value), value)

    def test_update(self):
        matrix = SparseMatrix(2, 2)
        matrix[0, 1] = 1
        matrix[1, 0] = 2
        matrix[1, 1] = 4

        self.channel.update(matrix)

        self.assertEqual(self.channel.im.getpixel((0, 0)),   0)
        self.assertEqual(self.channel.im.getpixel((1, 0)),  64)
        self.assertEqual(self.channel.im.getpixel((0, 1)), 128)
        self.assertEqual(self.channel.im.getpixel((1, 1)), 255)


class GrayscaleAdapterTest(unittest.TestCase):
    def setUp(self):
        self.rows = 2
        self.columns = 2

        self.adapter = GrayscaleAdapter(self.columns, self.rows)

        self.data = SparseMatrix(self.rows, self.columns)
        self.data[0, 0] = 1
        self.data[0, 1] = 2
        self.data[1, 0] = 3
        self.data[1, 1] = 4

        self.reference = Image.new('L', (self.columns, self.rows))
        draw = ImageDraw.Draw(self.reference)
        draw.point((0, 0),  64)
        draw.point((1, 0), 128)
        draw.point((0, 1), 192)
        draw.point((1, 1), 255)

    def test_update(self):
        self.adapter.update(self.data)

        for column in range(self.columns):
            for row in range(self.rows):
                with self.subTest(row = row, column = column):
                    self.assertEqual(self.adapter.get_image()
                                     .getpixel((row, column)),
                                     self.reference.getpixel((row, column)))

    def test_save(self):
        filename = '/tmp/adapter.png'
        self.adapter.update(self.data).save(filename)

        image = Image.open(filename)

        for column in range(self.columns):
            for row in range(self.rows):
                with self.subTest(row = row, column = column):
                    self.assertEqual(image.getpixel((row, column)),
                                     self.reference.getpixel((row, column)))


class RGBAdapterTests(unittest.TestCase):
    def setUp(self):
        self.rows = 3
        self.columns = 3

        self.adapter = RGBAdapter(self.columns, self.rows)

        self.data = SparseMatrix(self.rows, self.columns)
        for row in range(self.rows):
            for column in range(self.columns):
                self.data[row, column] = 1

        self.r = SparseMatrix(self.rows, self.columns)
        self.r.merge(self.data, row_offset = -1, column_offset = -1)

        self.g = SparseMatrix(self.rows, self.columns)
        self.g.merge(self.data, row_offset = -1, column_offset = 1)

        self.b = SparseMatrix(self.rows, self.columns)
        self.b.merge(self.data, row_offset = 1)

        self.reference = Image.new('RGB', (self.columns, self.rows))
        draw = ImageDraw.Draw(self.reference)
        draw.point((0, 0),  (255,   0,   0))
        draw.point((1, 0),  (255, 255,   0))
        draw.point((2, 0),  (  0, 255,   0))
        draw.point((0, 1),  (255,   0, 255))
        draw.point((1, 1),  (255, 255, 255))
        draw.point((2, 1),  (  0, 255, 255))
        draw.point((0, 2),  (  0,   0, 255))
        draw.point((1, 2),  (  0,   0, 255))
        draw.point((2, 2),  (  0,   0, 255))

    def test_update(self):
        self.adapter.update(self.r, self.g, self.b)

        for column in range(self.columns):
            for row in range(self.rows):
                with self.subTest(row = row, column = column):
                    self.assertEqual(self.adapter.get_image()
                                     .getpixel((row, column)),
                                     self.reference.getpixel((row, column)))

    def test_save(self):
        filename = '/tmp/adapter.png'
        self.adapter.update(self.r, self.g, self.b).save(filename)

        image = Image.open(filename)

        for column in range(self.columns):
            for row in range(self.rows):
                with self.subTest(row = row, column = column):
                    self.assertEqual(image.getpixel((row, column)),
                                     self.reference.getpixel((row, column)))
