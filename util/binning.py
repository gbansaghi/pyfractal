def bounds_check(min_, max_):
    if min_ >= max_:
        raise ValueError('invalid bounds (must be min_ < max_)')


def bin_for_value(min_, max_, bins, value):
    bounds_check(min_, max_)

    if value < min_ or value > max_:
        raise ValueError('value out of bounds (must be min_ <= value <= max_)')

    if value == max_:
        return bins - 1
    else:
        fraction = value / (max_ - min_)
        return int(fraction*bins)

def center_for_bin(min_, max_, bin_, bins):
    bounds_check(min_, max_)

    if bin_ < 0 or bin_ >= bins:
        raise ValueError('value out of bounds (must be 0 <= bin_ < bins)')

    bin_width = (max_ - min_) / bins
    return (bin_ + 0.5)*(bin_width)
