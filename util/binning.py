def bin_for_value(start, end, bins, value):
    if value < min(start, end) or value > max(start, end):
        raise ValueError('value out of bounds')

    if value == end:
        return bins - 1
    else:
        fraction = (value - start) / (end - start)
        return int(fraction*bins)

def center_for_bin(start, end, bin_, bins):
    if bin_ < 0 or bin_ >= bins:
        raise ValueError('bin number out of bounds')

    bin_width = (end - start) / bins
    return start + ((bin_ + 0.5)*(bin_width))
