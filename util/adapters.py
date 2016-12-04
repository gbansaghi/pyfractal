from PIL import Image, ImageDraw
from util.sparsematrix import SparseMatrix
from util import binning


class GrayscaleChannel:
    def __init__(self, width, height):
        self.im = Image.new('L', (width, height))
        self.dr = ImageDraw.Draw(self.im)
        self.levels = 256

    def fill(self, value, peak):
        return binning.bin_for_value(0, peak, self.levels, value)

    def update(self, data: SparseMatrix):
        if not data.values():
            return

        peak = max(data.values())
        for (row, column), level in data.items():
            # SparseMatrix row 0 is at the top, PIL y=0 is at the bottom
            y = (data.rows - 1) - row
            x = column
            self.dr.point((x, y), self.fill(level, peak))


class GrayscaleAdapter:
    def __init__(self, width, height):
        self.channel = GrayscaleChannel(width, height)

    @staticmethod
    def from_matrix(matrix: SparseMatrix, update = True):
        adapter = GrayscaleAdapter(matrix.columns, matrix.rows)
        if update:
            adapter.update(matrix)
        
        return adapter

    def update(self, data: SparseMatrix):
        self.channel.update(data)
        return self

    def get_image(self):
        return self.channel.im

    def save(self, filename: str):
        self.channel.im.save(filename)


class RGBAdapter:
    def __init__(self, width, height):
        self.channel_names = ('R', 'G', 'B')
        self.channels = {channel_name: GrayscaleChannel(width, height)
                         for channel_name in self.channel_names}

    @staticmethod
    def from_matrices(r_matrix: SparseMatrix, g_matrix: SparseMatrix,
                      b_matrix: SparseMatrix, update = True):
        if not r_matrix.rows == g_matrix.rows == b_matrix.rows:
            raise ValueError('matrices have mismatched number of rows!')
        if not r_matrix.columns == g_matrix.columns == b_matrix.columns:
            raise ValueError('matrices have mismatched number of columns!')

        adapter = RGBAdapter(width = r.matrix.columns, height = r.matrix.rows)
        if update:
            adapter.update(r_matrix, g_matrix, b_matrix)

        return adapter

    def update(self,
               r_data: SparseMatrix,
               g_data: SparseMatrix,
               b_data: SparseMatrix):
        data = {'R': r_data,
                'G': g_data,
                'B': b_data}
        for channel_name in self.channel_names:
            self.channels[channel_name].update(data[channel_name])
        return self

    def get_image(self):
        return Image.merge('RGB', [self.channels['R'].im,
                                   self.channels['G'].im,
                                   self.channels['B'].im])

    def save(self, filename: str):
        self.get_image().save(filename)
