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


class Adapter:
    def update_channel(self, data: SparseMatrix, channel: GrayscaleChannel):
        if not data.values():
            return

        peak = max(data.values())
        for (row, column), level in data.items():
            channel.dr.point((column, row), channel.fill(level, peak))

class GrayscaleAdapter(Adapter):
    def __init__(self, width, height):
        super(GrayscaleAdapter, self).__init__()

        self.channel = GrayscaleChannel(width, height)

    def update(self, data: SparseMatrix):
        self.update_channel(data, self.channel)
        return self

    def get_image(self):
        return self.channel.im

    def save(self, filename: str):
        self.channel.im.save(filename)


class RGBAdapter(Adapter):
    def __init__(self, width, height):
        super(RGBAdapter, self).__init__()

        self.channel_names = ('R', 'G', 'B')
        self.channels = dict()
        for channel_name in self.channel_names:
            self.channels[channel_name] = GrayscaleChannel(width, height)

    def update(self,
               r_data: SparseMatrix,
               g_data: SparseMatrix,
               b_data: SparseMatrix):
        data = {'R': r_data,
                'G': g_data,
                'B': b_data}
        for channel_name in self.channel_names:
            self.update_channel(data[channel_name],
                                self.channels[channel_name])
        return self

    def get_image(self):
        return Image.merge('RGB', [self.channels['R'].im,
                                   self.channels['G'].im,
                                   self.channels['B'].im])

    def save(self, filename: str):
        self.get_image().save(filename)
