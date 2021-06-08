# pear
Peering tool

## Installation

Get the code:
```zsh
git clone https://github.com/romain-fontugne/pear.git
```

Install dependencies:
```zsh
sudo pip install -r requirements.txt
```

## Usage

Traffic data should be in a csv file with at least 'prefix' and 
'avg_bps' columns. Here is an example:
```csv
idx,prefix,max_bps,avg_bps
1, 1.2.3.0/24, 1234, 123
2, 4.5.0.0/16, 4567, 456
```

Then run the tool with the following command line:
```zsh
python pear.py -p traffic_data.csv -c rrc06 2497
```

## Acknowledgments

This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.
