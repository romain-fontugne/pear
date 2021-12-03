import pandas as pd

# it doesn't really matters if it is bytes or bits
def convert_notation_to_number(size_str):
    """Convert human shorthand notations to numbers (e.g. 1k to 1000).

    :param size_str: A human-readable string representing a file size, e.g.,
    "22 M".
    :return: The number represented by the string.
    """
    multipliers = {
        'kilobyte':  1000,
        'megabyte':  1000 ** 2,
        'gigabyte':  1000 ** 3,
        'terabyte':  1000 ** 4,
        'petabyte':  1000 ** 5,
        'exabyte':   1000 ** 6,
        'zetabyte':  1000 ** 7,
        'yottabyte': 1000 ** 8,
        'kb': 1000,
        'mb': 1000**2,
        'gb': 1000**3,
        'tb': 1000**4,
        'pb': 1000**5,
        'eb': 1000**6,
        'zb': 1000**7,
        'yb': 1000**8,
        'k': 1000,
        'm': 1000**2,
        'g': 1000**3,
        't': 1000**4,
        'p': 1000**5,
        'e': 1000**6,
        'z': 1000**7,
        'y': 1000**8,
    }

    if isinstance(size_str, int) or isinstance(size_str, float):
        return size_str

    for suffix in multipliers:
        size_str = size_str.lower().strip().strip('s')
        if size_str.endswith(suffix):
            return float(size_str[0:-len(suffix)] * multipliers[suffix])

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
            self.dataset['__weights__'] = self.dataset[weight_column].apply(convert_notation_to_number)

    def raw_weights(self):
        return dict(zip(self.dataset['prefix'], self.dataset[self.weight_column]))

    def prefixes(self):
        return self.dataset['prefix']

