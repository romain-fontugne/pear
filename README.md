# pear
Peering tool

## Installation

Get the code:
```zsh
git clone https://github.com/romain-fontugne/pear.git
```

Install dependencies:
```zsh
cd pear
sudo pip install -r requirements.txt
```

## Input data

The tool needs two input files:
- one for traffic data (CSV format)
- one for routing data (MRT format)

### Traffic data
Traffic data should be in a csv file with at least 'prefix' and 
'avg_bps' columns. Here is an example:
```csv
idx,prefix,max_bps,avg_bps
1, 1.2.3.0/24, 1234, 123
2, 4.5.0.0/16, 4567, 456
```

### Routing data
Routing data should be RIB in the MRT format. The tool can read compressed files.


## Usage
Run the tool with the following command line:
```zsh
python src/pear.py -p traffic_data.csv -b rib.mrt 2497
```
where 'traffic_data.csv' is the file containing the traffic data and 'rib.mrt'
is the file containing the routing data.

The tool produces an HTML file (interactive_graph_ASXXX_avg_bps.html) in the 
same directory that contains the AS graph with traffic data.

## Acknowledgments

This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.
