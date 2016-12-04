import unittest
from util.sparsematrix import SparseMatrix

class SparseMatrixTest(unittest.TestCase):
    def setUp(self):
        self.rows = 2
        self.columns = 2
        self.matrix = SparseMatrix(self.rows, self.columns)

    def test_assignment(self):
        assigned_value = 1
        assigned_coord = (0, 0)
        self.matrix[assigned_coord] = assigned_value
        self.assertEqual(self.matrix[assigned_coord], assigned_value)

    def test_addition(self):
        assigned_value = 1
        assigned_coord = (0, 0)
        assignments = 2
        for i in range(assignments):
            self.matrix[assigned_coord] += assigned_value
        self.assertEqual(self.matrix[assigned_coord],
                         assigned_value*assignments)

    def test_sparsity(self):
        assignments = {(0, 0): 1,
                       (0, 1): 2}
        for coord, value in assignments.items():
            self.matrix[coord] = value
        self.assertEqual(len(self.matrix.keys()), len(assignments.keys()))

    def test_addition_sparsity(self):
        assignments = {(0, 0): 1,
                       (0, 1): 2}
        for coord, value in assignments.items():
            for i in range(value):
                self.matrix[coord] += value
        self.assertEqual(len(self.matrix.keys()), len(assignments.keys()))

    def test_str(self):
        self.matrix[0, 0] = 1
        self.matrix[0, 1] = 2
        self.matrix[1, 0] = 3
        self.matrix[1, 1] = 4
        self.assertEqual(str(self.matrix), '1 2\n3 4')

    def test_invalid_coord(self):
        with self.assertRaises(KeyError):
            self.matrix[-1, 0]
        with self.assertRaises(KeyError):
            self.matrix[0, -1]

    def test_out_of_bounds(self):
        with self.assertRaises(KeyError):
            self.matrix[0, self.columns+1]
        with self.assertRaises(KeyError):
            self.matrix[self.rows+1, 0]


class SparseMatrixOperationsTest(unittest.TestCase):
    def setUp(self):
        self.rows = 2
        self.columns = 2

        self.matrix = SparseMatrix(self.rows, self.columns)
        self.other  = SparseMatrix(self.rows, self.columns)

        self.other[0, 0] = 1
        self.other[0, 1] = 2
        self.other[1, 0] = 3
        self.other[1, 1] = 4

    def test_merge(self):
        self.matrix.merge(self.other)

        for row in range(self.rows):
            for column in range(self.columns):
                with self.subTest(row=row, column=column):
                    self.assertEqual(self.matrix[row, column],
                                     self.other[row, column])

    def test_merge_row_offset(self):
        self.matrix.merge(self.other, row_offset=1)

        for row in range(self.rows):
            for column in range(self.columns):
                with self.subTest(row=row, column=column):
                    if row == 0:
                        self.assertEqual(self.matrix[row, column], 0)
                    else:
                        self.assertEqual(self.matrix[row, column],
                                         self.other[row - 1, column])
        self.assertEqual(len(self.matrix.entries), 2)

    def test_merge_column_offset(self):
        self.matrix.merge(self.other, column_offset=1)

        for row in range(self.rows):
            for column in range(self.columns):
                with self.subTest(row=row, column=column):
                    if column == 0:
                        self.assertEqual(self.matrix[row, column], 0)
                    else:
                        self.assertEqual(self.matrix[row, column],
                                         self.other[row, column - 1])
        self.assertEqual(len(self.matrix.entries), 2)

    def test_merge_row_offset_negative(self):
        self.matrix.merge(self.other, row_offset=-1)

        for row in range(self.rows):
            for column in range(self.columns):
                with self.subTest(row=row, column=column):
                    if row == 1:
                        self.assertEqual(self.matrix[row, column], 0)
                    else:
                        self.assertEqual(self.matrix[row, column],
                                         self.other[row + 1, column])
        self.assertEqual(len(self.matrix.entries), 2)

    def test_merge_column_offset_negative(self):
        self.matrix.merge(self.other, column_offset=-1)

        for row in range(self.rows):
            for column in range(self.columns):
                with self.subTest(row=row, column=column):
                    if column == 1:
                        self.assertEqual(self.matrix[row, column], 0)
                    else:
                        self.assertEqual(self.matrix[row, column],
                                         self.other[row, column + 1])
        self.assertEqual(len(self.matrix.entries), 2)

    def test_add(self):
        result = self.matrix + self.other

        for row in range(self.rows):
            for column in range(self.columns):
                with self.subTest(row=row, column=column):
                    self.assertEqual(result[row, column],
                                     self.matrix[row, column] \
                                     + self.other[row, column])

    def test_inplace_add(self):
        original = SparseMatrix(self.rows, self.columns)
        original.add_entries(self.matrix.entries)
        self.matrix += self.other

        for row in range(self.rows):
            for column in range(self.columns):
                with self.subTest(row=row, column=column):
                    self.assertEqual(self.matrix[row, column],
                                     original[row, column] \
                                     + self.other[row, column])
