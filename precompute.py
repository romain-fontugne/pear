import argparse
from pear.pear import Pear

parser = argparse.ArgumentParser(description=
        "Process raw data (traffic, BGP, Atlas) and store in a database.")

parser.add_argument('ASN', type=int,
                    help='ASN of the network manageed by the user')
parser.add_argument('db', help="SQLite database to store computed data"),
#parser.add_argument('-c', '--route_collector', type=str, default='rrc06',
        #help="BGP route collector that peers with given ASN"),
parser.add_argument('-b', '--bgp_data', type=str, nargs='+', 
        help="MRT files containing a RIB for monitored prefixes"),
parser.add_argument('-p', '--prefixes', type=str, nargs='+', 
        help="CSV files with a list of selected prefixes and optional traffic volume"),
parser.add_argument('-w', '--weight_name', type=str, default='avg_bps',
        help="Name of the column in the csv file used for prefix weights"),
parser.add_argument('--atlas_msm', default=[], nargs='+',
        help="Atlas traceroute measurement IDs to use of RTT results"),
args = parser.parse_args()

pear = Pear(args.db, args.ASN, args.weight_name, 
    prefix_fnames=args.prefixes, bgp_fnames=args.bgp_data, 
    atlas_msm_ids=args.atlas_msm)
# Load all data (traffic and routing)
pear.load()
# Prepare AS graphs
# TODO remove this line??
plotter = pear.make_graphs()
