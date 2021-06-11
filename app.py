import argparse
import os
import sys

import pandas as pd
import json
import plotly
import plotly.express as px

from flask import Flask, render_template

from pear.as_graph import ASGraph
from pear.bgp_table_mrt import BGPTable
#from graph_plotter import GraphPlotter
from pear.sankey_plotter import SankeyPlotter
from pear.prefix_weights import PrefixWeights

import pickle

def sizeof_fmt(num, suffix=''):

    if isinstance(num, str):
        return num

    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('ASN', type=int,
                    help='ASN of the network manageed by the user')
#parser.add_argument('-c', '--route_collector', type=str, default='rrc06',
        #help="BGP route collector that peers with given ASN"),
parser.add_argument('-b', '--bgp_data', type=str, 
        help="MRT file containing a RIB for monitored prefixes"),
parser.add_argument('-p', '--prefixes', type=str, 
        help="CSV file with a list of selected prefixes and optional weights"),
parser.add_argument('-w', '--weight_name', type=str, default='avg_bps',
        help="Name of the column in the csv file used for prefix weights"),
parser.add_argument('-g', '--graph_filename', type=str, default='interactive_graph_AS{ASN}_{weight_name}.html',
        help="File name for the ploted AS graph"),
args = parser.parse_args()


# load prefix file and weights
weights = PrefixWeights(args.prefixes, args.weight_name)

# load routing data
rib = BGPTable(args.bgp_data, args.ASN)
sys.stderr.write('Reading BGP data\n')
rib.load_bgp()
sys.stderr.write('Adding selected prefixes\n')
# Add selected prefixes if not globally rechable
if args.prefixes is not None:
    rib.add_prefixes(weights.prefixes())
    sys.stderr.write('Adding prefixes info\n')
    rib.add_prefix_info(weights.prefixes())


# Create AS graph
sys.stderr.write('Building AS graph\n')
graph = ASGraph(args.ASN, rib)
graph.build_graph(weights.prefixes())

sys.stderr.write('Computing weights\n')
# compute edges/nodes weights
graph.propagate_prefix_weight(weights.dataset, hop_power=0)

graph.top_nodes(10, weights, rib)

plot_fname = args.graph_filename.format(
    ASN=args.ASN, prefixes=args.prefixes, weight_name=args.weight_name)
sys.stderr.write('Ploting AS Graph\n')
#gp = GraphPlotter(args.ASN)
#gp.plot(graph, plot_fname)
sp = SankeyPlotter(args.ASN)
sp.plot(graph, rib, plot_fname)


# Views
@app.route('/')
def index():
    return render_template('index.html', asgraph=sp.to_json())

@app.route('/routing')
def routing():
    return render_template('routing-table.html', rib=rib.list_aspaths())

@app.route('/traffic')
def traffic():

    flows = {}
    for prefix, vol in weights.raw_weights().items():
        info = rib.prefix_info(prefix)
        flows[prefix] = {
                'vol': sizeof_fmt(vol), 
                'info': info
                }

    return render_template('traffic-table.html', flows=flows) 

@app.route('/peers')
def peers():

    peers = {}
    for asn in rib.list_peers():
        peers[asn] = {
                'name': 'UNK',
                'vol': 0
                }

    return render_template('peers-table.html', peers=peers) 


app.run(debug=True)
