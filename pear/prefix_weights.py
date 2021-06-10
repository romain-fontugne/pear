import pandas as pd

# it doesn't really matters if it is bytes or bits
def convert_size_to_bytes(size_str):
    """Convert human filesizes to bytes.

    Special cases:
     - singular units, e.g., "1 byte"
     - byte vs b
     - yottabytes, zetabytes, etc.
     - with & without spaces between & around units.
     - floats ("5.2 mb")

    To reverse this, see hurry.filesize or the Django filesizeformat template
    filter.

    :param size_str: A human-readable string representing a file size, e.g.,
    "22 megabytes".
    :return: The number of bytes represented by the string.
    """
    multipliers = {
        'kilobyte':  1024,
        'megabyte':  1024 ** 2,
        'gigabyte':  1024 ** 3,
        'terabyte':  1024 ** 4,
        'petabyte':  1024 ** 5,
        'exabyte':   1024 ** 6,
        'zetabyte':  1024 ** 7,
        'yottabyte': 1024 ** 8,
        'kb': 1024,
        'mb': 1024**2,
        'gb': 1024**3,
        'tb': 1024**4,
        'pb': 1024**5,
        'eb': 1024**6,
        'zb': 1024**7,
        'yb': 1024**8,
        'k': 1024,
        'm': 1024**2,
        'g': 1024**3,
        't': 1024**4,
        'p': 1024**5,
        'e': 1024**6,
        'z': 1024**7,
        'y': 1024**8,
    }

    if isinstance(size_str, int) or isinstance(size_str, float):
        return size_str

    for suffix in multipliers:
        size_str = size_str.lower().strip().strip('s')
        if size_str.lower().endswith(suffix):
            return int(float(size_str[0:-len(suffix)]) * multipliers[suffix])
    else:
        if size_str.endswith('b'):
            size_str = size_str[0:-1]
        elif size_str.endswith('byte'):
            size_str = size_str[0:-4]
    return int(size_str)

class PrefixWeights(object):
    def __init__(self, csv_fname, weight_column) -> None:
        
        self.weight_column = weight_column
        self.dataset = None
        if csv_fname: 
            self.dataset = pd.read_csv(csv_fname) 
            # remove white spaces around prefixes
            self.dataset['prefix'] = self.dataset['prefix'].str.strip()

        self.prefix_weights = None
        if self.dataset is not None and weight_column in self.dataset.columns:
            # convert units
            self.dataset['__weights__'] = self.dataset[weight_column].apply(convert_size_to_bytes)

    def raw_weights(self):
        return dict(zip(self.dataset['prefix'], self.dataset[self.weight_column]))

    def prefixes(self):
        return self.dataset['prefix']
