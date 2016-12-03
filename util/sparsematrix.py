def bounds_checked(func):
    def wrapper(self, pos, *args, **kwargs):
        self.bounds_check(pos)
        return func(self, pos, *args, **kwargs)
    return wrapper


class SparseMatrix:
    def __init__(self, rows, columns):
        self.entries = dict()
        self.rows = rows
        self.columns = columns

    def bounds_check(self, key):
        if key[0] < 0 or key[1] < 0:
            raise KeyError("matrix coordinates cannot be negative")
        if key[0] > self.rows:
            raise KeyError("row index "+str(key[0])+" out of bounds")
        if key[1] > self.columns:
            raise KeyError("column index "+str(key[1])+" out of bounds")

    def keys(self):
        return self.entries.keys()

    def values(self):
        return self.entries.values()

    def items(self):
        return self.entries.items()

    @bounds_checked
    def __getitem__(self, pos):
        if pos not in self.entries:
            return 0
        return self.entries[pos]

    @bounds_checked
    def __setitem__(self, pos, value):
        if value == 0:
            self.entries.pop(pos, None)
        else:
            self.entries[pos] = value
        return self

    def __str__(self):
        row_strings = []
        try:
            decimals = len(str(max(self.entries.values())))
        except Exception:
            decimals = 1
        format_string='{{:{}d}}'.format(decimals)
        for row in range(0, self.rows):
            row_string = " ".join([format_string.format(self[row,i]) \
                                   for i in range(self.columns)])
            row_strings.append(row_string)
        return '\n'.join(row_strings)

    def merge(self, other, row_offset=0, column_offset=0):
        # Transform entries
        entries = {(row + row_offset, column + column_offset): value \
                   for (row, column), value in other.entries.items()}

        self.add_entries(entries)
        return self

    def add_entries(self, entries):
        # Filter entries
        filtered = {(row, column): value \
                    for (row, column), value in entries.items() \
                    if  row    < self.rows and row >= 0\
                    and column < self.columns and column >= 0}

        # Update existing entries
        for key in set(self.entries.keys()) & set(filtered.keys()):
            self.entries[key] += filtered[key]

        # Add new entries
        self.entries.update({key: filtered[key] \
                             for key in \
                             set(filtered.keys()) - set(self.entries.keys())})


    def __add__(self, other):
        result = SparseMatrix(self.rows, self.columns)
        result.add_entries(self.entries)
        result.add_entries(other.entries)
        return result

    def __iadd__(self, other):
        self.add_entries(other.entries)
        return self
