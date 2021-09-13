import argparse
import os
import json

from flask import Flask, render_template
from flask import request
from flask_basicauth import BasicAuth

from pear.pear import Pear

parser = argparse.ArgumentParser()
parser.add_argument('ASN', type=int,
                    help='ASN of the network manageed by the user')
#parser.add_argument('-c', '--route_collector', type=str, default='rrc06',
        #help="BGP route collector that peers with given ASN"),
parser.add_argument('-b', '--bgp_data', type=str, nargs='+', 
        help="MRT files containing a RIB for monitored prefixes"),
parser.add_argument('-p', '--prefixes', type=str, nargs='+', 
        help="CSV files with a list of selected prefixes and optional traffic volume"),
parser.add_argument('-w', '--weight_name', type=str, default='avg_bps',
        help="Name of the column in the csv file used for prefix weights"),
args = parser.parse_args()

# Initiate Flask app
app = Flask(__name__)

# set basic authentication if there is a auth.json file
if os.path.exists('auth.json'):
    auth = json.load(open('auth.json'))
    app.config['BASIC_AUTH_USERNAME'] = auth['username']
    app.config['BASIC_AUTH_PASSWORD'] = auth['password']
    app.config['BASIC_AUTH_FORCE'] = True
    basic_auth = BasicAuth(app)

# Main app
pear = Pear(args.ASN, args.weight_name)
# Load all data (traffic and routing)
pear.load(args.prefixes, args.bgp_data)
# Prepare AS graphs
plotter = pear.make_graphs()

# Views
@app.route('/')
def index():
    min_traffic = request.args.get('min_traffic', plotter.minimum_traffic)
    max_traffic = 1000000000
    plotter.plot( int(min_traffic) )
    return render_template('index.html', asgraph=plotter.to_json(),
            min_traffic=min_traffic,
            max_traffic=max_traffic
            )

@app.route('/routing')
def routing():
    rib=[]
    router_name = request.args.get('router', None)
    selected_router, rib = pear.get_rib(router_name)

    return render_template('routing-table.html', 
            rib=rib, 
            router_names=pear.get_router_names(),
            selected_router=selected_router
            )

@app.route('/traffic')
def traffic():

    router_name = request.args.get('router', None)
    selected_router, traffic = pear.get_traffic(router_name)

    return render_template('traffic-table.html', 
            flows=traffic,
            router_names=pear.get_router_names(),
            selected_router=selected_router
            ) 

@app.route('/peers')
def peers():

    peers = pear.get_all_peers()
    return render_template('peers-table.html', peers=peers) 


@app.route('/rtt')
def rtt():

    selected_country = request.args.get('country', None)
    country_rtt = pear.get_country_rtt()
    return render_template('rtt-table.html', traceroutes=country_rtt, 
            selected_country=selected_country) 


app.run()
