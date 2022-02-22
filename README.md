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

The tool needs two types of input files:
- traffic data (CSV format)
- routing data (MRT format)

### Traffic data
Traffic data should be in a csv file with at least 'prefix' and 
'avg_bps' columns. Here is an example:
```csv
idx,prefix,max_bps,avg_bps
1, 1.2.3.0/24, 1234, 123
2, 4.5.0.0/16, 4567, 456
```

The name of the files should be in the form: router.exampl1.csv 

### Routing data
Routing data should be RIB in the MRT format. The tool can read compressed files.

The name of the files should be in the form: router1.csv 

## Usage
Pre-process data with the following command line:
```zsh
python precompute.py 2497 ./db_2497_outbound.sql -p router*outbound.example.com.csv -b router*.example.com.mrt 
```
where 'router*.example.com.csv' are the files containing traffic data for each
router and 'router*.example.com.mrt' are the files containing routers routing data.
This will take a few minutes to read and load all the data. Computed data will
be stored in 2497_outbound.sql to enable faster load time for future executions.

Then run the server with the db argument set to the folder containing the computed database:
```zsh
python serve.py --db ./ --host 127.0.0.1 --port 5000
```

See results in your browser at: http://127.0.0.1:5000

## Acknowledgments

This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.
